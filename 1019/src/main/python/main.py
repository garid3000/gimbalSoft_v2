import sys, os
import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from gimbal_tab0  import tab0
from gimbal_tab1  import tab1
# from gimbal_tab2  import tab2
from gimbal_tab2_b  import tab2
from gimbal_tab3  import tab3

ASADMIN = 'asadmin'

class App(QMainWindow):
	def __init__(self):
		super().__init__()

		self.version = "v1.7"

		self.title = "Gimbal " + self.version
		self.left  = 100
		self.top   = 100
		self.width = 1024
		self.height= 768

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self. width, self.height)
		self.theCentral = theCentralWidget(1)
		self.setCentralWidget(self.theCentral)
		# self.setWindowIcon(QIcon('data/icon.png'))

		self.show()

class theCentralWidget(QWidget):
	def __init__(self, arg):
		super(QWidget, self).__init__()
		self.selectedFolder = ''

		appctxt = ApplicationContext()
		self.logsDir = appctxt.get_resource('_logs_/lastDir.tmp')
		
		self.createTabs()
		Main = QGridLayout()

		self.grp1_folder = QGroupBox('Data folder')
		self.grp1_folder_layout = QGridLayout()
		self.grp1_folder_dir_str = QLineEdit()
		self.grp1_folder_dir_chooser_btn = QPushButton("Find")
		self.grp1_folder_dir_chooser_btn.clicked.connect(self.openFileNameDialog)
		self.grp1_folder_layout.addWidget(self.grp1_folder_dir_str, 0,0,1,1)
		self.grp1_folder_layout.addWidget(self.grp1_folder_dir_chooser_btn, 0,1,1,1)
		self.grp1_folder.setLayout(self.grp1_folder_layout)



		# mainLayout = QGridLayout()
		# mainLayout.addWidget(self.mainTABs_widget,0, 0, 1, 1)

		Main.addWidget(self.grp1_folder, 0,0,1,1)
		Main.addWidget(self.mainTABs_widget, 1,0,1,1)
		Main.setRowStretch(0,0)
		Main.setRowStretch(1,1)

		# self.setLayout(mainLayout)
		self.setLayout(Main)
		self.initDirNameSetter()


	def createTabs(self):
		self.mainTABs_widget = QTabWidget()
		self.mainTABs_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
		self.mainTABs_widget.currentChanged.connect(self.mainTABs_widget_onChange)

		self.tab0 = tab0()
		self.tab1 = tab1()
		# self.tab2 = tab2()
		self.tab2 = tab2()
		self.tab3 = tab3()
		# self.tab0 = QTabWidget()
		# self.tab1 = QTabWidget()
		# self.tab2 = QTabWidget()
		# self.tab3 = QTabWidget()

		self.mainTABs_widget.addTab(self.tab0, "&Data")
		self.mainTABs_widget.addTab(self.tab1, "&2D RGB Projection")
		self.mainTABs_widget.addTab(self.tab2, "&Value 2D,3D Projection")
		# self.mainTABs_widget.addTab(self.tab2b, "&Custom")
		self.mainTABs_widget.addTab(self.tab3, "&Download")

	def openFileNameDialog(self):
		if os.path.isdir(self.dirName):
			print(1)
			self.dirName = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.dirName))
		else:
			print(2)
			self.dirName = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		
		if self.dirName:
			print(self.dirName)
			self.selectedFolder = self.dirName
			file = open(self.logsDir, 'w')
			file.write(self.dirName)
			file.close()
			self.grp1_folder_dir_str.setText(self.dirName)
			
			self.tab0.update_indShot_list()			# self.tab0.on_clicked(0)
			self.tab1.update_this_tab()
			print('self.tab1.update_this_tab()', self.tab1.dir)
			# self.tab2.reReadData_andDraw()
			# self.tab2b.reReadData_andDraw()
			
			QMessageBox.information(self,"Directory","Directory has been changed") #changed!
		else:
			QMessageBox.information(self,"Directory","No Directory")



	def initDirNameSetter(self):
		file = open(self.logsDir, 'r')
		self.dirName = file.readline()
		file.close()
		self.grp1_folder_dir_str.setText(self.dirName)

	def mainTABs_widget_onChange(self):
		x = self.mainTABs_widget.currentIndex()
		if x == 2:
			# self.tab2.reReadData_andDraw()
			# self.tab2b.reReadData_andDraw()
			print('changed', x)

			pass
		print('changed', x)

if __name__ == '__main__':
	# checking root
	if sys.argv[-1] != ASADMIN:
		script = os.path.abspath(sys.argv[0])
		params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
		import platform 
		if platform.system() == 'Windows':
			import win32com.shell.shell as shell
			shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
			sys.exit(0)
		elif platform.system() == 'Linux':
			pass



	appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
	window = App()
	window.show()
	exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
	sys.exit(exit_code)

#https://github.com/pyinstaller/pyinstaller/blob/develop/PyInstaller/hooks/hook-scipy.py
#this helped, fbs freezea