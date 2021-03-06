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

'''dialog wrapper function for UiFacade
'''

import datetime
import warnings
from .sl4a import sl4a
from .DroidConstants import TEXT, TEXT_PASSWORD, NUMBER_SIGNED, NUMBER_DECIMAL
from .DroidConstants import stringlize, isstring


# you can change them for custom Button text
YES = 'Yes'
NO = 'No'
OK = 'OK'
CANCEL = 'Cancel'


class _Dialog(object):
	'''basic dialog for android'''
	DialogType = {
		'alert': 'dialogCreateAlert',
		'date': 'dialogCreateDatePicker',
		'progress': 'dialogCreateHorizontalProgress',
		'input': 'dialogCreateInput',
		'password': 'dialogCreatePassword',
		'seekbar': 'dialogCreateSeekBar',
		'spinner': 'dialogCreateSpinnerProgress',
		'time': 'dialogCreateTimePicker',
	}

	def __init__(self):
		if not hasattr(_Dialog, '_a'):
			setattr(_Dialog, '_a', sl4a())
		self.result = None

	def call(self, func, *args):
		'''wrapper for sl4a.sl4a'''
		return getattr(self._a, func)(*args)

	def create(self, type, *args):
		'''create dialog, for TYPE, see DialogType'''
		self.call(self.DialogType[type], *args)

	def buttons(self, yes = YES, no = NO, cancel = None):
		'''set button text'''
		if yes: self.call('dialogSetPositiveButtonText', stringlize(yes))
		if no: self.call('dialogSetNegativeButtonText', stringlize(no))
		if cancel: self.call('dialogSetNeutralButtonText', stringlize(cancel))

	def list(self, items, multi = False):
		'''set list items for dialog'''
		if multi: self.call('dialogSetMultiChoiceItems', items)
		else: self.call('dialogSetSingleChoiceItems', items)

	def update(self, value):
		'''update progress'''
		self.call('dialogSetCurrentProgress', value)

	def show(self):
		'''show dialog'''
		self.call('dialogShow')

	def response(self):
		'''get dialog response'''
		return self.call('dialogGetResponse')

	def selected(self):
		'''get select items'''
		return self.call('dialogGetSelectedItems')

	def dismiss(self):
		'''dismiss dialog'''
		self.call('dialogDismiss')

	def yes(self, data):
		'''Positive button click callback function'''
		self.result = data

	def no(self, data):
		'''Negative button click callback function'''
		pass

	def cancel(self, data):
		'''Neutral button click callback function'''
		pass

	def back(self, data):
		'''BACK key click callback function'''
		self.cancel(data)

	def handle(self):
		'''handle dialog event'''
		_Handler = {
			'positive': self.yes,
			'neutral': self.cancel,
			'negative': self.no,
		}
		data = self.response()
		if 'which' in data:
			_Handler[data['which']](data)
		elif 'canceled' in data:
			self.back(data)
		else:
			warnings.warn('Unknown response: %s' % data)

	def main(self):
		self.handle()
		self.dismiss()

def _merge(d, **kw):
	# set default value for dict
	for k, v in kw.items():
		d.setdefault(k, v)

###############################################################
# input dialog

def _askstring(title, message, default, type, **kw):
	d = _Dialog()
	d.create('input', title, message, stringlize(default), type)
	_merge(kw, yes = OK, no = CANCEL)
	d.buttons(**kw)
	d.show()
	d.main()
	return d.result['value'] if d.result else None

def askstring(title, message, default = '', **kw):
	'''show a dialog to ask for string input.
	TITLE - the title of the dialog
	MESSAGE - the message of the dialog
	DEFAULT - default value of the string (empty string by default)
	KW - the keyword argument, used to set the button text on the dialog
	  `yes' - set the YES button text ("Yes" if not set)
	  `no' - set the NO button text ("Cancel" if not set)'''
	return _askstring(title, message, default, TEXT, **kw)

