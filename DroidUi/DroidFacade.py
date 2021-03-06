#
# Copyright (C) 2012-2014 Tommy Alex. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# DroidFacade.py
# misc droid function wrapper
#
# Create: 2012-11-13 01:49
#
# Update: 2013-05-19 04:11


import warnings
from base64 import b64encode, b64decode
from .sl4a import sl4a, sl4aError, _a
from .DroidConstants import SENSOR_ALL, BLUETOOTH_UUID, INBOX, CATEGORY_DEFAULT


class _Facade(object):
	pass


class Event(_Facade):
	'''Wrapper functions for EventFacade
	(http://www.mithril.com.au/android/doc/EventFacade.html)'''

	def __init__(self, droid, **handler):
		assert isinstance(droid, sl4a)
		self.droid = droid
		self._handler = {}
		self._loop = True
		for e, h in handler.items():
			self.reg(e, h)

	def clear(self):
		'''Clears all events from the event buffer'''
		self.droid.eventClearBuffer()

	def poll(self, count = 1):
		'''Returns and removes the oldest COUNT events
		(i.e. location or sensor update, etc.) from the event buffer'''
		return self.droid.eventPoll(count)

	def post(self, name, data, enqueue = False):
		'''Post an event to the event queue
		name (String) Name of event
		data (String) Data contained in event
		enqueue (Boolean) Set to False if you don't want your events to be added to the event queue, just dispatched'''
		self.droid.eventPost(name, data, enqueue)

	def wait(self, timeout = None):
		'''Blocks until an event occurs. The returned event is removed from the buffer
		timeout (Integer) the maximum time to wait (in ms)
		returns: (Event) Map of event properties'''
		return self.droid.eventWait(timeout)

	def waitFor(self, name, timeout = None):
		'''Blocks until an event with the supplied name occurs. The returned event is not removed from the buffer
		name (String)
		timeout (Integer) the maximum time to wait (in ms)
		returns: (Event) Map of event properties'''
		return self.droid.eventWait(name, timeout)

	def register(self, name, handler):
		'''register event handler
		NAME    the event name
		HANDLER should accept 1 param which contains event data
		HANDLER should return True if the event is handled properly'''
		assert callable(handler)
		if name in self._handler: warnings.warn('event handler is override: ev = %s' % name)
		self._handler[name] = handler
	reg = register

	def unregister(self, name):
		'''unregister event handler
		NAME    the event name'''
		if name in self._handler:
			handler = self._handler[name]
			del self._handler[name]
			return handler
		else:
			warnings.warn('no registered event handler: ev = %s' % name)
	unreg = unregister

	def quit(self, data = None):
		'''quit event loop
		there is a DATA parameter, so quit can be used as a event handler as well as a click handler or key handler'''
		self._loop = False
		return True

	def loop(self):
		'''event hanlding loop'''
		while self._loop:
			event = self.wait()
			name = event["name"]
			if name in self._handler:
				if not self._handler[name](event['data']):
					warnings.warn('unhandled event: %s' % str(event))
			else:
				warnings.warn('unknown event: %s' % str(event))
		# reset to allow reentry
		self._loop = True


class Broadcast(Event):

	def categories(self):
		'''Lists all the broadcast signals we are listening for'''
		return self.droid.eventGetBrodcastCategories()

	def register(self, category, enqueue = True):
		'''Registers a listener for a new broadcast signal
		category (String)
		enqueue (Boolean) Should this events be added to the event queue or only dispatched'''
		self.droid.eventRegisterForBroadcast(category, enqueue)
	reg = register

	def unregister(self, category):
		'''Stop listening for a broadcast signal'''
		self.droid.eventUnregisterForBroadcast(category)
	unreg = unregister


class Uri(_Facade):

	def __init__(self, init = ''):
		self.set(init)

	def __str__(self):
		return self.uri

	def set(self, uri):
		self.uri = uri

	def attr(self):
		'''Content Resolver Query Attributes'''
		return _a.queryAttributes(self.uri)

	def content(self):
		'''Content Resolver Query'''
		return _a.queryContent(self.uri)

	def pick(self):
		'''Display content to be picked by URI (e.g. contacts)'''
		return _a.pick(self.uri)

	def view(self, type, **extras):
		'''Start activity with view action by URI (i.e. browser, contacts, etc.)'''
		return _a.view(self.uri, type, extras)


