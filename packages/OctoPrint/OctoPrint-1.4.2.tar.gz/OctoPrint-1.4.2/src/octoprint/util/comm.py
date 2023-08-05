# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = "Gina Häußge <osd@foosel.net> based on work by David Braam"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2013 David Braam, Gina Häußge & others - Released under terms of the AGPLv3 License"

"""
The code in this file is based on Cura.util.machineCom from the Cura project from late 2012
(https://github.com/daid/Cura).
"""

import os
import glob
import fnmatch
import time
import re
import threading
import contextlib
import copy

try:
	import queue
except ImportError:
	import Queue as queue
from past.builtins import basestring, unicode

import logging

import serial

import wrapt

import octoprint.plugin

from collections import deque

from octoprint.settings import settings, default_settings
from octoprint.events import eventManager, Events
from octoprint.filemanager import valid_file_type
from octoprint.filemanager.destinations import FileDestinations
from octoprint.util import get_exception_string, sanitize_ascii, filter_non_ascii, CountedEvent, RepeatedTimer, \
	to_unicode, bom_aware_open, TypedQueue, PrependableQueue, TypeAlreadyInQueue, chunks, ResettableTimer, \
	monotonic_time
from octoprint.util.platform import get_os, set_close_exec

try:
	import winreg
except ImportError:
	try:
		import _winreg as winreg
	except ImportError:
		pass

_logger = logging.getLogger(__name__)

# a bunch of regexes we'll need for the communication parsing...

regex_float_pattern = r"[-+]?[0-9]*\.?[0-9]+"
regex_positive_float_pattern = r"[+]?[0-9]*\.?[0-9]+"
regex_int_pattern = r"\d+"

regex_command = re.compile(r"^\s*((?P<codeGM>[GM]\d+)(\.(?P<subcode>\d+))?|(?P<codeT>T)\d+|(?P<codeF>F)\d+)")
"""Regex for a GCODE command."""

regex_float = re.compile(regex_float_pattern)
"""Regex for a float value."""

regexes_parameters = dict(
	floatE=re.compile(r"(^|[^A-Za-z])[Ee](?P<value>%s)" % regex_float_pattern),
	floatF=re.compile(r"(^|[^A-Za-z])[Ff](?P<value>%s)" % regex_float_pattern),
	floatP=re.compile(r"(^|[^A-Za-z])[Pp](?P<value>%s)" % regex_float_pattern),
	floatR=re.compile(r"(^|[^A-Za-z])[Rr](?P<value>%s)" % regex_float_pattern),
	floatS=re.compile(r"(^|[^A-Za-z])[Ss](?P<value>%s)" % regex_float_pattern),
	floatX=re.compile(r"(^|[^A-Za-z])[Xx](?P<value>%s)" % regex_float_pattern),
	floatY=re.compile(r"(^|[^A-Za-z])[Yy](?P<value>%s)" % regex_float_pattern),
	floatZ=re.compile(r"(^|[^A-Za-z])[Zz](?P<value>%s)" % regex_float_pattern),
	intN=re.compile(r"(^|[^A-Za-z])[Nn](?P<value>%s)" % regex_int_pattern),
	intS=re.compile(r"(^|[^A-Za-z])[Ss](?P<value>%s)" % regex_int_pattern),
	intT=re.compile(r"(^|[^A-Za-z])[Tt](?P<value>%s)" % regex_int_pattern)
)
"""Regexes for parsing various GCODE command parameters."""

regex_minMaxError = re.compile(r"Error:[0-9]\n")
"""Regex matching first line of min/max errors from the firmware."""

regex_marlinKillError = re.compile(r"Heating failed|Thermal Runaway|MAXTEMP triggered|MINTEMP triggered|Invalid extruder number|Watchdog barked|KILL caused")
"""Regex matching first line of kill causing errors from Marlin."""

regex_sdPrintingByte = re.compile(r"(?P<current>[0-9]+)/(?P<total>[0-9]+)")
"""Regex matching SD printing status reports.

Groups will be as follows:

  * ``current``: current byte position in file being printed
  * ``total``: total size of file being printed
"""

regex_sdFileOpened = re.compile(r"File opened:\s*(?P<name>.*?)\s+Size:\s*(?P<size>%s)" % regex_int_pattern)
"""Regex matching "File opened" messages from the firmware.

Groups will be as follows:

  * ``name``: name of the file reported as having been opened (str)
  * ``size``: size of the file in bytes (int)
"""

regex_temp = re.compile(r"(?P<tool>B|C|T(?P<toolnum>\d*)):\s*(?P<actual>%s)(\s*\/?\s*(?P<target>%s))?" % (regex_float_pattern, regex_float_pattern))
"""Regex matching temperature entries in line.

Groups will be as follows:

  * ``tool``: whole tool designator, incl. optional ``toolnum`` (str)
  * ``toolnum``: tool number, if provided (int)
  * ``actual``: actual temperature (float)
  * ``target``: target temperature, if provided (float)
"""

regex_repetierTempExtr = re.compile(r"TargetExtr(?P<toolnum>\d+):(?P<target>%s)" % regex_float_pattern)
"""Regex for matching target temp reporting from Repetier.

Groups will be as follows:

  * ``toolnum``: number of the extruder to which the target temperature
    report belongs (int)
  * ``target``: new target temperature (float)
"""

regex_repetierTempBed = re.compile(r"TargetBed:(?P<target>%s)" % regex_float_pattern)
"""Regex for matching target temp reporting from Repetier for beds.

Groups will be as follows:

  * ``target``: new target temperature (float)
"""

regex_position = re.compile(r"X:\s*(?P<x>{float})\s*Y:\s*(?P<y>{float})\s*Z:\s*(?P<z>{float})\s*((E:\s*(?P<e>{float}))|(?P<es>(E\d+:\s*{float}\s*)+))".format(float=regex_float_pattern))
"""Regex for matching position reporting.

Groups will be as follows:

  * ``x``: X coordinate
  * ``y``: Y coordinate
  * ``z``: Z coordinate
  * ``e``: E coordinate if present, or
  * ``es``: multiple E coordinates if present, to be parsed further with regex_e_positions
"""

regex_e_positions = re.compile(r"E(?P<id>\d+):\s*(?P<value>{float})".format(float=regex_float_pattern))
"""Regex for matching multiple E coordinates in a position report.

Groups will be as follows:

  * ``id``: id of the extruder or which the position is reported
  * ``value``: reported position value
"""

regex_firmware_splitter = re.compile(r"\s*([A-Z0-9_]+):\s*")
"""Regex to use for splitting M115 responses."""

regex_resend_linenumber = re.compile(r"(N|N:)?(?P<n>%s)" % regex_int_pattern)
"""Regex to use for request line numbers in resend requests"""

def serialList():
	if os.name=="nt":
		candidates = []
		try:
			key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"HARDWARE\\DEVICEMAP\\SERIALCOMM")
			i = 0
			while True:
				candidates += [winreg.EnumValue(key,i)[1]]
				i += 1
		except Exception:
			pass

	else:
		candidates = glob.glob("/dev/ttyUSB*") \
		             + glob.glob("/dev/ttyACM*") \
		             + glob.glob("/dev/tty.usb*") \
		             + glob.glob("/dev/cu.*") \
		             + glob.glob("/dev/cuaU*") \
		             + glob.glob("/dev/ttyS*") \
		             + glob.glob("/dev/rfcomm*")

	# additional ports
	additionalPorts = settings().get(["serial", "additionalPorts"])
	if additionalPorts:
		for additional in additionalPorts:
			candidates += glob.glob(additional)

	hooks = octoprint.plugin.plugin_manager().get_hooks("octoprint.comm.transport.serial.additional_port_names")
	for name, hook in hooks.items():
		try:
			candidates += hook(candidates)
		except Exception:
			logging.getLogger(__name__).exception("Error while retrieving additional "
			                                      "serial port names from hook {}".format(name))

	# blacklisted ports
	blacklistedPorts = settings().get(["serial", "blacklistedPorts"])
	if blacklistedPorts:
		for pattern in settings().get(["serial", "blacklistedPorts"]):
			candidates = list(filter(lambda x: not fnmatch.fnmatch(x, pattern), candidates))

	# last used port = first to try, move to start
	prev = settings().get(["serial", "port"])
	if prev in candidates:
		candidates.remove(prev)
		candidates.insert(0, prev)

	return candidates

def baudrateList(candidates=None):
	if candidates is None:
		# sorted by likelihood
		candidates = [115200, 250000, 230400, 57600, 38400, 19200, 9600]

	# additional baudrates prepended, sorted descending
	additionalBaudrates = settings().get(["serial", "additionalBaudrates"])
	for additional in sorted(additionalBaudrates, reverse=True):
		try:
			candidates.insert(0, int(additional))
		except Exception:
			_logger.warning("{} is not a valid additional baudrate, ignoring it".format(additional))

	# blacklisted baudrates
	blacklistedBaudrates = settings().get(["serial", "blacklistedBaudrates"])
	if blacklistedBaudrates:
		for baudrate in blacklistedBaudrates:
			candidates.remove(baudrate)

	# last used baudrate = first to try, move to start
	prev = settings().getInt(["serial", "baudrate"])
	if prev in candidates:
		candidates.remove(prev)
		candidates.insert(0, prev)

	return candidates

gcodeToEvent = {
	# pause for user input
	"M226": Events.WAITING,
	"M0": Events.WAITING,
	"M1": Events.WAITING,
	# dwell command
	"G4": Events.DWELL,

	# part cooler
	"M245": Events.COOLING,

	# part conveyor
	"M240": Events.CONVEYOR,

	# part ejector
	"M40": Events.EJECT,

	# user alert
	"M300": Events.ALERT,

	# home print head
	"G28": Events.HOME,

	# emergency stop
	"M112": Events.E_STOP,

	# motors on/off
	"M80": Events.POWER_ON,
	"M81": Events.POWER_OFF,
}

class PositionRecord(object):
	_standard_attrs = {"x", "y", "z", "e", "f", "t"}

	@classmethod
	def valid_e(cls, attr):
		if not attr.startswith("e"):
			return False

		try:
			int(attr[1:])
		except ValueError:
			return False

		return True

	def __init__(self, *args, **kwargs):
		attrs = self._standard_attrs | set(key for key in kwargs if self.valid_e(key))
		for attr in attrs:
			setattr(self, attr, kwargs.get(attr))

	def copy_from(self, other):
		# make sure all standard attrs and attrs from other are set
		attrs = self._standard_attrs | set(key for key in dir(other) if self.valid_e(key))
		for attr in attrs:
			setattr(self, attr, getattr(other, attr))

		# delete attrs other doesn't have
		attrs = set(key for key in dir(self) if self.valid_e(key)) - attrs
		for attr in attrs:
			delattr(self, attr)

	def as_dict(self):
		attrs = self._standard_attrs | set(key for key in dir(self) if self.valid_e(key))
		return dict((attr, getattr(self, attr)) for attr in attrs)

class TemperatureRecord(object):
	RESERVED_IDENTIFIER_REGEX = re.compile("[0-9]+|[bc]")

	def __init__(self):
		self._tools = dict()
		self._bed = (None, None)
		self._chamber = (None, None)
		self._custom = dict()

	def copy_from(self, other):
		self._tools = other.tools
		self._bed = other.bed

	def set_tool(self, tool, actual=None, target=None):
		current = self._tools.get(tool, (None, None))
		self._tools[tool] = self._to_new_tuple(current, actual, target)

	def set_bed(self, actual=None, target=None):
		current = self._bed
		self._bed = self._to_new_tuple(current, actual, target)

	def set_chamber(self, actual=None, target=None):
		current = self._chamber
		self._chamber = self._to_new_tuple(current, actual, target)

	def set_custom(self, identifier, actual=None, target=None):
		if self.RESERVED_IDENTIFIER_REGEX.match(identifier):
			raise ValueError("{} is a reserved identifier".format(identifier))
		current = self._custom.get(identifier, (None, None))
		self._custom[identifier] = self._to_new_tuple(current, actual, target)

	@property
	def tools(self):
		return dict(self._tools)

	@property
	def bed(self):
		return self._bed

	@property
	def chamber(self):
		return self._chamber

	@property
	def custom(self):
		return dict(self._custom)

	def as_script_dict(self):
		result = dict()

		tools = self.tools
		for tool, data in tools.items():
			result[tool] = dict(actual=data[0],
			                    target=data[1])

		bed = self.bed
		result["b"] = dict(actual=bed[0],
		                   target=bed[1])

		chamber = self.chamber
		result["c"] = dict(actual=chamber[0],
		                   target=chamber[1])

		custom = self.custom
		for identifier, data in custom.items():
			result[identifier] = dict(actual=data[0],
			                          target=data[1])

		return result

	@classmethod
	def _to_new_tuple(cls, current, actual, target):
		if current is None or not isinstance(current, tuple) or len(current) != 2:
			current = (None, None)

		if actual is None and target is None:
			return current

		old_actual, old_target = current

		if actual is None:
			return old_actual, target
		elif target is None:
			return actual, old_target
		else:
			return actual, target

