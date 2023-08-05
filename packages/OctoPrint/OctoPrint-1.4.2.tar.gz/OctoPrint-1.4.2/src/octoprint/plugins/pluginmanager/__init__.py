# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2015 The OctoPrint Project - Released under terms of the AGPLv3 License"

from past.builtins import basestring

import octoprint.plugin
import octoprint.plugin.core

from octoprint.settings import valid_boolean_trues
from octoprint.server.util.flask import no_firstrun_access, with_revalidation_checking, check_etag
from octoprint.access import ADMIN_GROUP
from octoprint.access.permissions import Permissions
from octoprint.util import to_bytes, to_native_str, TemporaryDirectory
from octoprint.util.pip import LocalPipCaller
from octoprint.util.version import get_octoprint_version_string, get_octoprint_version, is_octoprint_compatible, is_python_compatible
from octoprint.util.platform import get_os, is_os_compatible
from octoprint.util.net import download_file
from octoprint.events import Events

from flask import jsonify, make_response
from flask_babel import gettext

import io
import logging
import sarge
import sys
import requests
import re
import os
import copy
import time
import threading
import tempfile
import shutil
import filetype

from datetime import datetime

try:
	from os import scandir
except:
	from scandir import scandir

_DATA_FORMAT_VERSION = "v3"


def map_repository_entry(entry):
	if not isinstance(entry, dict):
		return None

	result = copy.deepcopy(entry)

	if not "follow_dependency_links" in result:
		result["follow_dependency_links"] = False

	result["is_compatible"] = dict(
		octoprint=True,
		os=True,
		python=True
	)

	if "compatibility" in entry:
		if "octoprint" in entry["compatibility"] and entry["compatibility"]["octoprint"] is not None and isinstance(
			entry["compatibility"]["octoprint"], (list, tuple)) and len(entry["compatibility"]["octoprint"]):
			result["is_compatible"]["octoprint"] = is_octoprint_compatible(*entry["compatibility"]["octoprint"])

		if "os" in entry["compatibility"] and entry["compatibility"]["os"] is not None and isinstance(
			entry["compatibility"]["os"], (list, tuple)) and len(entry["compatibility"]["os"]):
			result["is_compatible"]["os"] = is_os_compatible(entry["compatibility"]["os"])

		if "python" in entry["compatibility"] and entry["compatibility"]["python"] is not None and isinstance(entry["compatibility"]["python"], basestring):
			result["is_compatible"]["python"] = is_python_compatible(entry["compatibility"]["python"])
		else:
			# we default to only assume py2 compatiblity for now
			result["is_compatible"]["python"] = is_python_compatible(">=2.7,<3")

	return result


already_installed_string = "Requirement already satisfied (use --upgrade to upgrade)"
success_string = "Successfully installed"
failure_string = "Could not install"