def askpassword(title, message, default = '', **kw):
	'''show a dialog to ask for password input.
	TITLE - the title of the dialog
	MESSAGE - the message of the dialog
	DEFAULT - default value of the password (empty string by default)
	KW - same as KW in askstring()'''
	return _askstring(title, message, default, TEXT_PASSWORD, **kw)

def askint(title, message, default = 0, **kw):
	'''show a dialog to ask for int input.
	TITLE - the title of the dialog
	MESSAGE - the message of the dialog
	DEFAULT - default value of the int (0 by default)
	KW - same as KW in askstring()'''
	ret = _askstring(title, message, default, NUMBER_SIGNED, **kw)
	return None if ret is None else int(ret)

def askfloat(title, message, default = 0.0, **kw):
	'''show a dialog to ask for float input.
	TITLE - the title of the dialog
	MESSAGE - the message of the dialog
	DEFAULT - default value of the float (0.0 by default)
	KW - same as KW in askstring()'''
	ret = _askstring(title, message, default, NUMBER_DECIMAL, **kw)
	return None if ret is None else float(ret)

###############################################################
# seekbar

def askvalue(title, message, value = 50, max = 100, **kw):
	'''get a value using seekbar
	TITLE - the title of the dialog
	MESSAGE - the message of the dialog
	VALUE - default value (50 by default)
	MAX - max value (100 by default)
	KW - same as KW in askstring()'''
	d = _Dialog()
	d.create('seekbar', value, max, title, message)
	_merge(kw, yes = OK, no = CANCEL)
	d.buttons(**kw)
	d.show()
	d.main()
	return d.result['progress'] if d.result else None

###############################################################
# date dialog

def askdate(date = None):
	'''get a date, if DATE is None, using today as default'''
	if date is None: date = datetime.date.today()
	d = _Dialog()
	d.create('date', date.year, date.month, date.day)
	d.show()
	d.main()
	r = d.result
	if r: r = datetime.date(r['year'], r['month'], r['day'])
	return r

###############################################################
# time dialog

def asktime(time = None):
	'''get a time, if TIME is None, using now as default
	NOTE: only hour and minute is supported'''
	if time is None: time = datetime.datetime.now().time()
	d = _Dialog()
	d.create('time', time.hour, time.minute, True)
	d.show()
	d.main()
	r = d.result
	if r: r = datetime.time(r['hour'], r['minute'])
	return r

###############################################################
# list items

def _choose(title, items, multi, **kw):
	d = _Dialog()
	d.create('alert', title)
	d.list(items, multi)
	_merge(kw, yes = OK, no = CANCEL)
	d.buttons(**kw)
	d.show()
	d.handle()
	if d.result is None: return None
	r = d.selected()
	if multi: return tuple([ items[i] for i in r ])
	else: return items[r[0]]

def select(title, items, **kw):
	'''select one item from ITEMS
	RETURN: the selected item, or None if cancelled'''
	return _choose(title, items, False, **kw)

def choose(title, items, **kw):
	'''choose one or more items from ITEMS
	RETURN: a tuple of chosen items, or None if cancelled'''
	return _choose(title, items, True, **kw)

def pick(title, items):
	'''choose one items from ITEMS
	RETURN:  the selected item, or None if cancelled'''
	d = _Dialog()
	d.create('alert', title)
	d.call('dialogSetItems', items)
	d.show()
	r = d.response()
	return 'item' in r and items[r['item']] or None

###############################################################
# alert dialog

class _Alert(_Dialog):

	def __init__(self, title, message, yes, no, cancel = None):
		_Dialog.__init__(self)
		self.create('alert', title, message)
		self.buttons(yes, no, cancel)
		self.show()

	def yes(self, data):
		self.result = True

	def no(self, data):
		self.result = False

def message(title, message, text = OK):
	'''show a message'''
	_Alert(title, message, text, None).main()

def askyesno(title, message, **kw):
	'''ask yes or no
	RETURN: True on Yes, False on No, or None if cancelled'''
	_merge(kw, yes = YES, no = NO)
	d = _Alert(title, message, kw['yes'], kw['no'])
	d.main()
	return d.result

