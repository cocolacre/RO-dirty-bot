import subprocess as sp
import winsound as ws
import os, ctypes,sys,math,random
from ctypes import *
from ctypes.wintypes import POINT
from screen import *
from mouse import *
GetWindowRect=ctypes.windll.user32.GetWindowRect
Structure = ctypes.Structure
fw = ctypes.windll.user32.FindWindowW
beep = ws.Beep



#this is used to wake me up\notify me when a bot is about to be banned
#this worked several times by allowing me to take control over the bot
#and to trick GM by playing dumb and to supress their suspicions 
def siren():
	for i in range(10):
		beep(2000,400)
		beep(1000,400)
	

class POINT(Structure):
    _fields_ = ("x", ctypes.c_int),("y",ctypes.c_int)
    
class RECT(Structure):
    _fields_ = ("a", POINT),("b", POINT)

class WINDOWINFO(Structure):
    _fields_ = [
        ("cbSize", c_uint),
        ("rcWindow", RECT),
        ("rcClient", RECT),
        ("dwStyle", c_uint),
        ("dwExStyle", c_uint),
        ("dwWindowStatus", c_uint),
        ("cxWindowBorders", c_uint),
        ("cyWindowBorders", c_uint),
        ("atomWindowType", c_uint),
        ("wCreatorVersion", c_ushort)
    ]

class WINDOWPLACEMENT(Structure):
    _fields_ = [
        ("length", c_uint),
        ("flags", c_uint),
        ("showCmd", c_uint),
        ("ptMinPosition", POINT),
        ("ptMaxPosition", POINT),
        ("rcNormalPosition", RECT)
    ]
	
class feature_by_fn():
	def __init__(self, name, client):
		self.name = name #login-welcome
		self.filename = 'feature-' + game + '-' + name