class Count(object):
	'''reference count'''

	def __init__(self, init = 0):
		self.count = init

	def clear(self):
		self.count = 0

	def get(self):
		return self.count

	def inc(self, value = 1):
		self.count += value

	def dec(self, value = 1):
		self.count -= value

	def inc_if_zero(self, callback, *args, **kwargs):
		'''if count is zero, call the CALLBACK with ARGS and KWARGS
		then inc the count'''
		if self.get() == 0:
			callback(*args, **kwargs)
		self.inc()

	def dec_if_zero(self, callback, *args, **kwargs):
		'''dec the count first,
		the check if count is zero, call the CALLBACK with ARGS and KWARGS'''
		self.dec()
		if self.get() == 0:
			callback(*args, **kwargs)


class Sensing(_Facade):
	'''Wrapper functions for SensorManagerFacade
	(http://www.mithril.com.au/android/doc/SensorManagerFacade.html)'''

	_refs = Count()

	def __init__(self, sensorNumber = SENSOR_ALL, delayTime = 250):
		self._refs.inc_if_zero(_a.startSensingTimed, sensorNumber, delayTime)

	def __del__(self):
		self._refs.dec_if_zero(_a.stopSensing)

	def read(self):
		'''Returns the most recently recorded sensor data'''
		return _a.readSensors()

	def accuracy(self):
		'''Returns the most recently received accuracy value'''
		return _a.sensorsGetAccuracy()

	def light(self):
		'''Returns the most recently received light value'''
		return _a.sensorsGetLight()

	def accelerometer(self):
		'''Returns the most recently received accelerometer values
		returns: (List) a List of Floats [(acceleration on the) X axis, Y axis, Z axis]'''
		return _a.sensorsReadAccelerometer()

	def magnetometer(self):
		'''Returns the most recently received magnetic field values
		returns: (List) a List of Floats [(magnetic field value for) X axis, Y axis, Z axis]'''
		return _a.sensorsReadMagnetometer()

	def orientation(self):
		'''Returns the most recently received orientation values
		returns: (List) a List of Doubles [azimuth, pitch, roll]'''
		return _a.sensorsReadOrientation()


class Location(_Facade):
	'''Wrapper functions for LocationFacade
	(http://www.mithril.com.au/android/doc/LocationFacade.html)'''

	_refs = Count()

	def __init__(self):
		self._refs.inc_if_zero(_a.startLocating)

	def __del__(self):
		self._refs.dec_if_zero(_a.stopLocating)

	def read(self):
		'''Returns the current location as indicated by all available providers'''
		return _a.readLocation()

	@classmethod
	def providers(cls):
		'''Returns availables providers on the phone'''
		return _a.locationProviders()

	@classmethod
	def enabled(cls, provider):
		'''Ask if provider is enabled'''
		return _a.locationProviderEnabled(provider)

	@classmethod
	def last(cls):
		'''Returns the last known location of the device'''
		return _a.getLastKnownLocation()

	@classmethod
	def geocode(cls, latitude, longitude, maxResults = 1):
		'''Returns a list of addresses for the given latitude and longitude
		latitude (Double)
		longitude (Double)
		maxResults (Integer) maximum number of results (default=1)
		returns: (List) A list of addresses'''
		return _a.geocode(latitude, longitude, maxResults)


class Battery(_Facade):
	'''Wrapper functions for BatteryManagerFacade
	(http://www.mithril.com.au/android/doc/BatteryManagerFacade.html)'''

	_refs = Count()

	HEALTH = (
		'invaild',
		'unknown',
		'good',
		'overheat',
		'dead',
		'over voltage',
		'unspecified failure',
	)

	PLUG_TYPE = (
		'unplugged',
		'AC charger',
		'USB port',
		'unknown',
	)

	STATUS = (
		'invalid',
		'unknown',
		'charging',
		'discharging',
		'not charging',
		'full',
	)

	def __init__(self):
		self._refs.inc_if_zero(_a.batteryStartMonitoring)

	def __del__(self):
		self._refs.dec_if_zero(_a.batteryStopMonitoring)

	def read(self):
		'''Returns the most recently recorded battery data'''
		return _a.readBatteryData()

	def present(self):
		'''Returns the most recently received battery presence data
		Min SDK level=5'''
		return _a.batteryCheckPresent()

	def health(self):
		'''Returns the most recently received battery health data'''
		return self.HEALTH[_a.batteryGetHealth()]

	def level(self):
		'''Returns the most recently received battery level (percentage)
		Min SDK level=5'''
		return _a.batteryGetLevel()

	def plugType(self):
		'''Returns the most recently received plug type data'''
		return self.PLUG_TYPE[_a.batteryGetPlugType()]

	def status(self):
		'''Returns the most recently received battery status data'''
		return self.STATUS[_a.batteryGetStatus()]

	def technology(self):
		'''Returns the most recently received battery technology data
		Min SDK level=5'''
		return _a.batteryGetTechnology()

	def temperature(self):
		'''Returns the most recently received battery temperature
		Min SDK level=5'''
		return _a.batteryGetTemperature()

	def voltage(self):
		'''Returns the most recently received battery voltage
		Min SDK level=5'''
		return _a.batteryGetVoltage()