class MachineCom(object):
	STATE_NONE = 0
	STATE_OPEN_SERIAL = 1
	STATE_DETECT_SERIAL = 2
	STATE_CONNECTING = 3
	STATE_OPERATIONAL = 4
	STATE_STARTING = 5
	STATE_PRINTING = 6
	STATE_PAUSED = 7
	STATE_PAUSING = 8
	STATE_RESUMING = 9
	STATE_FINISHING = 10
	STATE_CLOSED = 11
	STATE_ERROR = 12
	STATE_CLOSED_WITH_ERROR = 13
	STATE_TRANSFERING_FILE = 14
	STATE_CANCELLING = 15

	# be sure to add anything here that signifies an operational state
	OPERATIONAL_STATES = (STATE_PRINTING, STATE_STARTING, STATE_OPERATIONAL, STATE_PAUSED, STATE_CANCELLING,
	                      STATE_PAUSING, STATE_RESUMING, STATE_FINISHING, STATE_TRANSFERING_FILE)

	# be sure to add anything here that signifies a printing state
	PRINTING_STATES = (STATE_STARTING, STATE_PRINTING, STATE_CANCELLING, STATE_PAUSING, STATE_RESUMING, STATE_FINISHING)

	CAPABILITY_AUTOREPORT_TEMP = "AUTOREPORT_TEMP"
	CAPABILITY_AUTOREPORT_SD_STATUS = "AUTOREPORT_SD_STATUS"
	CAPABILITY_BUSY_PROTOCOL = "BUSY_PROTOCOL"
	CAPABILITY_EMERGENCY_PARSER = "EMERGENCY_PARSER"
	CAPABILITY_CHAMBER_TEMP = "CHAMBER_TEMPERATURE"

	CAPABILITY_SUPPORT_ENABLED = "enabled"
	CAPABILITY_SUPPORT_DETECTED = "detected"
	CAPABILITY_SUPPORT_DISABLED = "disabled"

	DETECTION_RETRIES = 3

	def __init__(self, port=None, baudrate=None, callbackObject=None, printerProfileManager=None):
		self._logger = logging.getLogger(__name__)
		self._serialLogger = logging.getLogger("SERIAL")
		self._phaseLogger = logging.getLogger(__name__ + ".command_phases")

		if port is None:
			port = settings().get(["serial", "port"])
		if baudrate is None:
			settingsBaudrate = settings().getInt(["serial", "baudrate"])
			if settingsBaudrate is None:
				baudrate = 0
			else:
				baudrate = settingsBaudrate
		if callbackObject is None:
			callbackObject = MachineComPrintCallback()

		self._port = port
		self._baudrate = baudrate
		self._callback = callbackObject
		self._printerProfileManager = printerProfileManager
		self._state = self.STATE_NONE
		self._serial = None

		self._detection_candidates = []
		self._detection_retry = self.DETECTION_RETRIES

		self._temperatureTargetSetThreshold = 25
		self._tempOffsets = dict()
		self._command_queue = CommandQueue()
		self._currentZ = None
		self._currentF = None
		self._heatupWaitStartTime = None
		self._heatupWaitTimeLost = 0.0
		self._pauseWaitStartTime = None
		self._pauseWaitTimeLost = 0.0
		self._currentTool = 0
		self._toolBeforeChange = None
		self._toolBeforeHeatup = None
		self._knownInvalidTools = set()

		self._long_running_command = False
		self._heating = False
		self._dwelling_until = False
		self._connection_closing = False

		self._timeout = None
		self._ok_timeout = None
		self._timeout_intervals = dict()
		for key, value in settings().get(["serial", "timeout"], merged=True, asdict=True).items():
			try:
				self._timeout_intervals[key] = float(value)
			except ValueError:
				pass

		self._consecutive_timeouts = 0
		self._consecutive_timeout_maximums = dict()
		for key, value in settings().get(["serial", "maxCommunicationTimeouts"], merged=True, asdict=True).items():
			try:
				self._consecutive_timeout_maximums[key] = int(value)
			except ValueError:
				pass

		self._max_write_passes = settings().getInt(["serial", "maxWritePasses"])

		self._hello_command = settings().get(["serial", "helloCommand"])
		self._hello_sent = 0
		self._trigger_ok_for_m29 = settings().getBoolean(["serial", "triggerOkForM29"])

		self._alwaysSendChecksum = settings().getBoolean(["serial", "alwaysSendChecksum"])
		self._neverSendChecksum = settings().getBoolean(["serial", "neverSendChecksum"])
		self._sendChecksumWithUnknownCommands = settings().getBoolean(["serial", "sendChecksumWithUnknownCommands"])
		self._unknownCommandsNeedAck = settings().getBoolean(["serial", "unknownCommandsNeedAck"])
		self._sdAlwaysAvailable = settings().getBoolean(["serial", "sdAlwaysAvailable"])
		self._sdRelativePath = settings().getBoolean(["serial", "sdRelativePath"])
		self._blockWhileDwelling = settings().getBoolean(["serial", "blockWhileDwelling"])
		self._send_m112_on_error = settings().getBoolean(["serial", "sendM112OnError"])
		self._disable_sd_printing_detection = settings().getBoolean(["serial", "disableSdPrintingDetection"])
		self._current_line = 1
		self._line_mutex = threading.RLock()
		self._resendDelta = None

		self._capability_support = {
			self.CAPABILITY_AUTOREPORT_TEMP: settings().getBoolean(["serial", "capabilities", "autoreport_temp"]),
			self.CAPABILITY_AUTOREPORT_SD_STATUS: settings().getBoolean(["serial", "capabilities", "autoreport_sdstatus"]),
			self.CAPABILITY_BUSY_PROTOCOL: settings().getBoolean(["serial", "capabilities", "busy_protocol"]),
			self.CAPABILITY_EMERGENCY_PARSER: settings().getBoolean(["serial", "capabilities", "emergency_parser"]),
			self.CAPABILITY_CHAMBER_TEMP: settings().getBoolean(["serial", "capabilities", "chamber_temp"])
		}

		self._lastLines = deque([], 50)
		self._lastCommError = None
		self._lastResendNumber = None
		self._currentResendCount = 0

		self._currentConsecutiveResendNumber = None
		self._currentConsecutiveResendCount = 0
		self._maxConsecutiveResends = settings().getInt(["serial", "maxConsecutiveResends"])

		self._errorValue = ""

		self._firmware_detection = settings().getBoolean(["serial", "firmwareDetection"])
		self._firmware_info_received = False
		self._firmware_info = dict()
		self._firmware_capabilities = dict()

		self._temperature_autoreporting = False
		self._sdstatus_autoreporting = False
		self._busy_protocol_detected = False
		self._busy_protocol_support = False

		self._trigger_ok_after_resend = settings().get(["serial", "supportResendsWithoutOk"])
		self._resend_ok_timer = None

		self._resendActive = False

		terminal_log_size = settings().getInt(["serial", "terminalLogSize"])
		self._terminal_log = deque([], min(20, terminal_log_size))

		self._disconnect_on_errors = settings().getBoolean(["serial", "disconnectOnErrors"])
		self._ignore_errors = settings().getBoolean(["serial", "ignoreErrorsFromFirmware"])

		self._log_resends = settings().getBoolean(["serial", "logResends"])

		# don't log more resends than 5 / 60s
		self._log_resends_rate_start = None
		self._log_resends_rate_count = 0
		self._log_resends_max = 5
		self._log_resends_rate_frame = 60

		self._long_running_commands = settings().get(["serial", "longRunningCommands"])
		self._checksum_requiring_commands = settings().get(["serial", "checksumRequiringCommands"])
		self._blocked_commands = settings().get(["serial", "blockedCommands"])
		self._pausing_commands = settings().get(["serial", "pausingCommands"])
		self._emergency_commands = settings().get(["serial", "emergencyCommands"])
		self._sanity_check_tools = settings().getBoolean(["serial", "sanityCheckTools"])

		self._ack_max = settings().getInt(["serial", "ackMax"])
		self._clear_to_send = CountedEvent(name="comm.clear_to_send", minimum=None, maximum=self._ack_max)
		self._send_queue = SendQueue()
		self._temperature_timer = None
		self._sd_status_timer = None

		self._consecutive_not_sd_printing = 0
		self._consecutive_not_sd_printing_maximum = settings().getInt(["serial", "maxNotSdPrinting"])

		self._job_queue = JobQueue()

		# hooks
		self._pluginManager = octoprint.plugin.plugin_manager()

		self._gcode_hooks = dict(
			queuing=self._pluginManager.get_hooks("octoprint.comm.protocol.gcode.queuing"),
			queued=self._pluginManager.get_hooks("octoprint.comm.protocol.gcode.queued"),
			sending=self._pluginManager.get_hooks("octoprint.comm.protocol.gcode.sending"),
			sent=self._pluginManager.get_hooks("octoprint.comm.protocol.gcode.sent")
		)
		self._received_message_hooks = self._pluginManager.get_hooks("octoprint.comm.protocol.gcode.received")
		self._error_message_hooks = self._pluginManager.get_hooks("octoprint.comm.protocol.gcode.error")
		self._atcommand_hooks = dict(
			queuing=self._pluginManager.get_hooks("octoprint.comm.protocol.atcommand.queuing"),
			sending=self._pluginManager.get_hooks("octoprint.comm.protocol.atcommand.sending")
		)
		self._firmware_info_hooks = dict(
			info=self._pluginManager.get_hooks("octoprint.comm.protocol.firmware.info"),
			capabilities=self._pluginManager.get_hooks("octoprint.comm.protocol.firmware.capabilities")
		)

		self._printer_action_hooks = self._pluginManager.get_hooks("octoprint.comm.protocol.action")
		self._gcodescript_hooks = self._pluginManager.get_hooks("octoprint.comm.protocol.scripts")
		self._serial_factory_hooks = self._pluginManager.get_hooks("octoprint.comm.transport.serial.factory")

		self._temperature_hooks = self._pluginManager.get_hooks("octoprint.comm.protocol.temperatures.received")

		# SD status data
		self._sdEnabled = settings().getBoolean(["feature", "sdSupport"])
		self._sdAvailable = False
		self._sdFileList = False
		self._sdFiles = []
		self._sdFileToSelect = None
		self._sdFileToSelectUser = None
		self._ignore_select = False
		self._manualStreaming = False

		self.last_temperature = TemperatureRecord()
		self.pause_temperature = TemperatureRecord()
		self.cancel_temperature = TemperatureRecord()

		self.last_position = PositionRecord()
		self.pause_position = PositionRecord()
		self.cancel_position = PositionRecord()

		self._record_pause_data = False
		self._record_cancel_data = False

		self._suppress_scripts = set()
		self._suppress_scripts_mutex = threading.RLock()

		self._action_users = dict()
		self._action_users_mutex = threading.RLock()

		self._pause_position_timer = None
		self._pause_mutex = threading.RLock()
		self._cancel_position_timer = None
		self._cancel_mutex = threading.RLock()

		self._log_position_on_pause = settings().getBoolean(["serial", "logPositionOnPause"])
		self._log_position_on_cancel = settings().getBoolean(["serial", "logPositionOnCancel"])
		self._abort_heatup_on_cancel = settings().getBoolean(["serial", "abortHeatupOnCancel"])

		# print job
		self._currentFile = None
		self._job_on_hold = CountedEvent()

		# multithreading locks
		self._jobLock = threading.RLock()
		self._sendingLock = threading.RLock()

		# monitoring thread
		self._monitoring_active = True
		self.monitoring_thread = threading.Thread(target=self._monitor, name="comm._monitor")
		self.monitoring_thread.daemon = True

		# sending thread
		self._send_queue_active = True
		self.sending_thread = threading.Thread(target=self._send_loop, name="comm.sending_thread")
		self.sending_thread.daemon = True

	def start(self):
		# doing this here instead of __init__ combats a race condition where
		# self._comm in the printer interface is still None on first pushs from
		# the comm layer during detection
		self.monitoring_thread.start()
		self.sending_thread.start()

	def __del__(self):
		self.close()

	@property
	def _active(self):
		return self._monitoring_active and self._send_queue_active

	def _capability_supported(self, cap):
		return self._capability_support.get(cap, False) and self._firmware_capabilities.get(cap, False)

	##~~ internal state management

	def _changeState(self, newState):
		if self._state == newState:
			return

		if newState == self.STATE_CLOSED or newState == self.STATE_CLOSED_WITH_ERROR:
			if settings().getBoolean(["feature", "sdSupport"]):
				self._sdFileList = False
				self._sdFiles = []
				self._callback.on_comm_sd_files([])

			if self._currentFile is not None:
				if self.isBusy():
					self._recordFilePosition()
				self._currentFile.close()

		oldState = self.getStateString()
		self._state = newState

		text = "Changing monitoring state from \"{}\" to \"{}\"".format(oldState, self.getStateString())
		self._log(text)
		self._logger.info(text)
		self._callback.on_comm_state_change(newState)

	def _dual_log(self, message, level=logging.ERROR, prefix=""):
		self._logger.log(level, message)
		self._log(prefix + message)

	def _log(self, message):
		message = to_unicode(message)

		self._terminal_log.append(message)
		self._callback.on_comm_log(message)
		self._serialLogger.debug(message)

	def _to_logfile_with_terminal(self, message=None, level=logging.INFO):
		log = "Last lines in terminal:\n" + "\n".join(map(lambda x: "| {}".format(x), list(self._terminal_log)))
		if message is not None:
			log = message + "\n| " + log
		self._logger.log(level, log)

	def _addToLastLines(self, cmd):
		self._lastLines.append(cmd)

	##~~ getters

	def getState(self):
		return self._state

	def getStateId(self, state=None):
		if state is None:
			state = self._state

		possible_states = list(filter(lambda x: x.startswith("STATE_"), self.__class__.__dict__.keys()))
		for possible_state in possible_states:
			if getattr(self, possible_state) == state:
				return possible_state[len("STATE_"):]

		return "UNKNOWN"

	def getStateString(self, state=None):
		if state is None:
			state = self._state

		if state == self.STATE_NONE:
			return "Offline"
		elif state == self.STATE_OPEN_SERIAL:
			return "Opening serial connection"
		elif state == self.STATE_DETECT_SERIAL:
			return "Detecting serial connection"
		elif state == self.STATE_CONNECTING:
			return "Connecting"
		elif state == self.STATE_OPERATIONAL:
			return "Operational"
		elif state == self.STATE_STARTING:
			if self.isSdFileSelected():
				return "Starting print from SD"
			elif self.isStreaming():
				return "Starting to send file to SD"
			else:
				return "Starting"
		elif state == self.STATE_PRINTING:
			if self.isSdFileSelected():
				return "Printing from SD"
			elif self.isStreaming():
				return "Sending file to SD"
			else:
				return "Printing"
		elif state == self.STATE_CANCELLING:
			return "Cancelling"
		elif state == self.STATE_PAUSING:
			return "Pausing"
		elif state == self.STATE_PAUSED:
			return "Paused"
		elif state == self.STATE_RESUMING:
			return "Resuming"
		elif state == self.STATE_FINISHING:
			return "Finishing"
		elif state == self.STATE_CLOSED:
			return "Offline"
		elif state == self.STATE_ERROR:
			return "Error: {}".format(self.getErrorString())
		elif state == self.STATE_CLOSED_WITH_ERROR:
			return "Offline (Error: {})".format(self.getErrorString())
		elif state == self.STATE_TRANSFERING_FILE:
			return "Transferring file to SD"
		return "Unknown State ({})".format(self._state)

	def getErrorString(self):
		return self._errorValue

	def isClosedOrError(self):
		return self._state in (self.STATE_ERROR, self.STATE_CLOSED, self.STATE_CLOSED_WITH_ERROR)

	def isError(self):
		return self._state in (self.STATE_ERROR, self.STATE_CLOSED_WITH_ERROR)

	def isOperational(self):
		return self._state in self.OPERATIONAL_STATES

	def isPrinting(self):
		return self._state in self.PRINTING_STATES

	def isCancelling(self):
		return self._state == self.STATE_CANCELLING

	def isPausing(self):
		return self._state == self.STATE_PAUSING

	def isResuming(self):
		return self._state == self.STATE_RESUMING

	def isStarting(self):
		return self._state == self.STATE_STARTING

	def isFinishing(self):
		return self._state == self.STATE_FINISHING

	def isSdPrinting(self):
		return self.isSdFileSelected() and self.isPrinting()

	def isSdFileSelected(self):
		return self._currentFile is not None and isinstance(self._currentFile, PrintingSdFileInformation)

	def isStreaming(self):
		return self._currentFile is not None and isinstance(self._currentFile, StreamingGcodeFileInformation) and not self._currentFile.done

	def isPaused(self):
		return self._state == self.STATE_PAUSED

	def isBusy(self):
		return self.isPrinting() or self.isPaused() or self._state in (self.STATE_CANCELLING, self.STATE_PAUSING)

	def isSdReady(self):
		return self._sdAvailable

	def getPrintProgress(self):
		if self._currentFile is None:
			return None
		return self._currentFile.getProgress()

	def getPrintFilepos(self):
		if self._currentFile is None:
			return None
		return self._currentFile.getFilepos()

	def getPrintTime(self):
		if self._currentFile is None or self._currentFile.getStartTime() is None:
			return None
		else:
			return monotonic_time() - self._currentFile.getStartTime() - self._pauseWaitTimeLost

	def getCleanedPrintTime(self):
		printTime = self.getPrintTime()
		if printTime is None:
			return None

		cleanedPrintTime = printTime - self._heatupWaitTimeLost
		if cleanedPrintTime < 0:
			cleanedPrintTime = 0.0
		return cleanedPrintTime

	def getTemp(self):
		return self.last_temperature.tools

	def getBedTemp(self):
		return self.last_temperature.bed

	def getOffsets(self):
		return dict(self._tempOffsets)

	def getCurrentTool(self):
		return self._currentTool

	def getConnection(self):
		port = self._port
		baudrate = self._baudrate

		if self._serial is not None:
			if hasattr(self._serial, "port"):
				port = self._serial.port
			if hasattr(self._serial, "baudrate"):
				baudrate = self._serial.baudrate

		return port, baudrate

	def getTransport(self):
		return self._serial

	##~~ external interface

	@contextlib.contextmanager
	def job_put_on_hold(self, blocking=True):
		if not self._job_on_hold.acquire(blocking=blocking):
			raise RuntimeError("Could not acquire job_on_hold lock")

		self._job_on_hold.set()
		try:
			yield
		finally:
			self._job_on_hold.clear()
			if self._job_on_hold.counter == 0:
				self._continue_sending()
			self._job_on_hold.release()

	@property
	def job_on_hold(self):
		return self._job_on_hold.counter > 0

	def set_job_on_hold(self, value, blocking=True):
		trigger = False

		# don't run any locking code beyond this...
		if not self._job_on_hold.acquire(blocking=blocking):
			return False

		try:
			if value:
				self._job_on_hold.set()
			else:
				self._job_on_hold.clear()
				if self._job_on_hold.counter == 0:
					trigger = True
		finally:
			self._job_on_hold.release()

		# locking code is now safe to run again
		if trigger:
			self._continue_sending()

		return True

	def close(self, is_error=False, wait=True, timeout=10.0, *args, **kwargs):
		"""
		Closes the connection to the printer.

		If ``is_error`` is False, will attempt to send the ``beforePrinterDisconnected``
		gcode script. If ``is_error`` is False and ``wait`` is True, will wait
		until all messages in the send queue (including the ``beforePrinterDisconnected``
		gcode script) have been sent to the printer.

		Arguments:
		   is_error (bool): Whether the closing takes place due to an error (True)
		      or not (False, default)
		   wait (bool): Whether to wait for all messages in the send
		      queue to be processed before closing (True, default) or not (False)
		"""

		# legacy parameters
		is_error = kwargs.get("isError", is_error)

		if self._connection_closing:
			return
		self._connection_closing = True

		if self._temperature_timer is not None:
			try:
				self._temperature_timer.cancel()
			except Exception:
				pass

		if self._sd_status_timer is not None:
			try:
				self._sd_status_timer.cancel()
			except Exception:
				pass

		def deactivate_monitoring_and_send_queue():
			self._monitoring_active = False
			self._send_queue_active = False

		if self._serial is not None:
			if not is_error and self._state in self.OPERATIONAL_STATES:
				self.sendGcodeScript("beforePrinterDisconnected")
				if wait:
					if timeout is not None:
						stop = monotonic_time() + timeout
						while (self._command_queue.unfinished_tasks or self._send_queue.unfinished_tasks) and monotonic_time() < stop:
							time.sleep(0.1)
					else:
						self._command_queue.join()
						self._send_queue.join()

			deactivate_monitoring_and_send_queue()

			try:
				if hasattr(self._serial, "cancel_read") and callable(self._serial.cancel_read):
					self._serial.cancel_read()
			except Exception:
				self._logger.exception("Error while cancelling pending reads from the serial port")

			try:
				if hasattr(self._serial, "cancel_write") and callable(self._serial.cancel_write):
					self._serial.cancel_write()
			except Exception:
				self._logger.exception("Error while cancelling pending writes to the serial port")

			try:
				self._serial.close()
			except Exception:
				self._logger.exception("Error while trying to close serial port")
				is_error = True

		else:
			deactivate_monitoring_and_send_queue()

		self._serial = None

		# if we are printing, this will also make sure of firing PRINT_FAILED
		if is_error:
			self._changeState(self.STATE_CLOSED_WITH_ERROR)
		else:
			self._changeState(self.STATE_CLOSED)

		if settings().getBoolean(["feature", "sdSupport"]):
			self._sdFileList = []

	def setTemperatureOffset(self, offsets):
		self._tempOffsets.update(offsets)

	def fakeOk(self):
		self._handle_ok()

	def sendCommand(self, cmd, cmd_type=None, part_of_job=False, processed=False, force=False, on_sent=None, tags=None):
		if not isinstance(cmd, QueueMarker):
			cmd = to_unicode(cmd, errors="replace")
			if not processed:
				cmd = process_gcode_line(cmd)
				if not cmd:
					return False

			gcode = gcode_command_for_cmd(cmd)
			force = force or gcode in self._emergency_commands

		if tags is None:
			tags = set()

		if part_of_job:
			self._job_queue.put((cmd, cmd_type, on_sent, tags | {"source:job"}))
			return True
		elif self.isPrinting() and not self.isSdFileSelected() and not self.job_on_hold and not force:
			try:
				self._command_queue.put((cmd, cmd_type, on_sent, tags), item_type=cmd_type)
				return True
			except TypeAlreadyInQueue as e:
				self._logger.debug("Type already in command queue: " + e.type)
				return False
		elif self.isOperational() or force:
			return self._sendCommand(cmd, cmd_type=cmd_type, on_sent=on_sent, tags=tags)

	def _getGcodeScript(self, scriptName, replacements=None):
		context = dict()
		if replacements is not None and isinstance(replacements, dict):
			context.update(replacements)

		context.update(dict(
			printer_profile=self._printerProfileManager.get_current_or_default(),
			last_position=self.last_position,
			last_temperature=self.last_temperature.as_script_dict()
		))

		if scriptName == "afterPrintPaused" or scriptName == "beforePrintResumed":
			context.update(dict(pause_position=self.pause_position,
			                    pause_temperature=self.pause_temperature.as_script_dict()))
		elif scriptName == "afterPrintCancelled":
			context.update(dict(cancel_position=self.cancel_position,
			                    cancel_temperature=self.cancel_temperature.as_script_dict()))

		scriptLinesPrefix = []
		scriptLinesSuffix = []

		for name, hook in self._gcodescript_hooks.items():
			try:
				retval = hook(self, "gcode", scriptName)
			except Exception:
				self._logger.exception("Error while processing hook {name}.".format(**locals()),
				                       extra=dict(plugin=name))
			else:
				if retval is None:
					continue
				if not isinstance(retval, (list, tuple)) or not len(retval) in [2, 3, 4]:
					continue

				def to_list(data, t):
					if isinstance(data, basestring):
						data = list(s.strip() for s in data.split("\n"))

					if isinstance(data, (list, tuple)):
						return list(map(lambda x: (x, t), data))
					else:
						return None

				additional_tags = {"plugin:{}".format(name)}
				if len(retval) == 4:
					additional_tags |= set(retval[3])

				prefix, suffix = map(lambda x: to_list(x, additional_tags), retval[0:2])
				if prefix:
					scriptLinesPrefix = list(prefix) + scriptLinesPrefix
				if suffix:
					scriptLinesSuffix += list(suffix)

				if len(retval) == 3:
					variables = retval[2]
					context.update(dict(plugins={name:variables}))

		template = settings().loadScript("gcode", scriptName, context=context)
		if template is None:
			scriptLines = []
		else:
			scriptLines = template.split("\n")

		scriptLines = scriptLinesPrefix + scriptLines + scriptLinesSuffix

		def process(line):
			tags = set()
			if isinstance(line, tuple) and len(line) == 2 and isinstance(line[0], basestring) and isinstance(line[1], set):
				tags = line[1]
				line = line[0]
			return process_gcode_line(line), tags

		return list(filter(lambda x: x[0] is not None and x[0].strip() != "",
		              	   map(process,
		                  	   scriptLines)))


	def sendGcodeScript(self, scriptName, replacements=None, tags=None, part_of_job=False):
		if tags is None:
			tags = set()

		scriptLines = self._getGcodeScript(scriptName, replacements=replacements)
		tags_to_use = tags | {"trigger:comm.send_gcode_script", "source:script", "script:{}".format(scriptName)}
		for line in scriptLines:
			# noinspection PyCompatibility
			if isinstance(line, tuple) and len(line) == 2 and isinstance(line[0], basestring) and isinstance(line[1], set):
				# 2-tuple: line + tags
				ttu = tags_to_use | line[1]
				line = line[0]
			elif isinstance(line, basestring):
				# just a line
				ttu = tags_to_use
			else:
				# whatever
				continue

			self.sendCommand(line, part_of_job=part_of_job, tags=ttu)

		return "\n".join(map(lambda x: x if isinstance(x, basestring) else x[0], scriptLines))

	def startPrint(self, pos=None, tags=None, external_sd=False, user=None):
		if not self.isOperational() or self.isPrinting():
			return

		if self._currentFile is None:
			raise ValueError("No file selected for printing")

		self._heatupWaitStartTime = None if not self._heating else monotonic_time()
		self._heatupWaitTimeLost = 0.0
		self._pauseWaitStartTime = 0
		self._pauseWaitTimeLost = 0.0

		if tags is None:
			tags = set()

		try:
			with self._jobLock:
				self._consecutive_not_sd_printing = 0

				self._currentFile.start()
				self._changeState(self.STATE_STARTING)

				if not self.isSdFileSelected():
					self.resetLineNumbers(part_of_job=True, tags={"trigger:comm.start_print"})

				self._callback.on_comm_print_job_started(user=user)

				if self.isSdFileSelected():
					if not external_sd:
						# make sure to ignore the "file selected" later on, otherwise we'll reset our progress data
						self._ignore_select = True

						self.sendCommand("M23 {filename}".format(filename=self._currentFile.getFilename()),
						                 part_of_job=True,
						                 tags=tags | {"trigger:comm.start_print",})
						if pos is not None and isinstance(pos, int) and pos > 0:
							self._currentFile.pos = pos
							self.sendCommand("M26 S{}".format(pos),
							                 part_of_job=True,
							                 tags=tags | {"trigger:comm.start_print",})
						else:
							self._currentFile.pos = 0

						self.sendCommand("M24",
						                 part_of_job=True,
						                 tags=tags | {"trigger:comm.start_print",})
				else:
					if pos is not None and isinstance(pos, int) and pos > 0:
						self._currentFile.seek(pos)

				self.sendCommand(SendQueueMarker(lambda: self._changeState(self.STATE_PRINTING)), part_of_job=True)

				# now make sure we actually do something, up until now we only filled up the queue
				self._continue_sending()
		except Exception:
			self._logger.exception("Error while trying to start printing")
			self._trigger_error(get_exception_string(), "start_print")

	def startFileTransfer(self, path, localFilename, remoteFilename, special=False, tags=None):
		if not self.isOperational() or self.isBusy():
			self._logger.info("Printer is not operational or busy")
			return

		if tags is None:
			tags = set()

		with self._jobLock:
			self.resetLineNumbers(tags={"trigger:comm.start_file_transfer"})

			if special:
				self._currentFile = SpecialStreamingGcodeFileInformation(path, localFilename, remoteFilename)
			else:
				self._currentFile = StreamingGcodeFileInformation(path, localFilename, remoteFilename)
			self._currentFile.start()

			self.sendCommand("M28 %s" % remoteFilename, tags=tags | {"trigger:comm.start_file_transfer",})
			self._callback.on_comm_file_transfer_started(localFilename,
			                                             remoteFilename,
			                                             self._currentFile.getFilesize(),
			                                             user=self._currentFile.getUser())

	def cancelFileTransfer(self, tags=None):
		if not self.isOperational() or not self.isStreaming():
			self._logger.info("Printer is not operational or not streaming")
			return

		self._finishFileTransfer(failed=True, tags=tags)

	def _finishFileTransfer(self, failed=False, tags=None):
		if tags is None:
			tags = set()

		with self._jobLock:
			remote = self._currentFile.getRemoteFilename()

			self._sendCommand("M29", tags=tags | {"trigger:comm.finish_file_transfer",})
			if failed:
				self.deleteSdFile(remote)

			local = self._currentFile.getLocalFilename()
			elapsed = self.getPrintTime()

			def finalize():
				self._currentFile = None
				self._changeState(self.STATE_OPERATIONAL)

				if failed:
					self._callback.on_comm_file_transfer_failed(local, remote, elapsed)
				else:
					self._callback.on_comm_file_transfer_done(local, remote, elapsed)

				self.refreshSdFiles(tags={"trigger:comm.finish_file_transfer",})
			self._sendCommand(SendQueueMarker(finalize))

	def selectFile(self, filename, sd, user=None, tags=None):
		if self.isBusy():
			return

		if tags is None:
			tags = set()

		if sd:
			if not self.isOperational():
				# printer is not connected, can't use SD
				return

			if filename.startswith("/") and self._sdRelativePath:
				filename = filename[1:]

			self._sdFileToSelect = filename
			self._sdFileToSelectUser = user
			self.sendCommand("M23 %s" % filename, tags=tags | {"trigger:comm.select_file",})
		else:
			self._currentFile = PrintingGcodeFileInformation(filename,
			                                                 offsets_callback=self.getOffsets,
			                                                 current_tool_callback=self.getCurrentTool,
			                                                 user=user)
			self._callback.on_comm_file_selected(filename, self._currentFile.getFilesize(), False, user=user)

	def unselectFile(self):
		if self.isBusy():
			return

		self._currentFile = None
		self._callback.on_comm_file_selected(None, None, False, user=None)

	def _cancel_preparation_failed(self):
		timeout = self._timeout_intervals.get("positionLogWait", 10.0)
		self._log("Did not receive parseable position data from printer within {}s, continuing without it".format(timeout))
		self._cancel_preparation_done()

	def _cancel_preparation_done(self, check_timer=True, user=None):
		if user is None:
			with self._action_users_mutex:
				try:
					user = self._action_users.pop("cancel")
				except KeyError:
					pass

		with self._cancel_mutex:
			if self._cancel_position_timer is not None:
				self._cancel_position_timer.cancel()
				self._cancel_position_timer = None
			elif check_timer:
				return

			self._currentFile.done = True
			self._recordFilePosition()
			self._callback.on_comm_print_job_cancelled(user=user)

			def finalize():
				self._changeState(self.STATE_OPERATIONAL)
			self.sendCommand(SendQueueMarker(finalize), part_of_job=True)
			self._continue_sending()

	def cancelPrint(self, firmware_error=None, disable_log_position=False, user=None, tags=None, external_sd=False):
		if not self.isOperational():
			return

		if not self.isBusy() or self._currentFile is None:
			# we aren't even printing, nothing to cancel...
			return

		if self.isStreaming():
			# we are streaming, we handle cancelling that differently...
			self.cancelFileTransfer()
			return

		if tags is None:
			tags = set()

		def _on_M400_sent():
			# we don't call on_print_job_cancelled on our callback here
			# because we do this only after our M114 has been answered
			# by the firmware
			self._record_cancel_data = True

			with self._cancel_mutex:
				if self._cancel_position_timer is not None:
					self._cancel_position_timer.cancel()
				self._cancel_position_timer = ResettableTimer(self._timeout_intervals.get("positionLogWait", 10.0),
				                                              self._cancel_preparation_failed)
				self._cancel_position_timer.daemon = True
				self._cancel_position_timer.start()
			self.sendCommand("M114", part_of_job=True, tags=tags | {"trigger:comm.cancel",
			                                                        "trigger:cancel",
			                                                        "trigger:record_position"})

		self._callback.on_comm_print_job_cancelling(firmware_error=firmware_error,
		                                            user=user)

		with self._jobLock:
			self._changeState(self.STATE_CANCELLING)

			if self._abort_heatup_on_cancel:
				# abort any ongoing heatups immediately to get back control over the printer
				self.sendCommand("M108",
				                 part_of_job=False,
				                 tags=tags | {"trigger:comm.cancel", "trigger:cancel", "trigger:abort_heatup"},
				                 force=True)

			if self.isSdFileSelected():
				if not external_sd:
					self.sendCommand("M25", part_of_job=True, tags=tags | {"trigger:comm.cancel", "trigger:cancel"})    # pause print
					self.sendCommand("M27", part_of_job=True, tags=tags | {"trigger:comm.cancel", "trigger:cancel"})    # get current byte position in file
					self.sendCommand("M26 S0", part_of_job=True, tags=tags | {"trigger:comm.cancel", "trigger:cancel"}) # reset position in file to byte 0

			if self._log_position_on_cancel and not disable_log_position:
				with self._action_users_mutex:
					self._action_users["cancel"] = user

				self.sendCommand("M400",
				                 on_sent=_on_M400_sent,
				                 part_of_job=True,
				                 tags=tags | {"trigger:comm.cancel",
				                              "trigger:cancel",
				                              "trigger:record_position"})
				self._continue_sending()
			else:
				self._cancel_preparation_done(check_timer=False,
				                              user=user)

	def _pause_preparation_failed(self):
		timeout = self._timeout_intervals.get("positionLogWait", 10.0)
		self._log("Did not receive parseable position data from printer within {}s, continuing without it".format(timeout))
		self._pause_preparation_done()

	def _pause_preparation_done(self, check_timer=True, suppress_script=False, user=None):
		if user is None:
			with self._action_users_mutex:
				try:
					user = self._action_users.pop("pause")
				except KeyError:
					pass

		with self._pause_mutex:
			if self._pause_position_timer is not None:
				self._pause_position_timer.cancel()
				self._pause_position_timer = None
			elif check_timer:
				return

			self._callback.on_comm_print_job_paused(suppress_script=suppress_script,
			                                        user=user)

			def finalize():
				# only switch to PAUSED if we were still PAUSING, to avoid "swallowing" received resumes during
				# pausing
				if self._state == self.STATE_PAUSING:
					self._changeState(self.STATE_PAUSED)
			self.sendCommand(SendQueueMarker(finalize), part_of_job=True)
			self._continue_sending()

	def setPause(self, pause, local_handling=True, user=None, tags=None):
		if self.isStreaming():
			return

		if not self._currentFile:
			return

		if tags is None:
			tags = set()

		valid_paused_states = (self.STATE_PAUSED, self.STATE_PAUSING)
		valid_running_states = (self.STATE_PRINTING, self.STATE_STARTING, self.STATE_RESUMING)

		if not self._state in valid_paused_states + valid_running_states:
			return

		with self._jobLock:
			if not pause and self._state in valid_paused_states:
				if self._pauseWaitStartTime:
					self._pauseWaitTimeLost = self._pauseWaitTimeLost + (monotonic_time() - self._pauseWaitStartTime)
					self._pauseWaitStartTime = None

				self._changeState(self.STATE_RESUMING)
				self._callback.on_comm_print_job_resumed(suppress_script=not local_handling,
				                                         user=user)

				if self.isSdFileSelected():
					if local_handling:
						self.sendCommand("M24",
						                 part_of_job=True,
						                 tags=tags | {"trigger:comm.set_pause","trigger:resume"})
					self.sendCommand("M27",
					                 part_of_job=True,
					                 tags=tags | {"trigger:comm.set_pause", "trigger:resume"})

				def finalize():
					if self._state == self.STATE_RESUMING:
						self._changeState(self.STATE_PRINTING)
				self.sendCommand(SendQueueMarker(finalize), part_of_job=True)

				# now make sure we actually do something, up until now we only filled up the queue
				self._continue_sending()

			elif pause and self._state in valid_running_states:
				if not self._pauseWaitStartTime:
					self._pauseWaitStartTime = monotonic_time()

				self._changeState(self.STATE_PAUSING)
				if self.isSdFileSelected() and local_handling:
					self.sendCommand("M25",
					                 part_of_job=True,
					                 tags=tags | {"trigger:comm.set_pause", "trigger:pause"}) # pause print

				def _on_M400_sent():
					# we don't call on_print_job_paused on our callback here
					# because we do this only after our M114 has been answered
					# by the firmware
					self._record_pause_data = True

					with self._pause_mutex:
						if self._pause_position_timer is not None:
							self._pause_position_timer.cancel()
							self._pause_position_timer = None
						self._pause_position_timer = ResettableTimer(self._timeout_intervals.get("positionLogWait", 10.0),
						                                             self._pause_preparation_failed)
						self._pause_position_timer.daemon = True
						self._pause_position_timer.start()
					self.sendCommand("M114",
					                 part_of_job=True,
					                 tags=tags | {"trigger:comm.set_pause",
					                              "trigger:pause",
					                              "trigger:record_position"})

				if self._log_position_on_pause and local_handling:
					with self._action_users_mutex:
						self._action_users["pause"] = user

					self.sendCommand("M400",
					                 on_sent=_on_M400_sent,
					                 part_of_job=True,
					                 tags=tags | {"trigger:comm.set_pause",
					                              "trigger:pause",
					                              "trigger:record_position"})
					self._continue_sending()
				else:
					self._pause_preparation_done(check_timer=False,
					                             suppress_script=not local_handling,
					                             user=user)

	def getSdFiles(self):
		return self._sdFiles

	def deleteSdFile(self, filename, tags=None):
		if not self._sdEnabled:
			return

		if tags is None:
			tags = set()

		if not self.isOperational() or (self.isBusy() and
				isinstance(self._currentFile, PrintingSdFileInformation) and
				self._currentFile.getFilename() == filename):
			# do not delete a file from sd we are currently printing from
			return

		self.sendCommand("M30 %s" % filename.lower(), tags=tags | {"trigger:comm.delete_sd_file",})
		self.refreshSdFiles()

	def refreshSdFiles(self, tags=None):
		if not self._sdEnabled:
			return

		if not self.isOperational() or self.isBusy():
			return

		if tags is None:
			tags = set()

		self.sendCommand("M20", tags=tags | {"trigger:comm.refresh_sd_files",})

	def initSdCard(self, tags=None):
		if not self._sdEnabled:
			return

		if not self.isOperational():
			return

		if tags is None:
			tags = set()

		self.sendCommand("M21", tags=tags | {"trigger:comm.init_sd_card"})
		if self._sdAlwaysAvailable:
			self._sdAvailable = True
			self.refreshSdFiles()
			self._callback.on_comm_sd_state_change(self._sdAvailable)

	def releaseSdCard(self, tags=None):
		if not self._sdEnabled:
			return

		if not self.isOperational() or (self.isBusy() and self.isSdFileSelected()):
			# do not release the sd card if we are currently printing from it
			return

		if tags is None:
			tags = set()

		self.sendCommand("M22", tags=tags | {"trigger:comm.release_sd_card",})
		self._sdAvailable = False
		self._sdFiles = []

		self._callback.on_comm_sd_state_change(self._sdAvailable)
		self._callback.on_comm_sd_files(self._sdFiles)

	def sayHello(self, tags=None):
		if tags is None:
			tags = set()

		self.sendCommand(self._hello_command, force=True, tags=tags | {"trigger:comm.say_hello",})
		self._clear_to_send.set()
		self._hello_sent += 1

	def resetLineNumbers(self, number=0, part_of_job=False, tags=None):
		if not self.isOperational():
			return

		if tags is None:
			tags = set()

		self.sendCommand("M110 N{}".format(number),
		                 part_of_job=part_of_job,
		                 tags=tags | {"trigger:comm.reset_line_numbers",})

	##~~ record aborted file positions

	def getFilePosition(self):
		if self._currentFile is None:
			return None

		origin = self._currentFile.getFileLocation()
		filename = self._currentFile.getFilename()
		pos = self._currentFile.getFilepos()

		return dict(origin=origin,
		            filename=filename,
		            pos=pos)

	def _recordFilePosition(self):
		if self._currentFile is None:
			return
		data = self.getFilePosition()
		self._callback.on_comm_record_fileposition(data["origin"], data["filename"], data["pos"])

	##~~ communication monitoring and handling

	def _processTemperatures(self, line):
		current_tool = self._currentTool if self._currentTool is not None else 0
		current_tool_key = "T%d" % current_tool
		maxToolNum, parsedTemps = parse_temperature_line(line, current_tool)

		maxToolNum = max(maxToolNum, self._printerProfileManager.get_current_or_default()["extruder"]["count"] - 1)

		for name, hook in self._temperature_hooks.items():
			try:
				parsedTemps = hook(self, parsedTemps)
				if parsedTemps is None or not parsedTemps:
					return
			except Exception:
				self._logger.exception("Error while processing temperatures in {}, skipping".format(name),
				                       extra=dict(plugin=name))

		if current_tool_key in parsedTemps or "T0" in parsedTemps:
			shared_nozzle = self._printerProfileManager.get_current_or_default()["extruder"]["sharedNozzle"]
			shared_temp = parsedTemps[current_tool_key] if current_tool_key in parsedTemps else parsedTemps["T0"]

			for n in range(maxToolNum + 1):
				tool = "T%d" % n
				if not tool in parsedTemps:
					if shared_nozzle:
						actual, target = shared_temp
					else:
						continue
				else:
					actual, target = parsedTemps[tool]
					del parsedTemps[tool]
				self.last_temperature.set_tool(n, actual=actual, target=target)

		# bed temperature
		if "B" in parsedTemps:
			actual, target = parsedTemps["B"]
			del parsedTemps["B"]
			self.last_temperature.set_bed(actual=actual, target=target)

		# chamber temperature
		if "C" in parsedTemps and (self._capability_supported(self.CAPABILITY_CHAMBER_TEMP) or self._printerProfileManager.get_current_or_default()["heatedChamber"]):
			actual, target = parsedTemps["C"]
			del parsedTemps["C"]
			self.last_temperature.set_chamber(actual=actual, target=target)

		# all other injected temperatures
		for key in parsedTemps.keys():
			actual, target = parsedTemps[key]
			self.last_temperature.set_custom(key, actual=actual, target=target)

	##~~ Serial monitor processing received messages

	def _monitor(self):
		feedback_controls, feedback_matcher = convert_feedback_controls(settings().get(["controls"]))
		feedback_errors = []
		pause_triggers = convert_pause_triggers(settings().get(["printerParameters", "pauseTriggers"]))

		disable_external_heatup_detection = not settings().getBoolean(["serial", "externalHeatupDetection"])

		self._consecutive_timeouts = 0

		# Open the serial port
		needs_detection = not (self._port and self._port != 'AUTO' and self._baudrate)
		try_hello = False

		if not needs_detection:
			self._changeState(self.STATE_OPEN_SERIAL)
			if not self._open_serial(self._port, self._baudrate):
				return
			try_hello = not settings().getBoolean(["serial", "waitForStartOnConnect"])
			self._changeState(self.STATE_CONNECTING)
			self._timeout = self._ok_timeout = self._get_new_communication_timeout()
		else:
			self._changeState(self.STATE_DETECT_SERIAL)
			self._perform_detection_step(init=True)

		if not self._state in (self.STATE_CONNECTING, self.STATE_DETECT_SERIAL):
			# we got cancelled during connection, bail
			return

		# Start monitoring the serial port
		self._log("Connected to: %s, starting monitor" % self._serial)

		startSeen = False
		supportRepetierTargetTemp = settings().getBoolean(["serial", "repetierTargetTemp"])
		supportWait = settings().getBoolean(["serial", "supportWait"])

		# enqueue the "hello command" first thing
		if try_hello:
			self.sayHello()

			# we send a second one right away because sometimes there's garbage on the line on first connect
			# that can kill oks
			self.sayHello()

		while self._monitoring_active:
			try:
				line = self._readline()
				if line is None:
					break

				now = monotonic_time()

				if line.strip() != "":
					self._consecutive_timeouts = 0
					self._timeout = self._get_new_communication_timeout()

					if self._dwelling_until and now > self._dwelling_until:
						self._dwelling_until = False

				if self._resend_ok_timer and line and not line.startswith("ok"):
					# we got anything but an ok after a resend request - this means the ok after the resend request
					# was in fact missing and we now need to trigger the timer
					self._resend_ok_timer.cancel()
					self._resendSimulateOk()

				##~~ busy protocol handling
				if line.startswith("echo:busy:") or line.startswith("busy:"):
					# reset the ok timeout, the regular comm timeout has already been reset
					self._ok_timeout = self._get_new_communication_timeout()

					# make sure the printer sends busy in a small enough interval to match our timeout
					if not self._busy_protocol_detected and self._capability_support.get(self.CAPABILITY_BUSY_PROTOCOL,
					                                                                     False):
						to_log = "Printer seems to support the busy protocol, will adjust timeouts and set busy " \
						         "interval accordingly"
						self._log(to_log)
						self._logger.info(to_log)

						self._busy_protocol_detected = True
						busy_interval = max(int(self._timeout_intervals.get("communicationBusy", 2)) - 1, 1)

						def busyIntervalSet():
							self._logger.info("Telling the printer to set the busy interval to our "
							                  "\"communicationBusy\" timeout - 1s = {}s".format(busy_interval))
							self._busy_protocol_support = True
							self._serial.timeout = self._get_communication_timeout_interval()

						self._set_busy_protocol_interval(interval=busy_interval, callback=busyIntervalSet)

					if self._state not in (self.STATE_CONNECTING, self.STATE_DETECT_SERIAL):
						continue

				##~~ debugging output handling
				elif line.startswith("//"):
					debugging_output = line[2:].strip()
					if debugging_output.startswith("action:"):
						action_command = debugging_output[len("action:"):].strip()

						if action_command == "cancel":
							self._log("Cancelling on request of the printer...")
							self.cancelPrint()
						elif action_command == "pause":
							self._log("Pausing on request of the printer...")
							self.setPause(True)
						elif action_command == "paused":
							self._log("Printer signalled that it paused, switching state...")
							self.setPause(True, local_handling=False)
						elif action_command == "resume":
							self._log("Resuming on request of the printer...")
							self.setPause(False)
						elif action_command == "resumed":
							self._log("Printer signalled that it resumed, switching state...")
							self.setPause(False, local_handling=False)
						elif action_command == "disconnect":
							self._log("Disconnecting on request of the printer...")
							self._callback.on_comm_force_disconnect()
						else:
							for name, hook in self._printer_action_hooks.items():
								try:
									hook(self, line, action_command)
								except Exception:
									self._logger.exception("Error while calling hook from plugin "
									                       "{} with action command {}".format(name, action_command),
									                       extra=dict(plugin=name))
									continue

					if self._state not in (self.STATE_CONNECTING, self.STATE_DETECT_SERIAL):
						continue

				def convert_line(line):
					if line is None:
						return None, None
					stripped_line = line.strip().strip("\0")
					return stripped_line, stripped_line.lower()

				##~~ Error handling
				line = self._handle_errors(line)
				line, lower_line = convert_line(line)

				##~~ SD file list
				# if we are currently receiving an sd file list, each line is just a filename, so just read it and abort processing
				if self._sdFileList and not "End file list" in line:
					preprocessed_line = lower_line
					fileinfo = preprocessed_line.rsplit(None, 1)
					if len(fileinfo) > 1:
						# we might have extended file information here, so let's split filename and size and try to make them a bit nicer
						filename, size = fileinfo
						try:
							size = int(size)
						except ValueError:
							# whatever that was, it was not an integer, so we'll just use the whole line as filename and set size to None
							filename = preprocessed_line
							size = None
					else:
						# no extended file information, so only the filename is there and we set size to None
						filename = preprocessed_line
						size = None

					if valid_file_type(filename, "machinecode"):
						if filter_non_ascii(filename):
							self._logger.warning("Got a file from printer's SD that has a non-ascii filename (%s), that shouldn't happen according to the protocol" % filename)
						else:
							if not filename.startswith("/"):
								# file from the root of the sd -- we'll prepend a /
								filename = "/" + filename
							self._sdFiles.append((filename, size))
						continue

				handled = False

				# process oks
				if line.startswith("ok") or (self.isPrinting() and supportWait and line == "wait"):
					# ok only considered handled if it's alone on the line, might be
					# a response to an M105 or an M114
					self._handle_ok()
					needs_further_handling = "T:" in line or "T0:" in line or "B:" in line or "C:" in line or \
					                         "X:" in line or "NAME:" in line
					handled = (line == "wait" or line == "ok" or not needs_further_handling)

				# process resends
				elif lower_line.startswith("resend") or lower_line.startswith("rs"):
					self._handle_resend_request(line)
					handled = True

				# process timeouts
				elif ((line == "" and now >= self._timeout) or (self.isPrinting()
				                                                and not self.isSdPrinting()
				                                                and (not self.job_on_hold or self._resendActive)
				                                                and not self._long_running_command
				                                                and not self._heating and now >= self._ok_timeout)) \
						and (not self._blockWhileDwelling or not self._dwelling_until or now > self._dwelling_until)\
						and not self._state in (self.STATE_DETECT_SERIAL,):
					# We have two timeout variants:
					#
					# Variant 1: No line at all received within the communication timeout. This can always happen.
					#
					# Variant 2: No ok received while printing within the communication timeout. This can happen if
					#            temperatures are auto reported, because then we'll continue to receive data from the
					#            firmware in fairly regular intervals, even if an ok got lost somewhere and the firmware
					#            is running dry but not sending a wait.
					#
					# Both variants can only happen if we are not currently blocked by a dwelling command

					self._handle_timeout()
					self._ok_timeout = self._get_new_communication_timeout()

					# timeout only considered handled if the printer is printing and it was a comm timeout, not an ok
					# timeout
					handled = self.isPrinting() and line == ""

				# we don't have to process the rest if the line has already been handled fully
				if handled and self._state not in (self.STATE_CONNECTING, self.STATE_DETECT_SERIAL):
					continue

				##~~ position report processing
				if 'X:' in line and 'Y:' in line and 'Z:' in line:
					parsed = parse_position_line(line)
					if parsed:
						# we don't know T or F when printing from SD since
						# there's no way to query it from the firmware and
						# no way to track it ourselves when not streaming
						# the file - this all sucks sooo much
						self.last_position.valid = True
						self.last_position.x = parsed.get("x")
						self.last_position.y = parsed.get("y")
						self.last_position.z = parsed.get("z")

						if "e" in parsed:
							self.last_position.e = parsed.get("e")
						else:
							# multiple extruder coordinates provided, find current one
							self.last_position.e = parsed.get("e{}".format(self._currentTool)) if not self.isSdFileSelected() else None

						for key in [key for key in parsed if key.startswith("e") and len(key) > 1]:
							setattr(self.last_position, key, parsed.get(key))

						self.last_position.t = self._currentTool if not self.isSdFileSelected() else None
						self.last_position.f = self._currentF if not self.isSdFileSelected() else None

						reason = None

						if self._record_pause_data:
							reason = "pause"
							self._record_pause_data = False
							self.pause_position.copy_from(self.last_position)
							self.pause_temperature.copy_from(self.last_temperature)
							self._pause_preparation_done()

						if self._record_cancel_data:
							reason = "cancel"
							self._record_cancel_data = False
							self.cancel_position.copy_from(self.last_position)
							self.cancel_temperature.copy_from(self.last_temperature)
							self._cancel_preparation_done()

						self._callback.on_comm_position_update(self.last_position.as_dict(), reason=reason)

				##~~ temperature processing
				elif ' T:' in line or line.startswith('T:') or ' T0:' in line or line.startswith('T0:') \
						or ((' B:' in line or line.startswith('B:')) and not 'A:' in line):

					if not disable_external_heatup_detection and not self._temperature_autoreporting \
							and not line.strip().startswith("ok") and not self._heating \
							and self._firmware_info_received:
						self._logger.info("Externally triggered heatup detected")
						self._heating = True
						self._heatupWaitStartTime = monotonic_time()

					self._processTemperatures(line)
					self._callback.on_comm_temperature_update(self.last_temperature.tools, self.last_temperature.bed, self.last_temperature.chamber, self.last_temperature.custom)

				elif supportRepetierTargetTemp and ('TargetExtr' in line or 'TargetBed' in line):
					matchExtr = regex_repetierTempExtr.match(line)
					matchBed = regex_repetierTempBed.match(line)

					if matchExtr is not None:
						toolNum = int(matchExtr.group(1))
						try:
							target = float(matchExtr.group(2))
							self.last_temperature.set_tool(toolNum, target=target)
							self._callback.on_comm_temperature_update(self.last_temperature.tools, self.last_temperature.bed, self.last_temperature.chamber, self.last_temperature.custom)
						except ValueError:
							pass
					elif matchBed is not None:
						try:
							target = float(matchBed.group(1))
							self.last_temperature.set_bed(target=target)
							self._callback.on_comm_temperature_update(self.last_temperature.tools, self.last_temperature.bed, self.last_temperature.chamber, self.last_temperature.custom)
						except ValueError:
							pass

				##~~ firmware name & version
				elif "NAME:" in line or line.startswith("NAME."):
					# looks like a response to M115
					data = parse_firmware_line(line)
					firmware_name = data.get("FIRMWARE_NAME")

					if firmware_name is None:
						# Malyan's "Marlin compatible firmware" isn't actually Marlin compatible and doesn't even
						# report its firmware name properly in response to M115. Wonderful - why stick to established
						# protocol when you can do your own thing, right?
						#
						# Examples:
						#
						#     NAME: Malyan VER: 2.9 MODEL: M200 HW: HA02
						#     NAME. Malyan	VER: 3.8	MODEL: M100	HW: HB02
						#     NAME. Malyan VER: 3.7 MODEL: M300 HW: HG01
						#
						# We do a bit of manual fiddling around here to circumvent that issue and get ourselves a
						# reliable firmware name (NAME + VER) out of the Malyan M115 response.
						name = data.get("NAME")
						ver = data.get("VER")
						if name and "malyan" in name.lower() and ver:
							firmware_name = name.strip() + " " + ver.strip()

					eventManager().fire(Events.FIRMWARE_DATA, dict(name=firmware_name, data=data))

					if not self._firmware_info_received and firmware_name:
						firmware_name = firmware_name.strip()
						self._logger.info("Printer reports firmware name \"{}\"".format(firmware_name))

						if self._firmware_detection:
							if "repetier" in firmware_name.lower() or "anet_a8" in firmware_name.lower():
								self._logger.info("Detected Repetier firmware, enabling relevant features for issue free communication")

								self._alwaysSendChecksum = True
								self._blockWhileDwelling = True
								supportRepetierTargetTemp = True
								disable_external_heatup_detection = True

								sd_always_available = self._sdAlwaysAvailable
								self._sdAlwaysAvailable = True
								if not sd_always_available and not self._sdAvailable:
									self.initSdCard()

							elif "reprapfirmware" in firmware_name.lower():
								self._logger.info("Detected RepRapFirmware, enabling relevant features for issue free communication")
								self._sdRelativePath = True

							elif "malyan" in firmware_name.lower():
								self._logger.info("Detected Malyan firmware, enabling relevant features for issue free communication")

								self._alwaysSendChecksum = True
								self._blockWhileDwelling = True

								sd_always_available = self._sdAlwaysAvailable
								self._sdAlwaysAvailable = True
								if not sd_always_available and not self._sdAvailable:
									self.initSdCard()

							elif "teacup" in firmware_name.lower():
								self._logger.info("Detected Teacup firmware, enabling relevant features for issue free communication")

								disable_external_heatup_detection = True # see #2854

							elif "klipper" in firmware_name.lower():
								self._logger.info("Detected Klipper firmware, enabling relevant features for issue free communication")

								self._unknownCommandsNeedAck = True

							elif "ultimaker2" in firmware_name.lower():
								self._logger.info("Detected Ultimaker2 firmware, enabling relevant features for issue free communication")

								self._disable_sd_printing_detection = True

						self._firmware_info_received = True
						self._firmware_info = data
						self._firmware_name = firmware_name

						# notify plugins
						for name, hook in self._firmware_info_hooks["info"].items():
							try:
								hook(self, firmware_name, copy.copy(data))
							except Exception:
								self._logger.exception("Error processing firmware info hook {}:".format(name),
								                       extra=dict(plugin=name))

				##~~ Firmware capability report triggered by M115
				elif lower_line.startswith("cap:"):
					parsed = parse_capability_line(lower_line)
					if parsed is not None:
						capability, enabled = parsed
						self._firmware_capabilities[capability] = enabled

						if self._capability_support.get(capability, False):
							if capability == self.CAPABILITY_AUTOREPORT_TEMP and enabled:
								self._logger.info("Firmware states that it supports temperature autoreporting")
								self._set_autoreport_temperature_interval()
							elif capability == self.CAPABILITY_AUTOREPORT_SD_STATUS and enabled:
								self._logger.info("Firmware states that it supports sd status autoreporting")
								self._set_autoreport_sdstatus_interval()
							elif capability == self.CAPABILITY_EMERGENCY_PARSER and enabled:
								self._logger.info("Firmware states that it supports emergency GCODEs to be sent without waiting for an acknowledgement first")

						# notify plugins
						for name, hook in self._firmware_info_hooks["capabilities"].items():
							try:
								hook(self, capability, enabled, copy.copy(self._firmware_capabilities))
							except Exception:
								self._logger.exception("Error processing firmware capability hook {}:".format(name),
								                       extra=dict(plugin=name))

				##~~ invalid extruder
				elif 'invalid extruder' in lower_line:
					tool = None

					match = regexes_parameters["intT"].search(line)
					if match:
						try:
							tool = int(match.group("value"))
						except ValueError:
							pass # should never happen

					if tool is None or tool == self._currentTool:
						if self._toolBeforeChange is not None:
							fallback_tool = self._toolBeforeChange
						else:
							fallback_tool = 0

						invalid_tool = self._currentTool

						if self._sanity_check_tools:
							# log to terminal and remember as invalid
							self._log("T{} reported as invalid, reverting to T{}".format(invalid_tool, fallback_tool))
							self._knownInvalidTools.add(invalid_tool)

							# we actually do send a T command here instead of just settings self._currentTool just in case
							# we had any scripts or plugins modify stuff due to the prior tool change
							self.sendCommand("T{}".format(fallback_tool), tags={"trigger:revert_invalid_tool",})
						else:
							# just log to terminal, user disabled sanity check
							self._log("T{} reported as invalid by the firmware, but you've "
							          "disabled tool sanity checking, ignoring".format(invalid_tool))

				##~~ SD Card handling
				elif 'SD init fail' in line or 'volume.init failed' in line or 'openRoot failed' in line:
					self._sdAvailable = False
					self._sdFiles = []
					self._callback.on_comm_sd_state_change(self._sdAvailable)
				elif 'SD card ok' in line and not self._sdAvailable:
					self._sdAvailable = True
					self.refreshSdFiles()
					self._callback.on_comm_sd_state_change(self._sdAvailable)
				elif 'Begin file list' in line:
					self._sdFiles = []
					self._sdFileList = True
				elif 'End file list' in line:
					self._sdFileList = False
					self._callback.on_comm_sd_files(self._sdFiles)
				elif 'SD printing byte' in line:
					# answer to M27, at least on Marlin, Repetier and Sprinter: "SD printing byte %d/%d"
					match = regex_sdPrintingByte.search(line)
					if match:
						try:
							current = int(match.group("current"))
							total = int(match.group("total"))
						except:
							self._logger.exception("Error while parsing SD status report")
						else:
							if current == total == 0 \
								and self.isSdPrinting() \
								and not self.isStarting() \
								and not self.isStarting() \
								and not self.isFinishing():
								# apparently not SD printing - some Marlin versions report it like that for some reason
								self._consecutive_not_sd_printing += 1
								if self._consecutive_not_sd_printing > self._consecutive_not_sd_printing_maximum:
									self.cancelPrint(external_sd=True)

							else:
								self._consecutive_not_sd_printing = 0
								if self.isSdFileSelected():

									# If we are not yet sd printing, the current does not equal the total, is larger
									# than zero and has increased since the last time we saw a position report, then
									# yes, this looks like we just started printing due to an external trigger.
									if not self.isSdPrinting() and current != total and current > 0 \
											and self._currentFile and current > self._currentFile.pos:
										self.startPrint(external_sd=True)

									self._currentFile.pos = current
									if self._currentFile.size == 0:
										self._currentFile.size = total

									if not self._currentFile.done:
										self._callback.on_comm_progress()
				elif 'Not SD printing' in line \
					and self.isSdPrinting() \
					and not self.isStarting() \
					and not self.isFinishing():
					self._consecutive_not_sd_printing += 1
					if self._consecutive_not_sd_printing > self._consecutive_not_sd_printing_maximum:
						# something went wrong, printer is reporting that we actually are not printing right now...
						self.cancelPrint(external_sd=True)
				elif 'File opened' in line and not self._ignore_select:
					# answer to M23, at least on Marlin, Repetier and Sprinter: "File opened:%s Size:%d"
					match = regex_sdFileOpened.search(line)
					if match:
						name = match.group("name")
						size = int(match.group("size"))
					else:
						name = "Unknown"
						size = 0
					user = None

					if self._sdFileToSelect:
						name = self._sdFileToSelect
						user = self._sdFileToSelectUser

					self._sdFileToSelect = None
					self._sdFileToSelectUser = None

					self._currentFile = PrintingSdFileInformation(name, size, user=user)
				elif 'File selected' in line:
					if self._ignore_select:
						self._ignore_select = False
					elif self._currentFile is not None and self.isSdFileSelected():
						# final answer to M23, at least on Marlin, Repetier and Sprinter: "File selected"
						self._callback.on_comm_file_selected(self._currentFile.getFilename(),
						                                     self._currentFile.getFilesize(),
						                                     True,
						                                     user=self._currentFile.getUser())
				elif 'Writing to file' in line and self.isStreaming():
					self._changeState(self.STATE_PRINTING)
				elif 'Done printing file' in line and self.isSdPrinting():
					# printer is reporting file finished printing
					self._changeState(self.STATE_FINISHING)

					self._currentFile.done = True
					self._currentFile.pos = 0

					self.sendCommand("M400", part_of_job=True)
					self._callback.on_comm_print_job_done()
					def finalize():
						self._changeState(self.STATE_OPERATIONAL)
					self.sendCommand(SendQueueMarker(finalize), part_of_job=True)
					self._continue_sending()
				elif 'Done saving file' in line:
					if self._trigger_ok_for_m29:
						# workaround for most versions of Marlin out in the wild
						# not sending an ok after saving a file
						self._handle_ok()
				elif 'File deleted' in line and line.strip().endswith("ok"):
					# buggy Marlin version that doesn't send a proper line break after the "File deleted" statement, fixed in
					# current versions
					self._handle_ok()

				##~~ Message handling
				self._callback.on_comm_message(line)

				##~~ Parsing for feedback commands
				if feedback_controls and feedback_matcher and not "_all" in feedback_errors:
					try:
						self._process_registered_message(line, feedback_matcher, feedback_controls, feedback_errors)
					except Exception:
						# something went wrong while feedback matching
						self._logger.exception("Error while trying to apply feedback control matching, disabling it")
						feedback_errors.append("_all")

				##~~ Parsing for pause triggers
				if pause_triggers and not self.isStreaming():
					if "enable" in pause_triggers and pause_triggers["enable"].search(line) is not None:
						self.setPause(True)
					elif "disable" in pause_triggers and pause_triggers["disable"].search(line) is not None:
						self.setPause(False)
					elif "toggle" in pause_triggers and pause_triggers["toggle"].search(line) is not None:
						self.setPause(not self.isPaused())

				### Serial detection
				if self._state == self.STATE_DETECT_SERIAL:
					if line == '' or monotonic_time() > self._ok_timeout:
						self._perform_detection_step()
					elif 'start' in line or line.startswith('ok'):
						self._onConnected()
						if 'start' in line:
							self._clear_to_send.set()

				### Connection attempt
				elif self._state == self.STATE_CONNECTING:
					if "start" in line and not startSeen:
						startSeen = True
						self.sayHello()
					elif line.startswith("ok") or (supportWait and line == "wait"):
						if line == "wait":
							# if it was a wait we probably missed an ok, so let's simulate that now
							self._handle_ok()
						self._onConnected()
					elif monotonic_time() > self._timeout:
						if try_hello and self._hello_sent < 3:
							self._log("No answer from the printer within the connection timeout, trying another hello")
							self.sayHello()
						else:
							self._log("There was a timeout while trying to connect to the printer")
							self.close(wait=False)

				### Operational (idle or busy)
				elif self._state in (self.STATE_OPERATIONAL,
				                     self.STATE_STARTING,
				                     self.STATE_PRINTING,
				                     self.STATE_PAUSED,
				                     self.STATE_TRANSFERING_FILE):
					if line == "start": # exact match, to be on the safe side
						with self.job_put_on_hold():
							idle = self._state in (self.STATE_OPERATIONAL,)
							if idle:
								message = "Printer sent 'start' while already operational. External reset? " \
								          "Resetting line numbers to be on the safe side"
								self._log(message)
								self._logger.warning(message)

								self._on_external_reset()

							else:
								verb = "streaming to SD" if self.isStreaming() else "printing"
								message = "Printer sent 'start' while {}. External reset? " \
								          "Aborting job since printer lost state.".format(verb)
								self._log(message)
								self._logger.warning(message)

								self._on_external_reset()
								self.cancelPrint(disable_log_position=True)

							eventManager().fire(Events.PRINTER_RESET, payload=dict(idle=idle))

			except Exception:
				self._logger.exception("Something crashed inside the serial connection loop, please report this in OctoPrint's bug tracker:")

				errorMsg = "See octoprint.log for details"
				self._log(errorMsg)
				self._errorValue = errorMsg
				eventManager().fire(Events.ERROR, {"error": self.getErrorString(), "reason": "crash"})
				self.close(is_error=True)
		self._log("Connection closed, closing down monitor")

	def _handle_ok(self):
		if self._resend_ok_timer:
			self._resend_ok_timer.cancel()
			self._resend_ok_timer = None

		self._ok_timeout = self._get_new_communication_timeout()
		self._clear_to_send.set()

		# reset long running commands, persisted current tools and heatup counters on ok

		self._long_running_command = False

		if self._toolBeforeHeatup is not None:
			self._currentTool = self._toolBeforeHeatup
			self._toolBeforeHeatup = None

		self._finish_heatup()

		if not self._state in self.OPERATIONAL_STATES:
			return

		if self._resendDelta is not None and self._resendNextCommand():
			# we processed a resend request and are done here
			return

		# continue with our queues and the job
		self._resendActive = False
		self._continue_sending()

	def _handle_timeout(self):
		if self._state not in self.OPERATIONAL_STATES:
			return

		general_message = "Configure long running commands or increase communication timeout if that happens regularly on specific commands or long moves."

		# figure out which consecutive timeout maximum we have to use
		if self._long_running_command:
			consecutive_max = self._consecutive_timeout_maximums.get("long", 0)
		elif self._state in self.PRINTING_STATES:
			consecutive_max = self._consecutive_timeout_maximums.get("printing", 0)
		else:
			consecutive_max = self._consecutive_timeout_maximums.get("idle", 0)

		# now increment the timeout counter
		self._consecutive_timeouts += 1
		self._logger.debug("Now at {} consecutive timeouts".format(self._consecutive_timeouts))

		if 0 < consecutive_max < self._consecutive_timeouts:
			# too many consecutive timeouts, we give up
			message = "No response from printer after {} consecutive communication timeouts, considering it dead.".format(consecutive_max + 1)
			self._logger.info(message)
			self._log(message + " " + general_message)
			self._errorValue = "Too many consecutive timeouts, printer still connected and alive?"
			eventManager().fire(Events.ERROR, {"error": self._errorValue, "reason": "timeout"})
			self.close(is_error=True)

		elif self._resendActive:
			# resend active, resend same command instead of triggering a new one
			message = "Communication timeout during an active resend, resending same line again to trigger response from printer."
			self._logger.info(message)
			self._log(message + " " + general_message)
			if self._resendSameCommand():
				self._clear_to_send.set()

		elif self._heating:
			# blocking heatup active, consider that finished
			message = "Timeout while in an active heatup, considering heatup to be over."
			self._logger.info(message)
			self._finish_heatup()

		elif self._long_running_command:
			# long running command active, ignore timeout
			self._logger.debug("Ran into a communication timeout, but a command known to be a long runner is currently active")

		elif self._state in self.PRINTING_STATES + (self.STATE_PAUSED,):
			# printing, try to tickle the printer
			message = "Communication timeout while printing, trying to trigger response from printer."
			self._logger.info(message)
			self._log(message + " " + general_message)
			if self._sendCommand("M105", cmd_type="temperature", tags={"trigger:comm.handle_timeout"}):
				self._clear_to_send.set()

		elif self._clear_to_send.blocked():
			# timeout while idle and no oks left, let's try to tickle the printer
			message = "Communication timeout while idle, trying to trigger response from printer."
			self._logger.info(message)
			self._log(message + " " + general_message)
			self._clear_to_send.set()

	def _perform_detection_step(self, init=False):
		def log(message):
			self._log(message)
			self._logger.info("Serial detection: {}".format(message))

		if init:
			port = self._port
			baudrate = self._baudrate

			if port and port != "AUTO":
				port_candidates = [port]
			else:
				port_candidates = serialList()

			if baudrate:
				baudrate_candidates = [baudrate]
			elif len(port_candidates) == 1:
				baudrate_candidates = baudrateList()
			else:
				# if we have no baudrate and more than one port we limit tested baudrates to
				# the two most common plus any additionally configured ones
				baudrate_candidates = baudrateList([115200, 250000])

			self._detection_candidates = [(p, b) for p in port_candidates for b in baudrate_candidates]
			self._detection_retry = self.DETECTION_RETRIES

			log("Performing autodetection with {} " \
			    "port/baudrate candidates: {}".format(len(self._detection_candidates),
			                                          ", ".join(map(lambda x: "{}@{}".format(x[0], x[1]),
			                                                    self._detection_candidates))))

		def attempt_handshake():
			self._detection_retry += 1
			timeout = self._get_communication_timeout_interval()

			log("Handshake attempt #{} with timeout {}s".format(self._detection_retry, timeout))
			try:
				if self._serial.timeout != timeout:
					self._serial.timeout = timeout
				self._timeout = self._ok_timeout = monotonic_time() + timeout
			except Exception:
				self._log("Unexpected error while setting timeout {}: {}".format(timeout, get_exception_string()))
				self._logger.exception("Unexpected error while setting timeout {}".format(timeout))
			else:
				self._do_send_without_checksum(b"", log=False)  # new line to reset things
				self.sayHello(tags={"trigger:detection", })

		while len(self._detection_candidates) > 0 or self._detection_retry < self.DETECTION_RETRIES:
			if self._state not in (self.STATE_DETECT_SERIAL,):
				return

			if self._detection_retry < self.DETECTION_RETRIES:
				if self._serial is None:
					self._detection_retry = self.DETECTION_RETRIES
					continue

				attempt_handshake()
				return

			else:
				(p, b) = self._detection_candidates.pop(0)

				try:
					log("Trying port {}, baudrate {}".format(p, b))
					if self._serial is None or self._serial.port != p:
						if not self._open_serial(p, b, trigger_errors=False):
							log("Could not open port {}, baudrate {}, skipping".format(p, b))
							continue
					else:
						self._serial.baudrate = b

					self._detection_retry = 0

					attempt_handshake()
					return

				except Exception:
					self._log("Unexpected error while setting baudrate {}: {}".format(b, get_exception_string()))
					self._logger.exception("Unexpected error while setting baudrate {}".format(b))

		error_text = "No more candidates to test, and no working port/baudrate combination detected."
		self._trigger_error(error_text, "autodetect")

	def _finish_heatup(self):
		if self._heating:
			if self._heatupWaitStartTime:
				self._heatupWaitTimeLost = self._heatupWaitTimeLost + (monotonic_time() - self._heatupWaitStartTime)
				self._heatupWaitStartTime = None
			self._heating = False

	def _continue_sending(self):
		while self._active:
			job_active = self._state in (self.STATE_STARTING, self.STATE_PRINTING) and not (self._currentFile is None or self._currentFile.done or self.isSdPrinting())

			if self._send_from_command_queue():
				# we found something in the command queue to send
				return True

			elif self.job_on_hold:
				# job is on hold, that means we must not send from either script queue or file
				return False

			elif self._send_from_job_queue():
				# we found something in the script queue to send
				return True

			elif job_active and self._send_from_job():
				# we sent the next line from the file
				return True

			elif not job_active:
				# nothing sent but also no job active, so we can just return false
				return False

			self._logger.debug("No command sent on ok while printing, doing another iteration")

	def _process_registered_message(self, line, feedback_matcher, feedback_controls, feedback_errors):
		feedback_match = feedback_matcher.search(line)
		if feedback_match is None:
			return

		for match_key in feedback_match.groupdict():
			try:
				feedback_key = match_key[len("group"):]
				if not feedback_key in feedback_controls or feedback_key in feedback_errors or feedback_match.group(match_key) is None:
					continue
				matched_part = feedback_match.group(match_key)

				if feedback_controls[feedback_key]["matcher"] is None:
					continue

				match = feedback_controls[feedback_key]["matcher"].search(matched_part)
				if match is None:
					continue

				outputs = dict()
				for template_key, template in feedback_controls[feedback_key]["templates"].items():
					try:
						output = template.format(*match.groups())
					except KeyError:
						output = template.format(**match.groupdict())
					except Exception:
						self._logger.debug("Could not process template {}: {}".format(template_key,
						                                                              template),
						                   exc_info=1)
						output = None

					if output is not None:
						outputs[template_key] = output
				eventManager().fire(Events.REGISTERED_MESSAGE_RECEIVED, dict(key=feedback_key, matched=matched_part, outputs=outputs))
			except Exception:
				self._logger.exception("Error while trying to match feedback control output, disabling key {key}".format(key=match_key))
				feedback_errors.append(match_key)

	def _poll_temperature(self):
		"""
		Polls the temperature.

		If the printer is not operational, capable of auto-reporting temperatures, closing the connection, not printing
		from sd, busy with a long running command or heating, no poll will be done.
		"""

		if self.isOperational() \
			and not self._temperature_autoreporting \
			and not self._connection_closing \
			and not self.isStreaming() \
			and not self._long_running_command \
			and not self._heating \
			and not self._dwelling_until \
			and not self._manualStreaming:
			self.sendCommand("M105", cmd_type="temperature_poll", tags={"trigger:comm.poll_temperature"})

	def _poll_sd_status(self):
		"""
		Polls the sd printing status.

		If the printer is not operational, closing the connection, not printing from sd, busy with a long running
		command or heating, no poll will be done.
		"""

		if self.isOperational() \
			and not self._sdstatus_autoreporting \
			and not self._connection_closing \
			and (self.isSdFileSelected() and not self._disable_sd_printing_detection or self.isSdPrinting()) \
			and not self._long_running_command \
			and not self._dwelling_until \
			and not self._heating:
			self.sendCommand("M27", cmd_type="sd_status_poll", tags={"trigger:comm.poll_sd_status"})

	def _set_autoreport_temperature_interval(self, interval=None):
		if interval is None:
			try:
				interval = int(self._timeout_intervals.get("temperatureAutoreport", 2))
			except Exception:
				interval = 2
		self.sendCommand("M155 S{}".format(interval), tags={"trigger:comm.set_autoreport_temperature_interval"})

	def _set_autoreport_sdstatus_interval(self, interval=None):
		if interval is None:
			try:
				interval = int(self._timeout_intervals.get("sdStatusAutoreport", 1))
			except Exception:
				interval = 1
		self.sendCommand("M27 S{}".format(interval), tags={"trigger:comm.set_autoreport_sdstatus_interval"})

	def _set_busy_protocol_interval(self, interval=None, callback=None):
		if interval is None:
			try:
				interval = max(int(self._timeout_intervals.get("communicationBusy", 3)) - 1, 1)
			except Exception:
				interval = 2
		self.sendCommand("M113 S{}".format(interval),
		                 tags={"trigger:comm.set_busy_protocol_interval"},
		                 on_sent=callback)

	def _onConnected(self):
		self._serial.timeout = self._get_communication_timeout_interval()
		self._temperature_timer = RepeatedTimer(self._get_temperature_timer_interval, self._poll_temperature, run_first=True)
		self._temperature_timer.start()

		self._sd_status_timer = RepeatedTimer(self._get_sd_status_timer_interval, self._poll_sd_status, run_first=True)
		self._sd_status_timer.start()

		self._changeState(self.STATE_OPERATIONAL)

		self.resetLineNumbers(tags={"trigger:comm.on_connected",})
		self.sendCommand("M115", tags={"trigger:comm.on_connected",})

		if self._sdAvailable:
			self.refreshSdFiles(tags={"trigger:comm.on_connected",})
		else:
			self.initSdCard(tags={"trigger:comm.on_connected"})

		payload = dict(port=self._port, baudrate=self._baudrate)
		eventManager().fire(Events.CONNECTED, payload)
		self.sendGcodeScript("afterPrinterConnected", replacements=dict(event=payload))

	def _on_external_reset(self):
		# hold queue processing, clear queues and acknowledgements, reset line number and last lines
		with self._send_queue.blocked():
			self._clear_to_send.reset()
			with self._command_queue.blocked():
				self._command_queue.clear()
			self._send_queue.clear()

			with self._line_mutex:
				self._current_line = 0
				self._lastLines.clear()

		self.sayHello(tags={"trigger:comm.on_external_reset"})
		self.resetLineNumbers(tags={"trigger:comm.on_external_reset"})

		if self._temperature_autoreporting:
			self._set_autoreport_temperature_interval()
		if self._sdstatus_autoreporting:
			self._set_autoreport_sdstatus_interval()
		if self._busy_protocol_support:
			self._set_busy_protocol_interval()

		self._consecutive_not_sd_printing = 0

	def _get_temperature_timer_interval(self):
		busy_default = 4.0
		target_default = 2.0

		def get(key, default):
			interval = self._timeout_intervals.get(key, default)
			if interval <= 0:
				interval = 1.0
			return interval

		if self.isBusy():
			return get("temperature", busy_default)

		tools = self.last_temperature.tools
		for temp in [tools[k][1] for k in tools.keys()]:
			if temp and temp > self._temperatureTargetSetThreshold:
				return get("temperatureTargetSet", target_default)

		bed = self.last_temperature.bed
		if bed and len(bed) > 1 and bed[1] is not None and bed[1] > self._temperatureTargetSetThreshold:
			return get("temperatureTargetSet", target_default)

		return get("temperature", busy_default)

	def _get_sd_status_timer_interval(self):
		interval = self._timeout_intervals.get("sdStatus", 1.0)
		if interval <= 0:
			interval = 1.0
		return interval

	def _get_communication_timeout_interval(self):
		# special rules during serial detection
		if self._state in (self.STATE_DETECT_SERIAL,):
			if self._detection_retry == 0:
				# first try
				return self._timeout_intervals.get("detectionFirst", 10.0)
			else:
				# consecutive tries
				return self._timeout_intervals.get("detectionConsecutive", 2.0)

		# communication timeout
		if self._busy_protocol_support:
			comm_timeout = self._timeout_intervals.get("communicationBusy", 2.0)
		else:
			comm_timeout = self._timeout_intervals.get("communication", 30.0)

		# temperature interval
		if self._temperature_autoreporting:
			temperature_timeout = self._timeout_intervals.get("temperatureAutoreport", 2.0)
		else:
			temperature_timeout = self._get_temperature_timer_interval()

		# use the max of both, add a second to temperature to avoid race conditions
		return max(comm_timeout, temperature_timeout + 1)

	def _get_new_communication_timeout(self):
		return monotonic_time() + self._get_communication_timeout_interval()

	def _send_from_command_queue(self):
		# We loop here to make sure that if we do NOT send the first command
		# from the queue, we'll send the second (if there is one). We do not
		# want to get stuck here by throwing away commands.
		while True:
			if self.isStreaming():
				# command queue irrelevant
				return False

			try:
				entry = self._command_queue.get(block=False)
			except queue.Empty:
				# nothing in command queue
				return False

			try:
				if isinstance(entry, tuple):
					if not len(entry) == 4:
						# something with that entry is broken, ignore it and fetch
						# the next one
						continue
					cmd, cmd_type, callback, tags = entry
				else:
					cmd = entry
					cmd_type = None
					callback = None
					tags = None

				if self._sendCommand(cmd, cmd_type=cmd_type, on_sent=callback, tags=tags):
					# we actually did add this cmd to the send queue, so let's
					# return, we are done here
					return True
			finally:
				self._command_queue.task_done()

	def _open_serial(self, port, baudrate, trigger_errors=True):
		def default(_, p, b, timeout):
			# connect to regular serial port
			self._dual_log("Connecting to port {}, baudrate {}".format(port, baudrate), level=logging.INFO)

			serial_port_args = {
				"baudrate": baudrate,
				"timeout": timeout,
				"write_timeout": 0,
			}

			if settings().getBoolean(["serial", "exclusive"]):
				serial_port_args["exclusive"] = True

			serial_obj = serial.Serial(**serial_port_args)
			serial_obj.port = str(p)

			use_parity_workaround = settings().get(["serial", "useParityWorkaround"])
			needs_parity_workaround = get_os() == "linux" and os.path.exists("/etc/debian_version") # See #673

			if use_parity_workaround == "always" or (needs_parity_workaround and use_parity_workaround == "detect"):
				serial_obj.parity = serial.PARITY_ODD
				serial_obj.open()
				serial_obj.close()
				serial_obj.parity = serial.PARITY_NONE

			serial_obj.open()

			# Set close_exec flag on serial handle, see #3212
			if hasattr(serial_obj, "fd"):
				# posix
				set_close_exec(serial_obj.fd)
			elif hasattr(serial_obj, "_port_handle"):
				# win32
				# noinspection PyProtectedMember
				set_close_exec(serial_obj._port_handle)

			return BufferedReadlineWrapper(serial_obj)

		serial_factories = list(self._serial_factory_hooks.items()) + [("default", default)]
		for name, factory in serial_factories:
			try:
				serial_obj = factory(self,
				                     port,
				                     baudrate,
				                     settings().getFloat(["serial", "timeout", "connection"]))
			except Exception:
				exception_string = get_exception_string()

				if trigger_errors:
					self._trigger_error("Connection error, see Terminal tab", "connection")

				error_message = "Unexpected error while connecting to " \
				                "serial port {}, baudrate {} from hook {}: {}".format(port,
				                                                                      baudrate,
				                                                                      name,
				                                                                      exception_string)
				self._log(error_message)
				self._logger.exception(error_message)
				return False

			if serial_obj is not None:
				# first hook to succeed wins, but any can pass on to the next
				self._serial = serial_obj
				self._clear_to_send.reset()
				return True

		return False

	_recoverable_communication_errors    = ("no line number with checksum",
	                                        "missing linenumber")
	_resend_request_communication_errors = ("line number", # since this error class gets checked after recoverable
	                                                       # communication errors, we can use this broad term here
	                                        "linenumber",  # since this error class gets checked after recoverable
	                                                       # communication errors, we can use this broad term here
	                                        "checksum",    # since this error class gets checked after recoverable
	                                                       # communication errors, we can use this broad term here
	                                        "format error",
	                                        "expected line")
	_sd_card_errors                      = ("volume.init",
	                                        "openroot",
	                                        "workdir",
	                                        "error writing to file",
	                                        "cannot open",
	                                        "open failed",
	                                        "cannot enter")
	_fatal_errors                        = ("kill() called",
	                                        "fatal:")
	def _handle_errors(self, line):
		if line is None:
			return

		lower_line = line.lower()

		if lower_line.startswith("fatal:"):
			# hello Repetier firmware -_-
			line = "Error:" + line
			lower_line = line.lower()

		if lower_line.startswith('error:') or line.startswith('!!'):
			if regex_minMaxError.match(line):
				# special delivery for firmware that goes "Error:x\n: Extruder switched off. MAXTEMP triggered !\n"
				line = line.rstrip() + self._readline()
				lower_line = line.lower()
			elif regex_marlinKillError.search(line):
				# special delivery for marlin kill errors that are split across multiple error lines
				next_line = self._readline().strip()
				if next_line.lower().startswith("error:"):
					next_line = next_line[6:].strip()
				line = line.rstrip() + " - " + next_line
				lower_line = line.lower()

			stripped_error = (line[6:] if lower_line.startswith("error:") else line[2:]).strip()

			if any(x in lower_line for x in self._recoverable_communication_errors):
				# manually trigger an ack for comm errors the printer doesn't send a resend request for but
				# from which we can recover from by just pushing on (because that then WILL trigger a fitting
				# resend request)
				self._handle_ok()

			elif any(x in lower_line for x in self._resend_request_communication_errors):
				# skip comm errors that the printer sends a resend request for anyhow
				self._lastCommError = stripped_error

			elif any(x in lower_line for x in self._sd_card_errors):
				# skip errors with the SD card
				pass

			elif 'unknown command' in lower_line:
				# ignore unknown command errors, it could be a typo or some missing feature
				pass

			elif not self.isError():
				# handle everything else
				for name, hook in self._error_message_hooks.items():
					try:
						ret = hook(self, stripped_error)
					except Exception:
						self._logger.exception("Error while processing hook {name}:".format(**locals()),
						                       extra=dict(plugin=name))
					else:
						if ret:
							return line

				self._to_logfile_with_terminal("Received an error from the printer's firmware: {}".format(stripped_error),
				                               level=logging.WARN)

				if not self._ignore_errors:
					if self._disconnect_on_errors or any(map(lambda x: x in lower_line, self._fatal_errors)):
						self._trigger_error(stripped_error, "firmware")
					elif self.isPrinting():
						self.cancelPrint(firmware_error=stripped_error)
						self._clear_to_send.set()

				else:
					self._log("WARNING! Received an error from the printer's firmware, ignoring that as configured "
					          "but you might want to investigate what happened here! Error: {}".format(stripped_error))
					self._clear_to_send.set()

		# finally return the line
		return line

	def _trigger_error(self, text, reason, close=True):
		self._errorValue = text
		self._changeState(self.STATE_ERROR)
		eventManager().fire(Events.ERROR, {"error": self.getErrorString(), "reason": reason})
		if close:
			if self._send_m112_on_error and not self.isSdPrinting() and reason not in ("connection",
			                                                                           "autodetect"):
				self._trigger_emergency_stop(close=False)
			self.close(is_error=True)

	def _readline(self):
		if self._serial is None:
			return None

		try:
			ret = self._serial.readline()
		except Exception as ex:
			if not self._connection_closing:
				self._logger.exception("Unexpected error while reading from serial port")
				self._log("Unexpected error while reading serial port, please consult octoprint.log for details: %s" % (get_exception_string()))
				if isinstance(ex, serial.SerialException):
					self._dual_log("Please see https://faq.octoprint.org/serialerror for possible reasons of this.",
					               level=logging.ERROR)
				self._errorValue = get_exception_string()
				self.close(is_error=True)
			return None

		null_pos = ret.find(b'\x00')

		try:
			ret = ret.decode('utf-8')
		except UnicodeDecodeError:
			ret = ret.decode('latin1')

		if ret != "":
			try:
				self._log("Recv: {}".format(sanitize_ascii(ret)))
			except ValueError as e:
				self._log("WARN: While reading last line: {}".format(e))
				self._log("Recv: {!r}".format(ret))

			if null_pos >= 0:
				self._logger.warning("Received line:")
				self._logger.warning("| {}".format(ret.replace('\0', '\\x00').rstrip()))
				self._dual_log("The received line contains at least one null byte character at position {}, "
				               "this hints at some data corruption going on".format(null_pos),
				               level=logging.WARNING,
				               prefix="WARN")

		for name, hook in self._received_message_hooks.items():
			try:
				ret = hook(self, ret)
			except Exception:
				self._logger.exception("Error while processing hook {name}:".format(**locals()),
				                       extra=dict(plugin=name))
			else:
				if ret is None:
					return ""

		return ret

	def _get_next_from_job(self):
		if self._currentFile is None:
			return None, None, None

		try:
			line, pos, lineno = self._currentFile.getNext()
		except EnvironmentError:
			self._log("There was an error reading from the file that's being printed, cancelling the print. Please "
			          "consult octoprint.log for details on the error.")
			self.cancelPrint()
			return None, None, None

		if line is None:
			if isinstance(self._currentFile, StreamingGcodeFileInformation):
				self._finishFileTransfer()
			else:
				self._changeState(self.STATE_FINISHING)
				self.sendCommand("M400", part_of_job=True)
				self._callback.on_comm_print_job_done()
				def finalize():
					self._changeState(self.STATE_OPERATIONAL)
				return SendQueueMarker(finalize), None, None
		return line, pos, lineno

	def _send_from_job(self):
		with self._jobLock:
			while self._active:
				# we loop until we've actually enqueued a line for sending
				if self._state not in (self.STATE_STARTING, self.STATE_PRINTING):
					# we are no longer printing, return false
					return False

				elif self.job_on_hold:
					# job is on hold, return false
					return False

				line, pos, lineno = self._get_next_from_job()
				if isinstance(line, QueueMarker):
					self.sendCommand(line, part_of_job=True)
					self._callback.on_comm_progress()

					# end of file, return false so that the next round in continue_sending will process
					# what we just enqueued (any scripts + marker)
					return False

				elif line is None:
					# end of file, return false
					return False

				result = self._sendCommand(line, tags={"source:file", "filepos:{}".format(pos), "fileline:{}".format(lineno)})
				self._callback.on_comm_progress()
				if result:
					# line from file sent, return true
					return True

				self._logger.debug("Command \"{}\" from file not enqueued, doing another iteration".format(line))

	def _send_from_job_queue(self):
		try:
			line, cmd_type, on_sent, tags = self._job_queue.get_nowait()
			result = self._sendCommand(line, cmd_type=cmd_type, on_sent=on_sent, tags=tags)
			if result:
				# line from script sent, return true
				return True
		except queue.Empty:
			pass

		return False

	def _handle_resend_request(self, line):
		try:
			lineToResend = parse_resend_line(line)
			if lineToResend is None:
				return False

			if self._resendDelta is None and lineToResend == self._current_line == 1:
				# We probably just handled a resend and this request originates from lines sent before that
				self._logger.info("Got a resend request for line 1 which is also our current line. It looks "
				                  "like we just handled a reset and this is a left over of this")
				return False

			elif self._resendDelta is None and lineToResend == self._current_line:
				# We don't expect to have an active resend request and the printer is requesting a resend of
				# a line we haven't yet sent.
				#
				# This means the printer got a line from us with N = self._current_line - 1 but had already
				# acknowledged that. This can happen if the last line was resent due to a timeout during
				# an active (prior) resend request.
				#
				# We will ignore this resend request and just continue normally.
				self._logger.info("Ignoring resend request for line %d == current line, we haven't sent that yet so "
				                   "the printer got N-1 twice from us, probably due to a timeout" % lineToResend)
				return False

			lastCommError = self._lastCommError
			self._lastCommError = None

			resendDelta = self._current_line - lineToResend

			if lastCommError is not None \
					and ("line number" in lastCommError.lower() or "expected line" in lastCommError.lower()) \
					and lineToResend == self._lastResendNumber \
					and self._resendDelta is not None and self._currentResendCount < resendDelta:
				self._logger.info("Ignoring resend request for line %d, that still originates from lines we sent "
				                   "before we got the first resend request" % lineToResend)
				self._currentResendCount += 1
				return True

			if self._currentConsecutiveResendNumber == lineToResend:
				self._currentConsecutiveResendCount += 1
				if self._currentConsecutiveResendCount >= self._maxConsecutiveResends:
					# printer keeps requesting the same line again and again, something is severely broken here
					error_text = "Printer keeps requesting line {} again and again, communication stuck".format(lineToResend)
					self._log(error_text)
					self._logger.warning(error_text)
					self._trigger_error(error_text, "resend_loop")
			else:
				self._currentConsecutiveResendNumber = lineToResend
				self._currentConsecutiveResendCount = 0

			self._resendActive = True
			self._resendDelta = resendDelta
			self._lastResendNumber = lineToResend
			self._currentResendCount = 0

			if self._resendDelta > len(self._lastLines) or len(self._lastLines) == 0 or self._resendDelta < 0:
				error_text = "Printer requested line {} but no sufficient history is available, can't resend".format(lineToResend)
				self._log(error_text)
				self._logger.warning(error_text + ". Printer requested line {}, current line is {}, line history has {} entries.".format(lineToResend, self._current_line, len(self._lastLines)))
				if self.isPrinting():
					# abort the print & disconnect, there's nothing we can do to rescue it
					self._trigger_error(error_text, "resend")
				else:
					# reset resend delta, we can't do anything about it
					self._resendDelta = None

			# if we log resends, make sure we don't log more resends than the set rate within a window
			#
			# this it to prevent the log from getting flooded for extremely bad communication issues
			if self._log_resends:
				now = monotonic_time()
				new_rate_window = self._log_resends_rate_start is None or self._log_resends_rate_start + self._log_resends_rate_frame < now
				in_rate = self._log_resends_rate_count < self._log_resends_max

				if new_rate_window or in_rate:
					if new_rate_window:
						self._log_resends_rate_start = now
						self._log_resends_rate_count = 0

					self._to_logfile_with_terminal("Got a resend request from the printer: requested line = {}, "
					                               "current line = {}".format(lineToResend, self._current_line))
					self._log_resends_rate_count += 1

			self._send_queue.resend_active = True

			return True
		finally:
			if self._trigger_ok_after_resend == "always":
				self._handle_ok()
			elif self._trigger_ok_after_resend == "detect":
				self._resend_ok_timer = threading.Timer(self._timeout_intervals.get("resendOk", 1.0), self._resendSimulateOk)
				self._resend_ok_timer.start()

	def _resendSimulateOk(self):
		self._resend_ok_timer = None
		self._handle_ok()
		self._logger.info("Firmware didn't send an 'ok' with their resend request. That's a known bug "
		                  "with some firmware variants out there. Simulating an ok to continue...")

	def _resendSameCommand(self):
		return self._resendNextCommand(again=True)

	def _resendNextCommand(self, again=False):
		self._lastCommError = None

		# Make sure we are only handling one sending job at a time
		with self._sendingLock:
			if again:
				# If we are about to send the last line from the active resend request
				# again, we first need to increment resend delta. It might already
				# be set to None if the last resend line was already sent, so
				# if that's the case we set it to 0. It will then be incremented,
				# the last line will be sent again, and then the delta will be
				# decremented and set to None again, completing the cycle.
				if self._resendDelta is None:
					self._resendDelta = 0
				self._resendDelta += 1

			elif self._resendDelta is None:
				# we might enter this twice in quick succession if we get triggered by the
				# resend_ok_timer, so make sure that resendDelta is actually still set (see #2632)
				return False

			cmd = self._lastLines[-self._resendDelta].decode("ascii")
			lineNumber = self._current_line - self._resendDelta

			result = self._enqueue_for_sending(cmd, linenumber=lineNumber, resend=True)

			self._resendDelta -= 1
			if self._resendDelta <= 0:
				# reset everything BUT the resendActive flag - that will have to stay active until we receive
				# our next ok!
				self._resendDelta = None
				self._lastResendNumber = None
				self._currentResendCount = 0

				self._send_queue.resend_active = False

			return result

	def _sendCommand(self, cmd, cmd_type=None, on_sent=None, tags=None):
		# Make sure we are only handling one sending job at a time
		with self._sendingLock:
			if self._serial is None:
				return False

			if isinstance(cmd, QueueMarker):
				if isinstance(cmd, SendQueueMarker):
					self._enqueue_for_sending(cmd)
					return True
				else:
					return False

			gcode, subcode = gcode_and_subcode_for_cmd(cmd)

			if not self.isStreaming():
				# trigger the "queuing" phase only if we are not streaming to sd right now
				results = self._process_command_phase("queuing", cmd, command_type=cmd_type, gcode=gcode, subcode=subcode, tags=tags)

				if not results:
					# command is no more, return
					return False
			else:
				results = [(cmd, cmd_type, gcode, subcode, tags)]

			# process helper
			def process(cmd, cmd_type, gcode, subcode, on_sent=None, tags=None):
				if cmd is None:
					# no command, next entry
					return False

				if gcode and gcode in gcodeToEvent:
					# if this is a gcode bound to an event, trigger that now
					eventManager().fire(gcodeToEvent[gcode])

				# process @ commands
				if gcode is None and cmd.startswith("@"):
					self._process_atcommand_phase("queuing", cmd, tags=tags)

				# actually enqueue the command for sending
				if self._enqueue_for_sending(cmd, command_type=cmd_type, on_sent=on_sent, tags=tags):
					if not self.isStreaming():
						# trigger the "queued" phase only if we are not streaming to sd right now
						self._process_command_phase("queued", cmd, cmd_type, gcode=gcode, subcode=subcode, tags=tags)
					return True
				else:
					return False

			# split off the final command, because that needs special treatment
			if len(results) > 1:
				last_command = results[-1]
				results = results[:-1]
			else:
				last_command = results[0]
				results = []

			# track if we enqueued anything at all
			enqueued_something = False

			# process all but the last ...
			for (cmd, cmd_type, gcode, subcode, tags) in results:
				enqueued_something = process(cmd, cmd_type, gcode, subcode, tags=tags) or enqueued_something

			# ... and then process the last one with the on_sent callback attached
			cmd, cmd_type, gcode, subcode, tags = last_command
			enqueued_something = process(cmd, cmd_type, gcode, subcode, on_sent=on_sent, tags=tags) or enqueued_something

			return enqueued_something

	##~~ send loop handling

	def _enqueue_for_sending(self, command, linenumber=None, command_type=None, on_sent=None, resend=False, tags=None):
		"""
		Enqueues a command and optional linenumber to use for it in the send queue.

		Arguments:
		    command (str or SendQueueMarker): The command to send.
		    linenumber (int): The line number with which to send the command. May be ``None`` in which case the command
		        will be sent without a line number and checksum.
		    command_type (str): Optional command type, if set and command type is already in the queue the
		        command won't be enqueued
		    on_sent (callable): Optional callable to call after command has been sent to printer.
		    resend (bool): Whether this is a resent command
		    tags (set of str or None): Tags to attach to this command
		"""

		try:
			target = "send"
			if resend:
				target = "resend"

			self._send_queue.put((command, linenumber, command_type, on_sent, False, tags), item_type=command_type, target=target)
			return True
		except TypeAlreadyInQueue as e:
			self._logger.debug("Type already in send queue: " + e.type)
			return False

	def _use_up_clear(self, gcode):
		# we only need to use up a clear if the command we just sent was either a gcode command or if we also
		# require ack's for unknown commands
		eats_clear = self._unknownCommandsNeedAck
		if gcode is not None:
			eats_clear = True

		if eats_clear:
			# if we need to use up a clear, do that now
			self._clear_to_send.clear()

		return eats_clear

	def _send_loop(self):
		"""
		The send loop is responsible of sending commands in ``self._send_queue`` over the line, if it is cleared for
		sending (through received ``ok`` responses from the printer's firmware.
		"""

		self._clear_to_send.wait()

		while self._send_queue_active:
			try:
				# wait until we have something in the queue
				try:
					entry = self._send_queue.get()
				except queue.Empty:
					# I haven't yet been able to figure out *why* this can happen but according to #3096 and SERVER-2H
					# an Empty exception can fly here due to resend_active being True but nothing being in the resend
					# queue of the send queue. So we protect against this possibility...
					continue

				try:
					# make sure we are still active
					if not self._send_queue_active:
						break

					# sleep if we are dwelling
					now = monotonic_time()
					if self._blockWhileDwelling and self._dwelling_until and now < self._dwelling_until:
						time.sleep(self._dwelling_until - now)
						self._dwelling_until = False

					# fetch command, command type and optional linenumber and sent callback from queue
					command, linenumber, command_type, on_sent, processed, tags = entry

					if isinstance(command, SendQueueMarker):
						command.run()
						self._continue_sending()
						continue

					# some firmwares (e.g. Smoothie) might support additional in-band communication that will not
					# stick to the acknowledgement behaviour of GCODE, so we check here if we have a GCODE command
					# at hand here and only clear our clear_to_send flag later if that's the case
					gcode, subcode = gcode_and_subcode_for_cmd(command)

					if linenumber is not None:
						# line number predetermined - this only happens for resends, so we'll use the number and
						# send directly without any processing (since that already took place on the first sending!)
						self._use_up_clear(gcode)
						self._do_send_with_checksum(command.encode("ascii"), linenumber)

					else:
						if not processed:
							# trigger "sending" phase if we didn't so far
							results = self._process_command_phase("sending", command, command_type,
							                                      gcode=gcode,
							                                      subcode=subcode,
							                                      tags=tags)

							if not results:
								# No, we are not going to send this, that was a last-minute bail.
								# However, since we already are in the send queue, our _monitor
								# loop won't be triggered with the reply from this unsent command
								# now, so we try to tickle the processing of any active
								# command queues manually
								self._continue_sending()

								# and now let's fetch the next item from the queue
								continue

							# we explicitly throw away plugin hook results that try
							# to perform command expansion in the sending/sent phase,
							# so "results" really should only have more than one entry
							# at this point if our core code contains a bug
							assert len(results) == 1

							# we only use the first (and only!) entry here
							command, _, gcode, subcode, tags = results[0]

						if command.strip() == "":
							self._logger.info("Refusing to send an empty line to the printer")

							# same here, tickle the queues manually
							self._continue_sending()

							# and fetch the next item
							continue

						# handle @ commands
						if gcode is None and command.startswith("@"):
							self._process_atcommand_phase("sending", command, tags=tags)

							# tickle...
							self._continue_sending()

							# ... and fetch the next item
							continue

						# now comes the part where we increase line numbers and send stuff - no turning back now
						used_up_clear = self._use_up_clear(gcode)
						self._do_send(command, gcode=gcode)
						if not used_up_clear:
							# If we didn't use up a clear we need to tickle the read queue - there might
							# not be a reply to this command, so our _monitor loop will stay waiting until
							# timeout. We definitely do not want that, so we tickle the queue manually here
							self._continue_sending()

					# trigger "sent" phase and use up one "ok"
					if on_sent is not None and callable(on_sent):
						# we have a sent callback for this specific command, let's execute it now
						on_sent()
					self._process_command_phase("sent", command, command_type, gcode=gcode, subcode=subcode, tags=tags)

				finally:
					# no matter _how_ we exit this block, we signal that we
					# are done processing the last fetched queue entry
					self._send_queue.task_done()

				# now we just wait for the next clear and then start again
				self._clear_to_send.wait()
			except Exception:
				self._logger.exception("Caught an exception in the send loop")
		self._log("Closing down send loop")

	def _log_command_phase(self, phase, command, *args, **kwargs):
		if self._phaseLogger.isEnabledFor(logging.DEBUG):
			output_parts = ["phase: {}".format(phase),
			                "command: {}".format(to_unicode(command, errors="replace"))]

			if kwargs.get("command_type"):
				output_parts.append("command_type: {}".format(kwargs["command_type"]))
			if kwargs.get("gcode"):
				output_parts.append("gcode: {}".format(kwargs["gcode"]))
			if kwargs.get("subcode"):
				output_parts.append("subcode: {}".format(kwargs["subcode"]))
			if kwargs.get("tags"):
				output_parts.append("tags: [ {} ]".format(", ".join(sorted(kwargs["tags"]))))

			self._phaseLogger.debug(u" | ".join(output_parts))

	def _process_command_phase(self, phase, command, command_type=None, gcode=None, subcode=None, tags=None):
		if gcode is None:
			gcode, subcode = gcode_and_subcode_for_cmd(command)
		results = [(command, command_type, gcode, subcode, tags)]

		self._log_command_phase(phase, command, command_type=command_type, gcode=gcode, subcode=subcode, tags=tags)

		if (self.isStreaming() and self.isPrinting()) or phase not in ("queuing", "queued", "sending", "sent"):
			return results

		# send it through the phase specific handlers provided by plugins
		for name, hook in self._gcode_hooks[phase].items():
			new_results = []
			for command, command_type, gcode, subcode, tags in results:
				try:
					hook_results = hook(self, phase, command, command_type, gcode, subcode=subcode, tags=tags)
				except Exception:
					self._logger.exception(u"Error while processing hook {name} for phase "
					                       u"{phase} and command {command}:".format(name=name,
					                                                                phase=phase,
					                                                                command=to_unicode(command,
					                                                                                   errors="replace")),
					                       extra=dict(plugin=name))
				else:
					normalized = _normalize_command_handler_result(command, command_type, gcode, subcode, tags,
					                                               hook_results,
					                                               tags_to_add={"source:rewrite",
					                                                            "phase:{}".format(phase),
					                                                            "plugin:{}".format(name)})

					# make sure we don't allow multi entry results in anything but the queuing phase
					if not phase in ("queuing",) and len(normalized) > 1:
						self._logger.error(u"Error while processing hook {name} for phase {phase} and command {command}: "
						                   u"Hook returned multi-entry result for phase {phase} and command {command}. "
						                   u"That's not supported, if you need to do multi expansion of commands you "
						                   u"need to do this in the queuing phase. Ignoring hook result and sending "
						                   u"command as-is.".format(name=name,
						                                            phase=phase,
						                                            command=to_unicode(command, errors="replace")),
						                   extra=dict(plugin=name))
						new_results.append((command, command_type, gcode, subcode, tags))
					else:
						new_results += normalized
			if not new_results:
				# hook handler returned None or empty list for all commands, so we'll stop here and return a full out empty result
				return []
			results = new_results

		# if it's a gcode command send it through the specific handler if it exists
		new_results = []
		modified = False
		for command, command_type, gcode, subcode, tags in results:
			if gcode is not None:
				gcode_handler = "_gcode_" + gcode + "_" + phase
				if hasattr(self, gcode_handler):
					handler_results = getattr(self, gcode_handler)(command,
					                                               cmd_type=command_type,
					                                               subcode=subcode,
					                                               tags=tags)
					new_results += _normalize_command_handler_result(command, command_type, gcode, subcode, tags,
					                                                 handler_results)
					modified = True
				else:
					new_results.append((command, command_type, gcode, subcode, tags))
			else:
				new_results.append((command, command_type, gcode, subcode, tags))

		if modified:
			if not new_results:
				# gcode handler returned None or empty list for all commands, so we'll stop here and return a full out empty result
				return []
			else:
				results = new_results

		# send it through the phase specific command handler if it exists
		command_phase_handler = "_command_phase_" + phase
		if hasattr(self, command_phase_handler):
			new_results = []
			for command, command_type, gcode, subcode, tags in results:
				handler_results = getattr(self, command_phase_handler)(command,
				                                                       cmd_type=command_type,
				                                                       gcode=gcode,
				                                                       subcode=subcode,
				                                                       tags=tags)
				new_results += _normalize_command_handler_result(command, command_type, gcode, subcode, tags,
				                                                 handler_results)
			results = new_results

		# finally return whatever we resulted on
		return results

	def _process_atcommand_phase(self, phase, command, tags=None):
		if (self.isStreaming() and self.isPrinting()) or phase not in ("queuing", "sending"):
			return

		split = command.split(None, 1)
		if len(split) == 2:
			atcommand = split[0]
			parameters = split[1]
		else:
			atcommand = split[0]
			parameters = ""

		atcommand = atcommand[1:]

		# send it through the phase specific handlers provided by plugins
		for name, hook in self._atcommand_hooks[phase].items():
			try:
				hook(self, phase, atcommand, parameters, tags=tags)
			except Exception:
				self._logger.exception(u"Error while processing hook {} for "
				                       u"phase {} and command {}:".format(name, phase, to_unicode(atcommand, errors="replace")),
				                       extra=dict(plugin=name))

		# trigger built-in handler if available
		handler = getattr(self, "_atcommand_{}_{}".format(atcommand, phase), None)
		if callable(handler):
			try:
				handler(atcommand, parameters, tags=tags)
			except Exception:
				self._logger.exception(u"Error in handler for phase {} and command {}".format(phase,
				                                                                              to_unicode(atcommand, errors="replace")))

	##~~ actual sending via serial

	def _needs_checksum(self, gcode=None):
		command_requiring_checksum = gcode is not None and gcode in self._checksum_requiring_commands
		command_allowing_checksum = gcode is not None or self._sendChecksumWithUnknownCommands
		return command_requiring_checksum or (command_allowing_checksum and self._checksum_enabled)

	@property
	def _checksum_enabled(self):
		return not self._neverSendChecksum and ((self.isPrinting() and self._currentFile and self._currentFile.checksum) or
		                                        self._alwaysSendChecksum or
		                                        not self._firmware_info_received)

	def _do_send(self, command, gcode=None):
		command_to_send = command.encode("ascii", errors="replace")
		if self._needs_checksum(gcode):
			self._do_increment_and_send_with_checksum(command_to_send)
		else:
			self._do_send_without_checksum(command_to_send)

	def _do_increment_and_send_with_checksum(self, cmd):
		with self._line_mutex:
			linenumber = self._current_line
			self._addToLastLines(cmd)
			self._current_line += 1
			self._do_send_with_checksum(cmd, linenumber)

	def _do_send_with_checksum(self, command, linenumber):
		command_to_send = b"N" + str(linenumber).encode("ascii") + b" " + command
		checksum = 0
		for c in bytearray(command_to_send):
			checksum ^= c
		command_to_send = command_to_send + b"*" + str(checksum).encode("ascii")
		self._do_send_without_checksum(command_to_send)

	def _do_send_without_checksum(self, cmd, log=True):
		if self._serial is None:
			return

		if log:
			self._log("Send: " + cmd.decode("ascii"))

		cmd += b"\n"
		written = 0
		passes = 0
		while written < len(cmd):
			to_send = cmd[written:]
			old_written = written

			try:
				result = self._serial.write(to_send)
				if result is None or not isinstance(result, int):
					# probably some plugin not returning the written bytes, assuming all of them
					written += len(cmd)
				else:
					written += result
			except serial.SerialTimeoutException:
				self._log("Serial timeout while writing to serial port, trying again.")
				try:
					result = self._serial.write(to_send)
					if result is None or not isinstance(result, int):
						# probably some plugin not returning the written bytes, assuming all of them
						written += len(cmd)
					else:
						written += result
				except Exception as ex:
					if not self._connection_closing:
						self._logger.exception("Unexpected error while writing to serial port")
						self._log("Unexpected error while writing to serial port: %s" % (get_exception_string()))
						if isinstance(ex, serial.SerialException):
							self._dual_log("Please see https://faq.octoprint.org/serialerror for possible reasons of this.",
							               level=logging.INFO)
						self._errorValue = get_exception_string()
						self.close(is_error=True)
					break
			except Exception as ex:
				if not self._connection_closing:
					self._logger.exception("Unexpected error while writing to serial port")
					self._log("Unexpected error while writing to serial port: %s" % (get_exception_string()))
					if isinstance(ex, serial.SerialException):
						self._dual_log("Please see https://faq.octoprint.org/serialerror for possible reasons of this.",
						               level=logging.INFO)
					self._errorValue = get_exception_string()
					self.close(is_error=True)
				break

			if old_written == written:
				# nothing written this pass
				passes += 1
				if passes > self._max_write_passes:
					# nothing written in max consecutive passes, we give up
					message = "Could not write anything to the serial port in {} tries, something appears to be wrong with the printer communication".format(self._max_write_passes)
					self._dual_log(message, level=logging.ERROR)
					self._errorValue = "Could not write to serial port"
					self.close(is_error=True)
					break
				# if we have failed to write data after an initial retry then the printer/system
				# may be busy, so give things a little time before we try again. Extend this
				# period each time we fail until either we write the data or run out of retry attempts.
				if passes > 1:
					time.sleep((passes-1)/10.0)

	##~~ command handlers

	## gcode

	def _gcode_T_queuing(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		toolMatch = regexes_parameters["intT"].search(cmd)
		if toolMatch:
			current_tool = self._currentTool
			new_tool = int(toolMatch.group("value"))

			if not self._validate_tool(new_tool):
				self._log("Not queuing T{}, that tool doesn't exist according to the printer profile or "
				          "was reported as invalid by the firmware".format(new_tool))
				return None,

			before = self._getGcodeScript("beforeToolChange", replacements=dict(tool=dict(old=current_tool, new=new_tool)))
			after = self._getGcodeScript("afterToolChange", replacements=dict(tool=dict(old=current_tool, new=new_tool)))

			def convert(data):
				result = []
				for d in data:
					# noinspection PyCompatibility
					if isinstance(d, tuple) and len(d) == 2:
						result.append((d[0], None, d[1]))
					elif isinstance(d, basestring):
						result.append(d)
				return result

			return convert(before) + [cmd] + convert(after)

	def _gcode_T_sending(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		toolMatch = regexes_parameters["intT"].search(cmd)
		if toolMatch:
			new_tool = int(toolMatch.group("value"))
			if not self._validate_tool(new_tool):
				self._log("Not sending T{}, that tool doesn't exist according to the printer profile or "
				          "was reported as invalid by the firmware".format(new_tool))
				return None,

	def _gcode_T_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		toolMatch = regexes_parameters["intT"].search(cmd)
		if toolMatch:
			new_tool = int(toolMatch.group("value"))
			self._toolBeforeChange = self._currentTool
			self._currentTool = new_tool
			eventManager().fire(Events.TOOL_CHANGE, dict(old=self._toolBeforeChange, new=self._currentTool))

	def _gcode_G0_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		if "Z" in cmd or "F" in cmd:
			# track Z
			match = regexes_parameters["floatZ"].search(cmd)
			if match:
				try:
					z = float(match.group("value"))
					if self._currentZ != z:
						self._currentZ = z
						self._callback.on_comm_z_change(z)
				except ValueError:
					pass

			# track F
			match = regexes_parameters["floatF"].search(cmd)
			if match:
				try:
					f = float(match.group("value"))
					self._currentF = f
				except ValueError:
					pass
	_gcode_G1_sent = _gcode_G0_sent

	def _gcode_G28_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		if "F" in cmd:
			match = regexes_parameters["floatF"].search(cmd)
			if match:
				try:
					f = float(match.group("value"))
					self._currentF = f
				except ValueError:
					pass

	def _gcode_M28_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		if not self.isStreaming():
			self._log("Detected manual streaming. Disabling temperature polling. Finish writing with M29. Do NOT attempt to print while manually streaming!")
			self._manualStreaming = True

	def _gcode_M29_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		if self._manualStreaming:
			self._log("Manual streaming done. Re-enabling temperature polling. All is well.")
			self._manualStreaming = False

	def _gcode_M140_queuing(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		if not self._printerProfileManager.get_current_or_default()["heatedBed"]:
			self._log("Warn: Not sending \"{}\", printer profile has no heated bed".format(cmd))
			return None, # Don't send bed commands if we don't have a heated bed
	_gcode_M190_queuing = _gcode_M140_queuing

	def _gcode_M141_queuing(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		if not self._printerProfileManager.get_current_or_default()["heatedChamber"]:
			self._log("Warn: Not sending \"{}\", printer profile has no heated chamber".format(cmd))
			return None, # Don't send chamber commands if we don't have a heated chamber
	_gcode_M191_queuing = _gcode_M141_queuing

	def _gcode_M104_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, wait=False, support_r=False, *args, **kwargs):
		toolNum = self._currentTool
		toolMatch = regexes_parameters["intT"].search(cmd)

		if toolMatch:
			toolNum = int(toolMatch.group("value"))

			if wait:
				self._toolBeforeHeatup = self._currentTool
				self._currentTool = toolNum

		match = regexes_parameters["floatS"].search(cmd)
		if not match and support_r:
			match = regexes_parameters["floatR"].search(cmd)

		if match and self.last_temperature.tools.get(toolNum) is not None:
			try:
				target = float(match.group("value"))
				self.last_temperature.set_tool(toolNum, target=target)
				self._callback.on_comm_temperature_update(self.last_temperature.tools, self.last_temperature.bed, self.last_temperature.chamber, self.last_temperature.custom)
			except ValueError:
				pass

	def _gcode_M140_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, wait=False, support_r=False, *args, **kwargs):
		match = regexes_parameters["floatS"].search(cmd)
		if not match and support_r:
			match = regexes_parameters["floatR"].search(cmd)

		if match:
			try:
				target = float(match.group("value"))
				self.last_temperature.set_bed(target=target)
				self._callback.on_comm_temperature_update(self.last_temperature.tools, self.last_temperature.bed, self.last_temperature.chamber, self.last_temperature.custom)
			except ValueError:
				pass

	def _gcode_M141_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, wait=False, support_r=False, *args, **kwargs):
		match = regexes_parameters["floatS"].search(cmd)
		if not match and support_r:
			match = regexes_parameters["floatR"].search(cmd)

		if match:
			try:
				target = float(match.group("value"))
				self.last_temperature.set_chamber(target=target)
				self._callback.on_comm_temperature_update(self.last_temperature.tools, self.last_temperature.bed, self.last_temperature.chamber, self.last_temperature.custom)
			except ValueError:
				pass

	def _gcode_M109_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		self._heatupWaitStartTime = monotonic_time()
		self._long_running_command = True
		self._heating = True
		self._gcode_M104_sent(cmd, cmd_type, wait=True, support_r=True)

	def _gcode_M190_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		self._heatupWaitStartTime = monotonic_time()
		self._long_running_command = True
		self._heating = True
		self._gcode_M140_sent(cmd, cmd_type, wait=True, support_r=True)

	def _gcode_M191_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		self._heatupWaitStartTime = monotonic_time()
		self._long_running_command = True
		self._heating = True
		self._gcode_M141_sent(cmd, cmd_type, wait=True, support_r=True)

	def _gcode_M116_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		self._heatupWaitStartTime = monotonic_time()
		self._long_running_command = True
		self._heating = True

	def _gcode_M155_sending(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		match = regexes_parameters["intS"].search(cmd)
		if match:
			interval = int(match.group("value"))
			self._temperature_autoreporting = self._firmware_capabilities.get(self.CAPABILITY_AUTOREPORT_TEMP, False) \
											  and (interval > 0)

	def _gcode_M27_sending(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		match = regexes_parameters["intS"].search(cmd)
		if match:
			interval = int(match.group("value"))
			self._sdstatus_autoreporting = self._firmware_capabilities.get(self.CAPABILITY_AUTOREPORT_SD_STATUS, False) \
										   and (interval > 0)

	def _gcode_M110_sending(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		newLineNumber = 0
		match = regexes_parameters["intN"].search(cmd)
		if match:
			newLineNumber = int(match.group("value"))

		with self._line_mutex:
			self._logger.info("M110 detected, setting current line number to {}".format(newLineNumber))

			# send M110 command with new line number
			self._current_line = newLineNumber

			# after a reset of the line number we have no way to determine what line exactly the printer now wants
			self._lastLines.clear()
		self._resendDelta = None

	def _trigger_emergency_stop(self, close=True):
		self._logger.info("Force-sending M112 to the printer")

		# emergency stop, jump the queue with the M112, regardless of whether the EMERGENCY_PARSER capability is
		# available or not
		#
		# send the M112 once without and with checksum
		self._do_send_without_checksum(b"M112")
		self._do_increment_and_send_with_checksum(b"M112")

		# No idea if the printer is still listening or if M112 won. Just in case
		# we'll now try to also manually make sure all heaters are shut off - better
		# safe than sorry. We do this ignoring the queue since at this point it
		# is irrelevant whether the printer has sent enough ack's or not, we
		# are going to shutdown the connection in a second anyhow.
		for tool in range(self._printerProfileManager.get_current_or_default()["extruder"]["count"]):
			self._do_increment_and_send_with_checksum("M104 T{tool} S0".format(tool=tool).encode("ascii"))
		if self._printerProfileManager.get_current_or_default()["heatedBed"]:
			self._do_increment_and_send_with_checksum(b"M140 S0")

		if close:
			# close to reset host state
			error_text = "Closing serial port due to emergency stop M112."
			self._log(error_text)

			self._errorValue = error_text
			self.close(is_error=True)

		# fire the M112 event since we sent it and we're going to prevent the caller from seeing it
		gcode = "M112"
		if gcode in gcodeToEvent:
			eventManager().fire(gcodeToEvent[gcode])

	def _gcode_M112_queuing(self, *args, **kwargs):
		self._trigger_emergency_stop()
		return None,

	def _gcode_M114_queued(self, *args, **kwargs):
		self._reset_position_timers()
	_gcode_M114_sent = _gcode_M114_queued

	def _gcode_G4_sent(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		# we are intending to dwell for a period of time, increase the timeout to match
		p_match = regexes_parameters["floatP"].search(cmd)
		s_match = regexes_parameters["floatS"].search(cmd)

		_timeout = 0
		if p_match:
			_timeout = float(p_match.group("value")) / 1000.0
		elif s_match:
			_timeout = float(s_match.group("value"))

		self._timeout = self._get_new_communication_timeout() + _timeout
		self._dwelling_until = monotonic_time() + _timeout

	def _emergency_force_send(self, cmd, message, gcode=None, *args, **kwargs):
		# only jump the queue with our command if the EMERGENCY_PARSER capability is available
		if not self._capability_supported(self.CAPABILITY_EMERGENCY_PARSER):
			return

		self._logger.info(message)

		# use up an ok since we will get one back for this command and don't want to get out of sync
		used_up_clear = self._use_up_clear(gcode)
		self._do_send(cmd, gcode=gcode)
		if not used_up_clear:
			self._continue_sending()

		return None,

	def _validate_tool(self, tool):
		return not self._sanity_check_tools \
		       or (tool < self._printerProfileManager.get_current_or_default()["extruder"]["count"]
		           and not tool in self._knownInvalidTools)

	def _reset_position_timers(self):
		if self._cancel_position_timer:
			self._cancel_position_timer.reset()
		if self._pause_position_timer:
			self._pause_position_timer.reset()

	## atcommands

	def _atcommand_pause_queuing(self, command, parameters, tags=None, *args, **kwargs):
		if tags is None:
			tags = set()
		if not "script:afterPrintPaused" in tags:
			self.setPause(True, tags={"trigger:atcommand_pause"})

	def _atcommand_cancel_queuing(self, command, parameters, tags=None, *args, **kwargs):
		if tags is None:
			tags = set()
		if not "script:afterPrintCancelled" in tags:
			self.cancelPrint(tags={"trigger:atcommand_cancel"})
	_atcommand_abort_queuing = _atcommand_cancel_queuing

	def _atcommand_resume_queuing(self, command, parameters, tags=None, *args, **kwargs):
		if tags is None:
			tags = set()
		if not "script:beforePrintResumed" in tags:
			self.setPause(False, tags={"trigger:atcommand_resume"})

	##~~ command phase handlers

	def _command_phase_queuing(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		if gcode is not None:
			tags = kwargs.get("tags")
			if tags is None:
				tags = set()

			if gcode in self._emergency_commands and gcode != "M112":
				return self._emergency_force_send(cmd,
				                                  "Force-sending {} to the printer".format(gcode),
				                                  gcode=gcode,
				                                  *args, **kwargs)

			if self.isPrinting() and gcode in self._pausing_commands and not "trigger:cancel" in tags and not "trigger:pause" in tags:
				self._logger.info("Pausing print job due to command {}".format(gcode))
				self.setPause(True)

			if gcode in self._blocked_commands:
				self._logger.info("Not sending {} to printer, it's configured as a blocked command".format(gcode))
				return None,

	def _command_phase_sending(self, cmd, cmd_type=None, gcode=None, subcode=None, *args, **kwargs):
		if gcode is not None and gcode in self._long_running_commands:
			self._long_running_command = True

### MachineCom callback ################################################################################################

class MachineComPrintCallback(object):
	def on_comm_log(self, message):
		pass

	def on_comm_temperature_update(self, temp, bedTemp, chamberTemp, customTemp):
		pass

	def on_comm_position_update(self, position, reason=None):
		pass

	def on_comm_state_change(self, state):
		pass

	def on_comm_message(self, message):
		pass

	def on_comm_progress(self):
		pass

	def on_comm_print_job_started(self, suppress_script=False, user=None):
		pass

	def on_comm_print_job_failed(self, reason=None):
		pass

	def on_comm_print_job_done(self, suppress_script=False):
		pass

	def on_comm_print_job_cancelling(self, firmware_error=None, user=None):
		pass

	def on_comm_print_job_cancelled(self, suppress_script=False, user=None):
		pass

	def on_comm_print_job_paused(self, suppress_script=False, user=None):
		pass

	def on_comm_print_job_resumed(self, suppress_script=False, user=None):
		pass

	def on_comm_z_change(self, newZ):
		pass

	def on_comm_file_selected(self, filename, filesize, sd, user=None):
		pass

	def on_comm_sd_state_change(self, sdReady):
		pass

	def on_comm_sd_files(self, files):
		pass

	def on_comm_file_transfer_started(self, local_filename, remote_filename, filesize, user=None):
		pass

	def on_comm_file_transfer_done(self, local_filename, remote_filename, elapsed):
		pass

	def on_comm_file_transfer_failed(self, local_filename, remote_filename, elapsed):
		pass

	def on_comm_force_disconnect(self):
		pass

	def on_comm_record_fileposition(self, origin, name, pos):
		pass

### Printing file information classes ##################################################################################

class PrintingFileInformation(object):
	"""
	Encapsulates information regarding the current file being printed: file name, current position, total size and
	time the print started.
	Allows to reset the current file position to 0 and to calculate the current progress as a floating point
	value between 0 and 1.
	"""

	checksum = True

	def __init__(self, filename, user=None):
		self._logger = logging.getLogger(__name__)
		self._filename = filename
		self._user = user
		self._pos = 0
		self._size = None
		self._start_time = None
		self._done = False

	def getStartTime(self):
		return self._start_time

	def getFilename(self):
		return self._filename

	def getFilesize(self):
		return self._size

	def getFilepos(self):
		return self._pos

	def getFileLocation(self):
		return FileDestinations.LOCAL

	def getUser(self):
		return self._user

	def getProgress(self):
		"""
		The current progress of the file, calculated as relation between file position and absolute size. Returns -1
		if file size is None or < 1.
		"""
		if self._size is None or not self._size > 0:
			return -1
		return float(self._pos) / float(self._size)

	def reset(self):
		"""
		Resets the current file position to 0.
		"""
		self._pos = 0

	def start(self):
		"""
		Marks the print job as started and remembers the start time.
		"""
		self._start_time = monotonic_time()
		self._done = False

	def close(self):
		"""
		Closes the print job.
		"""
		pass

	@property
	def done(self):
		return self._done

	@done.setter
	def done(self, value):
		self._done = value

class PrintingSdFileInformation(PrintingFileInformation):
	"""
	Encapsulates information regarding an ongoing print from SD.
	"""

	checksum = False

	def __init__(self, filename, size, user=None):
		PrintingFileInformation.__init__(self, filename, user=user)
		self._size = size

	def getFileLocation(self):
		return FileDestinations.SDCARD

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, value):
		self._size = value

	@property
	def pos(self):
		return self._pos

	@pos.setter
	def pos(self, value):
		self._pos = value

class PrintingGcodeFileInformation(PrintingFileInformation):
	"""
	Encapsulates information regarding an ongoing direct print. Takes care of the needed file handle and ensures
	that the file is closed in case of an error.
	"""

	def __init__(self, filename, offsets_callback=None, current_tool_callback=None, user=None):
		PrintingFileInformation.__init__(self, filename, user=user)

		self._handle = None
		self._handle_mutex = threading.RLock()

		self._offsets_callback = offsets_callback
		self._current_tool_callback = current_tool_callback

		if not os.path.exists(self._filename) or not os.path.isfile(self._filename):
			raise IOError("File %s does not exist" % self._filename)
		self._size = os.stat(self._filename).st_size
		self._pos = 0
		self._read_lines = 0

	def seek(self, offset):
		with self._handle_mutex:
			if self._handle is None:
				return

			self._handle.seek(offset)
			self._pos = self._handle.tell()
			self._read_lines = 0

	def start(self):
		"""
		Opens the file for reading and determines the file size.
		"""
		PrintingFileInformation.start(self)
		with self._handle_mutex:
			self._handle = bom_aware_open(self._filename, encoding="utf-8", errors="replace", newline="")
			self._pos = self._handle.tell()
			if self._handle.encoding.endswith("-sig"):
				# Apparently we found an utf-8 bom in the file.
				# We need to add its length to our pos because it will
				# be stripped transparently and we'll have no chance
				# catching that.
				import codecs
				self._pos += len(codecs.BOM_UTF8)
			self._read_lines = 0

	def close(self):
		"""
		Closes the file if it's still open.
		"""
		PrintingFileInformation.close(self)
		with self._handle_mutex:
			if self._handle is not None:
				try:
					self._handle.close()
				except Exception:
					pass
			self._handle = None

	def getNext(self):
		"""
		Retrieves the next line for printing.
		"""
		with self._handle_mutex:
			if self._handle is None:
				self._logger.warning("File {} is not open for reading".format(self._filename))
				return None, None, None

			try:
				offsets = self._offsets_callback() if self._offsets_callback is not None else None
				current_tool = self._current_tool_callback() if self._current_tool_callback is not None else None

				processed = None
				while processed is None:
					if self._handle is None:
						# file got closed just now
						self._pos = self._size
						self._done = True
						self._report_stats()
						return None, None, None

					# we need to manually keep track of our pos here since
					# codecs' readline will make our handle's tell not
					# return the actual number of bytes read, but also the
					# already buffered bytes (for detecting the newlines)
					line = self._handle.readline()
					self._pos += len(line.encode("utf-8"))

					if not line:
						self.close()
					processed = self._process(line, offsets, current_tool)
				self._read_lines += 1
				return processed, self._pos, self._read_lines
			except Exception as e:
				self.close()
				self._logger.exception("Exception while processing line")
				raise e

	def _process(self, line, offsets, current_tool):
		return process_gcode_line(line, offsets=offsets, current_tool=current_tool)

	def _report_stats(self):
		duration = monotonic_time() - self._start_time
		self._logger.info("Finished in {:.3f} s.".format(duration))
		pass

class StreamingGcodeFileInformation(PrintingGcodeFileInformation):
	def __init__(self, path, localFilename, remoteFilename, user=None):
		PrintingGcodeFileInformation.__init__(self, path, user=user)
		self._localFilename = localFilename
		self._remoteFilename = remoteFilename

	def start(self):
		PrintingGcodeFileInformation.start(self)
		self._start_time = monotonic_time()

	def getLocalFilename(self):
		return self._localFilename

	def getRemoteFilename(self):
		return self._remoteFilename

	def _process(self, line, offsets, current_tool):
		return process_gcode_line(line)

	def _report_stats(self):
		duration = monotonic_time() - self._start_time
		read_lines = self._read_lines
		if duration > 0 and read_lines > 0:
			stats = dict(lines=read_lines,
			             rate=float(read_lines) / duration,
			             time_per_line=duration * 1000.0 / float(read_lines),
			             duration=duration)
			self._logger.info("Finished in {duration:.3f} s. Approx. transfer rate of {rate:.3f} lines/s or {time_per_line:.3f} ms per line".format(**stats))


class SpecialStreamingGcodeFileInformation(StreamingGcodeFileInformation):
	"""
	For streaming files to the printer that aren't GCODE.

	Difference to regular StreamingGcodeFileInformation: no checksum requirement, only rudimentary line processing
	(stripping of whitespace from the end and ignoring of empty lines)
	"""

	checksum = False

	def _process(self, line, offsets, current_tool):
		line = line.rstrip()
		if not len(line):
			return None
		return line

class JobQueue(PrependableQueue):
	pass

class CommandQueue(TypedQueue):
	def __init__(self, *args, **kwargs):
		TypedQueue.__init__(self, *args, **kwargs)
		self._unblocked = threading.Event()
		self._unblocked.set()

	def block(self):
		self._unblocked.clear()

	def unblock(self):
		self._unblocked.set()

	@contextlib.contextmanager
	def blocked(self):
		self.block()
		try:
			yield
		finally:
			self.unblock()

	def get(self, *args, **kwargs):
		self._unblocked.wait()
		return TypedQueue.get(self, *args, **kwargs)

	def put(self, *args, **kwargs):
		self._unblocked.wait()
		return TypedQueue.put(self, *args, **kwargs)

	def clear(self):
		cleared = []
		while True:
			try:
				cleared.append(TypedQueue.get(self, False))
				TypedQueue.task_done(self)
			except queue.Empty:
				break
		return cleared

class SendQueue(PrependableQueue):

	def __init__(self, maxsize=0):
		PrependableQueue.__init__(self, maxsize=maxsize)

		self._unblocked = threading.Event()
		self._unblocked.set()

		self._resend_queue = PrependableQueue()
		self._send_queue = PrependableQueue()
		self._lookup = set()

		self._resend_active = False

	@property
	def resend_active(self):
		return self._resend_active

	@resend_active.setter
	def resend_active(self, resend_active):
		with self.mutex:
			self._resend_active = resend_active

	def block(self):
		self._unblocked.clear()

	def unblock(self):
		self._unblocked.set()

	@contextlib.contextmanager
	def blocked(self):
		self.block()
		try:
			yield
		finally:
			self.unblock()

	def prepend(self, item, item_type=None, target=None, block=True, timeout=None):
		self._unblocked.wait()
		PrependableQueue.prepend(self, (item, item_type, target), block=block, timeout=timeout)

	def put(self, item, item_type=None, target=None, block=True, timeout=None):
		self._unblocked.wait()
		PrependableQueue.put(self, (item, item_type, target), block=block, timeout=timeout)

	def get(self, block=True, timeout=None):
		self._unblocked.wait()
		item, _, _ = PrependableQueue.get(self, block=block, timeout=timeout)
		return item

	def clear(self):
		cleared = []
		while True:
			try:
				cleared.append(PrependableQueue.get(self, False))
				PrependableQueue.task_done(self)
			except queue.Empty:
				break
		return cleared

	def _put(self, item):
		_, item_type, target = item
		if item_type is not None:
			if item_type in self._lookup:
				raise TypeAlreadyInQueue(item_type, "Type {} is already in queue".format(item_type))
			else:
				self._lookup.add(item_type)

		if target == "resend":
			self._resend_queue.put(item)
		else:
			self._send_queue.put(item)

		pass

	def _prepend(self, item):
		_, item_type, target = item
		if item_type is not None:
			if item_type in self._lookup:
				raise TypeAlreadyInQueue(item_type, "Type {} is already in queue".format(item_type))
			else:
				self._lookup.add(item_type)

		if target == "resend":
			self._resend_queue.prepend(item)
		else:
			self._send_queue.prepend(item)

	def _get(self):
		if self.resend_active:
			item = self._resend_queue.get(block=False)
		else:
			try:
				item = self._resend_queue.get(block=False)
			except queue.Empty:
				item = self._send_queue.get(block=False)

		_, item_type, _ = item
		if item_type is not None:
			if item_type in self._lookup:
				self._lookup.remove(item_type)

		return item

	def _qsize(self):
		if self.resend_active:
			return self._resend_queue.qsize()
		else:
			return self._resend_queue.qsize() + self._send_queue.qsize()


_temp_command_regex = re.compile(r"^M(?P<command>104|109|140|190)(\s+T(?P<tool>\d+)|\s+S(?P<temperature>[-+]?\d*\.?\d*))+")

def apply_temperature_offsets(line, offsets, current_tool=None):
	if offsets is None:
		return line

	match = _temp_command_regex.match(line)
	if match is None:
		return line

	groups = match.groupdict()
	if not "temperature" in groups or groups["temperature"] is None:
		return line

	offset = 0
	if current_tool is not None and (groups["command"] == "104" or groups["command"] == "109"):
		# extruder temperature, determine which one and retrieve corresponding offset
		tool_num = current_tool
		if "tool" in groups and groups["tool"] is not None:
			tool_num = int(groups["tool"])

		tool_key = "tool%d" % tool_num
		offset = offsets[tool_key] if tool_key in offsets and offsets[tool_key] else 0

	elif groups["command"] == "140" or groups["command"] == "190":
		# bed temperature
		offset = offsets["bed"] if "bed" in offsets else 0

	if offset == 0:
		return line

	temperature = float(groups["temperature"])
	if temperature == 0:
		return line

	return line[:match.start("temperature")] + "%f" % (temperature + offset) + line[match.end("temperature"):]

def strip_comment(line):
	if not ";" in line:
		# shortcut
		return line

	escaped = False
	result = []
	for c in line:
		if c == ";" and not escaped:
			break
		result += c
		escaped = (c == "\\") and not escaped
	return "".join(result)

def process_gcode_line(line, offsets=None, current_tool=None):
	line = strip_comment(line).strip()
	if not len(line):
		return None

	if offsets is not None:
		line = apply_temperature_offsets(line, offsets, current_tool=current_tool)

	return line

def convert_pause_triggers(configured_triggers):
	if not configured_triggers:
		return dict()

	triggers = {
		"enable": [],
		"disable": [],
		"toggle": []
	}
	for trigger in configured_triggers:
		if not "regex" in trigger or not "type" in trigger:
			continue

		try:
			regex = trigger["regex"]
			t = trigger["type"]
			if t in triggers:
				# make sure regex is valid
				re.compile(regex)
				# add to type list
				triggers[t].append(regex)
		except Exception as exc:
			# invalid regex or something like this
			_logger.debug("Problem with trigger %r: %s", trigger, str(exc))

	result = dict()
	for t in triggers.keys():
		if len(triggers[t]) > 0:
			result[t] = re.compile("|".join(map(lambda pattern: "({pattern})".format(pattern=pattern), triggers[t])))
	return result


def convert_feedback_controls(configured_controls):
	if not configured_controls:
		return dict(), None

	def preprocess_feedback_control(control, result):
		if "key" in control and "regex" in control and "template" in control:
			# key is always the md5sum of the regex
			key = control["key"]

			if result[key]["pattern"] is None or result[key]["matcher"] is None:
				# regex has not been registered
				try:
					result[key]["matcher"] = re.compile(control["regex"])
					result[key]["pattern"] = control["regex"]
				except Exception as exc:
					_logger.warning("Invalid regex {regex} for custom control: {exc}".format(regex=control["regex"], exc=str(exc)))

			result[key]["templates"][control["template_key"]] = control["template"]

		elif "children" in control:
			for c in control["children"]:
				preprocess_feedback_control(c, result)

	def prepare_result_entry():
		return dict(pattern=None, matcher=None, templates=dict())

	from collections import defaultdict
	feedback_controls = defaultdict(prepare_result_entry)

	for control in configured_controls:
		preprocess_feedback_control(control, feedback_controls)

	feedback_pattern = []
	for match_key, entry in feedback_controls.items():
		if entry["matcher"] is None or entry["pattern"] is None:
			continue
		feedback_pattern.append("(?P<group{key}>{pattern})".format(key=match_key, pattern=entry["pattern"]))
	feedback_matcher = re.compile("|".join(feedback_pattern))

	return feedback_controls, feedback_matcher

def canonicalize_temperatures(parsed, current):
	"""
	Canonicalizes the temperatures provided in parsed.

	Will make sure that returned result only contains extruder keys
	like Tn, so always qualified with a tool number.

	The algorithm for cleaning up the parsed keys is the following:

	  * If ``T`` is not included with the reported extruders, return
	  * If more than just ``T`` is reported:
	    * If both ``T`` and ``T0`` are reported, remove ``T`` from
	      the result.
	    * Else set ``T0`` to ``T`` and delete ``T`` (Smoothie extra).
	  * If only ``T`` is reported, set ``Tc`` to ``T`` and delete ``T``
	  * return

	Arguments:
	    parsed (dict): the parsed temperatures (mapping tool => (actual, target))
	      to canonicalize
	    current (int): the current active extruder
	Returns:
	    dict: the canonicalized version of ``parsed``
	"""

	reported_extruders = list(filter(lambda x: x.startswith("T"), parsed.keys()))
	if not "T" in reported_extruders:
		# Our reported_extruders are either empty or consist purely
		# of Tn keys, no need for any action
		return parsed

	current_tool_key = "T%d" % current
	result = dict(parsed)

	if len(reported_extruders) > 1:
		if "T0" in reported_extruders:
			# Both T and T0 are present, let's check if Tc is too.
			# If it is, we just throw away T (it's redundant). It
			# it isn't, we first copy T to Tc, then throw T away.
			#
			# The easier construct would be to always overwrite Tc
			# with T and throw away T, but that assumes that if
			# both are present, T has the same value as Tc. That
			# might not necessarily be the case (weird firmware)
			# so we err on the side of caution here and trust Tc
			# over T.
			if current_tool_key not in reported_extruders:
				# T and T0 are present, but Tc is missing - copy
				# T to Tc
				result[current_tool_key] = result["T"]
			# throw away T, it's redundant (now)
			del result["T"]
		else:
			# So T is there, but T0 isn't. That looks like Smoothieware which
			# always reports the first extruder T0 as T:
			#
			#     T:<T0> T1:<T1> T2:<T2> ... B:<B>
			#
			# becomes
			#
			#     T0:<T0> T1:<T1> T2:<T2> ... B:<B>
			result["T0"] = result["T"]
			del result["T"]

	else:
		# We only have T. That can mean two things:
		#
		#   * we only have one extruder at all, or
		#   * we are currently parsing a response to M109/M190, which on
		#     some firmwares doesn't report the full M105 output while
		#     waiting for the target temperature to be reached but only
		#     reports the current tool and bed
		#
		# In both cases it is however safe to just move our T over
		# to Tc in the parsed data, current should always stay
		# 0 for single extruder printers. E.g. for current_tool == 1:
		#
		#     T:<T1>
		#
		# becomes
		#
		#     T1:<T1>

		result[current_tool_key] = result["T"]
		del result["T"]

	return result

def parse_temperature_line(line, current):
	"""
	Parses the provided temperature line.

	The result will be a dictionary mapping from the extruder or bed key to
	a tuple with current and target temperature. The result will be canonicalized
	with :func:`canonicalize_temperatures` before returning.

	Arguments:
	    line (str): the temperature line to parse
	    current (int): the current active extruder

	Returns:
	    tuple: a 2-tuple with the maximum tool number and a dict mapping from
	      key to (actual, target) tuples, with key either matching ``Tn`` for ``n >= 0`` or ``B``
	"""

	result = {}
	maxToolNum = 0
	for match in re.finditer(regex_temp, line):
		values = match.groupdict()
		tool = values["tool"]
		toolnum = values.get("toolnum", None)
		toolNumber = int(toolnum) if toolnum is not None and len(toolnum) else None
		if toolNumber and toolNumber > maxToolNum:
			maxToolNum = toolNumber

		try:
			actual = float(match.group(3))
			target = None
			if match.group(4) and match.group(5):
				target = float(match.group(5))

			result[tool] = (actual, target)
		except ValueError:
			# catch conversion issues, we'll rather just not get the temperature update instead of killing the connection
			pass

	return max(maxToolNum, current), canonicalize_temperatures(result, current)

def parse_firmware_line(line):
	"""
	Parses the provided firmware info line.

	The result will be a dictionary mapping from the contained keys to the contained
	values.

	Arguments:
	    line (str): the line to parse

	Returns:
	    dict: a dictionary with the parsed data
	"""

	if line.startswith("NAME."):
		# Good job Malyan. Why use a : when you can also just use a ., right? Let's revert that.
		line = list(line)
		line[4] = ":"
		line = "".join(line)

	result = dict()
	split_line = regex_firmware_splitter.split(line.strip())[1:] # first entry is empty start of trimmed string
	for key, value in chunks(split_line, 2):
		result[key] = value.strip()
	return result

def parse_capability_line(line):
	"""
	Parses the provided firmware capability line.

	Lines are expected to be of the format

	    Cap:<capability name in caps>:<0 or 1>

	e.g.

	    Cap:AUTOREPORT_TEMP:1
	    Cap:TOGGLE_LIGHTS:0

	Args:
		line (str): the line to parse

	Returns:
		tuple: a 2-tuple of the parsed capability name and whether it's on (true) or off (false), or None if the line
		    could not be parsed
	"""

	line = line.lower()
	if line.startswith("cap:"):
		line = line[len("cap:"):]

	parts = line.split(":")
	if len(parts) != 2:
		# wrong format, can't parse this
		return None

	capability, flag = parts
	if not flag in ("0", "1"):
		# wrong format, can't parse this
		return None

	return capability.upper(), flag == "1"

def parse_resend_line(line):
	"""
	Parses the provided resend line and returns requested line number.

	Args:
		line (str): the line to parse

	Returns:
		int or None: the extracted line number to resend, or None if no number could be extracted
	"""

	match = regex_resend_linenumber.search(line)
	if match is not None:
		return int(match.group("n"))

	return None


def parse_position_line(line):
	"""
	Parses the provided M114 response line and returns the parsed coordinates.

	Args:
		line (str): the line to parse

	Returns:
		dict or None: the parsed coordinates, or None if no coordinates could be parsed
	"""

	match = regex_position.search(line)
	if match is not None:
		result = dict(x=float(match.group("x")),
		              y=float(match.group("y")),
		              z=float(match.group("z")))
		if match.group("e") is not None:
			# report contains only one E
			result["e"] = float(match.group("e"))

		elif match.group("es") is not None:
			# report contains individual entries for multiple extruders ("E0:... E1:... E2:...")
			es = match.group("es")
			for m in regex_e_positions.finditer(es):
				result["e{}".format(m.group("id"))] = float(m.group("value"))

		else:
			# apparently no E at all, should never happen but let's still handle this
			return None

		return result

	return None


def gcode_command_for_cmd(cmd):
	"""
	Tries to parse the provided ``cmd`` and extract the GCODE command identifier from it (e.g. "G0" for "G0 X10.0").

	Arguments:
	    cmd (str): The command to try to parse.

	Returns:
	    str or None: The GCODE command identifier if it could be parsed, or None if not.
	"""

	gcode, _ = gcode_and_subcode_for_cmd(cmd)
	return gcode


def gcode_and_subcode_for_cmd(cmd):
	if not cmd:
		return None, None

	match = regex_command.search(cmd)
	if not match:
		return None, None

	values = match.groupdict()
	if "codeGM" in values and values["codeGM"]:
		gcode = values["codeGM"]
	elif "codeT" in values and values["codeT"]:
		gcode = values["codeT"]
	elif settings().getBoolean(["serial", "supportFAsCommand"]) and "codeF" in values and values["codeF"]:
		gcode = values["codeF"]
	else:
		# this should never happen
		return None, None

	return gcode, values.get("subcode", None)


def _normalize_command_handler_result(command, command_type, gcode, subcode, tags, handler_results, tags_to_add=None):
	"""
	Normalizes a command handler result.

	Handler results can be either ``None``, a single result entry or a list of result
	entries.

	``None`` results are ignored, the provided ``command``, ``command_type``,
	``gcode``, ``subcode`` and ``tags`` are returned in that case (as single-entry list with
	one 5-tuple as entry).

	Single result entries are either:

	  * a single string defining a replacement ``command``
	  * a 1-tuple defining a replacement ``command``
	  * a 2-tuple defining a replacement ``command`` and ``command_type``
	  * a 3-tuple defining a replacement ``command`` and ``command_type`` and additional ``tags`` to set

	A ``command`` that is ``None`` will lead to the entry being ignored for
	the normalized result.

	The method returns a list of normalized result entries. Normalized result
	entries always are a 4-tuple consisting of ``command``, ``command_type``,
	``gcode`` and ``subcode``, the latter three being allowed to be ``None``. The list may
	be empty in which case the command is to be suppressed.

	Examples:
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, None) # doctest: +ALLOW_UNICODE
	    [('M105', None, 'M105', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, "M110") # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, ["M110"]) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, ["M110", "M117 Foobar"]) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, None), ('M117 Foobar', None, 'M117', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, [("M110",), "M117 Foobar"]) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, None), ('M117 Foobar', None, 'M117', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, [("M110", "lineno_reset"), "M117 Foobar"]) # doctest: +ALLOW_UNICODE
	    [('M110', 'lineno_reset', 'M110', None, None), ('M117 Foobar', None, 'M117', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, []) # doctest: +ALLOW_UNICODE
	    []
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, ["M110", None]) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, [("M110",), (None, "ignored")]) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, None, [("M110",), ("M117 Foobar", "display_message"), ("tuple", "of", "unexpected", "length"), ("M110", "lineno_reset")]) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, None), ('M117 Foobar', 'display_message', 'M117', None, None), ('M110', 'lineno_reset', 'M110', None, None)]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, {"tag1", "tag2"}, ["M110", "M117 Foobar"]) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, {'tag1', 'tag2'}), ('M117 Foobar', None, 'M117', None, {'tag1', 'tag2'})]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, {"tag1", "tag2"}, ["M110", "M105", "M117 Foobar"], tags_to_add={"tag3"}) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, {'tag1', 'tag2', 'tag3'}), ('M105', None, 'M105', None, {'tag1', 'tag2'}), ('M117 Foobar', None, 'M117', None, {'tag1', 'tag2', 'tag3'})]
	    >>> _normalize_command_handler_result("M105", None, "M105", None, {"tag1", "tag2"}, ["M110", ("M105", "temperature_poll"), "M117 Foobar"], tags_to_add={"tag3"}) # doctest: +ALLOW_UNICODE
	    [('M110', None, 'M110', None, {'tag1', 'tag2', 'tag3'}), ('M105', 'temperature_poll', 'M105', None, {'tag1', 'tag2', 'tag3'}), ('M117 Foobar', None, 'M117', None, {'tag1', 'tag2', 'tag3'})]

	Arguments:
	    command (str or None): The command for which the handler result was
	        generated
	    command_type (str or None): The command type for which the handler
	        result was generated
	    gcode (str or None): The GCODE for which the handler result was
	        generated
	    subcode (str or None): The GCODE subcode for which the handler result
	        was generated
	    tags (set of str or None): The tags associated with the GCODE for which
	        the handler result was generated
	    handler_results: The handler result(s) to normalized. Can be either
	        a single result entry or a list of result entries.
	    tags_to_add (set of str or None): List of tags to add to expanded result
	        entries

	Returns:
	    (list) - A list of normalized handler result entries, which are
	        5-tuples consisting of ``command``, ``command_type``, ``gcode``
	        ``subcode`` and ``tags``, the latter three of which may be ``None``.
	"""

	original = (command, command_type, gcode, subcode, tags)

	if handler_results is None:
		# handler didn't return anything, we'll just continue
		return [original]

	if not isinstance(handler_results, list):
		handler_results = [handler_results,]

	result = []
	for handler_result in handler_results:
		# we iterate over all handler result entries and process each one
		# individually here

		if handler_result is None:
			# entry is None, we'll ignore that entry and continue
			continue

		if tags:
			# copy the tags
			tags = set(tags)

		if isinstance(handler_result, basestring):
			# entry is just a string, replace command with it
			command = handler_result

			if command != original[0]:
				# command changed, re-extract gcode and subcode and add tags if necessary
				gcode, subcode = gcode_and_subcode_for_cmd(command)

				if tags_to_add and isinstance(tags_to_add, set) and command != original[0]:
					if tags is None:
						tags = set()
					tags |= tags_to_add

			result.append((command, command_type, gcode, subcode, tags))

		elif isinstance(handler_result, tuple):
			# entry is a tuple, extract command and command_type
			hook_result_length = len(handler_result)
			handler_tags = None

			if hook_result_length == 1:
				# handler returned just the command
				command, = handler_result
			elif hook_result_length == 2:
				# handler returned command and command_type
				command, command_type = handler_result
			elif hook_result_length == 3:
				# handler returned command, command type and additional tags
				command, command_type, handler_tags = handler_result
			else:
				# handler returned a tuple of an unexpected length, ignore
				# and continue
				continue

			if command is None:
				# command is None, ignore it and continue
				continue

			if command != original[0] or command_type != original[2]:
				# command or command_type changed, re-extract gcode and subcode and add tags if necessary
				gcode, subcode = gcode_and_subcode_for_cmd(command)

				if tags_to_add and isinstance(tags_to_add, set):
					if tags is None:
						tags = set()
					tags |= tags_to_add

			if handler_tags and isinstance(handler_tags, set):
				# handler provided additional tags, add them
				if tags is None:
					tags = set()
				tags |= handler_tags

			result.append((command, command_type, gcode, subcode, tags))

		# reset to original
		command, command_type, gcode, subcode, tags = original

	return result


class QueueMarker(object):

	def __init__(self, callback):
		self.callback = callback

	def run(self):
		if callable(self.callback):
			try:
				self.callback()
			except Exception:
				_logger.exception("Error while running callback of QueueMarker")

class SendQueueMarker(QueueMarker):
	pass


class BufferedReadlineWrapper(wrapt.ObjectProxy):
	def __init__(self, obj):
		wrapt.ObjectProxy.__init__(self, obj)
		self._buffered = bytearray()

	def readline(self, terminator=serial.LF):
		termlen = len(terminator)
		timeout = serial.Timeout(self._timeout)

		while not timeout.expired():
			self._buffered += self.read(self.in_waiting)

			# check for terminator, if it's there we have found our line
			termpos = self._buffered.find(terminator)
			if termpos >= 0:
				# line: everything up to and incl. the terminator, buffered: rest
				line = self._buffered[:termpos + termlen]
				del self._buffered[:termpos + termlen]
				return bytes(line)

			if timeout.expired():
				break

			c = self.read(1)
			if not c:
				# EOF
				break

			self._buffered += c

		return b""


# --- Test code for speed testing the comm layer via command line follows


def upload_cli():
	"""
	Usage: python -m octoprint.util.comm <port> <baudrate> <local path> <remote path>

	Uploads <local path> to <remote path> on SD card of printer on port <port>, using baudrate <baudrate>.
	"""

	import sys
	from octoprint.util import Object

	logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

	# fetch port, baudrate, filename and target from commandline
	if len(sys.argv) < 5:
		print("Usage: comm.py <port> <baudrate> <local path> <target path>")
		sys.exit(-1)

	port = sys.argv[1]
	baudrate = sys.argv[2]
	path = sys.argv[3]
	target = sys.argv[4]

	# init settings & plugin manager
	settings(init=True)
	octoprint.plugin.plugin_manager(init=True)

	# create dummy callback
	class MyMachineComCallback(MachineComPrintCallback):
		progress_interval = 1

		def __init__(self, path, target):
			self.finished = threading.Event()
			self.finished.clear()

			self.comm = None
			self.error = False
			self.started = False

			self._path = path
			self._target = target
			self._state = None

		def on_comm_file_transfer_started(self, filename, filesize, user=None):
			# transfer started, report
			_logger.info("Started file transfer of {}, size {}B".format(filename, filesize))
			self.started = True

		def on_comm_file_transfer_done(self, filename):
			# transfer done, report, print stats and finish
			_logger.info("Finished file transfer of {}".format(filename))
			self.finished.set()

		def on_comm_state_change(self, state):
			self._state = state

			if state in (MachineCom.STATE_ERROR, MachineCom.STATE_CLOSED_WITH_ERROR):
				# report and exit on errors
				_logger.error("Error/closed with error, exiting.")
				self.error = True
				self.finished.set()

			elif state in (MachineCom.STATE_OPERATIONAL,) and not self.started:
				def run():
					_logger.info("Looks like we are operational, waiting a bit for everything to settle")
					time.sleep(15)
					if self._state in (MachineCom.STATE_OPERATIONAL,) and not self.started:
						# start transfer once we are operational
						self.comm.startFileTransfer(self._path, os.path.basename(self._path), self._target)

				thread = threading.Thread(target=run)
				thread.daemon = True
				thread.start()

	callback = MyMachineComCallback(path, target)

	# mock printer profile manager
	profile = dict(heatedBed=False,
	               extruder=dict(count=1, sharedNozzle=False))
	printer_profile_manager = Object()
	printer_profile_manager.get_current_or_default = lambda: profile

	# initialize serial
	comm = MachineCom(port=port, baudrate=baudrate, callbackObject=callback, printerProfileManager=printer_profile_manager)
	callback.comm = comm

	# wait for file transfer to finish
	callback.finished.wait()

	# close connection
	comm.close()

	_logger.info("Done, exiting...")

if __name__ == "__main__":
	upload_cli()