def askyesnocancel(title, message, **kw):
	'''ask yes or no or cancel
	RETURN: True on Yes, False on No, or None if cancelled'''
	_merge(kw, yes = YES, no = NO, cancel = CANCEL)
	d = _Alert(title, message, kw['yes'], kw['no'], kw['cancel'])
	d.main()
	return d.result

def info(what):
	'''show information INFO to user'''
	_Dialog().call('makeToast', what)
toast = info

def notify(title, message):
	'''Displays a notification'''
	_Dialog().call('notify', title, message)

###############################################################
# the final dialog api

# button meta data holder
class _btnMeta(object):
	def __init__(self, meta, text, ret):
		self.text = text
		self.ret = ret
		self.callback = None
		if meta is not None:
			self._set(meta)

	def _set(self, meta):
		if isstring(meta):
			self.text = stringlize(meta)
			self.ret = meta
		elif callable(meta):
			self.callback = meta
		elif isinstance(meta, list):
			self.text = stringlize(meta[0])
			if callable(meta[1]):
				self.callback = meta[1]
				self.ret = meta[0]
			else:
				self.ret = meta[1]
		else:
			self.ret = meta

class _Dialog2(_Dialog):
	def __init__(self, title, message, **kw):
		_Dialog.__init__(self)
		self._yes = _btnMeta(kw['yes'], YES, True)
		self._no = _btnMeta(kw['no'], NO, False)
		self._cancel = _btnMeta(kw['cancel'], CANCEL, None)
		self.create('alert', title, message)
		self.buttons(self._yes.text, self._no.text, self._cancel.text)
		self.show()

	def handler(self, meta, data):
		self.result = meta.ret
		if meta.callback:
			meta.callback(data)

	def yes(self, data):
		self.handler(self._yes, data)

	def no(self, data):
		self.handler(self._no, data)

	def cancel(self, data):
		self.handler(self._cancel, data)

	def back(self):
		pass

def dialog(title, message, **kw):
	'''The final dialog API
	TITLE: dialog title
	MESSAGE: dialog body message
	you can set `yes', `no' and `cancel' button behaviour with keyword param
	value for the keyword can be
	1. a string, will be the button text and the result of the dialog
	2. a callable object, will be called if the button clicked
	3. a list with to two element.
	  a. the first element will be the button text.
	  b. the second will be called if callable, or the result of the dialog
	4. all other situation, the value will be the result of the dialog
	'''
	_merge(kw, yes = None, no = None, cancel = None)
	d = _Dialog2(title, message, **kw)
	d.main()
	return d.result

###############################################################
# progress dialog

class _Progress(object):
	def __init__(self, title, message, max, type):
		self.d = _Dialog()
		self.d.create(type, title, message, max)
	def show(self):
		self.d.show()
	def update(self, value):
		self.d.update(value)
	def dismiss(self):
		self.d.dismiss()

def Progress(title, message, max = 100):
	'''get a Horizontal Progress dialog
	TITLE - the title of the dialog
	MESSAGE - the message of the dialog
	MAX - max value (100 by default)

	the dialog object support these methods
	show() - show the dialog
	update(value) - set the progress of the dialog to value
	dismiss() - dismiss the dialog'''
	return _Progress(title, message, max, 'progress')

def Loading(title, message, max = 100):
	'''get a Spinner Progress dialog
	TITLE - the title of the dialog
	MESSAGE - the message of the dialog
	MAX - max value (100 by default)

	the dialog object support these methods
	show() - show the dialog
	update(value) - set the progress of the dialog to value
	dismiss() - dismiss the dialog'''
	return _Progress(title, message, max, 'spinner')

###############################################################
# test

if __name__ == '__main__':
	# a sample use of Progress dialog
	import time
	p = Progress('DroidDialog', 'Sample usage of Progress Bar', 300)
	p.show()
	for i in range(30):
		time.sleep(0.1)
		p.update(i * 10)
	p.dismiss()