class Signal(_Facade):
	'''Wrapper functions for SignalStrengthFacade
	(http://www.mithril.com.au/android/doc/SignalStrengthFacade.html)'''

	_refs = Count()

	def __init__(self):
		self._refs.inc_if_zero(_a.startTrackingSignalStrengths)

	def __del__(self):
		self._refs.dec_if_zero(_a.stopTrackingSignalStrengths)

	def read(self):
		'''Returns the current signal strengths'''
		return _a.readSignalStrengths()


class Phone(_Facade):
	'''Wrapper functions for PhoneFacade and SettingsFacade
	(http://www.mithril.com.au/android/doc/PhoneFacade.html)'''

	@classmethod
	def roaming(cls):
		'''Returns true if the device is considered roaming on the current network, for GSM purposes'''
		return _a.checkNetworkRoaming()

	@classmethod
	def cellLocation(cls):
		'''Returns the current cell location'''
		return _a.getCellLocation()

	@classmethod
	def id(cls):
		'''Returns the unique device ID
		for example, the IMEI for GSM and the MEID for CDMA phones.
		Return null if device ID is not available'''
		return _a.getDeviceId()

	@classmethod
	def version(cls):
		'''Returns the software version number for the device
		for example, the IMEI/SV for GSM phones
		Return null if the software version is not available'''
		return _a.getDeviceSoftwareVersion()

	@classmethod
	def number(cls):
		'''Returns the phone number string for line 1
		for example, the MSISDN for a GSM phone
		Return null if it is unavailable'''
		return _a.getLine1Number()

	@classmethod
	def neighboring(cls):
		'''Returns the neighboring cell information of the device'''
		return _a.getNeighboringCellInfo()

	@classmethod
	def operator(cls):
		'''Returns the numeric name (MCC+MNC) of current registered operator'''
		return _a.getNetworkOperator()

	@classmethod
	def operatorName(cls):
		'''Returns the alphabetic name of current registered operator'''
		return _a.getNetworkOperatorName()

	@classmethod
	def network(cls):
		'''Returns a the radio technology (network type) currently in use on the device'''
		return _a.getNetworkType()

	@classmethod
	def type(cls):
		'''Returns the device phone type'''
		return _a.getPhoneType()

	@classmethod
	def subscriber(cls):
		'''Returns the unique subscriber ID
		for example, the IMSI for a GSM phone
		Return null if it is unavailable'''
		return _a.getSubscriberId()

	@classmethod
	def voiceMailAlphaTag(cls):
		'''Retrieves the alphabetic identifier associated with the voice mail number'''
		return _a.getVoiceMailAlphaTag()

	@classmethod
	def voiceMailNumber(cls):
		'''Returns the voice mail number
		Return null if it is unavailable'''
		return _a.getVoiceMailNumber()

	@classmethod
	def call(cls, uri):
		'''Calls a contact/phone number by URI'''
		if hasattr(uri, 'isdigit') and uri.isdigit():
			_a.phoneCallNumber(uri)
		else:
			_a.phoneCall(uri)

	@classmethod
	def dial(cls, uri):
		'''Dials a contact/phone number by URI'''
		if hasattr(uri, 'isdigit') and uri.isdigit():
			_a.phoneDialNumber(uri)
		else:
			_a.phoneDial(uri)

	@classmethod
	def volume(cls, volume = None):
		'''Gets or Sets the ringer volume'''
		if volume is None:
			return _a.getRingerVolume()
		else:
			_a.setRingerVolume(volume)

	@classmethod
	def maxVolume(cls):
		'''Returns the maximum ringer volume'''
		return _a.getMaxRingerVolume()

	@classmethod
	def airplane(cls, enabled = None):
		'''Toggles airplane mode on and off'''
		if enabled is None:
			return _a.checkAirplaneMode()
		else:
			return _a.toggleAirplaneMode(enabled)

	@classmethod
	def silent(cls, enabled = None):
		'''Toggles ringer silent mode on and off'''
		if enabled is None:
			return _a.checkRingerSilentMode()
		else:
			return _a.toggleRingerSilentMode(enabled)

	@classmethod
	def vibrate(cls, enabled = None, ringer = True):
		'''Toggles vibrate mode on and off
		If ringer=true then set Ringer setting, else set Notification setting'''
		if enabled is None:
			return _a.getVibrateMode(ringer)
		else:
			return _a.toggleVibrateMode(enabled, ringer)

	@classmethod
	def brightness(cls, bright = None):
		'''Gets or Sets the the screen backlight brightness
		bright (Integer) brightness value between 0 and 255'''
		if bright is None:
			return _a.getScreenBrightness()
		else:
			return _a.setScreenBrightness(bright)

	@classmethod
	def screen(cls, timeout = None):
		'''Gets or Sets the screen timeout to this number of seconds'''
		if timeout is None:
			return _a.getScreenTimeout()
		else:
			return _a.setScreenTimeout(timeout)


