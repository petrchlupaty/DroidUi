# Copyright 2012-2013 by Tommy Alex. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Symbolic constants for DroidUi

#########
# DroidUi

def joinattr(*attrs):
	'''join many attribute together'''
	return '|'.join(attrs)

# boolean
TRUE = 'true'
FALSE = 'false'

# layout_width and layout_height
WRAP_CONTENT = 'wrap_content'
MATCH_PARENT = 'match_parent'
FILL_PARENT = 'fill_parent'

# gravity and layout_gravity
TOP = 'top'
BOTTOM = 'bottom'
LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'
FILL = 'FILL'
CENTER_VERTICAL = 'center_vertical'
CENTER_HORIZONTAL = 'center_horizontal'
FILL_VERTICAL = 'fill_vertical'
FILL_HORIZONTAL = 'fill_horizontal'
CLIP_VERTICAL = 'clip_vertical'
CLIP_HORIZONTAL = 'clip_horizontal'

# misc
NONE = 'none'
HORIZONTAL = 'horizontal'
VERTICAL = 'vertical'

# visibility
VISIBLE = 'visible'
INVISIBLE = 'invisible'
GONE = 'gone'

# scrollbarStyle
INSIDE_OVERLAY = 'insideOverlay'
INSIDE_INSET = 'insideInset'
OUTSIDE_OVERLAY = 'outsideOverlay'
OUTSIDE_INSET = 'outsideInset'

# textStyle
NORMAL = 'normal'
BOLD = 'bold'
ITALIC = 'italic'

# typeface
SANS = 'sans'
SERIF = 'serif'
MONOSPACE = 'monospace'

# inputType
TEXT = 'text'
DATE = 'date'
TIME = 'time'
DATETIME = 'datetime'
PHONE = 'phone'
NUMBER = 'number'
NUMBER_SIGNED = 'numberSigned'
NUMBER_DECIMAL = 'numberDecimal'
TEXT_CAP_CHARACTERS = 'textCapCharacters'
TEXT_CAP_WORDS = 'textCapWords'
TEXT_CAP_SENTENCES = 'textCapSentences'
TEXT_AUTO_CORRECT = 'textAutoCorrect'
TEXT_AUTO_COMPLETE = 'textAutoComplete'
TEXT_MULTI_LINE = 'textMultiLine'
TEXT_IME_MULTI_LINE = 'textImeMultiLine'
TEXT_NO_SUGGESTIONS = 'textNoSuggestions'
TEXT_URI = 'textUri'
TEXT_EMAIL_ADDRESS = 'textEmailAddress'
TEXT_EMAIL_SUBJECT = 'textEmailSubject'
TEXT_SHORT_MESSAGE = 'textShortMessage'
TEXT_LONG_MESSAGE = 'textLongMessage'
TEXT_PERSON_NAME = 'textPersonName'
TEXT_POSTAL_ADDRESS = 'textPostalAddress'
TEXT_PASSWORD = 'textPassword'
TEXT_VISIBLE_PASSWORD = 'textVisiblePassword'
TEXT_WEB_EDIT_TEXT = 'textWebEditText'
TEXT_FILTER = 'textFilter'
TEXT_PHONETIC = 'textPhonetic'

#############
# DroidFacade

# SmsFacade
INBOX = 'inbox'

# Bluetooth
BLUETOOTH_UUID = '457807c0-4897-11df-9879-0800200c9a66'

# sensorNumber
SENSOR_ALL = 1
ORIENTATION = 1
ACCELEROMETER = 2
MAGNETOMETER = 3
LIGHT = 4

# axis parm
NO_AXIS = 0
X = 1
Y = 2
XY = 3
Z = 4
XZ = 5
YZ = 6
XYZ = 7

#####

