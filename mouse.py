import ctypes
import time
from ctypes import wintypes
import random

global MOUSEEVENTF_ABSOLUTE
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_ABSOLUTE_info = """
The dx and dy members contain normalized absolute coordinates. 
If the flag is not set, dxand dy contain relative data 
(the change in position since the last reported position). 
This flag can be set, or not set, regardless of what kind of
 mouse or other pointing device, if any, is connected to the system. 
 For further information about relative mouse motion, 
 see the following Remarks section.
"""

global MOUSEEVENTF_HWHEEL
MOUSEEVENTF_HWHEEL=0x01000
#The wheel was moved horizontally, if the mouse has a wheel. The amount of movement is specified in mouseData.
global MOUSEEVENTF_MOVE
MOUSEEVENTF_MOVE = 0x0001
#Movement occurred.
global MOUSEEVENTF_MOVE_NOCOALESCE
MOUSEEVENTF_MOVE_NOCOALESCE=0x2000
#The WM_MOUSEMOVE messages will not be coalesced. The default behavior is to coalesce WM_MOUSEMOVE messages.
global MOUSEEVENTF_LEFTDOWN
MOUSEEVENTF_LEFTDOWN=0x0002
#The left button was pressed.
global MOUSEEVENTF_LEFTUP
MOUSEEVENTF_LEFTUP=0x0004
#The left button was released.
global MOUSEEVENTF_RIGHTDOWN
MOUSEEVENTF_RIGHTDOWN=0x0008
#The right button was pressed.
global MOUSEEVENTF_RIGHTUP
MOUSEEVENTF_RIGHTUP=0x0010
#The right button was released.
global MOUSEEVENTF_MIDDLEDOWN
MOUSEEVENTF_MIDDLEDOWN=0x0020
#The middle button was pressed.
global MOUSEEVENTF_MIDDLEUP
MOUSEEVENTF_MIDDLEUP=0x0040
#The middle button was released.
global MOUSEEVENTF_VIRTUALDESK
MOUSEEVENTF_VIRTUALDESK=0x4000
#Maps coordinates to the entire desktop. Must be used with MOUSEEVENTF_ABSOLUTE.
global MOUSEEVENTF_WHEEL
MOUSEEVENTF_WHEEL=0x0800
#The wheel was moved, if the mouse has a wheel. The amount of movement is specified in mouseData.

ts = time.sleep
tt = time.time

SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

class ScreenResolution():
    w = ctypes.windll.user32.GetSystemMetrics(0)
    h = ctypes.windll.user32.GetSystemMetrics(1)
    print(w,h) #ADD RETURN

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class POINT(ctypes.Structure):
    _fields_ = ("x", ctypes.c_int),("y",ctypes.c_int)

def gcp():

	p = POINT()
	res = ctypes.windll.user32.GetCursorPos(ctypes.byref(p))
	#print(p.x, p.y)
	return p

	

def MouseWheel(n = 2):
    nInputs = 1
    dwFlags = 0x0800 #wheel
    mouseData = 120* n #can be negative
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    dx = 0
    dy = 0
    ii_.mi = MouseInput( dx, dy, mouseData, dwFlags, 0, ctypes.pointer(extra))
    x = Input(0, ii_)
    cbSize = ctypes.sizeof(x)
    SendInput(nInputs, ctypes.pointer(x), cbSize)	
	
def MouseLeftDown():
    nInputs = 1
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput( 0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra))
    x = Input(0, ii_)
    cbSize = ctypes.sizeof(x)
    SendInput(nInputs, ctypes.pointer(x), cbSize)


