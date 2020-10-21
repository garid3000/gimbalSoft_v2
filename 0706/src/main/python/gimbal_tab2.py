from fbs_runtime.application_context.PyQt5 import ApplicationContext
import time


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from file_reader import *
from new_3_2dRGB_plane_1 import *
from _2EARGB_3d_full import *
import shutil


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import colors
import  matplotlib  as mpl

import subprocess
import platform
import random
import webbrowser

def openExplorer_file(path):
	if platform.system() == 'Windows':
		FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
		subprocess.run([FILEBROWSER_PATH, path])
	elif platform.system() == 'Linux':
		os.system("nautilus " + path)


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(121, projection='polar')   
        self.axes1 = self.fig.add_subplot(122)     

        super(MplCanvas, self).__init__(self.fig)

class tab2(QWidget):
	def __init__(self):
		super(QWidget, self).__init__()	

		# self.projectDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

		appctxt	 = ApplicationContext()

		self.logsDir = appctxt.get_resource('_logs_/lastDir.tmp')		
		self.imgsDir = appctxt.get_resource('_imgs_')
		# self.three3dDir = appctxt.get_resource('_tmp_s_')
		# self.three3dDirCropped  = appctxt.get_resource('_tmp_s_/cropped')
		# self.three3dDirCompiled = appctxt.get_resource('_tmp_s_/compiled')
		self._4_3d_ = appctxt.get_resource('_4_3d_/4_3dViEW.py')
		self._helperData = appctxt.get_resource('_4_3d_/3dViewHelper.dat')
		# self._4_3d_ = appctxt.get_resource('_4_3d_/4_3dViEW_temp.py')
		# self.logsDir = os.path.join(self.projectDir, 'src','main','_logs_', 'lastDir.tmp')
		# self.imgsDir = os.path.join(self.projectDir, 'src','main','_imgs_')
		# self.three3dDir = os.path.join(self.projectDir, 'src','main','python', 'tmp_s')
		# self.three3dDirCropped = os.path.join(self.projectDir, 'src','main','python', 'tmp_s', 'cropped')
		# # self.three3dDirCompiled = os.path.join(self.projectDir, 'src','main','python', 'tmp_s', 'compiled')
		# self._4_3d_ = os.path.join(self.projectDir, 'src','main','python', '4_3dViEW.py')
		# self._4_3d_ = os.path.join(self.projectDir, 'src','main','python', '4_3dViEW_temp.py')

		self.plotUpdatingCount = 0

		self.meta      = None
		self.numShots  = 0
		self.dir  	   = ''
		self.layout = QGridLayout()
		self.readMeta()
		self.readData()
		self.readNDVI()
		self.cmapNames = {
			"Perceptually Uniform Sequential": 
				['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
			'Sequential':
				['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
				'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
				'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'],
            'Sequential (2)':
				 ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
				'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
				'hot', 'afmhot', 'gist_heat', 'copper'],
         	'Diverging': 
				['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
				'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'],
         	'Cyclic': ['twilight', 'twilight_shifted', 'hsv'],
         	'Qualitative': 
				['Pastel1', 'Pastel2', 'Paired', 'Accent',
				'Dark2', 'Set1', 'Set2', 'Set3',
				'tab10', 'tab20', 'tab20b', 'tab20c'],
			'Miscellaneous': 
				['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
				'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
				'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']
				}	


		self.populate_grp0()
		self.populate_grp1()
		self.populate_grp2()


		

		# self.populate_somehting()
		self.layout = QGridLayout()
		self.layout.addWidget(self.grp0    ,0,0,2,1)
		self.layout.addWidget(self.grp1    ,0,1,1,1)
		self.layout.addWidget(self.grp2    ,1,1,1,1)
		self.layout.setColumnStretch(0, 5)
		self.layout.setColumnStretch(1, 2)
		self.setLayout(self.layout)

	def populate_grp0(self):
		self.grp0 = QGroupBox("2D plane Index")
		self.grp0layout = QGridLayout()

		self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
		self.timer = QTimer()
		self.update_plot()
		self.show()	
		
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()


		# self.grp0layout.addWidget(self.projectedIcons,  0,0,3,1)
		self.grp0layout.addWidget(QLabel("2D plane"),    0,0,1,1)
		self.grp0layout.addWidget(self.canvas, 		     1,0,1,1)

		self.grp0layout.setRowStretch(0, 0)
		self.grp0layout.setRowStretch(1, 10)
		self.grp0.setLayout(self.grp0layout)

	def populate_grp1(self):

		self.grp1 = QGroupBox("max min choosser")
		self.grp1layout = QGridLayout()

		self.indexMaxVal = 1
		self.indexMinVal = 0
		self.index_maxLE = QLineEdit(str(self.indexMaxVal))
		self.index_minLE = QLineEdit(str(self.indexMinVal))
		self.index_maxLE.setValidator( QDoubleValidator(0, 10.00, 8) )
		self.index_minLE.setValidator( QDoubleValidator(-10.00, 10.00, 8) )
		self.index_maxLE.editingFinished.connect(self.on_lineedit_maxmin)
		self.index_minLE.editingFinished.connect(self.on_lineedit_maxmin)


		self.comboIndex = QComboBox(self)
		self.comboIndexGroup = QComboBox(self)
		self.comboColormap = QComboBox(self)
		self.for_initializing_combobox()
		self.comboIndex.currentTextChanged.connect(self.on_comboIndex_indexSelector)
		self.comboColormap.currentTextChanged.connect(self.on_comboColormap)
		self.comboIndexGroup.currentTextChanged.connect(self.on_comboColormapIndexGroup)
		self.myColorMapingFunc = plt.cm.RdYlGn
		self.on_comboColormapIndexGroup()
		self.readingFile_3dHelper()

		self.refmaxminbtn = QPushButton("Refresh/Save")
		self.refmaxminbtn.clicked.connect(self.refmaxminbtnCLK)
		self.seemore_aboutcmap = QPushButton("About Colormaps")
		self.seemore_aboutcmap.clicked.connect(self.seemore_aboutcmap_clik)
		self.grp1layout.addWidget(QLabel("Max value:"),    	0,0,1,1)#, alignment=Qt.AlignTop)
		self.grp1layout.addWidget(self.index_maxLE,    		0,1,1,1)#, alignment=Qt.AlignTop)
		self.grp1layout.addWidget(QLabel("Min value:"),    	1,0,1,1)#, alignment=Qt.AlignTop)
		self.grp1layout.addWidget(self.index_minLE,    		1,1,1,1)#, alignment=Qt.AlignTop)
		self.grp1layout.addWidget(self.refmaxminbtn,		1,2,1,1)#, alignment=Qt.AlignTop)
		self.grp1layout.addWidget(self.comboIndex,		    2,1,1,1)#, alignment=Qt.AlignTop)
		self.grp1layout.addWidget(self.comboIndexGroup,		3,0,1,1)#, alignment=Qt.AlignTop)
		self.grp1layout.addWidget(self.comboColormap,		3,1,1,1)#, alignment=Qt.AlignTop)
		self.grp1layout.addWidget(self.seemore_aboutcmap,	3,2,1,1)


		self.grp1layout.setRowStretch(0, 1)
		self.grp1layout.setRowStretch(1, 1)
		self.grp1layout.setRowStretch(2, 1)
		self.grp1layout.setRowStretch(3, 1)
		self.grp1layout.setRowStretch(4, 1)


		self.grp1.setLayout(self.grp1layout)

	def seemore_aboutcmap_clik(self):
		 webbrowser.open('https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html')

	def on_comboIndex_indexSelector(self):
		tmp = self.comboIndex.currentText()
		tmpi = self.comboIndex.currentIndex()
		self.indexOfIndexData = tmpi
		print(tmp, tmpi)
		print('on_comboIndex_indexSelector', self.indexOfIndexData)
		self.whichNDVI_selector(tmpi)
		self.update_plot()


	def on_lineedit_maxmin(self):
		print(self.index_maxLE.text())
		print(self.index_minLE.text())
		self.indexMaxVal = float(self.index_maxLE.text())
		self.indexMinVal = float(self.index_minLE.text())
		self.update_plot()

	def on_comboColormap(self):
		tmp = self.comboColormap.currentText()
		print(tmp)
		self.asdfCMAP = tmp
		self.myColorMapingFunc = cmap=plt.get_cmap(tmp)
		self.update_plot()

	def on_comboColormapIndexGroup(self):
		tmpGrpName = self.comboIndexGroup.currentText()
		print(tmpGrpName)
		print("self.cmapNames[tmpGrpName]", self.cmapNames[tmpGrpName])
		self.comboColormap.clear()
		for cmap_name in self.cmapNames[tmpGrpName]:
			self.comboColormap.addItem(cmap_name)

	def for_initializing_combobox(self):
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

		for cmap_category in self.cmapNames:
			self.comboIndexGroup.addItem(cmap_category)

		

	def update_plot(self):
		print('tyrign redraw')
		try:
			# Drop off the first y element, append a new one.
			# self.ydata = self.ydata[1:] + [random.randint(0, 10)]
			# self.canvas.axes.plot(self.xdata, self.ydata, 'r')
			# self.canvas.axes.plot(self.xdata, self.ydata, 'r')
			# # Trigger the canvas to update and redraw.
			# self.canvas.draw()

			# fig = plt.figure()
			theta = self.Azimuth * np.pi / 180.

			ndvi1 = self.ndvi - np.min(self.ndvi)
			colors = ndvi1/np.max(ndvi1)
			r = np.array(self.pitch) #somethings

			self.canvas.axes.cla() #cla()  # Clear the canvas.
			self.canvas.axes1.cla() #cla()  # Clear the canvas.
			# self.canvas.draw()
			# time.sleep(2)
			r1 = []
			theta1 = []
			colors = []
			for i in range(theta.shape[0]):
				if r[i] <= 90 and r[i] >= 0:
					if (self.ndvi[i] > self.indexMaxVal):
						color = (0.3,0.3,0.3)
					elif (self.ndvi[i] < self.indexMinVal):
						color = (0.1,0.1,0.1)
					else:
						tmp = self.ndvi[i]
						tmp = (tmp - self.indexMinVal)/(self.indexMaxVal - self.indexMinVal)
						# color = plt.cm.RdYlGn(tmp)
						color = self.myColorMapingFunc(tmp)
					colors.append(color)
					r1.append(r[i])
					theta1.append(theta[i])
				# print(color)

			print(theta.shape, r.shape)

			# c = self.canvas.axes.scatter(theta, r, c=self.ndvi, vmin = self.indexMinVal, vmax = self.indexMaxVal,  cmap='RdYlGn',  s=r*3, alpha=1) #
			r1 = 90 - np.array(r1)
			theta1 = np.array(theta1)
			c = self.canvas.axes.scatter(theta1, r1, c=colors, s=r1*1.2, alpha=1) # 
			self.forThe2nd(self.ndvi)
			self.canvas.draw()
			# plt.show()
			# 
			self.timer.stop()
			print("somethign")
		except :
			print('error length are diffrernt')
			self.timer.stop()

	def forThe2nd(self,x ):
		a = 0
		print(a)
		N, bins, patches = self.canvas.axes1.hist(x, bins=50, orientation="horizontal")
		# print(patches[0].xy[0], patches[1].xy[0], patches[2].xy[0])
		print(a)
		fracs = N / N.max()

		print(a)
		norm = colors.Normalize(fracs.min(), fracs.max())
		a= 2
		print(a)
		a = 0
		for thisfrac, thispatch in zip(fracs, patches):
			# print(a, thisfrac, norm(thisfrac))
			# color = plt.cm.viridis(norm(thisfrac))
			if (thispatch.xy[1] > self.indexMaxVal):
				color = (0.3,0.3,0.3)
			elif (thispatch.xy[1] < self.indexMinVal):
				color = (0.1,0.1,0.1)
			else:
				tmp = thispatch.xy[1]
				tmp = (tmp - self.indexMinVal)/(self.indexMaxVal - self.indexMinVal)
				# color = plt.cm.RdYlGn(tmp)
				color = self.myColorMapingFunc(tmp)

			thispatch.set_facecolor(color)
			a += 1
		self.canvas.axes1.plot([0,30], [self.indexMaxVal, self.indexMaxVal])
		self.canvas.axes1.plot([0,30], [self.indexMinVal, self.indexMinVal])

		norm = colors.Normalize(vmin=self.indexMinVal, vmax=self.indexMaxVal)
		
		if self.plotUpdatingCount == 0:
			self.cbar = self.canvas.axes1.figure.colorbar(
					mpl.cm.ScalarMappable(norm=norm, cmap=self.asdfCMAP),
					ax=self.canvas.axes1, pad=.05,  fraction=.1)#extend='both',
		else:
			self.cbar.update_normal(mpl.cm.ScalarMappable(norm=norm, cmap=self.asdfCMAP))
		self.plotUpdatingCount+=1


	def readMeta(self):
		file = open(self.logsDir, 'r')		
		self.dirName = file.readline()
		self.dir = self.dirName
		print(self.dirName)


		self.meta      = readMdata(self.dirName)
		self.numShots  = len(self.meta)

	def readData(self):
		self.Azimuth = np.zeros((self.numShots))
		self.pitch   = np.zeros((self.numShots))
		for i in range(self.numShots):
			self.Azimuth[i] = np.array(self.meta[i].jsonDic['Azimuth'])
			self.pitch[i]   = np.array(self.meta[i].jsonDic['Pitch'])

	def readNDVI(self):
		self.ndviFile = os.path.join(self.dirName, 'compiled', 'NDVI.npy')
		if os.path.isfile(self.ndviFile):
			self.ndviAll = np.load(self.ndviFile)
		else:
			self.ndviAll = np.zeros((20,10))

		self.ndvi = self.ndviAll[:,0]

	def whichNDVI_selector(self, index):
		self.ndvi = self.ndviAll[:,index]

	def reReadData_andDraw(self):
		self.readMeta()
		self.readData()
		self.readNDVI()
		self.update_plot()




	def populate_grp2(self):

		self.grp2 = QGroupBox("3d projection")
		self.grp2layout = QGridLayout()
		
		self.remake3d = QPushButton("") #3d projection
		self.remake3d.clicked.connect(self.Click_remake3d)
		self.remake3d.setIcon(QIcon(os.path.join(self.imgsDir,'projection','Slide1.PNG')))
		self.remake3d.setIconSize(QSize(300,300))


		self.grp2layout.addWidget(self.remake3d, 		0,0,1,1)
		self.grp2.setLayout(self.grp2layout)
	def Click_remake3d(self):

		# self.timer = QTimer()
		# self.timer.timeout.connect(self.remaknig3dhandleTimer)
		# self.timer.start(100)


		# self.msgBox.setDetailedText("The details are as follows:"
		shutil.copy(self._4_3d_, os.path.join(os.path.dirname(self.dir), '3dviewer.py'))
		self.updatingFile_3dHelper(self.dir.split('/')[-1], self.asdfCMAP, self.indexMaxVal, self.indexMinVal, self.indexOfIndexData)
		shutil.copy(self._helperData, os.path.join(os.path.dirname(self.dir), '3dViewHelper.dat'))

		# self.msgBox.exec_()
		QMessageBox.information(self,"3D projection","Run \"3dviewer.py\" file to start 3D projection.")
		self.exploreWindows(os.path.join(os.path.dirname(self.dir), '3dviewer.py'))

		# disconnectButton = messageBox.addButton(self.tr("Disconnect"),  QMessageBox.ActionRole)
		# try:
		# 	self.supro.kill()
		# 	self.timer.stop()
		# 	print('self.supro.kill()')
		# except:
		# 	pass
		# 	print('some')
		# 	self.timer.stop()
	'''
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
		print('python ' + self._4_3d_ + ' '+ self.asdfCMAP + ' src/main/python/tmp_s')
		# subprocess.call('python ' + self._4_3d_ + ' ' + self.three3dDir)
		print('self.asdfCMAP', self.asdfCMAP)
		# self.supro = subprocess.call('python ' + self._4_3d_ + ' '+ self.asdfCMAP + ' src/main/python/tmp_s')
		print('python ' + self._4_3d_ + ' '+ self.asdfCMAP + ' ' + self.three3dDir)
		self.supro = subprocess.call('python ' + self._4_3d_ + ' '+ self.asdfCMAP + ' ' + self.three3dDir)
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


	
	def exploreWindows(self,path):
		# explorer would choke on forward slashes
		path = os.path.normpath(path)
		openExplorer_file(path)
	def updatingFile_3dHelper(self, localDir, cmapStr, valueMax, valueMin, indexOfIndex):
		file = open(self._helperData, 'w')
		file.write(localDir + '\n' +cmapStr + '\n' +str(valueMax) + '\n' +str(valueMin) + '\n' + str(indexOfIndex) + '\n' + self.comboIndexGroup.currentText() + '\n')
		file.close()

	def readingFile_3dHelper(self):
		FILE = open(self._helperData, 'r')
		LinesOfFile = FILE.readlines()
		FILE.close()
		print(LinesOfFile)
		subDir = LinesOfFile[0].replace('\n', '').replace('\r', '')
		self.asdfCMAP = LinesOfFile[1].replace('\n', '').replace('\r', '')
		asdfCMAP_tmp = self.asdfCMAP
		self.indexMaxVal = float(LinesOfFile[2].replace('\n', '').replace('\r', ''))
		self.indexMinVal = float(LinesOfFile[3].replace('\n', '').replace('\r', ''))
		self.indexOfIndexData = int(LinesOfFile[4].replace('\n', '').replace('\r', ''))
		comboGroupStr = LinesOfFile[5].replace('\n', '').replace('\r', '')

		tmpindex = self.comboIndexGroup.findText(comboGroupStr, Qt.MatchFixedString) # MatchFixedString is from Qt
		if tmpindex >= 0:
			print('print(tmpindex)1', tmpindex, comboGroupStr)
			self.comboIndexGroup.setCurrentIndex(tmpindex)
			tmpindex = self.comboColormap.findText(asdfCMAP_tmp, Qt.MatchFixedString)
			print('print(tmpindex)2', tmpindex, asdfCMAP_tmp)
			if tmpindex >= 0:
				self.comboColormap.setCurrentIndex(tmpindex)
		self.index_maxLE.setText(str(self.indexMaxVal))
		self.index_minLE.setText(str(self.indexMinVal))

		
		self.comboIndex.setCurrentIndex(self.indexOfIndexData)
		



	def refmaxminbtnCLK(self):
		self.update_plot()
		self.updatingFile_3dHelper(self.dir.split('/')[-1], self.asdfCMAP, self.indexMaxVal, self.indexMinVal, self.indexOfIndexData)
		