from PyQt4 import QtCore, QtGui
import sys,time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess as sp
import os,ctypes
import cv2
import numpy as np
import time
from Client import Client
from ro_logic import *

client = Client('novaro')
client.refresh()
client.focus()
time.sleep(1)

var1 = 5 #get img from game or load from disk
#var = 1 : grab img - coords area, make gray - will cut out separate digits.

def get_coord_image(client = client):
	client.focus()
	time.sleep(0.05)
	img = client.grab(show = 0)
	coords_area = img[148:157, 517:566, :]
	coords_area_gray = cv2.cvtColor(coords_area, cv2.COLOR_BGR2GRAY)
	coords_area_gray[np.where(coords_area_gray < [255])] = 0
	print(coords_area_gray.shape)
	return coords_area_gray.copy()

def get_digits_dict():
	files = os.listdir('ro-data')
	digits = {}
	for f in files:
		if f[-4:] == '.bmp':
			fname = 'ro-data/'+ f
			img_ = cv2.imread(fname)
			#print fname, img_.shape
			#inp = raw_input('debug \n')
			digits[f[:-4]] = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
	return digits

digits = get_digits_dict() # DIGITS DICT CONSTRUCTED HERE!!!!!!!!!


def find_first_digit_in_coords_image(digits_dict,  digit):
	img = get_coord_image()


counter = 1000
k = 0
if var1 == 3: #find digit 8 within coords image
		#digit = digits['8'] #retrieed numpy array - img of 8 digit.
		#print(digit.shape)
		while k < counter:
			if ctypes.windll.user32.GetAsyncKeyState(0x91) != 0:
				break
			time.sleep(1)
			img = get_coord_image()
			#rint('IMG SHAPE: ', img.shape)
			#coords_scanned_till = 0
			record = []
			t0 = time.time()
			for d in digits.keys(): #we start scanning for 0 deltas. and remember digit and position.
				digit_width = digits[d].shape[1]
				#print('DIGIT: ',d, digits[d], digits[d].shape)
				for i in range(img.shape[1] - digit_width):
					delta = np.sum(img[:,i:i+digit_width] - digits[d])
					if delta == 0:
						record.append((d, i))
			#print(record)
			coords = sorted(record, key = lambda x: x[1])
			coords = ''.join([x[0] for x in coords])
			coords = coords.replace('__', ' ')
			coords = coords.replace('___', ' ')
			coords = coords.replace('_', ' ')
			coords = coords.split(' ')
			print(coords)
#print(time.time() - t0)

def print_coords_loop():
	k = 0
	counter = 1000
	
	while k < counter:
		if ctypes.windll.user32.GetAsyncKeyState(0x91) != 0:
			break
		time.sleep(1)
		img = get_coord_image()
		#rint('IMG SHAPE: ', img.shape)
		#coords_scanned_till = 0
		record = []
		t0 = time.time()
		for d in digits.keys(): #we start scanning for 0 deltas. and remember digit and position.
			digit_width = digits[d].shape[1]
			#print('DIGIT: ',d, digits[d], digits[d].shape)
			for i in range(img.shape[1] - digit_width):
				delta = np.sum(img[:,i:i+digit_width] - digits[d])
				if delta == 0:
					record.append((d, i))
		#print(record)
		coords = sorted(record, key = lambda x: x[1])
		coords = ''.join([x[0] for x in coords])
		coords = coords.replace('__', ' ')
		coords = coords.replace('___', ' ')
		coords = coords.replace('_', ' ')
		coords = coords.split(' ')
		coords = filter(lambda x: x != '', coords)
		print(coords)

		