class PhoneState(_Facade):
	'''Wrapper functions for PhoneFacade
	(http://www.mithril.com.au/android/doc/PhoneFacade.html)'''

	_refs = Count()

	def __init__(self):
		self._refs.inc_if_zero(_a.startTrackingPhoneState)

	def __del__(self):
		self._refs.dec_if_zero(_a.stopTrackingPhoneState)

	def read(self):
		'''Returns the current phone state and incoming number'''
		return _a.readPhoneState()


class Sim(_Facade):
	'''Wrapper functions for PhoneFacade
	(http://www.mithril.com.au/android/doc/PhoneFacade.html)'''

	@classmethod
	def state(cls):
		'''Returns the state of the device SIM card'''
		return _a.getSimState()

	@classmethod
	def serial(cls):
		'''Returns the serial number of the SIM, if applicable
		Return null if it is unavailable'''
		return _a.getSimSerialNumber()

	@classmethod
	def country(cls):
		'''Returns the ISO country code equivalent for the SIM provider's country code'''
		return _a.getSimCountryIso()

	@classmethod
	def operator(cls):
		'''Returns the MCC+MNC (mobile country code + mobile network code) of the provider of the SIM. 5 or 6 decimal digits'''
		return _a.getSimOperator()

	@classmethod
	def operatorName(cls):
		'''Returns the Service Provider Name (SPN)'''
		return _a.getSimOperatorName()


class Contact(_Facade):
	'''Wrapper functions for ContactsFacade
	(http://www.mithril.com.au/android/doc/ContactsFacade.html)'''

	@classmethod
	def attrs(cls):
		'''Returns a List of all possible attributes for contacts'''
		return _a.contactsGetAttributes()

	@classmethod
	def count(cls):
		'''Returns the number of contacts'''
		return _a.contactsGetCount()

	@classmethod
	def ids(cls):
		'''Returns a List of all contact IDs'''
		return _a.contactsGetIds()

	@classmethod
	def get(cls, id = None, *attributes):
		'''Returns contacts by ID or a List of all contacts'''
		if id is None:
			return _a.contactsGet(attributes)
		else:
			return _a.contactsGetById(id, attributes)

	@classmethod
	def pick(cls):
		'''Displays a list of contacts to pick from'''
		return _a.pickContact()

	@classmethod
	def view(cls):
		'''Opens the list of contacts'''
		return _a.viewContacts()


class Sms(_Facade):
	'''Wrapper functions for SmsFacade
	(http://www.mithril.com.au/android/doc/SmsFacade.html)'''

	@classmethod
	def attrs(cls):
		'''Returns a List of all possible message attributes'''
		return _a.smsGetAttributes()

	@classmethod
	def count(cls, unread = True, folder = INBOX):
		'''Returns a List of all message IDs'''
		return _a.smsGetMessageCount(unread, folder)

	@classmethod
	def ids(cls, unread = True, folder = INBOX):
		'''Returns a List of all message IDs'''
		return _a.smsGetMessageIds(unread, folder)

	@classmethod
	def get(cls, id, *attrs):
		'''Returns message attributes'''
		return _a.smsGetMessageById(id, attrs)

	@classmethod
	def gets(cls, unread = True, folder = INBOX, *attrs):
		'''Returns a List of all message IDs'''
		return _a.smsGetMessages(unread, folder, attrs)

	@classmethod
	def mark(cls, read = True, *id):
		'''Marks messages as read'''
		return _a.smsDeleteMessage(id, read)

	@classmethod
	def send(cls, address, text):
		'''Sends an SMS'''
		return _a.smsSend(address, text)

	@classmethod
	def delete(cls, id):
		'''Deletes a message'''
		return _a.smsDeleteMessage(id)


