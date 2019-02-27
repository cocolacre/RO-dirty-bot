import ctypes
from ctypes import wintypes
from ctypes.wintypes import *
import numpy as np
import time
import cv2
global SRCCOPY
SRCCOPY = 0xCC0020
global DIB_RGB_COLORS
DIB_RGB_COLORS = 0
global BI_RGB
BI_RGB = 0

BringWindowToTop = ctypes.windll.user32.BringWindowToTop
BitBlt = ctypes.windll.gdi32.BitBlt
CreateCompatibleBitmap = ctypes.windll.gdi32.CreateCompatibleBitmap
CreateCompatibleDC = ctypes.windll.gdi32.CreateCompatibleDC
DeleteDC = ctypes.windll.gdi32.DeleteDC
DeleteObject = ctypes.windll.gdi32.DeleteObject
FindWindow = ctypes.windll.user32.FindWindowW
GetBitmapBits = ctypes.windll.gdi32.GetBitmapBits
GetClientRect = ctypes.windll.user32.GetClientRect
GetDIBits = ctypes.windll.gdi32.GetDIBits
GetObject = ctypes.windll.gdi32.GetObjectW
GetPixel = ctypes.windll.gdi32.GetPixel
GetWindowDC = ctypes.windll.user32.GetWindowDC
GetWindowInfo = ctypes.windll.user32.GetWindowInfo
GetWindowRect = ctypes.windll.user32.GetWindowRect
PlgBlt = ctypes.windll.gdi32.PlgBlt
PrintWindow = ctypes.windll.user32.PrintWindow
ReleaseDC = ctypes.windll.user32.ReleaseDC
SelectObject = ctypes.windll.gdi32.SelectObject
SwitchToThisWindow = ctypes.windll.user32.SwitchToThisWindow
ShowWindow = ctypes.windll.user32.ShowWindow

BOOL    = ctypes.c_bool
INT     = ctypes.c_int
LONG    = ctypes.c_long
WORD    = ctypes.c_ushort
LPVOID  = ctypes.c_void_p
LPLONG  = ctypes.POINTER(LONG)
Structure = ctypes.Structure
UINT    = ctypes.c_uint
c_uint = ctypes.c_uint
c_ushort = ctypes.c_ushort
byref = ctypes.byref


class WINDOWINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("rcWindow", wintypes.RECT),
        ("rcClient", wintypes.RECT),
        ("dwStyle", ctypes.c_uint),
        ("dwExStyle", ctypes.c_uint),
        ("dwWindowStatus", ctypes.c_uint),
        ("cxWindowBorders", ctypes.c_uint),
        ("cyWindowBorders", ctypes.c_uint),
        ("atomWindowType", ctypes.c_uint),
        ("wCreatorVersion", ctypes.c_ushort)
    ]

class POINT(ctypes.Structure):
    _fields_ = ("x", ctypes.c_int),("y",ctypes.c_int)
    

class BITMAP(Structure):
    _fields_ = [
        ("bmType",          LONG),
        ("bmWidth",         LONG),
        ("bmHeight",        LONG),
        ("bmWidthBytes",    LONG),
        ("bmPlanes",        WORD),
        ("bmBitsPixel",     WORD),
        ("bmBits",          LPVOID),
    ]
class BITMAPFILEHEADER(Structure):
    _pack_ = 2
    _fields_ = [
        ('bfType',      WORD),
        ('bfSize',      DWORD),
        ('bfReserved1', WORD),
        ('bfReserved2', WORD),
        ('bfOffBits',   DWORD),
    ]



class BITMAPINFOHEADER(Structure):
     _fields_ = [
        ('biSize',          DWORD),
        ('biWidth',         LONG),
        ('biHeight',        LONG),
        ('biPlanes',        WORD),
        ('biBitCount',      WORD),
        ('biCompression',   DWORD),
        ('biSizeImage',     DWORD),
        ('biXPelsPerMeter', LONG),
        ('biYPelsPerMeter', LONG),
        ('biClrUsed',       DWORD),
        ('biClrImportant', DWORD),
    ]



class RGBQUAD(Structure):
    _fields_ = [
            ('rgbBlue', BYTE),
            ('rgbGreen', BYTE),
            ('rgbRed', BYTE),
            ('rgbReserved', BYTE),
    ]