class coord_reader(QtCore.QThread):
	def __init__(self,parent=None):
		QtCore.QThread.__init__(self,parent)
		self.client = Client('novaro')
		self.client.refresh()
		self.client.focus()
		time.sleep(1)
		self.is_running = True
		self.boss = None
		self.debug = True
		if self.debug:
			print 'parent:', parent
		#
		print self.boss
		
	def make_slot(self):
		self.connect(self.boss,QtCore.SIGNAL("clicked()"), self.grab)
	
	def grab(self):
		print 'GRAB'
		self.client.grab(show = 1)
	def get_coord_image(self):
		self.client.focus()
		time.sleep(0.05)
		img = self.client.grab(show = 0)
		coords_area = img[148:157, 517:566, :]
		coords_area_gray = cv2.cvtColor(coords_area, cv2.COLOR_BGR2GRAY)
		coords_area_gray[np.where(coords_area_gray < [255])] = 0
		print(coords_area_gray.shape)
		return coords_area_gray.copy()
	
	def get_digits_dict(self):
		files = os.listdir('ro-data')
		digits = {}
		for f in files:
			if f[-4:] == '.bmp':
				fname = 'ro-data/'+ f
				img_ = cv2.imread(fname)
				#print fname, img_.shape
				#inp = raw_input('debug \n')
				digits[f[:-4]] = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
		return digits
	
	def find_first_digit_in_coords_image(self,digits_dict,  digit):
		img = self.get_coord_image()
	
	
	def run(self):
		
		self.client.main_loop()
		print 'Finished the loop'
	
	def coords_loop(self):
		k = 0
		counter = 1000000
		digits = self.get_digits_dict()
		while k < counter:
			if ctypes.windll.user32.GetAsyncKeyState(0x91) != 0:
				self.emit(QtCore.SIGNAL("finished()"))
				break
			time.sleep(1)
			img = self.get_coord_image()
			record = []
			t0 = time.time()
			for d in digits.keys(): #we start scanning for 0 deltas. and remember digit and position.
				digit_width = digits[d].shape[1]
				for i in range(img.shape[1] - digit_width):
					delta = np.sum(img[:,i:i+digit_width] - digits[d])
					if delta == 0:
						record.append((d, i))
			coords = sorted(record, key = lambda x: x[1])
			coords = ''.join([x[0] for x in coords])
			coords = coords.replace('__', ' ')
			coords = coords.replace('___', ' ')
			coords = coords.replace('_', ' ')
			coords = coords.split(' ')
			coords = ' '.join(filter(lambda x: x != '', coords))
			print(coords)
			print 'thread:', int(QThread.currentThreadId())
			self.emit(QtCore.SIGNAL("mysignal2(QString)"), str(coords))
			