class Intent(_Facade):
	'''Wrapper functions for AndroidFacade
	(http://www.mithril.com.au/android/doc/AndroidFacade.html)'''

	def __init__(self, action, uri = None, type = None, package = None, clsname = None, flags = 0, *categories, **extras):
		'''Create an Intent'''
		if isinstance(uri, Uri): uri = uri.uri
		if len(categories) == 0: categories = (CATEGORY_DEFAULT,)
		self.intent = _a.makeIntent(action, uri, type, extras, categories, package, clsname, flags)

	def start(self, wait = False):
		'''Starts an activity and returns the result'''
		if wait:
			return _a.startActivityForResultIntent(self.intent)
		else:
			_a.startActivityIntent(self.intent)

	def broadcast(self):
		'''Send Broadcast Intent'''
		_a.sendBroadcastIntent(self.intent)


class Package(_Facade):
	'''Wrapper functions for ApplicationManagerFacade
	(http://www.mithril.com.au/android/doc/ApplicationManagerFacade.html)'''

	def __init__(self, classname):
		# try to find package name from a class name
		l = classname.split('.')
		for i in range(len(l), 0, -1):
			name = '.'.join(l[:i])
			if -1 != _a.getPackageVersionCode(name):
				self.pkg = name
				return
		self.pkg = classname

	def __str__(self):
		return 'package: %s, version: %s, code: %s' % (self.pkg, self.version(), self.code())

	def version(self):
		'''Returns package version name'''
		return _a.getPackageVersion(self.pkg)

	def code(self):
		'''Returns package version code'''
		return _a.getPackageVersionCode(self.pkg)

	def stop(self):
		'''Force stops a package'''
		_a.forceStopPackage(self.pkg)

	@classmethod
	def running(cls):
		'''Returns a list of packages running activities or services'''
		return _a.getRunningPackages()


# java class is different from Android package
class Class(_Facade):

	def __init__(self, name):
		self.name = name

	def launch(self):
		'''Start activity with the given class name'''
		_a.launch(self.name)

	def consts(self):
		'''Get list of constants (static final fields) for a class'''
		return _a.getConstants(self.name)

	@classmethod
	def launchable(cls):
		'''Returns a dict of all launchable application class names'''
		return _a.getLaunchableApplications()


class Preference(_Facade):
	'''Wrapper functions for PreferencesFacade
	(http://www.mithril.com.au/android/doc/PreferencesFacade.html)'''

	def __init__(self, file = None):
		self.file = file

	def all(self):
		'''Get list of Shared Preference Values'''
		return _a.prefGetAll(self.file)

	def get(self, key):
		'''Read a value from shared preferences'''
		return _a.prefGetValue(key, self.file)

	def put(self, key, value):
		'''Write a value to shared preferences'''
		return _a.prefPutValue(key, value, self.file)


class Wifi(_Facade):
	'''Wrapper functions for WifiFacade
	(http://www.mithril.com.au/android/doc/WifiFacade.html)'''

	@classmethod
	def state(cls, enabled = None):
		'''Toggle Wifi on and off'''
		if enabled is None:
			return _a.checkWifiState()
		else:
			return _a.toggleWifiState(enabled)

	@classmethod
	def acquire(cls, full = False):
		'''Acquires a full Wifi lock'''
		if full:
			_a.wifiLockAcquireFull()
		else:
			_a.wifiLockAcquireScanOnly()

	@classmethod
	def release(cls):
		'''Releases a previously acquired Wifi lock'''
		_a.wifiLockRelease()

	@classmethod
	def scan(cls):
		'''Starts a scan for Wifi access points'''
		return _a.wifiStartScan()

	@classmethod
	def result(cls):
		'''Returns the list of access points found during the most recent Wifi scan'''
		return _a.wifiGetScanResults()

	@classmethod
	def connect(cls):
		'''Reconnects to the currently active access point'''
		return _a.wifiReconnect()

	@classmethod
	def associate(cls):
		'''Reassociates with the currently active access point'''
		return _a.wifiReassociate()

	@classmethod
	def info(cls):
		'''Returns information about the currently active access point'''
		return _a.wifiGetConnectionInfo()

	@classmethod
	def close(cls):
		'''Disconnects from the currently active access point'''
		return _a.wifiDisconnect()