# key
KEY_UNKNOWN = 0
KEY_SOFT_LEFT = 1
KEY_SOFT_RIGHT = 2
HOME = KEY_HOME = 3
BACK = KEY_BACK = 4
KEY_CALL = 5
KEY_ENDCALL = 6
KEY_0 = 7
KEY_1 = 8
KEY_2 = 9
KEY_3 = 10
KEY_4 = 11
KEY_5 = 12
KEY_6 = 13
KEY_7 = 14
KEY_8 = 15
KEY_9 = 16
KEY_STAR = 17
KEY_POUND = 18
KEY_DPAD_UP = 19
KEY_DPAD_DOWN = 20
KEY_DPAD_LEFT = 21
KEY_DPAD_RIGHT = 22
KEY_DPAD_CENTER = 23
VOLUME_UP = KEY_VOLUME_UP = 24
VOLUME_DOWN = KEY_VOLUME_DOWN = 25
KEY_POWER = 26
KEY_CAMERA = 27
KEY_CLEAR = 28
KEY_A = 29
KEY_B = 30
KEY_C = 31
KEY_D = 32
KEY_E = 33
KEY_F = 34
KEY_G = 35
KEY_H = 36
KEY_I = 37
KEY_J = 38
KEY_K = 39
KEY_L = 40
KEY_M = 41
KEY_N = 42
KEY_O = 43
KEY_P = 44
KEY_Q = 45
KEY_R = 46
KEY_S = 47
KEY_T = 48
KEY_U = 49
KEY_V = 50
KEY_W = 51
KEY_X = 52
KEY_Y = 53
KEY_Z = 54
KEY_COMMA = 55
KEY_PERIOD = 56
KEY_ALT_LEFT = 57
KEY_ALT_RIGHT = 58
KEY_SHIFT_LEFT = 59
KEY_SHIFT_RIGHT = 60
KEY_TAB = 61
KEY_SPACE = 62
KEY_SYM = 63
KEY_EXPLORER = 64
KEY_ENVELOPE = 65
KEY_ENTER = 66
KEY_DEL = 67
KEY_GRAVE = 68
KEY_MINUS = 69
KEY_EQUALS = 70
KEY_LEFT_BRACKET = 71
KEY_RIGHT_BRACKET = 72
KEY_BACKSLASH = 73
KEY_SEMICOLON = 74
KEY_APOSTROPHE = 75
KEY_SLASH = 76
KEY_AT = 77
KEY_NUM = 78
KEY_HEADSETHOOK = 79
KEY_FOCUS = 80
KEY_PLUS = 81
MENU = KEY_MENU = 82
KEY_NOTIFICATION = 83
SEARCH = KEY_SEARCH = 84
KEY_MEDIA_PLAY_PAUSE = 85
KEY_MEDIA_STOP = 86
KEY_MEDIA_NEXT = 87
KEY_MEDIA_PREVIOUS = 88
KEY_MEDIA_REWIND = 89
KEY_MEDIA_FAST_FORWARD = 90
KEY_MUTE = 91
KEY_PAGE_UP = 92
KEY_PAGE_DOWN = 93
KEY_PICTSYMBOLS = 94
KEY_SWITCH_CHARSET = 95
KEY_BUTTON_A = 96
KEY_BUTTON_B = 97
KEY_BUTTON_C = 98
KEY_BUTTON_X = 99
KEY_BUTTON_Y = 100
KEY_BUTTON_Z = 101
KEY_BUTTON_L1 = 102
KEY_BUTTON_R1 = 103
KEY_BUTTON_L2 = 104
KEY_BUTTON_R2 = 105
KEY_BUTTON_THUMBL = 106
KEY_BUTTON_THUMBR = 107
KEY_BUTTON_START = 108
KEY_BUTTON_SELECT = 109
KEY_BUTTON_MODE = 110
KEY_ESCAPE = 111
KEY_FORWARD_DEL = 112
KEY_CTRL_LEFT = 113
KEY_CTRL_RIGHT = 114
KEY_CAPS_LOCK = 115
KEY_SCROLL_LOCK = 116
KEY_META_LEFT = 117
KEY_META_RIGHT = 118
KEY_FUNCTION = 119
KEY_SYSRQ = 120
KEY_BREAK = 121
KEY_MOVE_HOME = 122
KEY_MOVE_END = 123
KEY_INSERT = 124
KEY_FORWARD = 125
KEY_MEDIA_PLAY = 126
KEY_MEDIA_PAUSE = 127
KEY_MEDIA_CLOSE = 128
KEY_MEDIA_EJECT = 129
KEY_MEDIA_RECORD = 130
KEY_F1 = 131
KEY_F2 = 132
KEY_F3 = 133
KEY_F4 = 134
KEY_F5 = 135
KEY_F6 = 136
KEY_F7 = 137
KEY_F8 = 138
KEY_F9 = 139
KEY_F10 = 140
KEY_F11 = 141
KEY_F12 = 142
KEY_NUM_LOCK = 143
KEY_NUMPAD_0 = 144
KEY_NUMPAD_1 = 145
KEY_NUMPAD_2 = 146
KEY_NUMPAD_3 = 147
KEY_NUMPAD_4 = 148
KEY_NUMPAD_5 = 149
KEY_NUMPAD_6 = 150
KEY_NUMPAD_7 = 151
KEY_NUMPAD_8 = 152
KEY_NUMPAD_9 = 153
KEY_NUMPAD_DIVIDE = 154
KEY_NUMPAD_MULTIPLY = 155
KEY_NUMPAD_SUBTRACT = 156
KEY_NUMPAD_ADD = 157
KEY_NUMPAD_DOT = 158
KEY_NUMPAD_COMMA = 159
KEY_NUMPAD_ENTER = 160
KEY_NUMPAD_EQUALS = 161
KEY_NUMPAD_LEFT_PAREN = 162
KEY_NUMPAD_RIGHT_PAREN = 163
KEY_VOLUME_MUTE = 164
KEY_INFO = 165
KEY_CHANNEL_UP = 166
KEY_CHANNEL_DOWN = 167
KEY_ZOOM_IN = 168
KEY_ZOOM_OUT = 169
KEY_TV = 170
KEY_WINDOW = 171
KEY_GUIDE = 172
KEY_DVR = 173
KEY_BOOKMARK = 174
KEY_CAPTIONS = 175
KEY_SETTINGS = 176
KEY_TV_POWER = 177
KEY_TV_INPUT = 178
KEY_STB_POWER = 179
KEY_STB_INPUT = 180
KEY_AVR_POWER = 181
KEY_AVR_INPUT = 182
KEY_PROG_RED = 183
KEY_PROG_GREEN = 184
KEY_PROG_YELLOW = 185
KEY_PROG_BLUE = 186
KEY_APP_SWITCH = 187
KEY_BUTTON_1 = 188
KEY_BUTTON_2 = 189
KEY_BUTTON_3 = 190
KEY_BUTTON_4 = 191
KEY_BUTTON_5 = 192
KEY_BUTTON_6 = 193
KEY_BUTTON_7 = 194
KEY_BUTTON_8 = 195
KEY_BUTTON_9 = 196
KEY_BUTTON_10 = 197
KEY_BUTTON_11 = 198
KEY_BUTTON_12 = 199
KEY_BUTTON_13 = 200
KEY_BUTTON_14 = 201
KEY_BUTTON_15 = 202
KEY_BUTTON_16 = 203
KEY_LANGUAGE_SWITCH = 204
KEY_MANNER_MODE = 205
KEY_3D_MODE = 206
KEY_CONTACTS = 207
KEY_CALENDAR = 208
KEY_MUSIC = 209
KEY_CALCULATOR = 210
KEY_ZENKAKU_HANKAKU = 211
KEY_EISU = 212
KEY_MUHENKAN = 213
KEY_HENKAN = 214
KEY_KATAKANA_HIRAGANA = 215
KEY_YEN = 216
KEY_RO = 217
KEY_KANA = 218
KEY_ASSIST = 219
