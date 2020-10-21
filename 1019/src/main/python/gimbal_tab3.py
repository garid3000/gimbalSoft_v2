from fbs_runtime.application_context.PyQt5 import ApplicationContext
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os
import subprocess
from _downloader import downloader
import re

import platform
def openExplorer_file(path):
	if platform.system() == 'Windows':
		FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
		subprocess.run([FILEBROWSER_PATH, path])
	elif platform.system() == 'Linux':
		os.system("nautilus " + path)



class tab3(QWidget):
	def __init__(self):
		super(QWidget, self).__init__()		
		# self.logsDir = appctxt.get_resource('_logs_/lastDir.tmp')

		appctxt = ApplicationContext()		
		self.imgsDir = 			appctxt.get_resource('_imgs_')
		self.downloadFileDir = 	appctxt.get_resource('_logs_/downloadDir.tmp')
		self.userInfoDir = 		appctxt.get_resource('_logs_/uInfo.tmp')
		self.downloadDir = ''

		self.getDownloadDir()
		# self.projectDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
		# self.iconsDir = os.path.join(self.projectDir, 'src','main','icons')
		# self.logsDir = os.path.join(self.projectDir, 'src','main','_logs_', 'lastDir.tmp')
		# self.imgsDir = os.path.join(self.projectDir, 'src','main','_imgs_')


		self.download_i = 0
		self.layout = QGridLayout()
		self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)



		self.down_Button = QPushButton("Download")
		self.down_Button.clicked.connect(self.download)

		self.clear_Button = QPushButton("Clear")
		self.clear_Button.clicked.connect(self.clear)

		

		self.grp1 = QGroupBox("")
		# self.grp1layout = QGridLayout()
		self.layoutfbox = QGridLayout()

		self.usr = QLabel("Username:")
		self.pwd = QLabel("Password:")
		self.date = QLabel("Date:")
		self.downloadFolder = QLabel("Directory")
		self.downloadFolderFinder = QPushButton("set")
		self.downloadFolderFinder.clicked.connect(self.downloadFolderFinder_clk)

		self.usr1 = QLineEdit()
		self.pwd1 = QLineEdit()
		self.date1 = QLineEdit()
		self.downloadFolder1 = QLabel(self.downloadDir)
		self.progress = QProgressBar()

		self.getUserInfo()


		self.layoutfbox.addWidget(self.usr,				0,0,1,1, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.usr1,			0,1,1,2, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.pwd,				1,0,1,1, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.pwd1,			1,1,1,2, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.date,			2,0,1,1, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.date1,			2,1,1,2, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.downloadFolder,	3,0,1,1, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.downloadFolder1,	3,1,1,1, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.downloadFolderFinder,  3,2,1,1, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.clear_Button, 	4,0,1,3, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.down_Button, 	5,0,1,3, alignment=Qt.AlignTop)
		self.layoutfbox.addWidget(self.progress	, 		6,0,1,3, alignment=Qt.AlignTop)


		self.layoutfbox.setRowStretch(0, 1)
		self.layoutfbox.setRowStretch(1, 1)
		self.layoutfbox.setRowStretch(2, 1)
		self.layoutfbox.setRowStretch(3, 1)
		self.layoutfbox.setRowStretch(4, 1)
		self.layoutfbox.setRowStretch(5, 1)
		self.layoutfbox.setRowStretch(6, 1)
		self.layoutfbox.setRowStretch(7, 100)

	
		# self.layout.addWidget(self.downloadLink 			,2,0,1,1)
		# self.layout.addWidget(self.downloadLink1			,2,1,1,1)
		# self.layout.addWidget(self.downloadFolder 			,2,0,1,1)
		# self.layout.addWidget(self.downloadFolder1			,2,1,1,1)
		# self.layout.addWidget(self.tab1_delete_Button	    ,0,2,1,3)
		self.grp1.setLayout(self.layoutfbox)



		self.layout.addWidget(QLabel('')    ,0,0,1,1)
		self.layout.addWidget(self.grp1	    ,0,1,1,1)
		self.layout.addWidget(QLabel('')    ,0,2,1,1)

		self.layout.setColumnStretch(0, 5)
		self.layout.setColumnStretch(1, 4)
		self.layout.setColumnStretch(2, 5)
		self.setLayout(self.layout)


		self.timer = QTimer()
		self.timer.timeout.connect(self.handleTimer_download)

	def downloadFolderFinder_clk(self):
		pass
		tmp_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.downloadDir))
		if os.path.isdir(tmp_dir):
			self.setDownloadDir(tmp_dir)
			self.downloadDir = tmp_dir
			self.downloadFolder1.setText(tmp_dir)
		# else:
		# 	print(2)
		# 	self.dirName = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		
		# if self.dirName:
		# 	print(self.dirName)
		# 	self.selectedFolder = self.dirName
		# 	file = open(self.logsDir, 'w')
		# 	file.write(self.dirName)
		# 	file.close()
		# 	self.grp1_folder_dir_str.setText(self.dirName)
		# 	QMessageBox.information(self,"Directory","Directory has been changed") #changed!
		# self.tab0.update_indShot_list()
		# # self.tab0.on_clicked(0)
		# self.tab3.reReadData_andDraw()

	def download(self):
		print( self.usr1.text() )
		print( self.pwd1.text() )
		print( self.date.text() )
		print( self.downloadFolder1.text() )

		downlaodAbsolutePath = os.path.join(self.downloadFolder1.text(), self.date1.text())
		justmade = False
		if os.path.isdir(downlaodAbsolutePath) == False:
			os.mkdir(downlaodAbsolutePath)
			justmade = True
		self.downloader = downloader(self.usr1.text(), self.pwd1.text(), self.date1.text() ,  downlaodAbsolutePath)

		isThereData = self.downloader.processHTML()
		if isThereData:
			self.download_i = 0
			self.timer.start(0)
			print('downloaded', self.downloader.url)
		else:
			QMessageBox.information(self,"Information","Error: Data is not found on the web.\nCheck followings: username, password or date.")
			if os.path.isdir(downlaodAbsolutePath) == True and justmade ==True:
				os.rmdir(downlaodAbsolutePath)
		self.setUserInfo(self.usr1.text(), self.pwd1.text())
		QMessageBox.information(self,"Information",self.usr1.text()+' '+self.pwd1.text())
		# for i in range(self.downloader.numShots):
		# 	print(i)
		# 	self.downloader.download_1shot_i(i)
		# 	self.progress.setValue((i+1)/self.downloader.numShots * 100)

		# file = open('tmp.tmp', 'r')
		# dirName = file.readline()
		# print(dirName)
		# out = os.system("python C:\\Users\\Garid\\Documents\\0114\\0114\\1crop_img_creater.py " + dirName)
		# print(out)


	def handleTimer_download(self):
		if self.download_i  < self.downloader.numShots:
			self.downloader.download_1shot_i(self.download_i)
			self.progress.setValue((self.download_i+1)/self.downloader.numShots * 100)
			self.download_i+=1
		else:
			print('done')
			self.timer.stop()
			QMessageBox.information(self,"Information","Downloading is finished")
			self.progress.setValue(0)
			self.exploreWindows(self.downloadDir)
			#open the file expoleoror

	def clear(self):
		pass

	def getDownloadDir(self):
		file = open(self.downloadFileDir, 'r')
		self.downloadDir = file.readline()
		if not os.path.isdir(self.downloadDir):
			self.downloadDir = ''
		file.close()


	def setDownloadDir(self, dir):
		file = open(self.downloadFileDir, 'w')
		file.write(dir)
		file.close()
	
	def getUserInfo(self):
		file = open(self.userInfoDir, 'r')
		self.usernameStr = re.sub('[^a-zA-Z0-9]+', '', file.readline())
		# self.usernameStr = file.readline()
		self.passwordStr = file.readline()
		self.usr1.setText(self.usernameStr)
		self.pwd1.setText(self.passwordStr)
		file.close()


	def setUserInfo(self, uname, pword):
		file = open(self.userInfoDir, 'w')
		file.write(re.sub('[^a-zA-Z0-9]+', '', uname) + "\n" + pword)
		file.close()
	
			
	def exploreWindows(self,path):
		path = os.path.normpath(path)

		openExplorer_file(path)