class PluginManagerPlugin(octoprint.plugin.SimpleApiPlugin,
                          octoprint.plugin.TemplatePlugin,
                          octoprint.plugin.AssetPlugin,
                          octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.StartupPlugin,
                          octoprint.plugin.BlueprintPlugin,
                          octoprint.plugin.EventHandlerPlugin):

	ARCHIVE_EXTENSIONS = (".zip", ".tar.gz", ".tgz", ".tar")
	PYTHON_EXTENSIONS = (".py",)

	# valid pip install URL schemes according to https://pip.pypa.io/en/stable/reference/pip_install/
	URL_SCHEMES = ("http", "https", "git",
	               "git+http", "git+https", "git+ssh", "git+git",
	               "hg+http", "hg+https", "hg+static-http", "hg+ssh",
	               "svn", "svn+svn", "svn+http", "svn+https", "svn+ssh",
	               "bzr+http", "bzr+https", "bzr+ssh", "bzr+sftp", "bzr+ftp", "bzr+lp")

	OPERATING_SYSTEMS = dict(windows=["win32"],
	                         linux=lambda x: x.startswith("linux"),
	                         macos=["darwin"],
	                         freebsd=lambda x: x.startswith("freebsd"))

	PIP_INAPPLICABLE_ARGUMENTS = dict(uninstall=["--user"])

	RECONNECT_HOOKS = ["octoprint.comm.protocol.*",]

	# noinspection PyMissingConstructor
	def __init__(self):
		self._pending_enable = set()
		self._pending_disable = set()
		self._pending_install = set()
		self._pending_uninstall = set()

		self._pip_caller = None

		self._repository_available = False
		self._repository_plugins = []
		self._repository_cache_path = None
		self._repository_cache_ttl = 0
		self._repository_mtime = None

		self._notices = dict()
		self._notices_available = False
		self._notices_cache_path = None
		self._notices_cache_ttl = 0
		self._notices_mtime = None

		self._orphans = None

		self._console_logger = None

		self._get_throttled = lambda: False

	def initialize(self):
		self._console_logger = logging.getLogger("octoprint.plugins.pluginmanager.console")
		self._repository_cache_path = os.path.join(self.get_plugin_data_folder(), "plugins.json")
		self._repository_cache_ttl = self._settings.get_int(["repository_ttl"]) * 60
		self._notices_cache_path = os.path.join(self.get_plugin_data_folder(), "notices.json")
		self._notices_cache_ttl = self._settings.get_int(["notices_ttl"]) * 60
		self._confirm_disable = self._settings.global_get_boolean(["confirm_disable"])

		self._pip_caller = LocalPipCaller(force_user=self._settings.get_boolean(["pip_force_user"]))
		self._pip_caller.on_log_call = self._log_call
		self._pip_caller.on_log_stdout = self._log_stdout
		self._pip_caller.on_log_stderr = self._log_stderr

	##~~ Body size hook

	def increase_upload_bodysize(self, current_max_body_sizes, *args, **kwargs):
		# set a maximum body size of 50 MB for plugin archive uploads
		return [("POST", r"/upload_file", 50 * 1024 * 1024)]

	# Additional permissions hook

	def get_additional_permissions(self):
		return [
			dict(key="MANAGE",
			     name="Manage plugins",
			     description=gettext("Allows to enable, disable and uninstall installed plugins."),
			     default_groups=[ADMIN_GROUP],
			     roles=["manage"]),
			dict(key="INSTALL",
			     name="Install new plugins",
			     description=gettext("Allows to install new plugins. Includes the \"Manage plugins\" permission."),
			     default_groups=[ADMIN_GROUP],
			     roles=["install"],
			     permissions=["PLUGIN_PLUGINMANAGER_MANAGE"],
			     dangerous=True)
		]

	##~~ StartupPlugin

	def on_after_startup(self):
		from octoprint.logging.handlers import CleaningTimedRotatingFileHandler
		console_logging_handler = CleaningTimedRotatingFileHandler(self._settings.get_plugin_logfile_path(postfix="console"), when="D", backupCount=3)
		console_logging_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
		console_logging_handler.setLevel(logging.DEBUG)

		self._console_logger.addHandler(console_logging_handler)
		self._console_logger.setLevel(logging.DEBUG)
		self._console_logger.propagate = False

		helpers = self._plugin_manager.get_helpers("pi_support", "get_throttled")
		if helpers and "get_throttled" in helpers:
			self._get_throttled = helpers["get_throttled"]
			if self._settings.get_boolean(["ignore_throttled"]):
				self._logger.warning("!!! THROTTLE STATE IGNORED !!! You have configured the Plugin Manager plugin to ignore an active throttle state of the underlying system. You might run into stability issues or outright corrupt your install. Consider fixing the throttling issue instead of suppressing it.")

		# decouple repository fetching from server startup
		self._fetch_all_data(do_async=True)

	##~~ SettingsPlugin

	def get_settings_defaults(self):
		return dict(
			repository="https://plugins.octoprint.org/plugins.json",
			repository_ttl=24*60,
			notices="https://plugins.octoprint.org/notices.json",
			notices_ttl=6*60,
			pip_args=None,
			pip_force_user=False,
			confirm_disable=False,
			dependency_links=False,
			hidden=[],
			ignore_throttled=False
		)

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

		self._repository_cache_ttl = self._settings.get_int(["repository_ttl"]) * 60
		self._notices_cache_ttl = self._settings.get_int(["notices_ttl"]) * 60
		self._pip_caller.force_user = self._settings.get_boolean(["pip_force_user"])
		self._confirm_disable = self._settings.global_get_boolean(["confirm_disable"])

	##~~ AssetPlugin

	def get_assets(self):
		return dict(
			js=["js/pluginmanager.js"],
			clientjs=["clientjs/pluginmanager.js"],
			css=["css/pluginmanager.css"],
			less=["less/pluginmanager.less"]
		)

	##~~ TemplatePlugin

	def get_template_configs(self):
		return [
			dict(type="settings", name=gettext("Plugin Manager"), template="pluginmanager_settings.jinja2", custom_bindings=True),
			dict(type="about", name="Plugin Licenses", template="pluginmanager_about.jinja2")
		]

	def get_template_vars(self):
		plugins = sorted(self._get_plugins(), key=lambda x: x["name"].lower())
		return dict(
			all=plugins,
			thirdparty=list(filter(lambda p: not p["bundled"], plugins)),
			file_extensions=self.ARCHIVE_EXTENSIONS + self.PYTHON_EXTENSIONS
		)

	def get_template_types(self, template_sorting, template_rules, *args, **kwargs):
		return [
			("about_thirdparty", dict(), dict(template=lambda x: x + "_about_thirdparty.jinja2"))
		]

	##~~ BlueprintPlugin

	@octoprint.plugin.BlueprintPlugin.route("/upload_file", methods=["POST"])
	@no_firstrun_access
	@Permissions.PLUGIN_PLUGINMANAGER_INSTALL.require(403)
	def upload_file(self):
		import flask

		input_name = "file"
		input_upload_path = input_name + "." + self._settings.global_get(["server", "uploads", "pathSuffix"])
		input_upload_name = input_name + "." + self._settings.global_get(["server", "uploads", "nameSuffix"])

		if input_upload_path not in flask.request.values or input_upload_name not in flask.request.values:
			return flask.make_response("No file included", 400)
		upload_path = flask.request.values[input_upload_path]
		upload_name = flask.request.values[input_upload_name]

		exts = list(filter(lambda x: upload_name.lower().endswith(x), self.ARCHIVE_EXTENSIONS + self.PYTHON_EXTENSIONS))
		if not len(exts):
			return flask.make_response("File doesn't have a valid extension for a plugin archive or a single file plugin", 400)

		ext = exts[0]

		archive = tempfile.NamedTemporaryFile(delete=False, suffix="{ext}".format(**locals()))
		try:
			archive.close()
			shutil.copy(upload_path, archive.name)
			return self.command_install(path=archive.name,
			                            name=upload_name,
			                            force="force" in flask.request.values and flask.request.values["force"] in valid_boolean_trues)
		finally:
			try:
				os.remove(archive.name)
			except Exception as e:
				self._logger.warning("Could not remove temporary file {path} again: {message}".format(path=archive.name, message=str(e)))

	def is_blueprint_protected(self):
		return False

	##~~ EventHandlerPlugin

	def on_event(self, event, payload):
		from octoprint.events import Events
		if event != Events.CONNECTIVITY_CHANGED or not payload or not payload.get("new", False):
			return
		self._fetch_all_data(do_async=True)

	##~~ SimpleApiPlugin

	def get_api_commands(self):
		return {
			"install": ["url"],
			"uninstall": ["plugin"],
			"enable": ["plugin"],
			"disable": ["plugin"],
			"cleanup": ["plugin"],
			"cleanup_all": [],
			"refresh_repository": []
		}

	def on_api_get(self, request):
		if not Permissions.PLUGIN_PLUGINMANAGER_MANAGE.can():
			return make_response("Insufficient rights", 403)

		from octoprint.server import safe_mode

		refresh_repository = request.values.get("refresh_repository", "false") in valid_boolean_trues
		if refresh_repository or not self._is_repository_cache_valid():
			self._repository_available = self._refresh_repository()

		refresh_notices = request.values.get("refresh_notices", "false") in valid_boolean_trues
		if refresh_notices or not self._is_notices_cache_valid():
			self._notices_available = self._refresh_notices()

		refresh_orphan = request.values.get("refresh_orphans", "false") in valid_boolean_trues

		def view():
			return jsonify(plugins=self._get_plugins(),
			               repository=dict(
			                   available=self._repository_available,
			                   plugins=self._repository_plugins
			               ),
			               orphan_data=self._get_orphans(refresh=refresh_orphan),
			               os=get_os(),
			               octoprint=get_octoprint_version_string(),
			               pip=dict(
			                   available=self._pip_caller.available,
			                   version=self._pip_caller.version_string,
			                   install_dir=self._pip_caller.install_dir,
			                   use_user=self._pip_caller.use_user,
			                   virtual_env=self._pip_caller.virtual_env,
			                   additional_args=self._settings.get(["pip_args"]),
			                   python=sys.executable
		                    ),
			               safe_mode=safe_mode,
			               online=self._connectivity_checker.online)

		def etag():
			import hashlib
			hash = hashlib.sha1()
			def hash_update(value):
				value = value.encode('utf-8')
				hash.update(value)

			hash_update(repr(self._get_plugins()))
			hash_update(str(self._repository_available))
			hash_update(repr(self._repository_plugins))
			hash_update(str(self._notices_available))
			hash_update(repr(self._notices))
			hash_update(repr(self._get_orphans()))
			hash_update(repr(safe_mode))
			hash_update(repr(self._connectivity_checker.online))
			hash_update(repr(_DATA_FORMAT_VERSION))
			return hash.hexdigest()

		def condition():
			return check_etag(etag())

		return with_revalidation_checking(etag_factory=lambda *args, **kwargs: etag(),
		                                  condition=lambda *args, **kwargs: condition(),
		                                  unless=lambda: refresh_repository or refresh_notices or refresh_orphan)(view)()

	def on_api_command(self, command, data):
		if not Permissions.PLUGIN_PLUGINMANAGER_MANAGE.can():
			return make_response("Insufficient rights", 403)

		if self._printer.is_printing() or self._printer.is_paused():
			# do not update while a print job is running
			return make_response("Printer is currently printing or paused", 409)

		if command == "install":
			if not Permissions.PLUGIN_PLUGINMANAGER_INSTALL.can():
				return make_response("Insufficient rights", 403)
			url = data["url"]
			plugin_name = data["plugin"] if "plugin" in data else None
			return self.command_install(url=url,
			                            force="force" in data and data["force"] in valid_boolean_trues,
			                            dependency_links="dependency_links" in data
			                                             and data["dependency_links"] in valid_boolean_trues,
			                            reinstall=plugin_name)

		elif command == "uninstall":
			plugin_name = data["plugin"]
			if not plugin_name in self._plugin_manager.plugins:
				return make_response("Unknown plugin: %s" % plugin_name, 404)

			plugin = self._plugin_manager.plugins[plugin_name]
			return self.command_uninstall(plugin, cleanup=data.get("cleanup", False))

		elif command == "cleanup":
			plugin = data["plugin"]
			try:
				plugin = self._plugin_manager.plugins[plugin]
			except KeyError:
				# not installed, we are cleaning up left overs, that's ok
				pass

			return self.command_cleanup(plugin, include_disabled=True)

		elif command == "cleanup_all":
			return self.command_cleanup_all()

		elif command == "enable" or command == "disable":
			plugin_name = data["plugin"]
			if not plugin_name in self._plugin_manager.plugins:
				return make_response("Unknown plugin: %s" % plugin_name, 404)

			plugin = self._plugin_manager.plugins[plugin_name]
			return self.command_toggle(plugin, command)

	# noinspection PyMethodMayBeStatic
	def _is_archive(self, path):
		_, ext = os.path.splitext(path)
		if ext in PluginManagerPlugin.ARCHIVE_EXTENSIONS:
			return True

		kind = filetype.guess(to_native_str(path))
		if kind:
			return ".{}".format(kind.extension) in PluginManagerPlugin.ARCHIVE_EXTENSIONS
		return False

	def _is_pythonfile(self, path):
		_, ext = os.path.splitext(path)
		if ext in PluginManagerPlugin.PYTHON_EXTENSIONS:
			import ast
			try:
				with io.open(path, 'rb') as f:
					ast.parse(f.read(), filename=path)
				return True
			except Exception as exc:
				self._logger.exception("Could not parse {} as python file: {}".format(path, exc))

		return False

	def command_install(self, url=None, path=None, name=None, force=False, reinstall=None, dependency_links=False):
		folder = None

		try:
			source = path
			source_type = "path"

			if url is not None:
				# fetch URL
				folder = TemporaryDirectory()
				path = download_file(url, folder.name)
				source = url
				source_type = "url"

			# determine type of path
			if self._is_archive(path):
				return self._command_install_archive(path,
				                                     source=source,
				                                     source_type=source_type,
				                                     force=force,
				                                     reinstall=reinstall,
				                                     dependency_links=dependency_links)

			elif self._is_pythonfile(path):
				return self._command_install_pythonfile(path,
				                                        source=source,
				                                        source_type=source_type,
				                                        name=name)

			else:
				self._logger.error("{} is neither an archive nor a python file, can't install that.".format(source))
				result = dict(result=False,
				              source=source,
				              source_type=source_type,
				              reason="Could not install plugin from {}, was neither "
				                     "a plugin archive nor a single file plugin".format(source))
				self._send_result_notification("install", result)
				return jsonify(result)

		finally:
			if folder is not None:
				folder.cleanup()

	# noinspection DuplicatedCode
	def _command_install_archive(self, path, source=None, source_type=None, force=False, reinstall=None, dependency_links=False):
		throttled = self._get_throttled()
		if throttled and isinstance(throttled, dict) and throttled.get("current_issue", False) and not self._settings.get_boolean(["ignore_throttled"]):
			# currently throttled, we refuse to run
			return make_response("System is currently throttled, refusing to install "
			                     "anything due to possible stability issues", 409)

		path = os.path.abspath(path)
		path_url = "file://" + path
		if os.sep != "/":
			# windows gets special handling
			path = path.replace(os.sep, "/").lower()
			path_url = "file:///" + path

		already_installed_check = lambda line: path_url in line.lower() # lower case in case of windows

		self._logger.info("Installing plugin from {}".format(source))
		pip_args = ["--disable-pip-version-check", "install", sarge.shell_quote(path_url), "--no-cache-dir"]

		if dependency_links or self._settings.get_boolean(["dependency_links"]):
			pip_args.append("--process-dependency-links")

		all_plugins_before = self._plugin_manager.find_plugins(existing=dict())

		try:
			returncode, stdout, stderr = self._call_pip(pip_args)

			# pip's output for a package that is already installed looks something like any of these:
			#
			#   Requirement already satisfied (use --upgrade to upgrade): OctoPrint-Plugin==1.0 from \
			#     https://example.com/foobar.zip in <lib>
			#   Requirement already satisfied (use --upgrade to upgrade): OctoPrint-Plugin in <lib>
			#   Requirement already satisfied (use --upgrade to upgrade): OctoPrint-Plugin==1.0 from \
			#     file:///tmp/foobar.zip in <lib>
			#   Requirement already satisfied (use --upgrade to upgrade): OctoPrint-Plugin==1.0 from \
			#     file:///C:/Temp/foobar.zip in <lib>
			#
			# If we detect any of these matching what we just tried to install, we'll need to trigger a second
			# install with reinstall flags.

			if not force and any(map(lambda x: x.strip().startswith(already_installed_string) and already_installed_check(x),
			                         stdout)):
				self._logger.info("Plugin to be installed from {} was already installed, forcing a reinstall".format(source))
				self._log_message("Looks like the plugin was already installed. Forcing a reinstall.")
				force = True
		except Exception:
			self._logger.exception("Could not install plugin from %s" % source)
			return make_response("Could not install plugin from URL, see the log for more details", 500)
		else:
			if force:
				# We don't use --upgrade here because that will also happily update all our dependencies - we'd rather
				# do that in a controlled manner
				pip_args += ["--ignore-installed", "--force-reinstall", "--no-deps"]
				try:
					returncode, stdout, stderr = self._call_pip(pip_args)
				except Exception:
					self._logger.exception("Could not install plugin from {}".format(source))
					return make_response("Could not install plugin from source {}, see the log for more details"
					                     .format(source), 500)

		try:
			result_line = list(filter(lambda x: x.startswith(success_string) or x.startswith(failure_string),
			                     stdout))[-1]
		except IndexError:
			self._logger.error("Installing the plugin from {} failed, could not parse output from pip. "
			                   "See plugin_pluginmanager_console.log for generated output".format(source))
			result = dict(result=False,
			              source=source,
			              source_type=source_type,
			              reason="Could not parse output from pip, see plugin_pluginmanager_console.log "
			                     "for generated output")
			self._send_result_notification("install", result)
			return jsonify(result)

		# The final output of a pip install command looks something like this:
		#
		#   Successfully installed OctoPrint-Plugin-1.0 Dependency-One-0.1 Dependency-Two-9.3
		#
		# or this:
		#
		#   Successfully installed OctoPrint-Plugin Dependency-One Dependency-Two
		#   Cleaning up...
		#
		# So we'll need to fetch the "Successfully installed" line, strip the "Successfully" part, then split
		# by whitespace and strip to get all installed packages.
		#
		# We then need to iterate over all known plugins and see if either the package name or the package name plus
		# version number matches one of our installed packages. If it does, that's our installed plugin.
		#
		# Known issue: This might return the wrong plugin if more than one plugin was installed through this
		# command (e.g. due to pulling in another plugin as dependency). It should be safe for now though to
		# consider this a rare corner case. Once it becomes a real problem we'll just extend the plugin manager
		# so that it can report on more than one installed plugin.

		result_line = result_line.strip()
		if not result_line.startswith(success_string):
			self._logger.error("Installing the plugin from {} failed, pip did not report successful installation"
			                   .format(source))
			result = dict(result=False,
			              source=source,
			              source_type=source_type,
			              reason="Pip did not report successful installation")
			self._send_result_notification("install", result)
			return jsonify(result)

		installed = list(map(lambda x: x.strip(), result_line[len(success_string):].split(" ")))
		all_plugins_after = self._plugin_manager.find_plugins(existing=dict(), ignore_uninstalled=False)

		new_plugin = self._find_installed_plugin(installed, plugins=all_plugins_after)

		if new_plugin is None:
			self._logger.warning("The plugin was installed successfully, but couldn't be found afterwards to "
			                     "initialize properly during runtime. Please restart OctoPrint.")
			result = dict(result=True,
			              source=source,
			              source_type=source_type,
			              needs_restart=True,
			              needs_refresh=True,
			              needs_reconnect=True,
			              was_reinstalled=False,
			              plugin="unknown")
			self._send_result_notification("install", result)
			return jsonify(result)

		self._plugin_manager.reload_plugins()
		needs_restart = self._plugin_manager.is_restart_needing_plugin(new_plugin) \
		                or new_plugin.key in all_plugins_before \
		                or reinstall is not None
		needs_refresh = new_plugin.implementation \
		                and isinstance(new_plugin.implementation, octoprint.plugin.ReloadNeedingPlugin)
		needs_reconnect = self._plugin_manager.has_any_of_hooks(new_plugin, self._reconnect_hooks) and self._printer.is_operational()

		is_reinstall = self._plugin_manager.is_plugin_marked(new_plugin.key, "uninstalled")
		self._plugin_manager.mark_plugin(new_plugin.key,
		                                 uninstalled=False,
		                                 installed=not is_reinstall and needs_restart)

		self._plugin_manager.log_all_plugins()

		self._logger.info("The plugin was installed successfully: {}, version {}".format(new_plugin.name, new_plugin.version))

		# noinspection PyUnresolvedReferences
		self._event_bus.fire(Events.PLUGIN_PLUGINMANAGER_INSTALL_PLUGIN, dict(id=new_plugin.key,
		                                                                      version=new_plugin.version,
		                                                                      source=source,
		                                                                      source_type=source_type))

		result = dict(result=True,
		              source=source,
		              source_type=source_type,
		              needs_restart=needs_restart,
		              needs_refresh=needs_refresh,
		              needs_reconnect=needs_reconnect,
		              was_reinstalled=new_plugin.key in all_plugins_before or reinstall is not None,
		              plugin=self._to_external_plugin(new_plugin))
		self._send_result_notification("install", result)
		return jsonify(result)

	# noinspection DuplicatedCode
	def _command_install_pythonfile(self, path, source=None, source_type=None, name=None):
		if name is None:
			name = os.path.basename(path)

		self._logger.info("Installing single file plugin {} from {}".format(name, source))

		all_plugins_before = self._plugin_manager.find_plugins(existing=dict())

		destination = os.path.join(self._settings.global_get_basefolder("plugins"), name)
		plugin_id, _ = os.path.splitext(name)

		try:
			self._log_call("cp {} {}".format(path, destination))
			shutil.copy(path, destination)
		except:
			self._logger.exception("Could not install plugin from {}".format(source))
			return make_response("Could not install plugin from URL, see the log for more details", 500)

		plugins = self._plugin_manager.find_plugins(existing=dict(), ignore_uninstalled=False)
		new_plugin = plugins.get(plugin_id)
		if new_plugin is None:
			self._logger.warning("The plugin was installed successfully, but couldn't be found afterwards to "
			                     "initialize properly during runtime. Please restart OctoPrint.")
			result = dict(result=True,
			              source=source,
			              source_type=source_type,
			              needs_restart=True,
			              needs_refresh=True,
			              needs_reconnect=True,
			              was_reinstalled=False,
			              plugin="unknown")
			self._send_result_notification("install", result)
			return jsonify(result)

		self._plugin_manager.reload_plugins()
		needs_restart = self._plugin_manager.is_restart_needing_plugin(new_plugin) \
		                or new_plugin.key in all_plugins_before
		needs_refresh = new_plugin.implementation \
		                and isinstance(new_plugin.implementation, octoprint.plugin.ReloadNeedingPlugin)
		needs_reconnect = self._plugin_manager.has_any_of_hooks(new_plugin, self._reconnect_hooks) and self._printer.is_operational()

		self._logger.info("The plugin was installed successfully: {}, version {}".format(new_plugin.name, new_plugin.version))
		self._plugin_manager.log_all_plugins()

		# noinspection PyUnresolvedReferences
		self._event_bus.fire(Events.PLUGIN_PLUGINMANAGER_INSTALL_PLUGIN, dict(id=new_plugin.key,
		                                                                      version=new_plugin.version,
		                                                                      source=source,
		                                                                      source_type=source_type))

		result = dict(result=True,
		              source=source,
		              source_type=source_type,
		              needs_restart=needs_restart,
		              needs_refresh=needs_refresh,
		              needs_reconnect=needs_reconnect,
		              was_reinstalled=new_plugin.key in all_plugins_before,
		              plugin=self._to_external_plugin(new_plugin))
		self._send_result_notification("install", result)
		return jsonify(result)

	def command_uninstall(self, plugin, cleanup=False):
		if plugin.key == "pluginmanager":
			return make_response("Can't uninstall Plugin Manager", 403)

		if not plugin.managable:
			return make_response("Plugin is not managable and hence cannot be uninstalled", 403)

		if plugin.bundled:
			return make_response("Bundled plugins cannot be uninstalled", 403)

		if plugin.origin is None:
			self._logger.warning("Trying to uninstall plugin {plugin} but origin is unknown".format(**locals()))
			return make_response("Could not uninstall plugin, its origin is unknown")

		if plugin.origin.type == "entry_point":
			# plugin is installed through entry point, need to use pip to uninstall it
			origin = plugin.origin[3]
			if origin is None:
				origin = plugin.origin[2]

			pip_args = ["--disable-pip-version-check", "uninstall", "--yes", origin]
			try:
				self._call_pip(pip_args)
			except Exception:
				self._logger.exception("Could not uninstall plugin via pip")
				return make_response("Could not uninstall plugin via pip, see the log for more details", 500)

		elif plugin.origin.type == "folder":
			import os
			import shutil
			full_path = os.path.realpath(plugin.location)

			if os.path.isdir(full_path):
				# plugin is installed via a plugin folder, need to use rmtree to get rid of it
				self._log_stdout("Deleting plugin from {folder}".format(folder=plugin.location))
				shutil.rmtree(full_path)
			elif os.path.isfile(full_path):
				self._log_stdout("Deleting plugin from {file}".format(file=plugin.location))
				os.remove(full_path)

				if full_path.endswith(".py"):
					pyc_file = "{full_path}c".format(**locals())
					if os.path.isfile(pyc_file):
						os.remove(pyc_file)

		else:
			self._logger.warning("Trying to uninstall plugin {plugin} but origin is unknown ({plugin.origin.type})".format(**locals()))
			return make_response("Could not uninstall plugin, its origin is unknown")

		needs_restart = self._plugin_manager.is_restart_needing_plugin(plugin) or cleanup
		needs_refresh = plugin.implementation and isinstance(plugin.implementation, octoprint.plugin.ReloadNeedingPlugin)
		needs_reconnect = self._plugin_manager.has_any_of_hooks(plugin, self._reconnect_hooks) and self._printer.is_operational()

		was_pending_install = self._plugin_manager.is_plugin_marked(plugin.key, "installed")
		self._plugin_manager.mark_plugin(plugin.key,
		                                 uninstalled=not was_pending_install and needs_restart,
		                                 installed=False)

		if not needs_restart:
			try:
				if plugin.enabled:
					self._plugin_manager.disable_plugin(plugin.key, plugin=plugin)
			except octoprint.plugin.core.PluginLifecycleException as e:
				self._logger.exception("Problem disabling plugin {name}".format(name=plugin.key))
				result = dict(result=False, uninstalled=True, disabled=False, unloaded=False, reason=e.reason)
				self._send_result_notification("uninstall", result)
				return jsonify(result)

			try:
				if plugin.loaded:
					self._plugin_manager.unload_plugin(plugin.key)
			except octoprint.plugin.core.PluginLifecycleException as e:
				self._logger.exception("Problem unloading plugin {name}".format(name=plugin.key))
				result = dict(result=False, uninstalled=True, disabled=True, unloaded=False, reason=e.reason)
				self._send_result_notification("uninstall", result)
				return jsonify(result)

		self._plugin_manager.reload_plugins()

		# noinspection PyUnresolvedReferences
		self._event_bus.fire(Events.PLUGIN_PLUGINMANAGER_UNINSTALL_PLUGIN, dict(id=plugin.key,
		                                                                        version=plugin.version))

		result = dict(result=True,
		              needs_restart=needs_restart,
		              needs_refresh=needs_refresh,
		              needs_reconnect=needs_reconnect,
		              plugin=self._to_external_plugin(plugin))
		self._send_result_notification("uninstall", result)
		self._logger.info("Plugin {} uninstalled".format(plugin.key))

		self._cleanup_disabled(plugin.key)
		if cleanup:
			self.command_cleanup(plugin.key, result_notifications=False)

		return jsonify(result)

	def command_cleanup(self, plugin, include_disabled=False, result_notifications=True, settings_save=True):
		if isinstance(plugin, basestring):
			key = result_value = plugin
		else:
			key = plugin.key
			result_value = self._to_external_plugin(plugin)

		message = "Cleaning up plugin {}...".format(key)
		self._logger.info(message)
		self._log_stdout(message)

		# delete plugin settings
		self._cleanup_settings(key)

		# delete plugin disabled entry
		if include_disabled:
			self._cleanup_disabled(key)

		# delete plugin data folder
		result_data = True
		if not self._cleanup_data(key):
			message = "Could not delete data folder of plugin {}".format(key)
			self._logger.exception(message)
			self._log_stderr(message)
			result_data = False

		if settings_save:
			self._settings.save()

		result = dict(result=result_data,
		              needs_restart=True,
		              plugin=result_value)
		if result_notifications:
			self._send_result_notification("cleanup", result)

		# cleaning orphan cache
		self._orphans = None

		return jsonify(result)

	def command_cleanup_all(self):
		orphans = self._get_orphans()
		cleaned_up = set()

		for orphan in sorted(orphans.keys()):
			self.command_cleanup(orphan,
			                     include_disabled=True,
			                     result_notifications=False,
			                     settings_save=False)
			cleaned_up.add(orphan)

		self._settings.save()

		result = dict(result=True,
		              needs_restart=len(cleaned_up) > 0,
		              cleaned_up=sorted(list(cleaned_up)))
		self._send_result_notification("cleanup_all", result)
		self._logger.info("Cleaned up all data, {} left overs removed".format(len(cleaned_up)))

		# cleaning orphan cache
		self._orphans = None

		return jsonify(result)

	def _cleanup_disabled(self, plugin):
		# delete from disabled list
		disabled = self._settings.global_get(["plugins", "_disabled"])
		try:
			disabled.remove(plugin)
		except ValueError:
			# not in list, ok
			pass
		self._settings.global_set(["plugins", "_disabled"], disabled)

	def _cleanup_settings(self, plugin):
		# delete plugin settings
		self._settings.global_remove(["plugins", plugin])
		self._settings.global_remove(["server", "seenWizards", plugin])
		return True

	def _cleanup_data(self, plugin):
		import os
		import shutil

		data_folder = os.path.join(self._settings.getBaseFolder("data"), plugin)
		if os.path.exists(data_folder):
			try:
				shutil.rmtree(data_folder)
				return True
			except Exception:
				self._logger.exception("Could not delete plugin data folder at {}".format(data_folder))
				return False
		else:
			return True

	def command_toggle(self, plugin, command):
		if plugin.key == "pluginmanager" or (plugin.hidden and plugin.bundled):
			return make_response("Can't enable/disable Plugin Manager", 400)

		pending = ((command == "disable" and plugin.key in self._pending_enable) or (command == "enable" and plugin.key in self._pending_disable))
		safe_mode_victim = getattr(plugin, "safe_mode_victim", False)

		needs_restart = self._plugin_manager.is_restart_needing_plugin(plugin)
		needs_refresh = plugin.implementation and isinstance(plugin.implementation, octoprint.plugin.ReloadNeedingPlugin)
		needs_reconnect = self._plugin_manager.has_any_of_hooks(plugin, self._reconnect_hooks) and self._printer.is_operational()

		needs_restart_api = (needs_restart or safe_mode_victim or plugin.forced_disabled) and not pending
		needs_refresh_api = needs_refresh and not pending
		needs_reconnect_api = needs_reconnect and not pending

		try:
			if command == "disable":
				self._mark_plugin_disabled(plugin, needs_restart=needs_restart)
			elif command == "enable":
				self._mark_plugin_enabled(plugin, needs_restart=needs_restart)
		except octoprint.plugin.core.PluginLifecycleException as e:
			self._logger.exception("Problem toggling enabled state of {name}: {reason}".format(name=plugin.key, reason=e.reason))
			result = dict(result=False, reason=e.reason)
		except octoprint.plugin.core.PluginNeedsRestart:
			result = dict(result=True,
			              needs_restart=True,
			              needs_refresh=True,
			              needs_reconnect=True,
			              plugin=self._to_external_plugin(plugin))
		else:
			result = dict(result=True,
			              needs_restart=needs_restart_api,
			              needs_refresh=needs_refresh_api,
			              needs_reconnect=needs_reconnect_api,
			              plugin=self._to_external_plugin(plugin))

		self._send_result_notification(command, result)
		return jsonify(result)

	def _find_installed_plugin(self, packages, plugins=None):
		if plugins is None:
			plugins = self._plugin_manager.find_plugins(existing=dict(), ignore_uninstalled=False)

		for key, plugin in plugins.items():
			if plugin.origin is None or plugin.origin.type != "entry_point":
				continue

			package_name = plugin.origin.package_name
			package_version = plugin.origin.package_version
			versioned_package = "{package_name}-{package_version}".format(**locals())

			if package_name in packages or versioned_package in packages:
				# exact match, we are done here
				return plugin

			else:
				# it might still be a version that got stripped by python's package resources, e.g. 1.4.5a0 => 1.4.5a
				found = False

				for inst in packages:
					if inst.startswith(versioned_package):
						found = True
						break

				if found:
					return plugin

		return None

	def _send_result_notification(self, action, result):
		notification = dict(type="result", action=action)
		notification.update(result)
		self._plugin_manager.send_plugin_message(self._identifier, notification)

	def _call_pip(self, args):
		if self._pip_caller is None or not self._pip_caller.available:
			raise RuntimeError("No pip available, can't operate".format(**locals()))

		if "--process-dependency-links" in args:
			self._log_message("Installation needs to process external dependencies, that might make it take a bit longer than usual depending on the pip version")

		additional_args = self._settings.get(["pip_args"])

		if additional_args is not None:

			inapplicable_arguments = self.__class__.PIP_INAPPLICABLE_ARGUMENTS.get(args[0], list())
			for inapplicable_argument in inapplicable_arguments:
				additional_args = re.sub(r"(^|\s)" + re.escape(inapplicable_argument) + r"\\b", "", additional_args)

			if additional_args:
				args.append(additional_args)

		kwargs = dict(env=dict(PYTHONWARNINGS="ignore:DEPRECATION::pip._internal.cli.base_command"))

		return self._pip_caller.execute(*args, **kwargs)

	def _log_message(self, *lines):
		self._log(lines, prefix="*", stream="message")

	def _log_call(self, *lines):
		self._log(lines, prefix=" ", stream="call")

	def _log_stdout(self, *lines):
		self._log(lines, prefix=">", stream="stdout")

	def _log_stderr(self, *lines):
		self._log(lines, prefix="!", stream="stderr")

	def _log(self, lines, prefix=None, stream=None, strip=True):
		if strip:
			lines = list(map(lambda x: x.strip(), lines))

		self._plugin_manager.send_plugin_message(self._identifier, dict(type="loglines",
		                                                                loglines=[dict(line=line, stream=stream) for line in lines]))
		for line in lines:
			self._console_logger.debug("{prefix} {line}".format(**locals()))

	def _mark_plugin_enabled(self, plugin, needs_restart=False):
		disabled_list = list(self._settings.global_get(["plugins", "_disabled"],
		                                               validator=lambda x: isinstance(x, list),
		                                               fallback=[]))
		if plugin.key in disabled_list:
			disabled_list.remove(plugin.key)
			self._settings.global_set(["plugins", "_disabled"], disabled_list)
			self._settings.save(force=True)

		if not needs_restart and not plugin.forced_disabled and not getattr(plugin, "safe_mode_victim", False):
			self._plugin_manager.enable_plugin(plugin.key)
		else:
			if plugin.key in self._pending_disable:
				self._pending_disable.remove(plugin.key)
			elif not plugin.enabled and plugin.key not in self._pending_enable:
				self._pending_enable.add(plugin.key)

		# noinspection PyUnresolvedReferences
		self._event_bus.fire(Events.PLUGIN_PLUGINMANAGER_ENABLE_PLUGIN, dict(id=plugin.key,
		                                                                     version=plugin.version))

	def _mark_plugin_disabled(self, plugin, needs_restart=False):
		disabled_list = list(self._settings.global_get(["plugins", "_disabled"],
		                                               validator=lambda x: isinstance(x, list),
		                                               fallback=[]))
		if not plugin.key in disabled_list:
			disabled_list.append(plugin.key)
			self._settings.global_set(["plugins", "_disabled"], disabled_list)
			self._settings.save(force=True)

		if not needs_restart and not plugin.forced_disabled and not getattr(plugin, "safe_mode_victim", False):
			self._plugin_manager.disable_plugin(plugin.key)
		else:
			if plugin.key in self._pending_enable:
				self._pending_enable.remove(plugin.key)
			elif (plugin.enabled or plugin.forced_disabled or getattr(plugin, "safe_mode_victim", False)) and plugin.key not in self._pending_disable:
				self._pending_disable.add(plugin.key)

		# noinspection PyUnresolvedReferences
		self._event_bus.fire(Events.PLUGIN_PLUGINMANAGER_DISABLE_PLUGIN, dict(id=plugin.key,
		                                                                      version=plugin.version))

	def _fetch_all_data(self, do_async=False):
		def run():
			self._repository_available = self._fetch_repository_from_disk()
			self._notices_available = self._fetch_notices_from_disk()

		if do_async:
			thread = threading.Thread(target=run)
			thread.daemon = True
			thread.start()
		else:
			run()

	def _is_repository_cache_valid(self, mtime=None):
		import time
		if mtime is None:
			mtime = self._repository_mtime
		if mtime is None:
			return False
		return mtime + self._repository_cache_ttl >= time.time() > mtime

	def _fetch_repository_from_disk(self):
		repo_data = None
		if os.path.isfile(self._repository_cache_path):
			import time
			mtime = os.path.getmtime(self._repository_cache_path)
			if self._is_repository_cache_valid(mtime=mtime):
				try:
					import json
					with io.open(self._repository_cache_path, 'rt', encoding='utf-8') as f:
						repo_data = json.load(f)
					self._repository_mtime = mtime
					self._logger.info("Loaded plugin repository data from disk, was still valid")
				except Exception:
					self._logger.exception("Error while loading repository data from {}".format(self._repository_cache_path))

		return self._refresh_repository(repo_data=repo_data)

	def _fetch_repository_from_url(self):
		if not self._connectivity_checker.online:
			self._logger.info("Looks like we are offline, can't fetch repository from network")
			return None

		repository_url = self._settings.get(["repository"])
		try:
			r = requests.get(repository_url, timeout=30)
			r.raise_for_status()
			self._logger.info("Loaded plugin repository data from {}".format(repository_url))
		except Exception as e:
			self._logger.exception("Could not fetch plugins from repository at {repository_url}: {message}".format(repository_url=repository_url, message=e))
			return None

		try:
			repo_data = r.json()
		except Exception as e:
			self._logger.exception("Error while reading repository data: {}".format(e))
			return None

		# validation
		if not isinstance(repo_data, (list, tuple)):
			self._logger.warning("Invalid repository data: expected a list, got {!r}".format(repo_data))
			return None

		try:
			import json
			with octoprint.util.atomic_write(self._repository_cache_path, mode='wb') as f:
				f.write(to_bytes(json.dumps(repo_data)))
			self._repository_mtime = os.path.getmtime(self._repository_cache_path)
		except Exception as e:
			self._logger.exception("Error while saving repository data to {}: {}".format(self._repository_cache_path, e))

		return repo_data

	def _refresh_repository(self, repo_data=None):
		if repo_data is None:
			repo_data = self._fetch_repository_from_url()
			if repo_data is None:
				return False

		self._repository_plugins = list(filter(lambda x: x is not None,
		                                       map(map_repository_entry, repo_data)))
		return True

	def _is_notices_cache_valid(self, mtime=None):
		import time
		if mtime is None:
			mtime = self._notices_mtime
		if mtime is None:
			return False
		return mtime + self._notices_cache_ttl >= time.time() > mtime

	def _fetch_notices_from_disk(self):
		notice_data = None
		if os.path.isfile(self._notices_cache_path):
			import time
			mtime = os.path.getmtime(self._notices_cache_path)
			if self._is_notices_cache_valid(mtime=mtime):
				try:
					import json
					with io.open(self._notices_cache_path, 'rt', encoding='utf-8') as f:
						notice_data = json.load(f)
					self._notices_mtime = mtime
					self._logger.info("Loaded notice data from disk, was still valid")
				except Exception:
					self._logger.exception("Error while loading notices from {}".format(self._notices_cache_path))

		return self._refresh_notices(notice_data=notice_data)

	def _fetch_notices_from_url(self):
		if not self._connectivity_checker.online:
			self._logger.info("Looks like we are offline, can't fetch notices from network")
			return None

		notices_url = self._settings.get(["notices"])
		try:
			r = requests.get(notices_url, timeout=30)
			r.raise_for_status()
			self._logger.info("Loaded plugin notices data from {}".format(notices_url))
		except Exception as e:
			self._logger.exception("Could not fetch notices from {notices_url}: {message}".format(notices_url=notices_url, message=str(e)))
			return None

		notice_data = r.json()

		try:
			import json
			with octoprint.util.atomic_write(self._notices_cache_path, mode="wb") as f:
				f.write(to_bytes(json.dumps(notice_data)))
			self._notices_mtime = os.path.getmtime(self._notices_cache_path)
		except Exception as e:
			self._logger.exception("Error while saving notices to {}: {}".format(self._notices_cache_path, str(e)))
		return notice_data

	def _refresh_notices(self, notice_data=None):
		if notice_data is None:
			notice_data = self._fetch_notices_from_url()
			if notice_data is None:
				return False

		notices = dict()
		for notice in notice_data:
			if not "plugin" in notice or not "text" in notice or not "date" in notice:
				continue

			key = notice["plugin"]

			try:
				# Jekyll turns "%Y-%m-%d %H:%M:%SZ" into "%Y-%m-%d %H:%M:%S +0000", so be sure to ignore "+0000"
				#
				# Being able to use dateutil here would make things way easier but sadly that can no longer get
				# installed (from source) under OctoPi 0.14 due to its setuptools-scm dependency, so we have to do
				# without it for now until we can drop support for OctoPi 0.14.
				parsed_date = datetime.strptime(notice["date"], "%Y-%m-%d %H:%M:%S +0000")
				notice["timestamp"] = parsed_date.timetuple()
			except Exception as e:
				self._logger.warning("Error while parsing date {!r} for plugin notice "
				                  "of plugin {}, ignoring notice: {}".format(notice["date"], key,  str(e)))
				continue

			if not key in notices:
				notices[key] = []
			notices[key].append(notice)

		self._notices = notices
		return True

	def _get_orphans(self, refresh=False):
		from collections import defaultdict

		if self._orphans is not None and not refresh:
			return self._orphans

		installed_keys = self._plugin_manager.plugins.keys()
		orphans = defaultdict(lambda: dict(settings=False, data=False, disabled=False))

		# settings
		for key in list(self._settings.global_get(["plugins"]).keys()):
			if key.startswith("_"):
				# internal key, like _disabled
				continue

			if key not in installed_keys:
				orphans[key]["settings"] = True

		# data
		for entry in scandir(self._settings.getBaseFolder("data")):
			if not entry.is_dir():
				continue

			if entry.name not in installed_keys:
				orphans[entry.name]["data"] = True

		# disabled
		disabled = self._settings.global_get(["plugins", "_disabled"])
		for key in disabled:
			if key not in installed_keys:
				orphans[key]["disabled"] = True

		self._orphans = dict(**orphans)
		return self._orphans

	@property
	def _reconnect_hooks(self):
		reconnect_hooks = self.__class__.RECONNECT_HOOKS

		reconnect_hook_provider_hooks = self._plugin_manager.get_hooks("octoprint.plugin.pluginmanager.reconnect_hooks")
		for name, hook in reconnect_hook_provider_hooks.items():
			try:
				result = hook()
				if isinstance(result, (list, tuple)):
					reconnect_hooks.extend(filter(lambda x: isinstance(x, basestring), result))
			except Exception:
				self._logger.exception("Error while retrieving additional hooks for which a "
				                       "reconnect is required from plugin {name}".format(**locals()),
				                       extra=dict(plugin=name))

		return reconnect_hooks

	def _get_plugins(self):
		plugins = self._plugin_manager.plugins

		hidden = self._settings.get(["hidden"])
		result = []
		for key, plugin in plugins.items():
			if key in hidden or (plugin.bundled and plugin.hidden):
				continue
			result.append(self._to_external_plugin(plugin))

		return result

	def _to_external_plugin(self, plugin):
		return dict(
			key=plugin.key,
			name=plugin.name,
			description=plugin.description,
			disabling_discouraged=gettext(plugin.disabling_discouraged) if plugin.disabling_discouraged else False,
			author=plugin.author,
			version=plugin.version,
			url=plugin.url,
			license=plugin.license,
			python=plugin.pythoncompat,
			bundled=plugin.bundled,
			managable=plugin.managable,
			enabled=plugin.enabled,
			blacklisted=plugin.blacklisted,
			forced_disabled=plugin.forced_disabled,
			incompatible=plugin.incompatible,
			safe_mode_victim=getattr(plugin, "safe_mode_victim", False),
			pending_enable=(not plugin.enabled and not getattr(plugin, "safe_mode_victim", False) and plugin.key in self._pending_enable),
			pending_disable=((plugin.enabled or getattr(plugin, "safe_mode_victim", False)) and plugin.key in self._pending_disable),
			pending_install=(self._plugin_manager.is_plugin_marked(plugin.key, "installed")),
			pending_uninstall=(self._plugin_manager.is_plugin_marked(plugin.key, "uninstalled")),
			origin=plugin.origin.type,
			notifications = self._get_notifications(plugin)
		)

	def _get_notifications(self, plugin):
		key = plugin.key
		if not plugin.enabled:
			return

		if key not in self._notices:
			return

		octoprint_version = get_octoprint_version(base=True)
		plugin_notifications = self._notices.get(key, [])

		def filter_relevant(notification):
			return "text" in notification and "date" in notification and \
			       ("versions" not in notification or plugin.version in notification["versions"]) and \
			       ("octoversions" not in notification or is_octoprint_compatible(*notification["octoversions"],
			                                                                      octoprint_version=octoprint_version))

		def map_notification(notification):
			return self._to_external_notification(key, notification)

		return list(filter(lambda x: x is not None,
		              	   map(map_notification,
		                  	   filter(filter_relevant,
		                         	  plugin_notifications))))

	def _to_external_notification(self, key, notification):
		return dict(key=key,
		            date=time.mktime(notification["timestamp"]),
		            text=notification["text"],
		            link=notification.get("link"),
		            versions=notification.get("versions", []),
		            important=notification.get("important", False))


def _register_custom_events(*args, **kwargs):
	return ["install_plugin", "uninstall_plugin", "enable_plugin", "disable_plugin"]


__plugin_name__ = "Plugin Manager"
__plugin_author__ = "Gina Häußge"
__plugin_url__ = "http://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html"
__plugin_description__ = "Allows installing and managing OctoPrint plugins"
__plugin_license__ = "AGPLv3"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_hidden__ = True

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PluginManagerPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.server.http.bodysize": __plugin_implementation__.increase_upload_bodysize,
		"octoprint.ui.web.templatetypes": __plugin_implementation__.get_template_types,
		"octoprint.events.register_custom_events": _register_custom_events,
		"octoprint.access.permissions": __plugin_implementation__.get_additional_permissions
	}