class MyWindow(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.labelT = QtGui.QLabel('Character coordinates: (ScrLock to stop)')
		self.labelT.setAlignment(QtCore.Qt.AlignTop)
		self.label = QtGui.QLabel('--- ---')
		self.labelFGL = QtGui.QLabel('grab feature')
		#self.labelMM = QtGui.QLabel('grab feature')
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.buttonSCR=QtGui.QPushButton('make screenshot')
		self.buttonFGL=QtGui.QPushButton('grab features')
		self.buttonFKL=QtGui.QPushButton('Find kafra label')
		self.button=QtGui.QPushButton('start scanning')
		self.buttonMM=QtGui.QPushButton('move mouse')
		self.buttonAM=QtGui.QPushButton('move items to bank')
		self.buttonFAKP=QtGui.QPushButton('find and click tree')
		self.buttonUW=QtGui.QPushButton('use warper')
		self.buttonHP=QtGui.QPushButton('hunt pink')
		self.buttonGHP=QtGui.QPushButton('get hp:  ')
		self.buttonGHP2=QtGui.QPushButton('get hp 2 ')
		self.buttonGTT=QtGui.QPushButton('go to town')
		self.buttonUH=QtGui.QPushButton('use healer')
		self.buttonGMM=QtGui.QPushButton('get minimap')
		self.buttonTD=QtGui.QPushButton('toogle debug')
		self.buttonTC=QtGui.QPushButton('turn off chat chat')
		self.buttonCW=QtGui.QPushButton('check weight')
		self.buttonCA=QtGui.QPushButton('check ammo')
		self.buttonHT=QtGui.QPushButton('placeholder')
		
		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(self.labelT)
		self.vbox.addWidget(self.label)
		self.vbox.addWidget(self.button)
		self.vbox.addWidget(self.buttonSCR)
		self.vbox.addWidget(self.buttonFGL)
		self.vbox.addWidget(self.buttonFKL)
		self.vbox.addWidget(self.labelFGL)
		self.vbox.addWidget(self.buttonMM)
		self.vbox.addWidget(self.buttonAM)
		self.vbox.addWidget(self.buttonFAKP)
		self.vbox.addWidget(self.buttonUW)
		self.vbox.addWidget(self.buttonHP)
		self.vbox.addWidget(self.buttonGHP)
		self.vbox.addWidget(self.buttonGHP2)
		self.vbox.addWidget(self.buttonUH)
		self.vbox.addWidget(self.buttonGTT)
		self.vbox.addWidget(self.buttonGMM)
		self.vbox.addWidget(self.buttonTD)
		self.vbox.addWidget(self.buttonTC)
		self.vbox.addWidget(self.buttonCW)
		self.vbox.addWidget(self.buttonCA)
		self.vbox.addWidget(self.buttonHT)
		
		self.buttonSCR.setDisabled(True)
		self.setLayout(self.vbox)
		self._thread = coord_reader(self)
		print 'thread:', int(QThread.currentThreadId())
		self.client = self._thread.client
		
		print 'self._thread.boss',self._thread.boss
		self.connect(self.button, QtCore.SIGNAL("clicked()"),self.on_clicked)
		self.connect(self.buttonSCR, QtCore.SIGNAL("clicked()"),self.on_clickedSCR)
		self.connect(self.buttonFGL, QtCore.SIGNAL("clicked()"),self.on_clickedFGL)
		self.connect(self.buttonFKL, QtCore.SIGNAL("clicked()"),self.on_clickedFKL)
		self.connect(self.buttonMM, QtCore.SIGNAL("clicked()"),self.on_clickedMM)
		self.connect(self._thread, QtCore.SIGNAL("started()"),self.on_started)
		self.connect(self._thread, QtCore.SIGNAL("finished()"),self.on_finished)
		self.connect(self._thread, QtCore.SIGNAL("mysignal2(QString)"), self.on_update)
		self.connect(self.buttonAM, QtCore.SIGNAL("clicked()"),self.on_clickedAM)
		self.connect(self.buttonFAKP, QtCore.SIGNAL("clicked()"),self.on_clickedFAKP)
		self.connect(self.buttonUW, QtCore.SIGNAL("clicked()"),self.on_clickedUW)
		self.connect(self.buttonHP, QtCore.SIGNAL("clicked()"),self.on_clickedHP)
		self.connect(self.buttonGHP, QtCore.SIGNAL("clicked()"),self.on_clickedGHP)
		self.connect(self.buttonGHP2, QtCore.SIGNAL("clicked()"),self.on_clickedGHP2)
		self.connect(self.buttonUH, QtCore.SIGNAL("clicked()"),self.on_clickedUH)
		self.connect(self.buttonGTT, QtCore.SIGNAL("clicked()"),self.on_clickedGTT)
		self.connect(self.buttonGMM, QtCore.SIGNAL("clicked()"),self.on_clickedGMM)
		self.connect(self.buttonTD, QtCore.SIGNAL("clicked()"),self.on_clickedTD)
		self.connect(self.buttonTC, QtCore.SIGNAL("clicked()"),self.on_clickedTC)
		self.connect(self.buttonCW, QtCore.SIGNAL("clicked()"),self.on_clickedCW)
		self.connect(self.buttonCA, QtCore.SIGNAL("clicked()"),self.on_clickedCA)
		self.connect(self.buttonHT, QtCore.SIGNAL("clicked()"),self.on_clickedHT)
		
	def on_clickedTD(self):
		self.client.debug = not self.client.debug
		print 'DEBUG MODE: ', self.client.debug
		self.buttonTD.setText('debug: %s'%self.client.debug)
	def on_clicked(self):
		self._thread.start()
		self.button.setDisabled(True)
		self._thread.boss = self.buttonSCR
		#self._thread.make_slot()
		self.buttonSCR.setDisabled(False)
		print 'thread:', int(QThread.currentThreadId())
	def on_clickedCW(self):
		self.client.tasks.append('check weight')
		#just print for now on
		
	def on_clickedCA(self):
		self.client.tasks.append('check ammo')
	def on_clickedHT(self):
		self.client.tasks.append('placeholder')
		
	def on_clickedFGL(self):
		self.buttonSCR.setDisabled(True)
		#self.client.feature_grab_loop()
		self.client.tasks.append('feature_grab_loop')
		self.buttonSCR.setDisabled(False)

	def on_clickedFKL(self):
		self.client.tasks.append('get_kafra_pos')
		self.client.tasks.append('open-inventory')
		self.client.tasks.append('close-inventory')
		self.client.tasks.append('close-bank')
	def on_clickedMM(self):
		self.client.tasks.append(('move mouse',(100,100)))
		self.client.tasks.append(('move mouse',(200,100)))
		self.client.tasks.append(('move mouse',(100,200)))
		self.client.tasks.append(('move mouse',(200,200)))
		
	def on_clickedAM(self):
		self.client.tasks.append('get_kafra_pos')
		self.client.tasks.append('open-inventory')
		self.client.tasks.append(('drag to bank','jelly'))
		self.client.tasks.append(('drag to bank','branch'))
		self.client.tasks.append(('drag to bank','banana'))
		self.client.tasks.append(('drag to bank','honey'))
		self.client.tasks.append(('drag to bank','apple'))
		self.client.tasks.append('close-inventory')
		self.client.tasks.append('toogle chat')
		
		self.client.tasks.append('close-bank')

	def on_clickedFAKP(self):
		self.client.tasks.append('get minimap')
		self.client.tasks.append('find and click tree')
	
	def on_clickedHP(self):
		self.client.tasks.append('hunt pink')
	def on_clickedUH(self):
		self.client.tasks.append('use healer')
	def on_clickedGTT(self):
		self.client.tasks.append('go to town')
		
	def on_clickedHP(self):
		self.client.tasks.append('hunt pink')
	def on_clickedGHP(self):
		self.client.tasks.append('get hp')
		time.sleep(1)
		self.buttonGHP.setText('get hp:%r'%self.client.HP)
	def on_clickedGHP2(self):
		self.client.tasks.append('get hp 2')
		#time.sleep(1)
		#self.buttonGHP.setText('get hp:%r'%self.client.HP)
	def on_clickedTC(self):
		self.client.tasks.append('toogle chat')
		
	def on_clickedUW(self):
		self.client.tasks.append('use last warp')
	def on_clickedGMM(self):
		self.client.tasks.append('get minimap')
		
	def on_clickedSCR(self, opt = 1):
		if opt == 1:
			self.client.tasks = ['screenshot',] +  self.client.tasks
			#print 'thread:', int(QThread.currentThreadId())
			#cv2.imwrite('test.png',img)
		else:
			self.emit(QtCore.SIGNAL("mysignal(QString)"), opt)
			
	def on_started(self):
		self.label.setText('reading coords...')
		
	def on_finished(self):
		self.label.setText('stopped reading coords...')
		self.button.setDisabled(False)
	def on_update(self,data):
		self.label.setText(data)
	

		
if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	w = MyWindow()
	w.setWindowTitle('RO Coordinates reader')
	#w.resize(300,100)
	w.show()
	sys.exit(app.exec_())