class Bluetooth(_Facade):
	'''Wrapper functions for BluetoothFacade
	(http://www.mithril.com.au/android/doc/BluetoothFacade.html)'''

	SCAN_MODE = (
		'non discoverable, non connectable',
		'connectable, non discoverable',
		'invaild scan mode',
		'connectable, discoverable',
		'Bluetooth is disabled',
	)

	def __init__(self, conn = ''):
		self.conn = conn

	def connect(self, address = None, uuid = BLUETOOTH_UUID):
		'''Connect to a device over Bluetooth. Blocks until the connection is established or fails
		uuid (String) The UUID passed here must match the UUID used by the server device.'''
		try: self.conn = _a.bluetoothConnect(uuid, address)
		except sl4aError: return None
		return self.conn

	def accept(self, timeout = 30000, uuid = BLUETOOTH_UUID):
		'''Listens for and accepts a Bluetooth connection. Blocks until the connection is established or fails
		uuid (String) (default=457807c0-4897-11df-9879-0800200c9a66)
		timeout (Integer) How long to wait for a new connection, in millseconds'''
		try: _a.bluetoothAccept(uuid, timeout)
		except sl4aError: return None
		for conn, address in self.connections().items():
			if self.remote(address) == self.name():
				self.conn = conn
				break
		return self.conn

	def read(self, buffer = 4096):
		'''Read up to bufferSize ASCII characters'''
		try: return _a.bluetoothRead(buffer, self.conn)
		except sl4aError: return None

	def readbin(self, buffer = 4096):
		'''Read up to bufferSize Binary bytes'''
		try: return b64decode(_a.bluetoothReadBinary(buffer, self.conn))
		except sl4aError: return None

	def readline(self):
		'''Read the next line'''
		try: return _a.bluetoothReadLine(self.conn)
		except sl4aError: return None

	def ready(self):
		'''Returns True if the next read is guaranteed not to block'''
		return _a.bluetoothReadReady(self.conn)

	def write(self, data):
		'''Sends ASCII characters over the currently open Bluetooth connection'''
		return _a.bluetoothWrite(data, self.conn)

	def writebin(self, data):
		'''Send bytes over the currently open Bluetooth connection'''
		return _a.bluetoothWriteBinary(b64encode(data), self.conn)

	def stop(self):
		'''Stops Bluetooth connection'''
		_a.bluetoothStop(self.conn)
		self.conn = ''

	def name(self):
		'''Returns the name of the connected device'''
		return _a.bluetoothGetConnectedDeviceName(self.conn)

	@classmethod
	def address(cls):
		'''Returns the hardware address of the local Bluetooth adapter'''
		return _a.bluetoothGetLocalAddress()

	@classmethod
	def remote(cls, address):
		'''Queries a remote device for it's name or null if it can't be resolved'''
		return _a.bluetoothGetRemoteDeviceName(address)

	@classmethod
	def local(cls, name = None):
		'''Gets or Sets the Bluetooth Visible device name
		name (String) New local name'''
		if name is None:
			return _a.bluetoothGetLocalName()
		else:
			_a.bluetoothSetLocalName(name)

	@classmethod
	def connections(cls):
		'''Returns active Bluetooth connections'''
		return _a.bluetoothActiveConnections()

	@classmethod
	def scanMode(cls):
		'''Gets the scan mode for the local dongle'''
		return cls.SCAN_MODE[_a.bluetoothGetScanMode()]

	@classmethod
	def state(cls, enabled = None, prompt = True):
		'''Toggle Bluetooth on and off
		prompt (Boolean) Prompt the user to confirm changing the Bluetooth state'''
		if enabled is None:
			return _a.checkBluetoothState()
		else:
			return _a.toggleBluetoothState(enabled, prompt)

	@classmethod
	def discover(cls, duration = None):
		'''Requests that the device be discoverable for Bluetooth connections
		duration (Integer) period of time, in seconds, during which the device should be discoverable'''
		if duration is None:
			return _a.bluetoothIsDiscovering()
		else:
			_a.bluetoothMakeDiscoverable(duration)

	@classmethod
	def start(cls):
		'''Start the remote device discovery process'''
		return _a.bluetoothDiscoveryStart()

	@classmethod
	def cancel(cls):
		'''Cancel the current device discovery process'''
		return _a.bluetoothDiscoveryCancel()


class Camera(_Facade):
	'''Wrapper functions for CameraFacade
	(http://www.mithril.com.au/android/doc/CameraFacade.html)'''

	@classmethod
	def capture(cls, path, autoFocus = True):
		'''Take a picture and save it to the specified path
		path (String)
		autoFocus (Boolean) (default=true)
		returns: (Bundle) A map of Booleans autoFocus and takePicture where True indicates success.'''
		return _a.cameraCapturePicture(path, autoFocus)

	@classmethod
	def interactive(cls, path):
		'''Starts the image capture application to take a picture and saves it to the specified path
		targetPath (String)'''
		return _a.cameraInteractiveCapturePicture(path)