def MouseLeftUp():
    nInputs = 1
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput( 0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
    x = Input(0, ii_)
    cbSize = ctypes.sizeof(x)
    SendInput(nInputs, ctypes.pointer(x), cbSize)


def lClick():
    MouseLeftDown()
    time.sleep(0.1)
    MouseLeftUp()

def MouseRightDown():
    nInputs = 1
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput( 0, 0, 0, MOUSEEVENTF_RIGHTDOWN, 0, ctypes.pointer(extra))
    x = Input(0, ii_)
    cbSize = ctypes.sizeof(x)
    SendInput(nInputs, ctypes.pointer(x), cbSize)


def MouseRightUp():
    nInputs = 1
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput( 0, 0, 0, MOUSEEVENTF_RIGHTUP, 0, ctypes.pointer(extra))
    x = Input(0, ii_)
    cbSize = ctypes.sizeof(x)
    SendInput(nInputs, ctypes.pointer(x), cbSize)

def rClick():
    MouseRightDown()
    time.sleep(0.05)
    MouseRightUp()
	
def GetCursorPos():
    p=POINT()
    res=ctypes.windll.user32.GetCursorPos(ctypes.pointer(p))
    #print(p.x,p.y)
    return (p.x, p.y)



def LogicalToPhysical(x,y, dbg):
    """ Convert from  65535 *65532 to ~1920*1080  """
    scr_w = ScreenResolution.w
    scr_h = ScreenResolution.h
    x_phs = int((scr_w * x)/65535)
    y_phs = int((scr_h * y)/65535)
    return(x_phs, y_phs)
    
    
def PhysicalToLogical(x,y, dbg=False):
    """ Convert from  ~1920*1080 to 65535 *65532"""
    scr_w = ScreenResolution.w
    scr_h = ScreenResolution.h
    x_lg = int(65535 *x/scr_w)
    y_lg = int(65535 *y/scr_h)
    if  dbg:
        print "PhysicalToLogical (%r %r)"%(x,y)
        print "screen W, H : %r %r "%(scr_w, scr_h)
        print "x_lg = int(65535 *%r/%r) = %r"%(x, scr_w,x_lg)
        print "y_lg = int(65535 *%r/%r) = %r"%(y, scr_h,y_lg)
        
    return(x_lg, y_lg)

def MouseMove(x,y, move_absolute = True, dbg = False):
    infos ="""
    global MOUSEEVENTF_VIRTUALDESK=0x4000
    #Maps coordinates to the entire desktop. Must be used with MOUSEEVENTF_ABSOLUTE."""
    nInputs = 1
    mouseData = 0 # "placeholder for wheel mmovement data; DWORD"
    TIME = 0
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    dwFlags = MOUSEEVENTF_MOVE #movement occured
    
    if move_absolute: #if ABSOLUTE
        dwFlags = dwFlags | MOUSEEVENTF_ABSOLUTE
        dx, dy = PhysicalToLogical(x,y, dbg)
    else:
        dx, dy = x,y
        pos = GetCursorPos() #tuple
        
    
    ii_.mi = MouseInput( dx, dy, mouseData, dwFlags, TIME, ctypes.pointer(extra))
    INPUTS = Input(0, ii_)
    cbSize = ctypes.sizeof(INPUTS)
    if dbg:
        print "cbSize: ", cbSize
    SendInput(nInputs, ctypes.pointer(INPUTS), cbSize)
def MouseMoveInLine(x,y, move_absolute = True, steps = 10, interval = 0.5,dbg = False):
	cur_x, cur_y = GetCursorPos()
	x_step,y_step = (x - cur_x)/steps, (y - cur_y)/steps
	for i in range(steps):
		time.sleep(1.0*interval/steps)
		MouseMove(cur_x + (i+1)*x_step, cur_y + (i+1)*y_step)

		
	

A = 0x1E
D = 0x20
Q = 0x10
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))	
	
def HitKey(vCode):
	PressKey(vCode)
	time.sleep(0.03)
	ReleaseKey(vCode)