class Client():
	notes = """
	~ Feature detection depends on WINDOW SIZE. Use self.resize_window(). Improve.
	~ STATE, composite states:
		[LAMBDA,(feature1,feature2,f3)) -> f1 OR f2 OR f3 -> state = LAMBDA
			several features - > to state
	"""						
	
	print notes
	print 'TODO: "interactable" feature attr; interaction type;'
	print 'TODO[!!!]: next_step->get_state->check change_state available -> change_state-> verify'
	print 'TODO[!!!]: determine state - determine POSSIBLE transitions - choose.'
	import time
	import subprocess as sp
	def __init__(self,game='talonro'):
		self.game = game
		self.status = None
		self.p = None
		self.games = {'osrs':u"Old School RuneScape",'novaro':u"Nova Ragnarok", 'talonro':u"TalonRO 2012-10-12"}
		self.title = self.games[game]
		self.exe_fnames = {'osrs':'JagexLauncher.exe','novaro':'NovaRO.exe','talonro':'talonexe.exe' }
		self.exe_fname = self.exe_fnames[game]
		self.application_strings = {'osrs':r"C:\Users\User\jagexcache\jagexlauncher\bin\JagexLauncher.exe oldschool", 'novaro':'','talonro':''}
		self.application_string = self.application_strings[game]
		self.pid = None
		self.hwnd = ctypes.windll.user32.FindWindowW(0, self.title)
		print 'FindWindowW:', self.hwnd
		self.kb = keyboard()
		self.wi = None
		#self.obj_created = time.time()
		self.top = 0
		self.bottom = 0
		self.right = 0
		self.left = 0
		self.x = self.left
		self.y = self.top
		self.w = 0
		self.h = 0
		self.window = 0
		self.x_wnd = 0
		self.y_wnd = 0
		self.w_wnd = 0
		self.h_wnd = 0
		self.refresh()
		self.debug = 0
		
		self.fts = {} #FeatureS Dict
		self.feature_names = []
		self.feature_filenaems = []
		self.feature_ROI = {}
		self.feature_images = {}
		self.feature_thr = {}
		self.feature_pos = {}
		self.feature_color_mode = {}
		self.feature_missed = {}
		
		self.BEHAVIOURAL_TREE = 'TODO'

		self.update_features()
		self.i_see = dict(zip(self.feature_names, [False for fn in self.feature_names]))
		
		self.context = {}
		self.banker = False
		self.last_grab = np.zeros((self.h, self.w, 3))
		self.gui = False
		self.focus()
		self.frame = self.grab(show=0)
		self.i = 0
		self.collect = True
		self.tasks = []
		self.last_message = ' '
		self.ammo = -1
		self.HP = 0
		self.current_map = 'unknown'
		print self.get_pid()
		self.start_time = time.time()
		
		self.counter_zeny =0
		self.counter_strawberry=0
		self.counter_acorn =0
		self.per_hour_strawberry=0
		self.per_hour_zeny=0
		self.per_hour_acorn=0
	def main_loop(self):
		teleport_counter = 0
		rad = np.zeros((self.h,self.w), dtype = np.int8)
		for i in range(self.w):
			for j in range(self.h):
				rad[j,i] = 250-int(math.sqrt((self.w/2 - i)**2 + (self.h/2 - j)**2))/3

		tasks = self.tasks
		tasks.append('start')
		task_counter = 0
		task = 'start'
		#######   BUFFS  #############
		buff1_prev = time.time() - 180
		buff2_prev = time.time() - 90
		##############################
		###### coordinates reading ###
		##############################
		def get_coord_image(self):
			self.focus()
			#time.sleep(0.05)
			#img = self.grab(x=517, y = 148,w=50,h=9,show = 0)
			coords_area = self.frame[148:157, 517:566, :]
			coords_area_gray = cv2.cvtColor(coords_area, cv2.COLOR_BGR2GRAY)
			coords_area_gray[np.where(coords_area_gray < [255])] = 0
			#print(coords_area_gray.shape)
			return coords_area_gray.copy()

		def get_digits_dict(self):
			files = os.listdir('ro-data')
			digits = {}
			for f in files:
				if f[-4:] == '.bmp':
					fname = 'ro-data/'+ f
					img_ = cv2.imread(fname)
					digits[f[:-4]] = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
			return digits
		digits = get_digits_dict(self)
	
		def get_coords(self,digits=digits):
			img = get_coord_image(self)
			record = []
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
			coords = filter(lambda x: x != '', coords)
			return coords	
		
		##############################
		## coordinates reading end ###
		##############################
		
		
		######## ammo amount read start ###########
		def get_amount(frame,digits=digits):
			"""
			pass image of cursor hovering over ammunition here.
			dirty solution. as usual. should implement fast.
			1) frame must be same H as digits ( = 9 )
			"""
			
			img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			img[img<255] = 0
			if img.shape[0] != 9:
				print 'wrong frame shape in get_amount!'
				sys.exit()
			record = []
			try:
				digits.pop('_')
			except Exception as _e:
				infos = """dirty hackery"""
		
			for d in digits.keys():
				digit_width = digits[d].shape[1]
				for i in range(img.shape[1] - digit_width):
					delta = np.sum(img[:,i:i+digit_width]-digits[d])
					if delta == 0:
						record.append((d, i))
			amount = sorted(record, key = lambda x: x[1])
			amount = ''.join([x[0] for x in amount])
			print 'AMOUNT OF BULLETS:', amount
			try:
				return int(amount)
			except Exception as _e:
				print 'could not convert amount to int!'
				return 0
		######## ammo amount read end ###########
		
		
		def get_black_digits_dict(self):
			files = os.listdir('ro-data2')
			digits = {}
			for f in files:
				if f[-4:] == '.bmp':
					fname = 'ro-data2/'+ f
					img_ = cv2.imread(fname)
					digits[f[:-4]] = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
			return digits
		
		def idle(delay = 2):
			if self.debug:
				print 'Idle %r seconds.'%delay
			time.sleep(delay)
		halt = 'halt'
		retry = 0
		MIN_DELAY = 0.1
		task_found = False
		self.tasks.append(idle)
		prev_coords = [0,0]
		prev_coords_time = time.time()
		loop_started = time.time()
		unknown_minimap_counter = 0
		tasks_after_teleport = 0
		while self.tasks[0] != halt:
			time.sleep(0.03)
			#do next task
			prev_task = task
			task = self.tasks.pop(0)
			
			if self.debug:
				print '[ CURRENT TASK ]: ',task
				print 'TASK LIST:', self.tasks
			if type(task) ==str:
				pass
			elif type(task) == tuple:
				task_tuple = task
				task,task_params = task_tuple[0],task_tuple[1]
				
			else:
				task()
			
			#######################
			if task == 'move mouse':
				print 'moving mouse:', task_params
				time.sleep(1)
				self.mouse_move_line(*task_params)
			#############################	
			if task == 'get_kafra_pos':
				target = 'kafra-label'
				res = self.match_feature(target)
				print res
				if res[0]:
					pos = (res[1][0],res[1][1] + 20)
					time.sleep(1)
					self.lClick(*pos)
					print 'clicked kafra'
					time.sleep(1)
					print 'searching for NEXT button'
					target = 'next-button'
					res = self.match_feature(target)
				if res[0]:
					print 'NEXT button found'
					self.type_line('', ENTER=True)
					time.sleep(1)
					print 'searching for USE_STORAGE option'
					target = 'use-storage'
					res = self.match_feature(target)
				if res[0]:
					print 'USE_STORAGE option found'
					self.kb.Arrow('down')
					self.type_line('', ENTER=True)
					time.sleep(1)
					self.type_line('', ENTER=True)
					time.sleep(1)
					
					print 'searching for CLOSE_BUTTON'
					target = 'close-button'
					res = self.match_feature(target)
					
				if res[0]:
					print 'CLOSE button found'
					self.type_line('', ENTER=True)
					time.sleep(1)
					retry = 0
				if not res[0]:
					print 'something went wrong. Retry'
					retry +=1
					if retry < 3:
						self.tasks = [task] + self.tasks
					else:
						retry = 0
						self.tasks.append(halt)
						print 'Retried 3 times, man. I am done failing. Bye.'
			#############################
			if task == 'close-bank':
				time.sleep(1)
				print 'searching for CLOSE_BUTTON'
				target = 'close-bank-button'
				res = self.match_feature(target)
				if res[0]:
					pos = (res[1][0],res[1][1])
					time.sleep(1)
					self.lClick(*pos)
				else:
					
					print 'Could not find CLOSE button'
					print 'Maybe it is obscured by chat?'
					target = 'bank-label'
					res = self.match_feature(target)
					if res[0]:
						print 'found bank label. click to focus'
						pos = (res[1][0],res[1][1])
						time.sleep(1)
						self.mouse_move_line(*pos)
						lClick()
						time.sleep(0.3)
						#move cursor away from bank label
						pos = (res[1][0],res[1][1]+100)
						self.mouse_move_line(*pos)
						time.sleep(1)
				#now verify that bank is closed.
				target = 'bank-label'
				res = self.match_feature(target)
				if not res[0]:
					print 'bank label not found,therefore bank closed. SUCCESS!'
					retry = 0
				else:
					print 'still seeing bank label, retry:', retry
					if retry < 3:
						print 'again lets try to close bank'
						self.tasks = [task] + self.tasks
						retry+=1
					else:
						print 'failed to close bank 3 times. HALT!'
						self.tasks = [halt]
					
						
			###################
			if task == 'open-inventory':
				print 'doing task:', task
				time.sleep(1)
				res = self.match_feature('inventory-label')
				print 'inventory-label:',res
				if not res[0]:
					print 'inventory is not opened. Opening.'
					self.kb.PressKey('LMENU')
					time.sleep(0.1)
					self.kb.PressKey('E')
					time.sleep(0.1)
					self.kb.ReleaseKey('LMENU')
					self.kb.ReleaseKey('E')
					target = 'inventory-label'
					time.sleep(1)
					res = self.match_feature(target)
				if res[0]:
					print 'inventory now opened'
					time.sleep(1)
					inventory_label_pos = res[1]
				else:
					print 'failed opening inventory'
					print 'Maybe retry?'
			#############################3	
			if task == 'close-inventory':
				print 'doing task:', task
				time.sleep(1)
				self.kb.PressKey('LMENU')
				time.sleep(0.1)
				self.kb.PressKey('E')
				time.sleep(0.1)
				self.kb.ReleaseKey('LMENU')
				self.kb.ReleaseKey('E')
				time.sleep(0.5)
				res = self.match_feature('inventory-label')
				if res[0]:
					time.sleep(1)
					print 'inventory is opened.closing.'
					self.kb.PressKey('LMENU')
					time.sleep(0.1)
					self.kb.PressKey('E')
					time.sleep(0.1)
					self.kb.ReleaseKey('LMENU')
					self.kb.ReleaseKey('E')
					res = self.match_feature('inventory-label')
				else:
					print 'inventory closed'
					time.sleep(1)
			
			if ctypes.windll.user32.GetAsyncKeyState(0x91) != 0:
				self.tasks.append(halt)
			######################
			## PAUSE KEY
			#############################
			if task == 'drag apple to bank':
				target = 'apple'
				res = self.match_feature(target)
				if res[0]:
					pos = res[1]
					self.mouse_move_line(*pos)
					target = 'bank-label'
					res = self.match_feature(target)
					pos = res[1]
					self.lDrag(pos[0] +100, pos[1] + 100)
					self.type_line('', ENTER=True)
					print 'hope apple is moved...'
				else:
					print 'failed to detect apple on the screen'
			###############################
			if task == 'drag to bank':
				self.mouse_move_line(0,0)
				target = task_params
				time.sleep(1)
				res = self.match_feature(target)
				if res[0]:
					pos = res[1]
					self.mouse_move_line(*pos)
					print 'getting bank-label position'
					target = 'bank-label'
					res = self.match_feature(target)
					if res[0]:
						pos = res[1]
						self.lDrag(pos[0] +100, pos[1] + 100)
					else:
						print 'could not find bank label while stocking loot!'
					self.type_line('', ENTER=True)
					print 'hope %s is moved...'%task_params
				else:
					print 'failed to detect %s on the screen'%task_params
			###############################
			if task == 'find and click pink':
				task_counter +=1
				print 'task_counter:', task_counter
				if task_counter > 1000:
					self.tasks.append('halt')
				self.focus()
				img = self.grab()
				hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
				lo = np.array([158,170,0])
				hi = np.array([159,200,250])
				mask1 = cv2.inRange(hsv,lo,hi)
				lo = np.array([154,160,0])
				hi = np.array([154,195,250])
				mask2 =cv2.inRange(hsv,lo,hi)
				mask = mask1 + mask2
				if mask.max() !=0:
					print 'Found pink thing! Clicking'
					task_found = True
					mask_rad = mask/2 + rad/10
					(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask_rad)
					pos = maxLoc				
					self.mouse_move_line(pos[0],pos[1],interval=0.15)
					self.lClick()
					time.sleep(0.15)
				else:
					print 'No pink things found'
					time.sleep(0.15)
					task_found = False
			###############################
			if task == 'use last warp':
				time.sleep(1)
				frame = self.grab()
				target = 'warper'
				if target in self.feature_ROI.keys():
					self.feature_ROI.pop(target)
				res = self.match_feature(target,frame=frame)
				if res[0]:
					print 'found warper.'
					pos = (res[1][0], res[1][1] + 30)
					self.mouse_move_line(*pos)
					self.lClick()
					time.sleep(1)
					self.type_line('',ENTER=True)
					#GET MAP NAME
					#CHECK MAP
				else:
					print 'Could not find warper'
				time.sleep(5)
			###############################
			if task =='check ammo':
				self.focus()
				
				self.tasks = ['open-inventory',
							'open-inventory-M', 
							'read ammo ammount', 
							'close-inventory'] + self.tasks

			###############################
			#assuming inventory is open at right tab.
			if task == 'read ammo ammount':
				target = 'fire-bullets'
				try:
					self.feature_ROI.pop(target)
				except Exception as e:
					pass
	
				res = self.match_feature(target)
				
				if res[0]:
					pos = res[1]
					print 'found fire ammo in inventory. Try to read ammount!'
					self.mouse_move_line(pos[0], pos[1])
					time.sleep(1)
					frame = self.grab(x = pos[0]+90, y = pos[1]-21, w = 50,h = 9, show=0)
					amount = get_amount(frame=frame)
					self.ammo = amount
					time.sleep(1)
					print 'there are %r BULLETS LEFT!'%amount
					frame = self.grab() #trying to fix a bug
					time.sleep(1)
					if amount < 750:
						print 'Need to get ammo from bank!'
						tasks = list(self.tasks)
						self.tasks = ['close-inventory','get_kafra_pos', 'open-inventory']
						self.tasks.append('get ammo from bank')
						self.tasks.append('close-inventory')
						self.tasks.append('close-bank')
						self.tasks.append('toogle chat')
						self.tasks = self.tasks + tasks
			
			###############################
			if task == 'get ammo from bank':
				print 'Bank must have been opened now'
				target = 'ammo-tab'
				res = self.match_feature(target)
				if not res[0]:
					print 'could not find AMMO bank tab! HALT!'
					sys.exit()
				else:
					print 'found ammo tab.clicking'
					del pos
					pos = res[1]
					time.sleep(0.5)
					print pos
					self.mouse_move_line(pos[0], pos[1])
					time.sleep(0.5)
					self.lClick(pos[0],pos[1])
					time.sleep(1)
				target = 'fire-bullet-bank'
				print 'searching for fire-bullet in bank!'
				res = self.match_feature(target)
				if not res[0]:
					print 'could not find fire-bullet in bank! halt! restock manualy!'
					print 'TODO: buy ammo!'
					sys.exit()
				else:
					pos = res[1]
					print 'dragging ammo to inventory!'
					self.mouse_move_line(pos[0]-66, pos[1])
					pos = inventory_label_pos
					self.lDrag(pos[0]+20, pos[1]+20)
					#now lets drag it TO inventory!
					ammo_needed = 2200-self.ammo
					self.type_line('%d'%ammo_needed,ENTER=True)
			###############################
			if task == 'get hp':
				hp_bar_present = False
				t0 = time.time()
				frame = self.frame
				hp_bar_y_start = 236
				hp_bar_x_start = 285
				for ind in range(20):
					hp_pixel_A = frame[hp_bar_y_start+ind, 320,1]
					if hp_pixel_A == 24 or hp_pixel_A == 25:
						hp_pixel_B = frame[hp_bar_y_start+ind, 321,1]
						if hp_pixel_B == 24 or hp_pixel_B == 25:
							hp_bar_y = hp_bar_y_start+ind
							break
						#found Y of border of HP-SP bar. Now lets find X
				for ind in range(20):
					hp_pixel_C = frame[hp_bar_y,hp_bar_x_start + ind,1]
					if hp_pixel_C == 24 or hp_pixel_C == 25:
						hp_pixel_D = frame[hp_bar_y,hp_bar_x_start + ind+ 1,1]
						if hp_pixel_D == 24 or hp_pixel_D == 25:
							hp_bar_x = hp_bar_x_start + ind
							hp_bar_present = True
							break
						#found X of border of  HP-SP bar. Now lets get XY of HP bat itself.

				if hp_bar_present:
					print 'Found HP BAR.'
					
					hp_bar_y +=1	
					hp_bar_x +=1
					HP_abs = 57
					for hp_pixel in range(HP_abs):
						current_pixel_G = frame[hp_bar_y,hp_bar_x+hp_pixel,1]
						if current_pixel_G  ==66:
							HP_abs = hp_pixel
							break
						elif current_pixel_G ==239 or current_pixel_G == 16:
							pass
						else:
							print 'PROBABLY HP bar not found correctly'
					HP_pc = int(HP_abs*100.0 / 57)
					self.HP = HP_pc
					print 'HP: %r %%'%HP_pc
				else:
					print 'cant see HP bar!'
					self.HP = -1
			###############################
			###############################
			if task == 'get hp 2': #fast prototyping shit
				t0 = time.time()
				target = 'red-hp'
				res = self.match_feature(target)
				print 'reading red-hp took %r seconds'%(time.time()-t0)
			
				if res[0]:
					print 'HP BAR IS RED! Need to heal fast!'
					self.HP = 10 #fast prototyping shit
				else:
					self.HP = 99 #fast prototyping shit
					print 'ok'
				
			###############################
			if task == 'screenshot':
				self.grab(show=1)
			###############################
			if task == 'use healer':
				print 'using healer'
				target = 'healer'
				res = self.match_feature(target)
				if res[0]:
					print 'healer found.'
					pos = res[1]
					self.lClick(pos[0], pos[1]+20)
				self.grab(show=0)
				self.tasks = ['get hp 2',] + self.tasks
				
				time.sleep(2)
			###############################		
			if task == 'hunt pink':
				if task_found == True:
					self.tasks = self.tasks + ['find and click pink',]*3
				else:
					self.type_line('Q',ENTER=False)
					time.sleep(1)
					self.tasks = self.tasks + ['find and click pink',]*3
				self.tasks.append('hunt pink')
			###############################
			if task == 'go to town':
				print 'going to town'
				#self.focus()
				time.sleep(0.1)
				self.kb.PressKey('1')
				time.sleep(0.1)

				self.kb.ReleaseKey('1')
				time.sleep(5)
				#now check that we are in geffen.
			###############################
			if task == 'get minimap':
				t0 = time.time()
				self.current_map = 'unknown'
				targets = ['gon-dun01-minimap', 'geffen-minimap']
				for t in targets:
					res = self.match_feature(t)
					if res[0]:
						self.current_map = '-'.join(t.split('-')[:-1])
						unknown_minimap_counter = 0
						break
				print 'Current map: ', self.current_map
				if self.debug:
					print "'get minimap' took: ", time.time() - t0
			
			
			###############################
			if task == 'open-inventory-I':
				print 'assuming inventory IS already open. Clicking _I_'
				target = 'inv-I-label'
				res = self.match_feature(target)
				time.sleep(1)
				if not res[0]:
					print 'failed to locate _I_. This should not happen.HALT!'
					sys.exit()
				else:
					pos = res[1]
					self.lClick(pos[0], pos[1])
					self.mouse_move_line(0,0)
					print 'Should have opened _I_ tab'
			
			###############################
			if task == 'open-inventory-M':
				print 'assuming inventory IS already open. Clicking _M_'
				target = 'inv-M-label'
				try:
					self.feature_ROI.pop(target)
				except Exception as e:
					pass
				res = self.match_feature(target)
				time.sleep(1)
				if not res[0]:
					print 'failed to locate _M_. This should not happen.HALT!'
					sys.exit()
				else:
					pos = res[1]
					self.lClick(pos[0], pos[1])
					self.mouse_move_line(0,0)
					print 'Should have opened _M_ tab'
					
			###############################
			if task == 'open-inventory-E':
				print 'assuming inventory IS already open. Clicking _E_'
				target = 'inv-E-label'
				try:
					self.feature_ROI.pop(target)
				except Exception as e:
					pass
				res = self.match_feature(target)
				time.sleep(1)
				if not res[0]:
					print 'failed to locate _E_. This should not happen.HALT!'
					sys.exit()
				else:
					pos = res[1]
					self.lClick(pos[0], pos[1])
					self.mouse_move_line(0,0)
					print 'Should have opened _E_ tab'
			###############################
			if task == 'unfold-basic-info':
				frame = self.grab().copy()
				time.sleep(0.3)
				print 'check if basic info is folded by looking for ZENY label'
				target = 'zeny-label'
				res = self.match_feature(target)
				if not res[0]: #not found zeny label. need to unfold.
					print 'basic info folded. unfolding'
					target = 'unfold-basic-info'
					res = self.match_feature(target)
					if not res[0]: #not found UNFOLD BUTTON
						print 'cant find BASIC INFO button! HALT!'
						sys.exit()
						
					else:
						print 'clicking to unfold basic info'
						pos = res[1]
						self.mouse_move_line(pos[0]+4, pos[1]+3,interval=0.1)
						time.sleep(0.3)
						self.lClick()
						time.sleep(0.3)
						self.mouse_move_line(0,0)
						time.sleep(0.3)
					#now checking that basic info is unfolded.
					target = 'zeny-label'
					res = self.match_feature(target)
					if not res[0]:
						print 'could not get basic info window. HALTING'
						sys.exit()
					else:
						print 'unfolded basic info.'
				
				else:
					print 'unfolded basic info. '
			###############################
			
			###############################
			if task == 'check weight':
				print 'checking weight'
				
				frame = self.grab().copy()
				time.sleep(0.3)
				print 'check if basic info is folded by looking for ZENY label'
				target = 'zeny-label'
				res = self.match_feature(target)
				if not res[0]: #not found zeny label. need to unfold.
					print 'basic info folded. unfolding'
					target = 'unfold-basic-info'
					
					self.mouse_move_line(400,400)
					time.sleep(0.3)
					res = self.match_feature(target)
					if not res[0]: #not found UNFOLD BUTTON
						print 'cant find BASIC INFO button! HALT!'
						sys.exit()
						
					else:
						print 'clicking to unfold basic info'
						pos = res[1]
						unfold_button = pos
						self.mouse_move_line(pos[0]+3, pos[1]+3,interval=0.5)
						time.sleep(0.3)
						self.lClick(pos[0]+3, pos[1]+3)
						time.sleep(0.3)
						self.mouse_move_line(0,0)
						time.sleep(0.3)
					#now checking that basic info is unfolded.
					target = 'zeny-label'
					frame = self.grab().copy()
					time.sleep(0.3)
					res = self.match_feature(target)
					if not res[0]:
						print 'could not get basic info window. HALTING'
						sys.exit()
					else:
						print 'unfolded basic info.'
				
				else:
					print 'unfolded basic info. now looking for RED WEIGHT label.'
					#pos = res[1]
					#self.grab(x=pos[0]-40, y = pos[1]-8, w = 65, h = 16, show = 1)
				target = 'weight-red-label'
				res = self.match_feature(target)
				if res[0]:
					print 'RED LABEL WEIGHT! unloading loot'
					tasks = list(self.tasks)
					self.tasks = ['get_kafra_pos',]
					self.tasks.append('open-inventory')
					self.tasks.append('open-inventory-I')
					self.tasks.append(('drag to bank','jelly'))
					self.tasks.append(('drag to bank','branch'))
					self.tasks.append(('drag to bank','banana'))
					self.tasks.append(('drag to bank','honey'))
					self.tasks.append(('drag to bank','apple'))
					self.tasks.append(('drag to bank','obb'))
					self.tasks.append('open-inventory-M')
					self.tasks.append(('drag to bank','loot1'))
					self.tasks.append(('drag to bank','loot2'))
					self.tasks.append(('drag to bank','loot3'))
					self.tasks.append(('drag to bank','loot4'))
					self.tasks.append(('drag to bank','loot5'))
					self.tasks.append(('drag to bank','peach-loot'))
					self.tasks.append('close-inventory')
					self.tasks.append('close-bank')
					self.tasks.append('toogle chat')
					
					self.tasks = self.tasks + tasks
				else:
					print 'no overweight yet. continuing operation...'
				self.mouse_move_line(0,0)
				time.sleep(0.5)
				target = 'unfold-basic-info'
				res = self.match_feature(target)
				pos = res[1]
				self.mouse_move_line(pos[0]+4, pos[1]+3,interval=0.5)
				time.sleep(0.5)
				self.lClick()
				print 'finished inventory overweight check.'
				
			###############################
			if task == 'toogle chat':
				self.focus()
				time.sleep(0.5)
				frame = self.grab()
				target = 'chat-active-label'
				res = self.match_feature(target)
				if res[0]:
					self.HitKey('RETURN')
				else:
					pass
			###############################
							
			###############################
			if task == 'find and click tree':
				
				self.focus()
				
				if self.HP >= 0 and self.HP < 40:
					print 'LOW HP TRIGGER! Going to town to healer'
					self.tasks = ['go to town',
								'use healer',
								'check weight',
								'check ammo',
								'get hp 2', 
								'use last warp',
								task]
					continue
					self.frame = self.grab().copy()
					
				if task_counter % 10 == 0:
					print 'checking sp!'
					target = 'red-sp'
					res = self.match_feature(target)
					if res[0]:
						print 'LOW SP DETECTED!'
						self.tasks = ['go to town',
								'use healer',
								'get hp 2', 
								'use last warp',
								task]
						continue
				
				if time.time() - buff1_prev > 180:
					buff1_prev = time.time()
					#BUFFING self
					self.HitKey('F',ENTER=False)
					time.sleep(2)
					self.HitKey('B', ENTER=False)
					time.sleep(2)

				if time.time() - buff2_prev> 90:
					buff2_prev = time.time()
					self.HitKey('F',ENTER=False)
					time.sleep(1.4)
					self.HitKey('T', ENTER=False)
				coords = get_coords(self)
				print 'player position:', coords
				task_counter +=1
				print 'task_counter:', task_counter
				
				if task_counter > 25001:
					self.tasks = ['go to town',]
					self.tasks.append('halt')
					t0 =  time.time() - loop_started
					print 'Finished %r loops in %r seconds. check loot'%(task_counter, int(t0)) 
				img = self.grab()
				hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
				hsv[:160,566:,:]=0
				hsv[:160,490:,:]=0
				hsv[380:480,:,:] = 0
				hsv[0:90,:,:] = 0
				lo = np.array([46,60,220])
				hi = np.array([51,70,255])
				mask = cv2.inRange(hsv, lo, hi)
				mask_rad = mask/2 + rad/10
				if mask.max() !=0:
					print 'Found tree! Clicking'
					task_found = True
					mask_rad = mask/2 + rad/10
					(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask_rad)
					pos = maxLoc
					
					#####################
					### In case we are staying too long on the same spot:
					#############
					if coords != prev_coords:
						prev_coords_time = time.time() #new player coordinates time
						prev_coords = list(coords) #update previous coordinates
					else:
						#same coordinates.staying in place!
						if time.time() - prev_coords_time > 3:
							#staying in place for more then 4 seconds!
							self.tasks = ['teleport',] + self.tasks
					####################
					
					self.mouse_move_line(pos[0],pos[1]+10,interval=0.05) #hit the target
					self.lClick()
					time.sleep(0.05)
					self.HitKey('X', ENTER=False)
					
				else:
					print 'NO TREES FOUND!'
					task_found = False
					self.tasks = ['teleport']
					self.tasks.append('get minimap')
					#self.tasks.append(task)
				
				if task_counter % 1000 == 0: #a trick to force going to town
					self.HP = 1
				print '[[HP]]: ', self.HP
				
				if self.current_map == 'unknown':
					unknown_minimap_counter +=1
					print 'Failed to ID minimap: ',unknown_minimap_counter
					if unknown_minimap_counter > 8:
						print 'Check gon_dun02 and gonryun!'
						target = 'gon-dun02-minimap'
						res = self.match_feature(target)
						target = 'gonryun-minimap'
						res2 = self.match_feature(target)
						if res[0] or res2[0]:
							print 'we are at gon_dun02! going back...'
							self.tasks = ['go to town', 'use last warp']
							self.current_map = 'geffen'
						else:
							print 'UNKNOWN MAP! PROBABLY a prison!'
							print 'God help us all! Hope Vadim is near the computer.'
							self.tasks = [halt]
							for i in range(100):
								beep(1000,300)
								beep(1500,300)
								beep(2000,300)
							print 'If bot hasnt been freed from prison during this silent moment'
							print 'he"s probably already banned. /sob....'
				elif self.current_map == 'geffen':
					self.tasks.append('go to town')
					self.tasks.append('use last warp')
				self.tasks.append('get hp 2') ####### !!!!!!!!!!! change to "get hp" if needed
				self.tasks.append(task)
				self.tasks.append('get minimap')

				if ctypes.windll.user32.GetAsyncKeyState(0x91) != 0:
					self.tasks.append(halt)
				#time.sleep(1)
			###############################
			
			if task == 'find and click coco':
				pixel_to_click_G = 0
				self.focus()
				time.sleep(0.1)
				img = self.grab(show = 0)[:,:,0]
				img[:160,566:]=0
				img[:160,490:]=0
				img[380:480,:] = 0
				img[0:90,:] = 0
				img[190:290,300:340]=0
				img[img<255] = 0
				#cv2.imwrite('test.png', img)
				
				mask_rad = img/2 + rad/10
				(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask_rad)
				pos = maxLoc
				if img.max() !=0:
					print 'Found coco! Clicking'
					self.mouse_move_line(pos[0],pos[1],interval=0.1) #hit the target
					self.lClick()
					self.mouse_move_line(0,0)
					print 'clicked somewhere'
					self.tasks.append('get strawberry')
					time.sleep(1)
				else:
					print 'NO COCO FOUND!'
					#task_found = False
					#self.tasks = ['teleport2']
					teleport_counter +=1
					if teleport_counter % 8 == 0:
						self.tasks = ['teleport2']
					time.sleep(0.2)
					
					img = self.grab()
					while pixel_to_click_G != 58:
						new_phi = 3.14*2*random.random()
						new_R_100_part = int(100*random.random())
						new_x = int(new_R_100_part + 220 + 200*math.cos(new_phi))
						new_y = int(new_R_100_part + 140 + 150*math.sin(new_phi))
						pixel_to_click_G = img[new_y, new_x][1]
					self.mouse_move_line(new_x,new_y)
					self.lClick()
					time.sleep(1)
					img = self.grab()
					fname = 'C:/LAB/' + str(int(time.time())) + '.png'
					#cv2.imwrite(fname, img)
					time.sleep(7)
				self.tasks.append(task)
				
				
			###############################
			if task == 'find and click blue':
				pixel_to_click_G = 0
				self.focus()
				
				time.sleep(0.05)
				img = self.grab(show = 0)
				
				
					
				hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
				lo = np.array([119,254,254])
				hi = np.array([120,255,255])
				mask = cv2.inRange(hsv, lo, hi)
				if mask.max() == 255:
					mask_rad = mask/2 + rad/10
					mask_rad[:100,:100] = 0
					time.sleep(0.05)
				
					#cv2.imwrite('test.png', mask_rad)
					(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask_rad)
					pos = maxLoc
					print pos, maxVal
					if pos[1] < 10:
						self.tasks = ['teleport3']
						self.tasks.append(task)
						continue
					if img.max() !=0:
						print 'Found blue! Clicking'
						self.mouse_move_line(pos[0],pos[1],interval=0.03) #hit the target
						self.lClick()
						#self.mouse_move_line(0,0)
						print 'clicked somewhere'
						#self.tasks.append('get karvo')
						#time.sleep(1)
					else:
						print 'NO BLUE FOUND!'
						self.tasks = ['toogle chat']
						self.tasks.append('teleport3')
						time.sleep(0.1)
				else:
					print 'NO BLUE FOUND!'
					self.tasks = ['toogle chat']
					self.tasks.append('teleport3')
					time.sleep(0.1)
				task_counter +=1
				self.tasks.append(task)
				if task_counter % 1000 == 0:
					time.sleep(120)
			###############################
			if task == 'find and click sleeper':
				pixel_to_click_G = 0
				self.focus()
				tasks_after_teleport +=1
				print 'attack task:', tasks_after_teleport
				time.sleep(0.01)
				img = self.grab(show = 0)
				
				
				if tasks_after_teleport > 50:
					tasks_after_teleport = 0
					self.tasks = ['teleport3']
					self.tasks.append(task)
					continue
				hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
				lo = np.array([119,254,254])
				hi = np.array([120,255,255])
				mask = cv2.inRange(hsv, lo, hi)
				if mask.max() == 255:
					mask_rad = mask/2 + rad/10
					mask_rad[:100,:100] = 0
					time.sleep(0.01)
				
					#cv2.imwrite('test.png', mask_rad)
					(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask_rad)
					pos = maxLoc
					print pos, maxVal
					if maxVal > 124:
						tasks_after_teleport = 0
						self.tasks = ['toogle chat']
						self.tasks.append('teleport3')
						self.tasks.append(task)
						continue
					if pos[1] < 10:
						tasks_after_teleport = 0
						self.tasks = ['teleport3']
						self.tasks.append(task)
						continue
					if img.max() !=0:
						print 'Found blue! Clicking'
						self.mouse_move_line(pos[0],pos[1],interval=0.03) #hit the target
						self.lClick()
						#self.mouse_move_line(0,0)
						print 'clicked somewhere'
						#self.tasks.append('get karvo')
						#time.sleep(1)
					else:
						print 'NO BLUE FOUND!'
						tasks_after_teleport = 0
						self.tasks = ['toogle chat']
						self.tasks.append('teleport3')
						time.sleep(0.1)
				else:
					tasks_after_teleport = 0
					print 'NO BLUE FOUND!'
					self.tasks = ['toogle chat']
					self.tasks.append('teleport3')
					time.sleep(0.1)
				#sys.exit()
				#if task_counter % 10 == 0:
				#self.tasks.append('toogle chat')
				task_counter +=1
				self.tasks.append(task)
				if task_counter % 1000 == 0:
					time.sleep(120)
			###############################
			if task == 'get karvo':
				print 'looking for karvo'
				time.sleep(2)
				target = 'karvo'
				frame = self.grab(show = 0)
				res = self.match_feature(target, frame=frame)
				if res[0]:
					print 'found karvo'
					pos = res[1]
					self.mouse_move_line(pos[0],pos[1],interval=0.1) #hit the target
					self.lClick()
					self.mouse_move_line(0,0)
					time.sleep(2)
				else:
					print 'no karvo found'
				frame = self.grab(show = 0)
				print 'looking for spore'
				target = 'mushroom-spore'
				res = self.match_feature(target, frame=frame)
				if res[0]:
					print 'found spore'
					pos = res[1]
					self.mouse_move_line(pos[0],pos[1],interval=0.1) #hit the target
					self.lClick()
					self.mouse_move_line(0,0)
					time.sleep(2)
				else:
					print 'no spore found'
			###############################
			if task == 'get strawberry':
				time.sleep(2)
		
				target = 'strawberry'
				res = (True,True)
				while res[0] == True:
					frame = self.grab(show = 0)
					frame[:,580:,:] =0
					frame[:160,566:,:]=0
					frame[:160,490:,:]=0
					frame[380:480,:] = 0
					frame[0:90,:] = 0
					frame[200:245,310:330,:]=0
					res = self.match_feature(target, frame=frame)
					if res[0]:
						print 'found strawberry'
						pos = res[1]
						self.counter_strawberry +=1
						self.counter_zeny = self.counter_zeny  + 2000
						self.per_hour_strawberry = self.counter_strawberry * 3600.0 / (time.time() - self.start_time)
						self.per_hour_zeny = self.counter_zeny * 3600.0 / (time.time() - self.start_time)
						
						self.mouse_move_line(pos[0],pos[1],interval=0.1) #hit the target
						self.lClick()
						self.mouse_move_line(0,0)
						time.sleep(2)
									
					else:
						print 'no strawberry found!!'
				target = 'acorn'
				res = (True,True)
				while res[0] == True:
					frame = self.grab(show = 0)
					frame[:,580:,:] =0
					frame[:160,566:,:]=0
					frame[:160,490:,:]=0
					frame[380:480,:] = 0
					frame[0:90,:] = 0
					frame[200:245,310:330,:]=0
					res = self.match_feature(target,frame=frame)	
					if res[0]:
						print 'found acorn!!!'
						self.counter_acorn +=1
						self.counter_zeny = self.counter_zeny + 500
						self.per_hour_acorn  = self.counter_acorn * 3600.0 / (time.time() - self.start_time)
						self.per_hour_zeny = self.counter_zeny * 3600.0 / (time.time() - self.start_time)
						pos = res[1]
						self.mouse_move_line(pos[0],pos[1],interval=0.1) #hit the target
						self.lClick()
						time.sleep(0.1)
						self.mouse_move_line(0,0)
						time.sleep(2)
					else:
						print 'no acorn found'
				print 'current ZPH:', int(self.per_hour_zeny)
				print 'current earnt zeny:', int(self.counter_zeny)
				
			###############################	
			if task == 'teleport':
				print 'TELEPORTING!'
				self.tasks.append('get minimap')
				self.HitKey('Q', ENTER=False)
				time.sleep(1)
				
			if task == 'teleport2':
				print 'TELEPORTING!'
				#self.tasks.append('get minimap')
				self.HitKey('Q', ENTER=False)
				time.sleep(1)	
			###############################
			if task == 'teleport3':
				print 'TELEPORTING!'
				#self.tasks.append('get minimap')
				self.HitKey('Q', ENTER=False)
				time.sleep(0.5)
				self.HitKey('RETURN', ENTER=False)
				time.sleep(1)
			###############################
			if len(self.tasks) == 0:
				print 'ZERO tasks in task list. Adding IDLE'
				self.tasks.append(idle)
			
	def update_features(self):
		f_conf = open('features_conf.csv', 'r')
		f_conf_data = f_conf.readlines()[2:]
		f_conf.close()
				
		filenames = filter(lambda x: x.count(self.game) != 0, os.listdir('features/'))
		names = map(lambda x: '-'.join(x[:-4].split('_')[0].split('-')[2:]), filenames)
		
		self.feature_names = names
		self.feature_filenames = filenames
		self.feature_ROI_static = dict(zip(self.feature_names, [False for fn in self.feature_names]))
		#print self.feature_ROI_static

		self.feature_images = dict(zip(self.feature_names, map(lambda x: cv2.imread('features/' + x), filenames))) 
		
		####
		#### FIX ROI!!!
		####

		for ind, line in enumerate(f_conf_data):
			### break if row-separator '#END' is met
			if line.count('#END') == 1:
				print 'Loaded %r FEATURES CONFIGURATION from CSV.'%ind
				break

			### extract columns
			cols = [_line.strip() for _line in line.split('\t')]
			name , threshold = cols[0], cols[1]
			
			if threshold[0].strip() == '0':
				self.feature_thr[name] = float(threshold.replace(',','.').strip())
				#print 'CSV threshold:',threshold, name, self.feature_thr[name]
			
			static = cols[2]
			
			### Exctact ROI
			if bool(int(static)):
				_roi = RECT(POINT(0,0), POINT(0, 0))		
				static_roi = [int(data) for data in cols[3].split('.')]
				
				#print '{6}',self.w ,static_roi
				if static_roi[0] < 0: ###counting ROI fron right border
					_roi.a.x = self.w + static_roi[0]
					#print '{5}', _roi.a.x
				else:
					_roi.a.x = static_roi[0]
				if static_roi[1] < 0:
					_roi.a.y = self.h + static_roi[1]
				else:
					_roi.a.y = static_roi[1]
				if static_roi[2] < 0: ###counting ROI fron right border
					_roi.b.x = self.w + static_roi[2]
				else:
					_roi.b.x = static_roi[2]
				if static_roi[3] < 0:
					_roi.b.y = self.h + static_roi[3]
				else:
					_roi.b.y = static_roi[3]
				self.feature_ROI[name] = _roi
				self.feature_ROI_static[name] = True
				if self.debug == 1:
					print name, 'Added static_ROI:',static_roi, _roi.a.x,_roi.a.y,_roi.b.x,_roi.b.y
			else:
				self.feature_ROI_static[name] = False
				
			#print 'end NAME:' ,name 	
			### Extract color mode 
			###		needed this because of the minimap changing color regulary
			color_mode = cols[4]
			
			#DEBUG
			if self.debug and color_mode[0] == 'h':
				print color_mode
			
			
			if color_mode == 'rgb':
				pass
			if color_mode == 'lap':
				lap = cv2.Laplacian(self.feature_images[name], cv2.CV_64F)
				self.feature_images[name] = lap
			if color_mode[:3] == 'hsv':
				if self.debug:
					print 'We need to convert frame to hsv within ROI'
			self.feature_color_mode[name] = color_mode
			#print 'color_mode:', color_mode
		#names = filter(lambda x: x in f_conf_names, names)
		
		if self.debug == 1:
			for item in self.feature_names:
				print(item)
		return self.feature_names

	def match_feature(self,feature_name, 
					frame = None, 
					mono = False,
					threshold = 0.9, 
					region = None,
					):
		"""
		1,3,5 - NORMED methods
		1 - SQDIFF
		"""
		
		if self.debug == 1:
			_begin = time.time()
		methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
		method = 3 #CHOOSE BEST METHOD
				
		templ = self.feature_images[feature_name]
		
		### get THRESHOLD from dict if set
		if feature_name in self.feature_thr.keys():
			threshold = self.feature_thr[feature_name]
			
		### determine ROI:
		if feature_name in self.feature_ROI.keys(): ### if ROI is set and strict
			roi = self.feature_ROI[feature_name]
		elif self.feature_ROI_static[feature_name]: ### is ROI is static
			roi = self.feature_ROI[feature_name]
			if self.debug:
				print 'static roi:',roi.a.x,roi.a.y,roi.b.x, roi.b.y 
		else: 
			roi = RECT(POINT(0,0), POINT(self.w-1, self.h-1))
		
		if type(frame) == type(None): ### if new frame if grabbed.
			frame = self.grab(show = 0)

		if type(roi) == type(None): ### ROI of the feature is unknown.
			pass
		else:
			### lets get ROI from where feature was last seen.
			### print 'ROI DIMS: ', roi.b.x - roi.a.x, roi.b.y - roi.a.y
			### print 'TEMPL dims: ', templ.shape
			infos = """
			ADDED THIS STRING TO DISABLE ROI SHIT:
			roi = RECT(POINT(0,0), POINT(self.w-1, self.h-1))
			"""
			#roi = RECT(POINT(0,0), POINT(self.w-1, self.h-1))
			
			
			_frame = frame[ roi.a.y : roi.b.y + 1,roi.a.x : roi.b.x + 1, :]
			frame = _frame
			#if self.debug:
			#	print '_frame:', _frame.shape, _frame.dtype
			#	print 'frame:', frame.shape, frame.dtype			
		### if single channel - which one to choose? Red ?.
		if mono and frame.ndim >2 and frame.shape[2] >1:
			if mono == True:
				channel = 0
			elif mono in [0,1,2]:
				channel = mono
			frame = frame[:,:,channel]
			templ = templ[:,:,channel]
		
		### if HSV:
		# load hsv coords, transform frame.
		colod_mode = self.feature_color_mode[feature_name]
		if colod_mode[:3] == 'hsv':
			colorLO = np.array([int(x) for x in colod_mode.split('.')[1:4]])
			colorHI = np.array([int(x) for x in colod_mode.split('.')[4:]])
			#if self.debug:
			#	print 'colorLO:, HO: ', colorLO,colorHI
			#print 'HSV shapes:', frame.shape, templ.shape			
			_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			#if self.debug:
			#	
			#	print 'frame:', frame.shape, frame.dtype
			_templ = cv2.cvtColor(templ, cv2.COLOR_BGR2HSV)
			#time.sleep(1)
			frame = cv2.inRange(_frame, colorLO, colorHI) 
			templ = cv2.inRange(_templ, colorLO, colorHI) 
			#print 'after hsv conversion:', frame.shape, templ.shape
		#print frame.shape, templ.shape
		res = cv2.matchTemplate(frame, templ, method)
		(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(res)
		
		if method in [0,1]: #MIN: 0,1 
			Val = minVal
			_Loc = minLoc
		elif method in [2,3,4,5]: # MAX:  3,4,5
			Val = maxVal
			_Loc = maxLoc
		
		if method == 1:
			Val = 1.0-Val #adjusting minimal SQDIFF to use threshold. 
		
		Loc = (_Loc[0] + roi.a.x, _Loc[1] + roi.a.y)
		Loc_center = (Loc[0] + templ.shape[1]/2 , Loc[1] + templ.shape[0]/2)
		if Val < threshold:
			found = False
			x, y = None, None
			try:
				self.feature_missed[feature_name] +=1
				if not self.feature_ROI_static[feature_name]:
					if self.feature_missed[feature_name] == 10 :
						self.feature_ROI.pop(feature_name)
					#self.feature_missed[feature_name] = 0
					
			except Exception as _e:
				self.feature_missed[feature_name] = 1
				
			
		else:
			found = True
			self.feature_missed[feature_name] = 0
			x, y = Loc_center[0] , Loc_center[1] 
			
			self.feature_pos[feature_name] = (x,y)
			
			#DEBUG
			#print self.feature_pos[feature_name]
			
			# set ROI of a found feature
			ROI = RECT(POINT(Loc[0], 
			Loc[1]), 
			POINT(Loc[0] + templ.shape[1] ,
			Loc[1]+ templ.shape[0] )
			)
			
			### Do not change ROI if it's static
			if self.feature_ROI_static[feature_name] == True:
				pass
			else:
				pass
				#self.feature_ROI[feature_name] = ROI
				#DEBUG
				#print self.feature_ROI[feature_name]
		if self.debug == 1 and found == True:
			print (feature_name, found, (x,y), Val, 'threshold= ', threshold, 'time:', time.time()-_begin)
		
		if self.gui == True and found == True:
			self.last_grab[:,:,:] = self.last_grab[:,:,:] * 0.75
			cv2.rectangle(self.last_grab, (ROI.a.x, ROI.a.y),(ROI.b.x, ROI.b.y), (255,0,0),3)
			
		self.i_see[feature_name] = found
		try:
			if self.feature_ROI_static[feature_name]:
				pass
			else:
				self.feature_ROI.pop(feature_name)
		except Exception as _e:
			if self.debug == 1:
				print 'tried to disable ROI caching. failed! Maybe cache wasnt used?'
				print str(_e)
		
		return (found, (x,y))
				
	
	def get_pid(self):
		cmd = """wmic process where "name='""" + self.exe_fname + "'" + '"' + " get ProcessID"
		#cmd = """wmic where 'name="%r"' get ProcessID"""%self.exe_fname
		res = map(int, filter(lambda y: y!='' and y[0].isdigit(), [x.replace('\r','').strip() for x in sp.check_output(cmd).split('\n')]))
		
		if len(res) == 0:
			if self.debug == 1:
				print("[!] get_pid(): PROCESS NOT FOUND!")
			return None
		elif len(res) >1:
			if self.debug == 1:
				print("[!] get_pid(): DUPLICATE PROCESSES FOUND!")
			return None
		else:
			self.pid = res[0]
			return res[0]
		
	def is_running(self):
		res = self.get_pid()
		if res == None:
			return False
		else:
			return True
	def kill(self):
		cmd = "taskkill /F /PID " + str(self.pid)
		res = os.system(cmd)
		time.sleep(5)
		res = not self.is_running()
		if self.debug == 1:
			if res == True:
				print("Killed client.")
			else:
				print('Could not kill client')
		return res
	
	def launch(self):
		proc = sp.Popen(self.application_string.split(' '))
		time.sleep(3)
		self.pid = self.get_pid()
		if self.pid != None:
			if self.debug == 1:
				print('Launched client. PID:', self.pid)
			return True
		else:
			if self.debug == 1:
				print('Could not launch client. Exit(TODO: retry)')
			return False

	def refresh(self, dbg = True):
		infos = """This is to resresh client window coordinates."""
		#if self.pid and self.hwnd:
		#if dbg:
		#print("pid: ", pid)
		#print infos
		self.hwnd = ctypes.windll.user32.FindWindowW(0, self.title)
		wi = WINDOWINFO()
		res = ctypes.windll.user32.GetWindowInfo(self.hwnd, ctypes.pointer(wi)) 
		#print "Refresh window data:\n"
		self.wi = wi
		self.rc = wi.rcClient
		
		self.top = self.wi.rcClient.a.y
		self.bottom = self.wi.rcClient.b.y
		self.right = self.wi.rcClient.b.x
		self.left = self.wi.rcClient.a.x
		self.w = self.right - self.left
		self.h = self.bottom - self.top
		self.x = self.left
		self.y = self.top
		self.window = self.wi.rcWindow
		self.x_wnd = self.window.a.x
		self.y_wnd = self.window.a.y
		self.w_wnd = self.window.b.x - self.window.a.x
		self.h_wnd = self.window.b.y - self.window.a.y
		#print "self.top, self.left :", self.top, self.left
		#print "While making screenshots, try using client.x AND client.x_wnd !!!"
	def move_window(self):
		infos = """
		BOOL WINAPI MoveWindow(
	_In_ HWND hWnd,
	_In_ int  X,
	_In_ int  Y,
	_In_ int  nWidth,
	_In_ int  nHeight,
	_In_ BOOL bRepaint
		);
		"""
	def resize_window(self, w=776,h=600):
		self.refresh()
		x_borders = self.left - self.window.a.x + self.right - self.window.b.x
		y_borders = self.top - self.window.a.y + self.window.b.y - self.bottom
		
		w_wnd_new = x_borders + w
		h_wnd_new = y_borders + h
		if self.debug == 1:
			print 'BORDERS: ', x_borders, y_borders
			print 'New W,H: ', w_wnd_new, h_wnd_new, '|', w,h
	
		ctypes.windll.user32.SetWindowPos(self.hwnd, 0, self.x_wnd, self.y_wnd, w_wnd_new, h_wnd_new,0x0004)
		self.refresh()
		
	def focus(self):
		self.refresh()
		fAltTab = True
		_SwitchToThisWindow = ctypes.windll.user32.SwitchToThisWindow
		_SwitchToThisWindow(self.hwnd, fAltTab)

	def grab(self, x=0, y=0, w = 0, h = 0, show = 0):
		
		self.i_see = {}
		x_border_offset = self.left - self.x_wnd #BORDER?
		y_border_offset = self.top - self.y_wnd	#BORDER?
		if w == 0:
			w = self.w
		if h == 0:
			h = self.h
		x = x + x_border_offset
		y = y + y_border_offset
		
		res = capture(hwnd = self.hwnd,x=x , y=y, w = w, h = h, show = show)
		if self.gui:
			#_frame = np.zeros((self.h, self.w))
			lap = cv2.Laplacian(res, cv2.CV_64F)
			self.last_grab[:,:,:] = self.last_grab[:,:,:]*0.9
			cv2.imwrite('images-pile/%r.png'%self.i, self.last_grab)
			print res.shape, x,y,w,h
			print lap.shape, self.w, self.h, self.last_grab.shape
			try:
				self.last_grab[:, :, :] = self.last_grab[:, :, :]*0.5 +  lap[:,:,:]*0.5
			except Exception as _e:
				self.last_grab = np.zeros((self.h, self.w, 3))
				self.last_grab[y- y_border_offset:y- y_border_offset +h, x - x_border_offset :x+w- x_border_offset, :] = lap[:,:,:].copy()
				print 'EXCEPTION!', str(_e)
			#self.last
			self.i = self.i + 1
		self.frame = res
		return res
	
	def grab_roi(self, roi):
		if type(roi) != ROI:
			if debug:
				print 'grab_roi NEEDS ROI-class'
		else:
			### extract x,y,w,h
			x,y,x1,y1 = roi.a.x, roi.a.y,roi.b.x,roi.b.y
			w,h = x1-x, y1-y
			x_border_offset = self.left - self.x_wnd #BORDER?
			y_border_offset = self.top - self.y_wnd	#BORDER?
			x = x + x_border_offset
			y = y + y_border_offset
			res = capture(hwnd = self.hwnd,x=x , y=y, w = w, h = h, show = show)
		return res
		
	def feature_grab_loop(self):
		self.resize_window()
		while ctypes.windll.user32.GetAsyncKeyState(0x1B) == 0:
			inp = raw_input("Set filename for next feature image OR 'x' to finish:\n")
			#Example:
			#dialog-npc-banker-first-label
			#dialog-npc-banker-first-proceed-ready-to-click
			if inp == 'x':
				break
			print("Is this correct? \n " + inp + "\n [y] or [n] only.")
			control = str(raw_input('\n : '))
			if control != 'n' and control != 'y':
				print("wrong answer. try again.")
				time.sleep(1)
				continue
				#sys.exit()
			if control == 'n':
				#restart loop
				continue
			if control == 'y':
				print("Set cursor to the left upper feature ROI point is and hit Scroll-Lock.")
				self.focus()
				time.sleep(0.5)
				while ctypes.windll.user32.GetAsyncKeyState(0x91) == 0: #scroll lock
					time.sleep(0.2)
					pA = gcp()
					print 'First point:', pA
				
				#print("Captured cursor position is:  " + str(posA))
				#print("\n Now set cursor to right lower point of the feature rectangle")
				time.sleep(1)
				self.focus()
				time.sleep(0.5)
				while ctypes.windll.user32.GetAsyncKeyState(0x91) == 0:
					time.sleep(0.2)
					pB = gcp()
					print 'second point:', pB
				time.sleep(0.3)
				
				print("pA pB:" , pA.x,pA.y,'\t', pB.x, pB.y)
				feature_left = pA.x - self.left
				feature_top = pA.y - self.top
				feature_right = pB.x - self.left
				feature_bottom = pB.y - self.top
				print(feature_left , " ",feature_top , " ",feature_right , " ",feature_bottom , " ")  
				res = self.grab()

				feature_image = res[feature_top:feature_bottom, feature_left:feature_right, :]
				print("Saving image. Go check it and proceed.")
				img_name = "features/"+"feature-" + inp+'_' +str(feature_left)+'-'+str(feature_top)+'-'+str(feature_right)+'-'+str(feature_bottom)+".bmp" 
				cv2.imwrite(img_name, feature_image)
				print("Saved:" + img_name)
				self.update_features()
				print('Updated features dict.')
				print('Edit feature configuration in CSV.')
				with open('feature_conf.csv', 'a+') as f:
					try:
						f.write(inp)
					except Exception as _e:
						print str(_e)
						print 'Could not write to CSV!'
						sys.exit()
				
		self.update_features()
		
	def feature_present(self, feature):
		"""
		Detect filenames, strings, etc
		"""	
		print('FOUND filename for: ', feature)
		index = feature_names.index(feature)
		feature_filename ='features/' +  feature_file_list[index]
		print(feature_filename)
			
		x1,y1,x2,y2 = map(int , feature_filename[:-4].split("_")[1].split('-'))
		print 'x1,y1,x2,y2 : ', x1,y1,x2,y2
		print('Reading file: ', feature_filename)
		feature_img = cv2.imread(feature_filename)
		time.sleep(1)
		
		print 'feature_img: ', feature_img.shape
		w = x2 - x1
		h = y2 - y1
		roi_img = client.grab(x=x1, y=y1, w=x2-x1, h=y2-y1, show=0)
		print 'roi_img: ', roi_img.shape
		delta = roi_img - feature_img
		delta_sum = np.sum(np.abs(delta0))
		
		delta_min = 100
		delta_max = 3000
		if delta_sum < delta_min:
			return True
		elif delta_sum >= delta_min and delta < delta_max:
			return 'NOT SURE'
		else:
			return False
	
	def feature_present_2(self, feature):
		"""
		feature:
			an object with fields:
				-name 
					EXAMPLE: login-welcome
				-filename
					feature-osrs-login-welcome_228-11-4334-11.bmp
				-filename_full
					features/feature-osrs-login-welcome_228-11-4334-11.bmp
				-ref
					some short reference...optional, TODO.
				-img
					np array
				-rect
					
		"""
			#get coords from filename (BETTER: extract while constructing obj)
		t0 = time.time()
		
		roi = self.features[feature]
		feature_img = self.feature_images[feature]
		
		roi_xywh = (roi.a.x, roi.a.y, roi.b.x - roi.a.x, roi.b.y - roi.a.y)
		roi_img = self.grab(*roi_xywh, show = 1)
		delta = roi_img - feature_img
		delta_sum = np.sum(np.abs(delta))
		
		t1 = time.time()
		
		delta_min = 100
		delta_max = 3000
		
		if delta_sum < delta_min:
			res = True
		elif delta_sum >= delta_min and delta_sum < delta_max:
			res =  'NOT SURE'
		else:
			res = False
		if self.debug == 1:
			prefixes = {'True': '+++ ', 'False':'--- ', 'NOT SURE':'~?~ '}
			prefix = prefixes[str(res)]
			print prefix + 'Feature: %r'%feature, 'ROI: ', roi_xywh, 'delta_sum: %r'%str(delta_sum), 'time:'+str(t1-t0)
			report = np.vstack((roi_img, feature_img, delta))
			cv2.imwrite(str(int(time.time())) +'_' + feature+'_report.png', report)
		return res
		
	def feature_interact(self, feature, action='simple L click'):
		pass
		
	def mouse_move(self,x,y):
		if self.debug == 1:
			print('mouse_move: ', x, y)
		MouseMove(self.left + x, self.top + y)
	def mouse_move_line(self,x,y,interval=0.5):
		if self.debug == 1:
			print('mouse_move_line: ', x, y)
		MouseMoveInLine(self.left + x, self.top + y,interval=interval)
	
	def lClick(self, x=0,y=0, delay = 0.1, wait = 0.05):
		if x != 0 and y != 0:
			self.mouse_move(x,y)
		time.sleep(delay)
		lClick()
		time.sleep(wait)
	def type_line(self, line, ENTER=True):
		kb = keyboard()
		kb.TypeLine(line, ENTER)
	def HitKey(self, vCode,ENTER = False):
		kb = keyboard()
		kb.HitKey(vCode)
		
	def rClick(self, x=0,y=0, delay = 0.2, wait = 0.1):
		if x != 0 and y != 0:
			self.mouse_move(x,y)
		time.sleep(delay)
		rClick()
		time.sleep(wait)
		
	def lDrag(self,x,y):
		MouseLeftDown()
		time.sleep(0.3)
		self.mouse_move_line(x,y)
		MouseLeftUp()
		time.sleep(0.4)
		