class Player(_Facade):
	'''Wrapper functions for MediaPlayerFacade
	(http://www.mithril.com.au/android/doc/MediaPlayerFacade.html)'''

	@classmethod
	def playing(cls, tag = 'default'):
		'''Checks if media file is playing
		tag (String) string identifying resource (default=default)
		returns: (boolean) true if playing'''
		return _a.mediaIsPlaying(tag)

	@classmethod
	def play(cls, url, tag = 'default', start = True):
		'''Open a media file
		url (String) url of media resource
		tag (String) string identifying resource (default=default)
		start (Boolean) start playing immediately (default=true)
		returns: (boolean) true if play successful'''
		return _a.mediaPlay(url, tag, start)

	@classmethod
	def start(cls, tag = 'default'):
		'''start playing media file
		tag (String) string identifying resource (default=default)
		returns: (boolean) true if successful'''
		return _a.mediaPlayStart(tag)

	@classmethod
	def pause(cls, tag = 'default'):
		'''pause playing media file
		tag (String) string identifying resource (default=default)
		returns: (boolean) true if successful'''
		return _a.mediaPlayPause(tag)

	@classmethod
	def seek(cls, msec, tag = 'default'):
		'''Seek To Position
		msec (Integer) Position in millseconds
		tag (String) string identifying resource (default=default)
		returns: (int) New Position (in ms)'''
		return _a.mediaPlaySeek(msec, tag)

	@classmethod
	def close(cls, tag = 'default'):
		'''Close media file
		tag (String) string identifying resource (default=default)
		returns: (boolean) true if successful'''
		return _a.mediaPlayClose(tag)

	@classmethod
	def info(cls, tag = 'default'):
		'''Information on current media
		tag (String) string identifying resource (default=default)
		returns: (Map) Media Information'''
		return _a.mediaPlayInfo(tag)

	@classmethod
	def loop(cls, enabled = True, tag = 'default'):
		'''Set Looping
		enabled (Boolean) (default=true)
		tag (String) string identifying resource (default=default)
		returns: (boolean) True if successful'''
		return _a.mediaPlaySetLooping(enabled, tag)

	@classmethod
	def list(cls, tag = 'default'):
		'''Lists currently loaded media
		returns: (Set) List of Media Tags'''
		return _a.mediaPlayList()

	@classmethod
	def volume(cls, volume = None):
		'''Gets or Sets the media volume'''
		if volume is None:
			return _a.getMediaVolume()
		else:
			_a.setMediaVolume(volume)

	@classmethod
	def maxVolume(cls):
		'''Returns the maximum media volume'''
		return _a.getMaxMediaVolume()


class Recorder(_Facade):
	'''Wrapper functions for MediaRecorderFacade
	(http://www.mithril.com.au/android/doc/MediaRecorderFacade.html)'''

	@classmethod
	def video(cls, path, duration = 0, size = 1):
		'''Records video from the camera and saves it to the given location
		Duration specifies the maximum duration of the recording session
		If duration is 0 this method will return and the recording will only be stopped
		when recorderStop is called or when a scripts exits
		Otherwise it will block for the time period equal to the duration argument
		size: 0=160x120, 1=320x240, 2=352x288, 3=640x480, 4=800x480
		path (String)
		duration (Integer) (default=0)
		size (Integer) (default=1)'''
		return _a.recorderStartVideo(path, duration, size)

	@classmethod
	def audio(cls, path):
		'''Records audio from the microphone and saves it to the given location
		path (String)'''
		return _a.recorderStartMicrophone(path)

	@classmethod
	def capture(cls, path, audio = True):
		'''Records video (and optionally audio) from the camera and saves it to the given location
		Duration specifies the maximum duration of the recording session
		If duration is not provided this method will return immediately and the recording will only be stopped
		when recorderStop is called or when a scripts exits
		Otherwise it will block for the time period equal to the duration argument
		path (String)
		audio (Boolean) (default=true)'''
		return _a.recorderCaptureVideo(path, audio)

	@classmethod
	def stop(cls):
		'''Stops a previously started recording'''
		return _a.recorderStop()

	@classmethod
	def interactive(cls, path):
		'''Starts the video capture application to record a video and saves it to the specified path
		path (String)'''
		return _a.startInteractiveVideoRecording(path)