vKey_dict = {
    'ESCAPE': 0x01,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    'MINUS': 0x0C,
    'EQUALS': 0x0D,
    'BACK': 0x0E,
    'TAB': 0x0F,
    'Q': 0x10,
    'W': 0x11,
    'E': 0x12,
    'R': 0x13,
    'T': 0x14,
    'Y': 0x15,
    'U': 0x16,
    'I': 0x17,
    'O': 0x18,
    'P': 0x19,
    'LBRACKET': 0x1A,
    'RBRACKET': 0x1B,
    'RETURN': 0x1C,
    'LCONTROL': 0x1D,
    'A': 0x1E,
    'S': 0x1F,
    'D': 0x20,
    'F': 0x21,
    'G': 0x22,
    'H': 0x23,
    'J': 0x24,
    'K': 0x25,
    'L': 0x26,
    # 'SEMICOLON': 0x27,
    'APOSTRAPHE': 0x28,
    # 'GRAVE': 0x29,
    'LSHIFT': 0x2A,
    'BACKSLASH': 0x2B,
    'Z': 0x2C,
    'X': 0x2D,
    'C': 0x2E,
    'V': 0x2F,
    'B': 0x30,
    'N': 0x31,
    'M': 0x32,
    'COMMA': 0x33,
    'PERIOD': 0x34,
    'SLASH': 0x35,
    'RSHIFT': 0x36,
    'MULTIPLY': 0x37,
    'LMENU': 0x38,
    'SPACE': 0x39,
    'CAPITAL': 0x3A,
    'F1': 0x3B,
    'F2': 0x3C,
    'F3': 0x3D,
    'F4': 0x3E,
    'F5': 0x3F,
    'F6': 0x40,
    'F7': 0x41,
    'F8': 0x42,
    'F9': 0x43,
    'F10': 0x44,
    'NUMLOCK': 0x45,
    'SCROLL': 0x46,
    'NUMPAD7': 0x47,
    'NUMPAD8': 0x48,
    'NUMPAD9': 0x49,
    'SUBTRACT': 0x4A,
    'NUMPAD4': 0x4B,
    'NUMPAD5': 0x4C,
    'NUMPAD6': 0x4D,
    'ADD': 0x4E,
    'NUMPAD1': 0x4F,
    'NUMPAD2': 0x50,
    'NUMPAD3': 0x51,
    'NUMPAD0': 0x52,
    'DECIMAL': 0x53,
    'F11': 0x57,
    'F12': 0x58,
    'F13': 0x64,
    'F14': 0x65,
    'F15': 0x66,
}
class keyboard():
	global vKey_dict
	def PressKey(self,hexKeyCode, scan=True, ext=True ):
		extra = ctypes.c_ulong(0)
		ii_ = Input_I()
		
		if hexKeyCode == 'LMENU':
			scan=False
			hexKeyCode = 0x12
		if type(hexKeyCode) == str:
			hexKeyCode = vKey_dict[hexKeyCode]
			
		if scan:
			vk = 0
			scanCode = hexKeyCode
			dwFlags = 0x0008
			
		else: 
			vk = hexKeyCode
			scanCode = 0
			dwFlags = 0x0000
			#ii_.ki = KeyBdInput( hexKeyCode, 0, 0x0008, 0, ctypes.pointer(extra) )
		
		ii_.ki = KeyBdInput( vk, scanCode, dwFlags, 0, ctypes.pointer(extra) )
		x = Input( ctypes.c_ulong(1), ii_ )
		ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

	def ReleaseKey(self,hexKeyCode,scan=True, ext=True):
		extra = ctypes.c_ulong(0)
		ii_ = Input_I()
		
		if hexKeyCode == 'LMENU':
			scan=False
			hexKeyCode = 0x12
		if type(hexKeyCode) == str:
			hexKeyCode = vKey_dict[hexKeyCode]
			
		if scan:
			vk = 0
			scanCode = hexKeyCode
			dwFlags = 0x0008| 0x0002
			
		else: 
			vk = hexKeyCode
			scanCode = 0
			dwFlags = 0x0000 | 0x0002
			
		ii_.ki = KeyBdInput( vk, scanCode, dwFlags, 0, ctypes.pointer(extra) )	
		x = Input( ctypes.c_ulong(1), ii_ )
		ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))	
	
	def Arrow(self, arrow = 'up'):
		#also ALT implemented here for now on
		if arrow == 'up':
			vk = 0x26
		elif arrow == 'down':
			vk = 0x28

		scanCode = 0
		dwFlags = 0x0001
		extra = ctypes.c_ulong(0)
		ii_ = Input_I()
		ii_.ki = KeyBdInput( vk, scanCode, dwFlags, 0, ctypes.pointer(extra) )
		x = Input( ctypes.c_ulong(1), ii_ )
		ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
		
		time.sleep(0.2)
		dwFlags = 0x0001  | 0x0002
		#extra = ctypes.c_ulong(0)
		ii_ = Input_I()
		ii_.ki = KeyBdInput( vk, scanCode, dwFlags, 0, ctypes.pointer(extra) )
		x = Input( ctypes.c_ulong(1), ii_ )
		ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

	def HitKey(self,vCode,delay = 0.03):
		vKey_dict = {
		'ESCAPE': 0x01,
		'1': 0x02,
		'2': 0x03,
		'3': 0x04,
		'4': 0x05,
		'5': 0x06,
		'6': 0x07,
		'7': 0x08,
		'8': 0x09,
		'9': 0x0A,
		'0': 0x0B,
		'MINUS': 0x0C,
		'EQUALS': 0x0D,
		'BACK': 0x0E,
		'TAB': 0x0F,
		'Q': 0x10,
		'W': 0x11,
		'E': 0x12,
		'R': 0x13,
		'T': 0x14,
		'Y': 0x15,
		'U': 0x16,
		'I': 0x17,
		'O': 0x18,
		'P': 0x19,
		'LBRACKET': 0x1A,
		'RBRACKET': 0x1B,
		'RETURN': 0x1C,
		'LCONTROL': 0x1D,
		'A': 0x1E,
		'S': 0x1F,
		'D': 0x20,
		'F': 0x21,
		'G': 0x22,
		'H': 0x23,
		'J': 0x24,
		'K': 0x25,
		'L': 0x26,
		# 'SEMICOLON': 0x27,
		'APOSTRAPHE': 0x28,
		# 'GRAVE': 0x29,
		'LSHIFT': 0x2A,
		'BACKSLASH': 0x2B,
		'Z': 0x2C,
		'X': 0x2D,
		'C': 0x2E,
		'V': 0x2F,
		'B': 0x30,
		'N': 0x31,
		'M': 0x32,
		'COMMA': 0x33,
		'PERIOD': 0x34,
		'SLASH': 0x35,
		'RSHIFT': 0x36,
		'MULTIPLY': 0x37,
		'LMENU': 0x38,
		'SPACE': 0x39,
		'CAPITAL': 0x3A,
		'F1': 0x3B,
		'F2': 0x3C,
		'F3': 0x3D,
		'F4': 0x3E,
		'F5': 0x3F,
		'F6': 0x40,
		'F7': 0x41,
		'F8': 0x42,
		'F9': 0x43,
		'F10': 0x44,
		'NUMLOCK': 0x45,
		'SCROLL': 0x46,
		'NUMPAD7': 0x47,
		'NUMPAD8': 0x48,
		'NUMPAD9': 0x49,
		'SUBTRACT': 0x4A,
		'NUMPAD4': 0x4B,
		'NUMPAD5': 0x4C,
		'NUMPAD6': 0x4D,
		'ADD': 0x4E,
		'NUMPAD1': 0x4F,
		'NUMPAD2': 0x50,
		'NUMPAD3': 0x51,
		'NUMPAD0': 0x52,
		'DECIMAL': 0x53,
		'F11': 0x57,
		'F12': 0x58,
		'F13': 0x64,
		'F14': 0x65,
		'F15': 0x66,
			}
		if type(vCode) == str:
			vCode = vKey_dict[vCode]
		
		PressKey(vCode)
		time.sleep(delay)
		ReleaseKey(vCode)


		
	#def HitKeyScancode(
	def TypeLine(self,line, ENTER = True):
		vKey_dict = {
    'ESCAPE': 0x01,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    'MINUS': 0x0C,
    'EQUALS': 0x0D,
    'BACK': 0x0E,
    'TAB': 0x0F,
    'Q': 0x10,
    'W': 0x11,
    'E': 0x12,
    'R': 0x13,
    'T': 0x14,
    'Y': 0x15,
    'U': 0x16,
    'I': 0x17,
    'O': 0x18,
    'P': 0x19,
    'LBRACKET': 0x1A,
    'RBRACKET': 0x1B,
    'RETURN': 0x1C,
    'LCONTROL': 0x1D,
    'A': 0x1E,
    'S': 0x1F,
    'D': 0x20,
    'F': 0x21,
    'G': 0x22,
    'H': 0x23,
    'J': 0x24,
    'K': 0x25,
    'L': 0x26,
    # 'SEMICOLON': 0x27,
    'APOSTRAPHE': 0x28,
    # 'GRAVE': 0x29,
    'LSHIFT': 0x2A,
    'BACKSLASH': 0x2B,
    'Z': 0x2C,
    'X': 0x2D,
    'C': 0x2E,
    'V': 0x2F,
    'B': 0x30,
    'N': 0x31,
    'M': 0x32,
    'COMMA': 0x33,
    'PERIOD': 0x34,
    'SLASH': 0x35,
    'RSHIFT': 0x36,
    'MULTIPLY': 0x37,
    'LMENU': 0x38,
    'SPACE': 0x39,
    'CAPITAL': 0x3A,
    'F1': 0x3B,
    'F2': 0x3C,
    'F3': 0x3D,
    'F4': 0x3E,
    'F5': 0x3F,
    'F6': 0x40,
    'F7': 0x41,
    'F8': 0x42,
    'F9': 0x43,
    'F10': 0x44,
    'NUMLOCK': 0x45,
    'SCROLL': 0x46,
    'NUMPAD7': 0x47,
    'NUMPAD8': 0x48,
    'NUMPAD9': 0x49,
    'SUBTRACT': 0x4A,
    'NUMPAD4': 0x4B,
    'NUMPAD5': 0x4C,
    'NUMPAD6': 0x4D,
    'ADD': 0x4E,
    'NUMPAD1': 0x4F,
    'NUMPAD2': 0x50,
    'NUMPAD3': 0x51,
    'NUMPAD0': 0x52,
    'DECIMAL': 0x53,
    'F11': 0x57,
    'F12': 0x58,
    'F13': 0x64,
    'F14': 0x65,
    'F15': 0x66,
		}
		def isCapitalLetter(ch, debug = False):
			if ord(ch) >= 97 and ord(ch) <= 122:
				if debug == True:
					print("This is small letter [%r]"%ch)
				return False
			elif ord(ch) >=65 and ord(ch) <= 90:
				if debug == True:
					print("This is big letter [%r]"%ch)
				return True
			else:
				if debug == True:
					print("This is not a letter!")
				return False
	
		#data = line.replace(' ', ' SPACE ')
	
		#print('TEST1')
		for character in line:
			time.sleep(random.random()*0.3+0.2)
			if character in set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 #@+-'):		
				if isCapitalLetter(character):
					PressKey(vKey_dict['LSHIFT'])
					HitKey(vKey_dict[character])
					ReleaseKey(vKey_dict['LSHIFT'])
				elif character == ' ':
					HitKey(vKey_dict['SPACE'])
				elif character == '#':
					PressKey(vKey_dict['LSHIFT'])
					HitKey(vKey_dict['3'])
					ReleaseKey(vKey_dict['LSHIFT'])
				elif character == '@':
					PressKey(vKey_dict['LSHIFT'])
					HitKey(vKey_dict['2'])
					ReleaseKey(vKey_dict['LSHIFT'])
				elif character == '-':
					HitKey(vKey_dict['MINUS'])
				elif character == '+':
					PressKey(vKey_dict['LSHIFT'])
					HitKey(vKey_dict['EQUALS'])
					ReleaseKey(vKey_dict['LSHIFT'])
				else:
					HitKey(vKey_dict[character.upper()])
		if ENTER == True:
			time.sleep(random.random()*0.5+0.5)
			HitKey(vKey_dict['RETURN'])
