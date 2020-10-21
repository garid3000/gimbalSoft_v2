from fbs_runtime.application_context.PyQt5 import ApplicationContext
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from file_reader import *
from _3_2dRGB_plane_1 import *
from _2EARGB_3d_full import *
import shutil

import subprocess
# FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')



import platform
def openExplorer_file(path):
	if platform.system() == 'Windows':
		FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
		subprocess.run([FILEBROWSER_PATH, path])
	elif platform.system() == 'Linux':
		os.system("nautilus " + path)

class tab1(QWidget):
	def __init__(self):
		super(tab1, self).__init__()

		appctxt = ApplicationContext()
		self.logsDir = appctxt.get_resource('_logs_/lastDir.tmp')		
		self.imgsDir = appctxt.get_resource('_imgs_')

		# self.projectDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
		# self.iconsDir = os.path.join(self.projectDir, 'src','main','icons')
		# self.logsDir = os.path.join(self.projectDir, 'src','main','_logs_', 'lastDir.tmp')
		# self.imgsDir = os.path.join(self.projectDir, 'src','main','_imgs_')
		# self._4_3d_ = os.path.join(self.projectDir, 'src','main','python', '4_3dViEW.py')
		# self.three3dDir = os.path.join(self.projectDir, 'src','main','python', 'tmp_s')
		# self.three3dDirCropped = os.path.join(self.projectDir, 'src','main','python', 'tmp_s', 'cropped')
		# self.three3dDirCompiled = os.path.join(self.projectDir, 'src','main','python', 'tmp_s', 'compiled')


		self.meta      = None
		self.numShots  = 0
		self.dir  	   = ''
		self.layout = QGridLayout()
		self.readMeta()


		self.projected2dimg = QPushButton("")  
		self.projected2dimg_without = QPushButton("")  
		self.projected2dimg_color = QPushButton("")  

		self.populate_grp0()
		self.populate_grp1()
		self.populate_grp2()
		self.populate_grp3()
		# self.populate_grp4()

		self.layout.addWidget(self.grp0    ,0,0,1,4)
		self.layout.addWidget(self.grp1    ,1,0,1,1)
		self.layout.addWidget(self.grp2    ,1,1,1,1)
		self.layout.addWidget(self.grp3    ,1,2,1,1)
		# self.layout.addWidget(self.grp4    ,1,3,1,1)
		self.setLayout(self.layout)

	def exploreWindows(self,path):
		# explorer would choke on forward slashes
		path = os.path.normpath(path)
		openExplorer_file(path)
		# if os.path.isdir(path):
		# 	subprocess.run([FILEBROWSER_PATH, path])
		# elif os.path.isfile(path):
		# 	subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])


	def populate_grp0(self):
		self.grp0 = QGroupBox("2D plane projection")
		self.grp0layout = QGridLayout()

		self.projectedIcons = QLabel(self)
		self.pixmap = QPixmap(os.path.join(self.imgsDir,'projectionRadius.png')).scaled(1000, 500, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.projectedIcons.setPixmap(self.pixmap)
		self.projectedIcons.show()

		self.lineRadius = QLineEdit("5.00")
		self.lineRadius.setValidator( QDoubleValidator(0, 100, 8) )

		
		self.preprocess = QPushButton("\tPreprocess")  #2d plant projection
		self.preprocess.clicked.connect(self.Click_preprocess)
		self.preprocess.setIcon(QIcon(os.path.join(self.imgsDir,'gear.png')))
		self.preprocess.setIconSize(QSize(100,100))


		self.grp0layout.addWidget(self.projectedIcons,  0,0,3,1)
		self.grp0layout.addWidget(QLabel("r value"),    0,1,1,1)
		self.grp0layout.addWidget(self.lineRadius, 		0,2,1,1)
		self.grp0layout.addWidget(self.preprocess, 		1,1,1,2)
		self.grp0.setLayout(self.grp0layout)


	def populate_grp1(self):
		self.grp1 = QGroupBox("2D plane projection")
		self.grp1layout = QGridLayout()
		
		self.remake2d_with = QPushButton("Remake")  #2d plant projection
		self.remake2d_with.clicked.connect(self.Click_remake2d_with)
		# self.remake2d_with.setIcon(QIcon(os.path.join(self.imgsDir,'projection','Slide2.PNG')))
		# self.remake2d_with.setIconSize(QSize(300,300))

		self.is2dpresent()
		# self.pixmap = QPixmap(self.dir_2d).scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
		# self.projected2dimg.setPixmap(self.pixmap)
		# self.projected2dimg.show()

		#2d plant projection
		self.projected2dimg.clicked.connect(self.Click_projected2dimg)
		self.projected2dimg.setIcon(QIcon(os.path.join(self.imgsDir,'projection','Slide2.PNG')))
		self.projected2dimg.setIconSize(QSize(400,400))
		self.is2dpresent()


		self.grp1layout.addWidget(self.projected2dimg ,	0,0,1,1, alignment=Qt.AlignCenter)
		self.grp1layout.addWidget(self.remake2d_with, 		1,0,1,1)
		self.grp1.setLayout(self.grp1layout)

		pass

	def update_this_tab(self):
		self.readMeta()
		self.is2dpresent()
		self.is2dpresent_without()
		self.is2dpresent_withColor()


		self.projected2dimg.setIcon(QIcon(self.dir_2d))
		self.projected2dimg_without.setIcon(QIcon(self.dir_2dwithout))
		self.projected2dimg_color.setIcon(QIcon(self.dir_2dColor))
		


	def Click_projected2dimg(self):
		self.exploreWindows(self.dir_2d)
		pass

	def Click_projected2dimg_without(self):
		self.exploreWindows(self.dir_2dwithout)
		pass

	def Click_projected2dimg_color(self):
		self.exploreWindows(self.dir_2dColor)


	def populate_grp2(self):

		self.grp2 = QGroupBox("2D plane projection (with FoV perimeter)")
		self.grp2layout = QGridLayout()
			
		self.remake2d_without = QPushButton("Remake")#2d plant projection
		self.remake2d_without.clicked.connect(self.Click_remake2d_without)
		# self.remake2d_without.setIcon(QIcon(os.path.join(self.imgsDir,'projection','Slide3.PNG')))
		# self.remake2d_without.setIconSize(QSize(300,300))

		self.is2dpresent_without()
		# self.pixmap = QPixmap(self.dir_2dwithout).scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
		# print(self.dir_2dwithout)
		# self.projected2dimg_without.setPixmap(self.pixmap)
		# self.projected2dimg_without.show()
		self.projected2dimg_without.clicked.connect(self.Click_projected2dimg_without)
		self.projected2dimg_without.setIcon(QIcon(os.path.join(self.imgsDir,'projection','Slide2.PNG')))
		self.projected2dimg_without.setIconSize(QSize(400,400))
		self.is2dpresent_without()

		self.grp2layout.addWidget(self.projected2dimg_without ,	0,0,1,1, alignment=Qt.AlignCenter)
		self.grp2layout.addWidget(self.remake2d_without,		1,0,1,1)
		self.grp2.setLayout(self.grp2layout)



		pass

	def populate_grp3(self):

		self.grp3 = QGroupBox("2D plane projection (with FoV colored)")
		self.grp3layout = QGridLayout()
			
		self.remake2d_color = QPushButton("Remake")#2d plant projection
		self.remake2d_color.clicked.connect(self.Click_remake2d_color)
		# self.remake2d_color.clicked.connect(self.Click_remake2d_color)
		# self.remake2d_color.setIcon(QIcon(os.path.join(self.imgsDir,'projection','Slide3.PNG')))
		# self.remake2d_color.setIconSize(QSize(300,300))

		# self.pixmap = QPixmap(self.dir_2dColor).scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
		# print(self.dir_2dColor)
		# self.projected2dimg_color.setPixmap(self.pixmap)
		# self.projected2dimg_color.show()


		self.projected2dimg_color.clicked.connect(self.Click_projected2dimg_color)
		self.projected2dimg_color.setIcon(QIcon(os.path.join(self.imgsDir,'projection','Slide2.PNG')))
		self.projected2dimg_color.setIconSize(QSize(400,400))
		self.is2dpresent_withColor()

		self.grp3layout.addWidget(self.projected2dimg_color ,	0,0,1,1, alignment=Qt.AlignCenter)
		self.grp3layout.addWidget(self.remake2d_color,		1,0,1,1)
		self.grp3.setLayout(self.grp3layout)

		pass

	'''	
	def Click_remake3d(self):

		self.timer = QTimer()
		self.timer.timeout.connect(self.remaknig3dhandleTimer)
		self.timer.start(100)

		self.msgBox = QMessageBox(self)
		self.msgBox.setIcon(QMessageBox.Warning)
		self.msgBox.setText("Warning")
		self.msgBox.setInformativeText("To continue, please close tab, which shows 3d, first then click on the OK button ")
		self.msgBox.setWindowTitle("Warning")
		# self.msgBox.setDetailedText("The details are as follows:"
		self.msgBox.exec_()
		# disconnectButton = messageBox.addButton(self.tr("Disconnect"),  QMessageBox.ActionRole)
		try:
			self.supro.kill()
			self.timer.stop()
			print('self.supro.kill()')
		except:
			pass
			print('some')
			self.timer.stop()
	
	def remaknig3dhandleTimer(self):
		self.timer.stop()
		# shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"4_3dViEW.py"), self.dir + "/tmp.py")
		# self.three3d
		folder = self.three3dDir
		for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))


		folder = self.three3dDirCropped
		for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))


		folder = self.three3dDirCompiled
		for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))



		#################################################################				
		# print('os.listdir(self.dir)', os.listdir(self.dir))
		for filename in os.listdir(os.path.join(self.dir, 'compiled')):
			onlyFname = filename
			filename = os.path.join(self.dir, 'compiled',filename)
			if os.path.isfile(filename):
				print(filename, os.path.isfile(filename))
				file_path = os.path.join(folder, filename)
				shutil.copy(file_path, os.path.join(self.three3dDirCompiled,onlyFname))
				# print(file_path)


		for filename in os.listdir(os.path.join(self.dir, 'cropped')):
			onlyFname = filename
			filename = os.path.join(self.dir, 'cropped', filename)
			if os.path.isfile(filename):
				print(filename, os.path.isfile(filename))
				file_path = os.path.join(folder, filename)
				shutil.copy(file_path, os.path.join(self.three3dDirCropped,onlyFname))
				# print(file_path)

		for filename in os.listdir(os.path.join(self.dir)):
			onlyFname = filename
			filename = os.path.join(self.dir, filename)
			if os.path.isfile(filename) and 'json' in onlyFname:
				print(filename, os.path.isfile(filename))
				file_path = os.path.join(folder, filename)
				shutil.copy(file_path, os.path.join(self.three3dDir,onlyFname))
				# print(file_path)

		###########################################################
		print(self._4_3d_ + ' ' + self.three3dDir)
		# subprocess.call('python ' + self._4_3d_ + ' ' + self.three3dDir)
		print('self.timer.stop()')
		self.supro = subprocess.call('python ' + self._4_3d_ + ' src/main/python/tmp_s')
		# self.doneWorkDone("Task Creating 3d-Plots has been done")
	'''

	def doneWorkDone(self, someTxt):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)

		msg.setText("This is a message box")
		msg.setInformativeText(someTxt)
		msg.setWindowTitle("Information")
		msg.setDetailedText(" ")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()
	'''	
	def populate_grp4(self):

		self.grp4 = QGroupBox("3d projection")
		self.grp4layout = QGridLayout()
		
		self.remake3d = QPushButton("") #3d projection
		self.remake3d.clicked.connect(self.Click_remake3d)
		self.remake3d.setIcon(QIcon(os.path.join(self.imgsDir,'projection','Slide1.PNG')))
		self.remake3d.setIconSize(QSize(300,300))



		self.comboIndex = QComboBox(self)
		self.comboIndex.addItem("Index 1: NDVI")
		self.comboIndex.addItem("Index 2")
		self.comboIndex.addItem("Index 3")
		self.comboIndex.addItem("Index 4")
		self.comboIndex.addItem("Index 5")
		self.comboIndex.addItem("Index 6")
		self.comboIndex.addItem("Index 7")
		self.comboIndex.addItem("Index 8")
		self.comboIndex.addItem("Index 9")
		self.comboIndex.addItem("Index 10")
		


		self.comboColormap = QComboBox(self)
		self.comboColormap.addItem("viridis")
		self.comboColormap.addItem("plasma")
		self.comboColormap.addItem("inferno")
		self.comboColormap.addItem("magma")
		self.comboColormap.addItem("cividis")
		
		self.minValue = QLineEdit()	
		self.maxValue = QLineEdit()

		self.grp4layout.addWidget(QLabel("Index"),		0,0,1,1)
		self.grp4layout.addWidget(self.comboIndex, 		0,1,1,1)
		self.grp4layout.addWidget(QLabel("Colormap"),	1,0,1,1)
		self.grp4layout.addWidget(self.comboColormap,	1,1,1,1)
		self.grp4layout.addWidget(QLabel("Max:"),		2,0,1,1)
		self.grp4layout.addWidget(self.maxValue,		2,1,1,1)
		self.grp4layout.addWidget(QLabel("Min:"),		3,0,1,1)
		self.grp4layout.addWidget(self.minValue,		3,1,1,1)


		self.grp4layout.addWidget(self.remake3d, 		4,0,1,2)
		self.grp4.setLayout(self.grp4layout)


		self.timer = QTimer()
		self.timer.timeout.connect(self.three3d)

		pass
		pass
	'''
	def doneWorkDone(self, someTxt):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)

		msg.setText(someTxt)
		# msg.setInformativeText(someTxt)
		msg.setWindowTitle("Information")
		msg.setDetailedText(" ")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()

	def Click_remake2d_with(self):
		print("Click_remake2d_with")
		self.savingstate = 1
		self.p2d = project_2d(self.dir, show = False, peri = True)
		print("Click_remake2d_with")
		try:
			
			self.msgBox = QMessageBox(self)
			self.msgBox.setIcon(QMessageBox.Information)
			self.msgBox.setText("Making 2D plane projection ")#(with FoV perimeter)
			# self.msgBox.setInformativeText("todo3")
			self.msgBox.setWindowTitle("Processing")
			# self.msgBox.setDetailedText("The details are as follows:")

			self.msgBox.setWindowFlags((self.msgBox.windowFlags() & ~Qt.WindowCloseButtonHint) & ~Qt.WindowSystemMenuHint )


			l = self.msgBox.layout()
			l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()
			self.progress = QProgressBar()
			l.addWidget(self.progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )


			self.msgBox.show()

			self.timer = QTimer()
			self.timer.timeout.connect(self.Handle_Click_remake2d_with)
			self.Handle_Click_remake2d_with_index = 0
			self.timer.start(0)
		except :
			QMessageBox.information(self,"Error","Click on \"Preprocess\" button in this tab and try again.")
		pass
	def Handle_Click_remake2d_with(self):
		if self.Handle_Click_remake2d_with_index == 0:
			self.p2d.calc_stage1()
		elif self.Handle_Click_remake2d_with_index == 1:
			self.p2d.calc_stage2()
		elif self.Handle_Click_remake2d_with_index == 2:
			self.p2d.calc_stage3()
		elif self.Handle_Click_remake2d_with_index == 3:
			self.p2d.calc_stage4()
		elif self.Handle_Click_remake2d_with_index == 4:
			self.p2d.calc_stage5()
		elif self.Handle_Click_remake2d_with_index == 5:
			if self.savingstate == 2:
				self.p2d.addPeri()
			elif self.savingstate == 3:
				self.p2d.addColor()
		elif self.Handle_Click_remake2d_with_index == 6:
			if self.savingstate == 1:
				print('savingstate == 1')
				self.p2d.saveImg()
				self.is2dpresent()
			elif self.savingstate == 2:
				print('savingstate == 2')
				self.p2d.savePeriImg()
				self.is2dpresent_without()
			elif self.savingstate == 3:
				print('savingstate == 3')
				self.p2d.saveFullImg()
				self.is2dpresent_withColor()
		else:
			print('done 123')
			self.timer.stop()
			self.msgBox.done(0)

			self.doneWorkDone("Recreatnig Image is finished")


		self.Handle_Click_remake2d_with_index += 1
		self.p2d.updateMeta()
		self.progress.setValue((self.Handle_Click_remake2d_with_index+1)/7 * 100)

		pass
	def Click_remake2d_without(self):
		try:
			self.savingstate = 2
			print('Click_remake2d_without')
			self.p2d = project_2d(self.dir, show = False, peri = False)
			
			print("Click_remake2d_without")
			self.msgBox = QMessageBox(self)
			self.msgBox.setIcon(QMessageBox.Information)
			self.msgBox.setText("Making 2D plane projection (with FoV perimeter)")
			# self.msgBox.setInformativeText("todo3")
			self.msgBox.setWindowTitle("Processing")
			# self.msgBox.setDetailedText("The details are as follows:")

			self.msgBox.setWindowFlags((self.msgBox.windowFlags() & ~Qt.WindowCloseButtonHint) & ~Qt.WindowSystemMenuHint )


			l = self.msgBox.layout()
			l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()
			self.progress = QProgressBar()
			l.addWidget(self.progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )


			self.msgBox.show()

			self.timer = QTimer()
			self.timer.timeout.connect(self.Handle_Click_remake2d_with)
			self.Handle_Click_remake2d_with_index = 0
			self.timer.start(0)
			pass
		except :
			QMessageBox.information(self,"Error","Click on \"Preprocess\" button in this tab and try again.")


	def Click_remake2d_color(self):
		try:
			self.savingstate = 3
			print("Click_remake2d_color")
			self.p2d = project_2d(self.dir, show = False, peri = True)
			self.msgBox = QMessageBox(self)
			self.msgBox.setIcon(QMessageBox.Information)
			self.msgBox.setText("Making 2D plane projection (with FoV colored)")#
			# self.msgBox.setInformativeText("todo2")
			self.msgBox.setWindowTitle("Processing")
			# self.msgBox.setDetailedText("The details are as follows:")

			self.msgBox.setWindowFlags((self.msgBox.windowFlags() & ~Qt.WindowCloseButtonHint) & ~Qt.WindowSystemMenuHint )


			l = self.msgBox.layout()
			l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()
			self.progress = QProgressBar()
			l.addWidget(self.progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )


			self.msgBox.show()

			self.timer = QTimer()
			self.timer.timeout.connect(self.Handle_Click_remake2d_with)
			self.Handle_Click_remake2d_with_index = 0
			self.timer.start(0)

		except :
			QMessageBox.information(self,"Error","Click on \"Preprocess\" button in this tab and try again.")

		pass
		pass

	def Click_preprocess(self):
		print("This should be preprocess", self.lineRadius.text())
		try:
			self.eargb = EARGB(self.dir)


			self.msgBox = QMessageBox(self)
			self.msgBox.setIcon(QMessageBox.Information)
			self.msgBox.setText("Pre-processing...")
			# self.msgBox.setInformativeText("todo1")
			self.msgBox.setWindowTitle("Information")
			# self.msgBox.setDetailedText("The details are as follows:")

			self.msgBox.setWindowFlags((self.msgBox.windowFlags() & ~Qt.WindowCloseButtonHint) & ~Qt.WindowSystemMenuHint )


			l = self.msgBox.layout()
			l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()
			self.progress = QProgressBar()
			l.addWidget(self.progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )


			self.msgBox.show()

			self.timer = QTimer()
			self.timer.timeout.connect(self.handleTimer_Click_preprocess_calc_1_shot)
			self.handleTimer_Click_preprocess_calc_1_shot_index = 0
			self.timer.start(0)
			pass


		except:
			QMessageBox.information(self,"Error","Click on \"Start Cropping\" button in \"Data\" tab and try again.")

	def handleTimer_Click_preprocess_calc_1_shot(self):
		if self.handleTimer_Click_preprocess_calc_1_shot_index  < self.eargb.numShots:
			self.eargb.calc_1_shot0(self.handleTimer_Click_preprocess_calc_1_shot_index)
			self.eargb.calc_1_shot1(self.handleTimer_Click_preprocess_calc_1_shot_index)
			self.progress.setValue((self.handleTimer_Click_preprocess_calc_1_shot_index)/self.eargb.numShots * 100)
			print(self.meta[self.handleTimer_Click_preprocess_calc_1_shot_index].id)

			self.handleTimer_Click_preprocess_calc_1_shot_index+=1
		else:
			self.eargb.save0()
			print('done   self.eargb.save0()')
			time.sleep(4)
			self.eargb.save1()
			print('done   self.eargb.save1()')
			time.sleep(4)
			self.timer.stop()
			self.msgBox.done(0)
			self.doneWorkDone("Pre-processing is finished")

			# self.csvcrop.updateMeta()

			

	def readMeta(self):
		file = open(self.logsDir, 'r')		
		dirName = file.readline()
		self.dir = dirName
		print(dirName, self.dir)


		self.meta      = readMdata(dirName)
		self.numShots  = len(self.meta)

	def is2dpresent(self):
		self.dir_2d = self.dir + '/compiled/2d.jpg'
		if os.path.isfile(self.dir_2d):
			self.projected2dimg.setIcon(QIcon(self.dir_2d))
			return True
		self.dir_2d = os.path.join(self.imgsDir,"noimg.png")
		return False
	def is2dpresent_without(self):
		self.dir_2dwithout = self.dir + '/compiled/2d_p.jpg'
		if os.path.isfile(self.dir_2dwithout):
			self.projected2dimg_without.setIcon(QIcon(self.dir_2dwithout))

			return True
		self.dir_2dwithout = os.path.join(self.imgsDir, "noimg.png")
		return False


	def is2dpresent_withColor(self):
		self.dir_2dColor = self.dir + '/compiled/2d_f.jpg'
		if os.path.isfile(self.dir_2dColor):
			self.projected2dimg_color.setIcon(QIcon(self.dir_2dColor))
			return True
		self.dir_2dColor = os.path.join(self.imgsDir,"noimg.png")
		return False

	def	 three3d(self):
		if self.download_i  < self.downloader.numShots:
			self.downloader.download_1shot_i(self.download_i)
			self.progress.setValue((self.download_i+1)/self.downloader.numShots * 100)
			self.download_i+=1
		else:
			print('done')
			self.timer.stop()