class WakeLock(_Facade):
	'''Wrapper functions for WakeLockFacade
	(http://www.mithril.com.au/android/doc/WakeLockFacade.html)'''

	@classmethod
	def bright(cls):
		'''Acquires a bright wake lock (CPU on, screen bright)'''
		_a.wakeLockAcquireBright()

	@classmethod
	def dim(cls):
		'''Acquires a dim wake lock (CPU on, screen dim)'''
		_a.wakeLockAcquireDim()

	@classmethod
	def full(cls):
		'''Acquires a full wake lock (CPU on, screen bright, keyboard bright)'''
		_a.wakeLockAcquireFull()

	@classmethod
	def partial(cls):
		'''Acquires a partial wake lock (CPU on)'''
		_a.wakeLockAcquirePartial()

	@classmethod
	def release(cls):
		'''Releases the wake lock'''
		_a.wakeLockRelease()


class Misc(_Facade):
	'''Wrapper functions for Misc Facade
	(SpeechRecognitionFacade, TextToSpeechFacade, ToneGeneratorFacade, AndroidFacade)'''

	@classmethod
	def env(cls):
		'''A map of various useful environment details'''
		return _a.environment()

	@classmethod
	def clipboard(cls, text = None):
		'''Read/Put text from/to the clipboard'''
		if text is None:
			return _a.getClipboard()
		else:
			return _a.setClipboard(text)

	@classmethod
	def email(cls, to, subject, body, attach = None):
		'''Launches an activity that sends an e-mail message to a given recipient'''
		_a.sendEmail(to, subject, body, attach)

	@classmethod
	def log(cls, msg):
		'''Writes message to logcat'''
		return _a.log(msg)

	@classmethod
	def barcode(cls):
		'''Starts the barcode scanner'''
		return _a.scanBarcode()

	@classmethod
	def recognize(cls, prompt = None):
		'''Recognizes user's speech and returns the most likely result'''
		return _a.recognizeSpeech(prompt)

	@classmethod
	def tts(cls, msg = None):
		'''Speaks the provided message via TTS'''
		if msg is None:
			return _a.ttsIsSpeaking()
		else:
			return _a.ttsSpeak(msg)

	@classmethod
	def dtmf(cls, number, duration):
		'''Generate DTMF tones for the given phone number
		number (String)
		duration (Integer) duration of each tone in milliseconds (default=100)'''
		return _a.generateDtmfTones(number, duration)


if __name__ == '__main__':
	import time

	def bluetooth(server = False):
		import DroidDialog as D
		b = Bluetooth()
		if not b.state(True): return
		try:
			print('local:', b.local())
			if server:
				b.discover(120)
				c = b.accept()
			else:
				c = b.connect()
			if not c: return
			print('connection:', b.name(), c)
			if server:
				msg = D.askstring('Chat', 'Enter a message')
				if not msg:
					return
				b.writebin(msg.encode('gb18030'))
			while True:
				msg = b.readbin()
				if not msg:
					break
				say = D.askstring('Chat', 'message: ' + msg.decode('gb18030'))
				if not say:
					break
				b.writebin(say.encode('gb18030'))
		finally:
			b.stop()
			#b.state(False, False)

	def tests(cls, methods):
		o = cls()
		print(cls.__name__)
		time.sleep(0.5)
		for m in methods:
			r = getattr(o, m)()
			print('%s:' % m, r)
		print()
		del o
	tests(Sensing, ['read', 'accuracy', 'light', 'accelerometer', 'magnetometer', 'orientation'])
	tests(Location, ['read', 'providers', 'last'])
	tests(Battery, ['read', 'present', 'health', 'level', 'plugType', 'status', 'technology', 'temperature', 'voltage'])
	tests(Signal, ['read'])
	tests(Phone, ['roaming', 'cellLocation', 'id', 'version', 'number', 'neighboring', 'operator', 'operatorName', 'network', 'type', 'subscriber', 'voiceMailNumber', 'voiceMailAlphaTag', 'volume', 'maxVolume', 'airplane', 'silent', 'vibrate', 'brightness', 'screen',])
	tests(PhoneState, ['read'])
	tests(Sim, ['country', 'operator', 'operatorName', 'serial', 'state'])
	tests(Contact, ['attrs', 'count', 'ids'])
	tests(Sms, ['attrs', 'count', 'ids'])
	tests(Player, ['loop', 'playing', 'start', 'pause', 'close', 'info', 'list', 'volume', 'maxVolume'])
	tests(Preference, ['all'])
	tests(Bluetooth, ['address', 'local', 'scanMode', 'state', 'discover', 'connections'])
	tests(Wifi, ['state', 'acquire', 'scan', 'connect', 'associate', 'result', 'release', 'info', 'close'])
	tests(WakeLock, ['bright', 'dim', 'full', 'partial', 'release'])
	tests(Misc, ['env', 'clipboard', 'barcode', 'tts'])
	bluetooth()