class BITMAPINFO(Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ('bmiColors', RGBQUAD * 1),
    ]



def capture(hwnd=0, x=0,y=0,w=0,h=0,dbg=True, show = 0):
	capture_begin = time.time()
	if w == 0 and h == 0 and hwnd == 0:
		w = ctypes.windll.user32.GetSystemMetrics(0)
		h = ctypes.windll.user32.GetSystemMetrics(1)
		if dbg == True:
			print("W,H: ", w,h)
	wDC = HDC() #Create device context
	wDC = GetWindowDC(hwnd) #Define device context
	#print "TODO: Check if window is Active, Foreground and has focus"
	memdc = HDC() #Create memory context
	memdc = CreateCompatibleDC(wDC) #
	hBitmap = HGDIOBJ()
	hBitmap = CreateCompatibleBitmap(wDC, w, h)
	replaced_object = HGDIOBJ()
	replaced_object = SelectObject(memdc, hBitmap)
	BitBlt(memdc, 0, 0, w, h, wDC, x, y, SRCCOPY)
	bmp_size = 4*w*h
	bmp_buffer = np.zeros((h,w,4), dtype=np.uint8)
	p_bmp_buffer = bmp_buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
	res = GetBitmapBits( hBitmap, bmp_size, p_bmp_buffer )
	DeleteObject(SelectObject(memdc,hBitmap ))
	DeleteDC(memdc)
	ReleaseDC(hwnd, wDC)
	if dbg:
		capture_complete = time.time()
		capture_elapsed =capture_complete - capture_begin
		#print "Captued %r x %r image in %rs"%(w, h, capture_elapsed)
		#print("bmp_buffer: ", bmp_buffer.shape)
	#print "RGBA array! Dont forget to delette alpha channel if needded."
	img = bmp_buffer[:,:,0:3]
	if show == 1:
		#cv2.imshow("img",img)
		img_name = str(int(time.time())) + '.png'
		cv2.imwrite(img_name, img)
	return img
	
info = """	
def capture(hwnd = 0,dbg=True, x=0, y=0, w=0, h=0):
    #if dbg:
    #    capture_begin = time.time()
    #    print "(X,Y): %r %r"%(x,y)
    #    print "(W,H): %r %r"%(w,h)
    #client.refresh()
    #x = client.x 
    #y = client.y 
    #w = client.w 
    #h = client.h
    
    wDC = HDC() #Create device context
    wDC = GetWindowDC(client.hwnd) #Define device context
    #print "TODO: Check if window is Active, Foreground and has focus"
    memdc = HDC() #Create memory context
    memdc = CreateCompatibleDC(wDC) #
    hBitmap = HGDIOBJ()
    hBitmap = CreateCompatibleBitmap(wDC, w, h)
    replaced_object = HGDIOBJ()
    replaced_object = SelectObject(memdc, hBitmap)
    
    x0 = 0 # WITHIN RCCLIENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
    y0 = 0
    
    x0 = client.x - client.x_wnd
    y0 = client.y - client.y_wnd
    BitBlt(memdc, 0, 0, w, h, wDC, x0, y0, SRCCOPY)
    
    bmp_size = 4*w*h
    bmp_buffer = np.zeros((h,w,4), dtype=np.uint8)
    p_bmp_buffer = bmp_buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
    res = GetBitmapBits( hBitmap, bmp_size, p_bmp_buffer )
    DeleteObject(SelectObject(memdc,hBitmap ))
    DeleteDC(memdc)
    ReleaseDC(client.hwnd, wDC)
    
    #bmp_header = struct.pack('LHHHH', struct.calcsize('LHHHH'), w, h, 1, 24)
    #c_bmp_header = ctypes.c_buffer(bmp_header)
    #c_bits = ctypes.c_buffer(' ' * (h * ((w * 3 + 3) & -4)))
    #DIBits = ctypes.windll.gdi32.GetDIBits(memdc, hBitmap, 0, h, c_bits, c_bmp_header, DIB_RGB_COLORS)
    
    
    if dbg:
        capture_complete = time.time()
        capture_elapsed =capture_complete - capture_begin
        print "Captued %r x %r image in %rs"%(client.w, client.h, capture_elapsed)
    print "RGBA array! Dont forget to delette alpha channel if needded."
    return bmp_buffer
"""