from fbs_runtime.application_context.PyQt5 import ApplicationContext
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os
import json
import subprocess

from _1crop_img_creater import cropper
from _d_CSVs_processer import *

from file_reader import *
import shutil

import platform
def openExplorer_file(path):
	if platform.system() == 'Windows':
		FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
		subprocess.run([FILEBROWSER_PATH, path])
	elif platform.system() == 'Linux':
		os.system("nautilus " + path)



class tab0(QWidget):
	def __init__(self):
		super(QWidget, self).__init__()		

		appctxt = ApplicationContext()
		self.logsDir = appctxt.get_resource('_logs_/lastDir.tmp')

		# self.projectDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
		#self.iconsDir = os.path.join(self.projectDir, 'src','main','icons')
		#self.logsDir = os.path.join(self.projectDir, 'src','main','_logs_', 'lastDir.tmp')
		self.imgsDir = appctxt.get_resource('_imgs_')#os.path.join(self.projectDir, 'src','main','_imgs_')

		self.meta      = None
		self.numShots  = 0
		self.layout = QGridLayout()

		self.dir = ''

		self.Img = QLabel(self)

		self.Img_crop = QLabel(self)
		# self.cropPlot = QLabel(self)

		# self.indexPlot = QLabel(self)
		self.indexPlotButton = QPushButton("Show file")  #2d plant projection
		self.indexPlotButton.clicked.connect(self.indexPlotButton_click)
		self.indexPlotButton.setIcon(QIcon(os.path.join(self.imgsDir,'no.png')))
		self.indexPlotButton.setIconSize(QSize(500,500))

		# self.cropPlot = QLabel(self)
		self.cropPlotButton = QPushButton("Show file")  #2d plant projection
		self.cropPlotButton.clicked.connect(self.cropPlotButton_click)
		self.cropPlotButton.setIcon(QIcon(os.path.join(self.imgsDir,'no.png')))
		self.cropPlotButton.setIconSize(QSize(500,500))


		self.populate_grp1()
		self.populate_grp2()
		self.populate_grp3()
		self.populate_grp4()


		self.layout.addWidget(self.grp1	,0,0,2,1)
		self.layout.addWidget(self.grp2	,0,1,1,1)
		self.layout.addWidget(self.grp3	,0,2,2,1)
		self.layout.addWidget(self.grp4	,1,1,1,1)

		self.layout.setColumnStretch(0, 0)
		self.layout.setColumnStretch(1, 1)
		self.layout.setColumnStretch(2, 1)

		self.setLayout(self.layout)
		self.update_indShot_list()

	def exploreWindows(self,path):
		# explorer would choke on forward slashes
		path = os.path.normpath(path)

		openExplorer_file(path)

		# if os.path.isdir(path):
		# 	subprocess.run([FILEBROWSER_PATH, path])
		# elif os.path.isfile(path):
		# 	subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])

	def indexPlotButton_click(self):
		self.exploreWindows(self.indexPlotButton_str)
		pass	
	def cropPlotButton_click(self):
		self.exploreWindows(self.cropPlotButton_str)
		pass


	def populate_grp1(self):
		self.grp1 = QGroupBox('Individual Measurement')
		self.grp1_layout = QGridLayout()

		self.listView = QListView()
		self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.entry = QStandardItemModel()
		self.listView.setModel(self.entry)
		self.listView.clicked[QModelIndex].connect(self.on_clicked)

		self.grp1_layout.addWidget(self.listView , 0,1,1,1)
		self.grp1.setLayout(self.grp1_layout)

	def populate_grp2(self):
		self.grp2 = QGroupBox('Image')
		self.grp2_layout = QGridLayout()


		self.pixmap = QPixmap(os.path.join(self.imgsDir, "noimg.png")).scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.Img.setPixmap(self.pixmap)
		self.Img.show()
		self.pixmap = QPixmap(os.path.join(self.imgsDir, "noimg.png")).scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.Img_crop.setPixmap(self.pixmap)
		self.Img_crop.show()

		self.metaLabel = QLabel()

		self.grp2_layout.addWidget(QLabel("Image") , 			0,0,1,1)
		self.grp2_layout.addWidget(self.Img , 					1,0,1,1)
		self.grp2_layout.addWidget(QLabel("Image (cropped)") , 	2,0,1,1)
		self.grp2_layout.addWidget(self.Img_crop , 				3,0,1,1)
		self.grp2_layout.addWidget(QLabel("Meta") , 			0,1,1,1)
		self.grp2_layout.addWidget(self.metaLabel , 			1,1,3,1)
		self.grp2_layout.addWidget(QLabel() , 					4,1,1,2)


		self.grp2_layout.setRowStretch(0, 0)
		self.grp2_layout.setRowStretch(1, 0)
		self.grp2_layout.setRowStretch(2, 0)
		self.grp2_layout.setRowStretch(3, 0)
		self.grp2_layout.setRowStretch(4, 1)

		self.grp2.setLayout(self.grp2_layout)

	def populate_grp3(self):

		self.grp3 = QGroupBox('Plot')
		self.grp3_layout = QGridLayout()

		self.pixmap = QPixmap(os.path.join(self.imgsDir, "noimg.png")).scaled(700, 700, Qt.KeepAspectRatio, Qt.FastTransformation)
		# self.cropPlot.setPixmap(self.pixmap)
		# self.cropPlot.show()

		# self.indexPlot.setPixmap(self.pixmap)
		# self.indexPlot.show()



		

		self.grp3_layout.addWidget(QLabel('Spectrum (CSV crop)') , 0,0,1,1)
		self.grp3_layout.addWidget(self.cropPlotButton  , 1,0,1,1)
		self.grp3_layout.addWidget(QLabel('Index') , 2,0,1,1)
		self.grp3_layout.addWidget(self.indexPlotButton  , 3,0,1,1)
		self.grp3.setLayout(self.grp3_layout)


	def populate_grp4(self):
		self.grp4 = QGroupBox('Control')
		self.grp4_layout = QGridLayout()

		self.notReadyButtonIcon = QIcon('_icons_/check_red.png')
		self.ReadyButtonIcon = QIcon('_icons_/check_grn.png')

		self.buttonClean = QPushButton('Start\n   Cleaning', self)
		self.buttonClean.clicked.connect(self.handleButtonClean)
		#check and set the icon for the button
		self.buttonClean.setIcon(self.notReadyButtonIcon)
		self.buttonClean.setIconSize(QSize(72,72))

		self.buttonCrop = QPushButton('Start\n   Cropping', self)
		self.buttonCrop.clicked.connect(self.handleButtonCrop)
		self.buttonCrop.setIcon(self.notReadyButtonIcon)
		self.buttonCrop.setIconSize(QSize(72,72))

		self.buttonPlot = QPushButton('Start\n   Plotting', self)
		self.buttonPlot.clicked.connect(self.handleButtonPlot)
		self.buttonPlot.setIcon(self.notReadyButtonIcon)
		self.buttonPlot.setIconSize(QSize(72,72))


		self.buttonPlot_spec = QPushButton('Start\n   Plotting spec', self)
		self.buttonPlot_spec.clicked.connect(self.handleButtonPlot_spec)
		self.buttonPlot_spec.setIcon(self.notReadyButtonIcon)
		self.buttonPlot_spec.setIconSize(QSize(72,72))

		# self.grp4_layout.addWidget(QLabel('Spectrum (CSV crop)') , 0,0,1,1)
		# self.grp4_layout.addWidget(self.cropPlot  , 1,0,1,1)
		# self.grp4_layout.addWidget(QLabel('Index') , 2,0,1,1)
		self.grp4_layout.addWidget(self.buttonClean , 1,0,1,1)
		self.grp4_layout.addWidget(self.buttonCrop  , 1,1,1,1)
		self.grp4_layout.addWidget(self.buttonPlot  , 1,2,1,1)
		self.grp4_layout.addWidget(self.buttonPlot_spec  , 1,3,1,1)
		self.grp4.setLayout(self.grp4_layout)

	def handleButtonClean(self):
		print("handleButtonClean")
		folder = self.dir
		for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			if os.path.isdir(file_path):
				print(file_path)
				shutil.rmtree(file_path)
		self.doneWorkDone("Folder cleaning is finished")
		# QMessageBox.information(self,"Information",)

			# try:
			# 	if os.path.isfile(file_path):
			# 		os.unlink(file_path)
			# 	elif os.path.isdir(file_path):
			# 		shutil.rmtree(file_path)
			# except Exception as e:
			# 	print('Failed to delete %s. Reason: %s' % (file_path, e))


	def handleButtonCrop(self):
		self.cropper = cropper(self.dir)
		self.cropper_i = 0
		self.msgBox = QMessageBox(self)
		self.msgBox.setIcon(QMessageBox.Information)
		self.msgBox.setText("Making cropped images")
		# self.msgBox.setInformativeText("")
		self.msgBox.setWindowTitle("Processing")
		# self.msgBox.setDetailedText("The details are as follows:")

		self.msgBox.setWindowFlags((self.msgBox.windowFlags() & ~Qt.WindowCloseButtonHint) & ~Qt.WindowSystemMenuHint )


		l = self.msgBox.layout()
		l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()
		self.progress = QProgressBar()
		l.addWidget(self.progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )


		self.msgBox.show()

		self.timer = QTimer()
		self.timer.timeout.connect(self.handleTimer)
		self.timer.start(0)

		
	def handleButtonPlot(self):


		self.csvcrop = CSVcrop(self.dir)
		self.csvcrop_i = 0


		self.msgBox = QMessageBox(self)
		self.msgBox.setIcon(QMessageBox.Information)
		self.msgBox.setText("Processing")
		self.msgBox.setInformativeText("Making Plot images")
		self.msgBox.setWindowTitle("Processing")
		# self.msgBox.setDetailedText("The details are as follows:")

		self.msgBox.setWindowFlags((self.msgBox.windowFlags() & ~Qt.WindowCloseButtonHint) & ~Qt.WindowSystemMenuHint )


		l = self.msgBox.layout()
		l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()
		self.progress = QProgressBar()
		l.addWidget(self.progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )


		self.msgBox.show()

		self.timer = QTimer()
		self.timer.timeout.connect(self.handleTimer1)
		self.timer.start(0)

		
		print("handleButtonPlot")

	def handleButtonPlot_spec(self):
		self.csvspec = CSVspec(self.dir)
		self.csvspec_i = 0


		self.msgBox = QMessageBox(self)
		self.msgBox.setIcon(QMessageBox.Information)
		self.msgBox.setText("Processing")
		self.msgBox.setInformativeText("Making index images")
		self.msgBox.setWindowTitle("Processing")
		# self.msgBox.setDetailedText("The details are as follows:")

		self.msgBox.setWindowFlags((self.msgBox.windowFlags() & ~Qt.WindowCloseButtonHint) & ~Qt.WindowSystemMenuHint )


		l = self.msgBox.layout()
		l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()
		self.progress = QProgressBar()
		l.addWidget(self.progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )


		self.msgBox.show()

		self.timer = QTimer()
		self.timer.timeout.connect(self.handleTimer2)
		self.timer.start(0)
		self.msgBox.setEscapeButton(QPushButton('asdf'))

		
		print("handleButtonPlot")

	def handleTimer(self):
		if self.cropper_i  < self.cropper.numShots:
			self.cropper.crop_1_shot(self.cropper_i)
			self.progress.setValue((self.cropper_i+1)/self.cropper.numShots * 100)
			print(self.meta[self.cropper_i].id)

			self.cropper_i+=1
		else:
			print('done')
			self.timer.stop()
			self.cropper.compile_all_index()
			self.cropper.updateMeta()

			self.buttonCrop.setIcon(self.ReadyButtonIcon)
			self.buttonCrop.setIconSize(QSize(72,72))
			self.readMeta()
			self.msgBox.done(0)
			self.doneWorkDone("Task Cropping Image has been done.")




	def handleTimer1(self):
		if self.csvcrop_i  < self.csvcrop.numShots:
			self.csvcrop.plot_1shot(self.csvcrop_i)
			self.progress.setValue((self.csvcrop_i+1)/self.csvcrop.numShots * 100)
			print(self.meta[self.csvcrop_i].id)

			self.csvcrop_i+=1
		else:
			print('done')
			self.timer.stop()
			self.csvcrop.updateMeta()

			self.buttonPlot.setIcon(self.ReadyButtonIcon)
			self.buttonPlot.setIconSize(QSize(72,72))
			self.readMeta()
			self.msgBox.done(0)
			self.doneWorkDone("Task Creating Plots has been done")

			# self.cropPlotButton.setIcon(QIcon(self.cropPlotButton_str))
			# self.indexPlotButton.setIcon(QIcon(self.indexPlotButton_str))
			self.on_clicked_1()



	def handleTimer2(self):
		if self.csvspec_i  < self.csvspec.numShots:
			self.csvspec.plot_1shot(self.csvspec_i)
			self.progress.setValue((self.csvspec_i+1)/self.csvspec.numShots * 100)
			print(self.meta[self.csvspec_i].id)

			self.csvspec_i+=1
		else:
			print('done')
			self.timer.stop()
			self.csvspec.updateMeta()

			self.buttonPlot_spec.setIcon(self.ReadyButtonIcon)
			self.buttonPlot_spec.setIconSize(QSize(72,72))
			self.readMeta()
			self.msgBox.done(0)
			self.doneWorkDone("Task Creating Spec-Plots has been done")

			# self.cropPlotButton.setIcon(QIcon(self.cropPlotButton_str))
			# self.indexPlotButton.setIcon(QIcon(self.indexPlotButton_str))
			self.on_clicked_1()


	def doneWorkDone(self, someTxt):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)

		msg.setText(someTxt)
		# msg.setInformativeText(someTxt)
		msg.setWindowTitle("Information")
		msg.setDetailedText(" ")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()

	def on_clicked(self, index):
		self.tmpIndex = index
		item = self.entry.itemFromIndex(index)
		i = index.row()
		print("on_clicked\t", item.text(), index.row())

		# self.pixmap = QPixmap('next.png').scaled(800, 500, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.pixmap = QPixmap(self.meta[i].pics_dir).scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
		print(self.meta[index.row()].pics_dir)
		self.Img.setPixmap(self.pixmap)
		self.Img.show()

		self.pixmap = QPixmap(self.meta[i].crop_img_dir).scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.Img_crop.setPixmap(self.pixmap)
		self.Img_crop.show()


		print(self.meta[index.row()].plot_img_crop)
		self.cropPlotButton_str = self.meta[index.row()].plot_img_crop
		self.cropPlotButton.setIcon(QIcon(self.cropPlotButton_str))


		print(self.meta[index.row()].plot_img_spec)
		self.indexPlotButton_str = self.meta[index.row()].plot_img_spec
		self.indexPlotButton.setIcon(QIcon(self.indexPlotButton_str))

		strinqlabel = ''

		for x, y in self.meta[i].jsonDic.items():
			strinqlabel += '\t' + x + '\t' + y + '\n'
		self.metaLabel.setText(strinqlabel)

	def on_clicked_1(self):
		index = self.tmpIndex 
		item = self.entry.itemFromIndex(index)
		i = index.row()
		print("on_clicked\t", item.text(), index.row())

		# self.pixmap = QPixmap('next.png').scaled(800, 500, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.pixmap = QPixmap(self.meta[i].pics_dir).scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
		print(self.meta[index.row()].pics_dir)
		self.Img.setPixmap(self.pixmap)
		self.Img.show()

		self.pixmap = QPixmap(self.meta[i].crop_img_dir).scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.Img_crop.setPixmap(self.pixmap)
		self.Img_crop.show()


		print(self.meta[index.row()].plot_img_crop)
		self.cropPlotButton_str = self.meta[index.row()].plot_img_crop
		self.cropPlotButton.setIcon(QIcon(self.cropPlotButton_str))


		print(self.meta[index.row()].plot_img_spec)
		self.indexPlotButton_str = self.meta[index.row()].plot_img_spec
		self.indexPlotButton.setIcon(QIcon(self.indexPlotButton_str))

		strinqlabel = ''

		for x, y in self.meta[i].jsonDic.items():
			strinqlabel += '\t' + x + '\t' + y + '\n'
		self.metaLabel.setText(strinqlabel)


	def update_indShot_list(self):
		file = open(self.logsDir, 'r')		
		print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', file)
		dirName = file.readline()
		self.dir = dirName
		print(dirName)


		self.meta      = readMdata(dirName)
		self.numShots  = len(self.meta)

		#onlyfiles = [f for f in os.listdir(dirName) if ".jpeg" in f and os.path.isfile(os.path.join(dirName, f))]
		self.entry.clear()
		for i in range(self.numShots):#["Itemname1", "Itemname2", "Itemname3", "Itemname4"]:
			it = QStandardItem(self.meta[i].id)
			self.entry.appendRow(it)
		self.itemOld = QStandardItem("text")

	def readMeta(self):
		file = open(self.logsDir, 'r')
		dirName = file.readline()
		self.dir = dirName
		print(dirName)


		self.meta      = readMdata(dirName)
		self.numShots  = len(self.meta)
