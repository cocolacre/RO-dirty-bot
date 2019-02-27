from Client import Client
from screen import *
from mouse import *
from PyQt4 import QtCore, QtGui
import sys,time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess as sp
import os,ctypes
import cv2
import numpy as np
import time


class Logics():
	def __init__(self):
		self.record = ''
	
	
	
#need to pass task with parameters!
def get_kafra_pos(client):
	target = 'kafra-label'
	res = client.match_feature(tg)
	print res
	time.sleep(1)
