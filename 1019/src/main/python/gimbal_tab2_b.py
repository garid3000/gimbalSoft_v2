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
from matplotlib import rc

import  matplotlib  as mpl

import subprocess
import platform
import random
import webbrowser


class MplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(121, projection='polar')   
		self.axes1 = self.fig.add_subplot(122)     
		super(MplCanvas, self).__init__(self.fig)


class MplCanvasB(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(211, projection='polar')   
		self.axes1 = self.fig.add_subplot(212)     
		super(MplCanvasB, self).__init__(self.fig)



class MplCanvas1(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(121)   
		self.axes1 = self.fig.add_subplot(122)     
		super(MplCanvas1, self).__init__(self.fig)




class MplCanvas2(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)   
		self.axes.axis('off')
		super(MplCanvas2, self).__init__(self.fig)




class tab2(QWidget):
	def __init__(self):
		super(QWidget, self).__init__()	
		appctxt	 = ApplicationContext()
		self.logsDir = appctxt.get_resource('_logs_/lastDir.tmp')		
		self.imgsDir = appctxt.get_resource('_imgs_')
		self.imgsDir_grp4tab2sub1_img = appctxt.get_resource('_imgs_/preSpectrum.png')
		self._4_3d_ = appctxt.get_resource('_4_3d_/4_3dViEW.py')
		self._helperData = appctxt.get_resource('_4_3d_/3dViewHelper.dat')
		
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
		self.populate_grp1()
		self.populate_grp2()
		self.populate_grp3()
		self.populate_grp4()

		self.layout = QGridLayout()
		# self.layout.addWidget(self.grp0    ,0,0,2,1)
		self.layout.addWidget(self.grp4    ,0,0,1,3)
		self.layout.addWidget(self.grp2    ,1,0,1,1)
		self.layout.addWidget(self.grp3    ,1,1,1,1)
		self.layout.addWidget(self.grp1    ,1,2,1,1)

		self.layout.setColumnStretch(0, 0)
		self.layout.setColumnStretch(1, 10)
		self.layout.setColumnStretch(2, 10)
		# self.layout.setColumnStretch(2, 0)
		self.layout.setRowStretch(1, 4)
		self.layout.setRowStretch(0, 3)
		# self.layout.setRowStretch(2, 1)
		self.setLayout(self.layout)


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


	def populate_grp1(self):
		self.grp1 = QGroupBox("2D Value Distribution")
		self.grp1layout = QGridLayout()

		self.canvas = MplCanvas(self, width=2, height=2, dpi=100)
		self.timer = QTimer()
		self.update_plot()
		self.show()	
		
		# self.timer.setInterval(100)
		# self.timer.timeout.connect(self.update_plot)
		# self.timer.start()


		# self.grp0layout.addWidget(self.projectedIcons,  0,0,3,1)
		self.grp1layout.addWidget(QLabel("2D plane"),    0,0,1,1)
		self.grp1layout.addWidget(self.canvas, 		     1,0,1,1)

		self.grp1layout.setRowStretch(0, 0)
		self.grp1layout.setRowStretch(1, 10)
		self.grp1.setLayout(self.grp1layout)
	def populate_grp2(self):

		self.grp2 = QGroupBox("Value Color Control Panel")
		self.grp2layout = QGridLayout()

		self.indexMaxVal = 1
		self.indexMinVal = 0
		self.index_maxLE = QLineEdit(str(self.indexMaxVal))
		self.index_minLE = QLineEdit(str(self.indexMinVal))
		self.index_maxLE.setValidator( QDoubleValidator(0, 10.00, 8) )
		self.index_minLE.setValidator( QDoubleValidator(-10.00, 10.00, 8) )
		# self.index_maxLE.editingFinished.connect(self.on_lineedit_maxmin)
		# self.index_minLE.editingFinished.connect(self.on_lineedit_maxmin)

		# self.CustomEquation = QLineEdit()

		# self.comboIndex = QComboBox(self)
		self.comboIndexGroup = QComboBox(self)
		self.comboColormap = QComboBox(self)
		self.for_initializing_combobox()
		# self.comboIndex.currentTextChanged.connect(self.on_comboIndex_indexSelector)
		# self.comboColormap.currentTextChanged.connect(self.on_comboColormap)
		self.comboIndexGroup.currentTextChanged.connect(self.on_comboColormapIndexGroup)
		self.myColorMapingFunc = plt.cm.RdYlGn
		self.on_comboColormapIndexGroup()
		self.readingFile_3dHelper()

		self.refmaxminbtn = QPushButton("Refresh/Save")
		# self.refmaxminbtn.clicked.connect(self.refmaxminbtnCLK)
		self.seemore_aboutcmap = QPushButton("About Colormaps")
		# self.seemore_aboutcmap.clicked.connect(self.seemore_aboutcmap_clik)
		self.grp2layout.addWidget(QLabel("Max value:"),    	0,0,1,1)#, alignment=Qt.AlignTop)
		self.grp2layout.addWidget(self.index_maxLE,    		0,1,1,1)#, alignment=Qt.AlignTop)
		self.grp2layout.addWidget(QLabel("Min value:"),    	1,0,1,1)#, alignment=Qt.AlignTop)
		self.grp2layout.addWidget(self.index_minLE,    		1,1,1,1)#, alignment=Qt.AlignTop)
		self.grp2layout.addWidget(self.refmaxminbtn,		3,1,1,1)#, alignment=Qt.AlignTop)
		# self.grp2layout.addWidget(self.comboIndex,		    2,1,1,1)#, alignment=Qt.AlignTop)
		self.grp2layout.addWidget(self.comboIndexGroup,		2,0,1,1)#, alignment=Qt.AlignTop)
		self.grp2layout.addWidget(self.comboColormap,		2,1,1,1)#, alignment=Qt.AlignTop)
		self.grp2layout.addWidget(self.seemore_aboutcmap,	3,0,1,1)
		# self.grp2layout.addWidget(QLabel("Custom equation"),4,1,1,3)
		# self.grp2layout.addWidget(self.CustomEquation,      5,0,1,3)


		self.grp2layout.setRowStretch(0, 1)
		self.grp2layout.setRowStretch(1, 1)
		self.grp2layout.setRowStretch(2, 1)
		self.grp2layout.setRowStretch(3, 1)
		self.grp2layout.setRowStretch(4, 1)


		self.grp2.setLayout(self.grp2layout)
		pass
	def populate_grp3(self):
		self.grp3 = QGroupBox("Single")
		self.grp3layout = QGridLayout()

		self.canvas_single = MplCanvasB(self, width=2, height=2, dpi=100)
		self.timer = QTimer()
		self.update_plot_single()
		self.show()	

		self.grp3valueshower = QLabel("Index Val:")
		self.grp3shotIDselector= QComboBox()
		
		# self.timer.setInterval(100)
		# self.timer.timeout.connect(self.update_plot)
		# self.timer.start()


		# self.grp0layout.addWidget(self.projectedIcons,  0,0,3,1)
		# self.grp3layout.addWidget(QLabel("2D plane"),      0,0,1,1)
		self.grp3layout.addWidget(self.canvas_single, 	   0,0,1,2)
		self.grp3layout.addWidget(self.grp3shotIDselector, 1,0,1,1)
		self.grp3layout.addWidget(self.grp3valueshower,    1,1,1,1)

		self.grp3layout.setRowStretch(0, 0)
		self.grp3layout.setRowStretch(1, 10)
		self.grp3.setLayout(self.grp3layout)
		pass


	def populate_grp4(self):
		self.grp4tabwidget = QTabWidget()
		self.grp4tabwidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
		self.grp4tabwidget.currentChanged.connect(self.onChange_grp4tabwidget)

		self.populate_grp4_tab1()
		self.populate_grp4_tab2()

		self.grp4tabwidget.addTab(self.grp4tab1,"Index selector")
		self.grp4tabwidget.addTab(self.grp4tab2,"Index creator")


		self.grp4 = QGroupBox("Index selector/creator")
		self.grp4layout = QGridLayout()
		self.grp4layout.addWidget(self.grp4tabwidget, 	 0,0,1,1)
		self.grp4.setLayout(self.grp4layout)
		pass

	def populate_grp4_tab1(self):
		self.grp4tab1 = QWidget()

		self.grp4tab1_cbox_stockIndexs = QComboBox()
		self.grp4tab1_cbox_stockIndexs_init()
		self.grp4tab1_tableWidget = QTableWidget() 
		self.grp4tab1_create_tableWidge()




		self.grp4tab1_lbl_stockIndexs_val = QLabel("Index val:     ")


		self.grp4tab1.layout = QGridLayout(self)
		self.grp4tab1.layout.addWidget(self.grp4tab1_cbox_stockIndexs,      0,0)
		self.grp4tab1.layout.addWidget(self.grp4tab1_tableWidget,	        0,1,2,1)
		self.grp4tab1.layout.addWidget(self.grp4tab1_lbl_stockIndexs_val,	1,0)
		self.grp4tab1.setLayout(self.grp4tab1.layout)


		# self.grp1layout.setColumnStretch(0, 10)
		# self.grp1layout.setColumnStretch(1, 0)
		pass

	def grp4tab1_create_tableWidge(self): 

		#Row count 
		self.grp4tab1_tableWidget.setRowCount(9)  

		#Column count 
		self.grp4tab1_tableWidget.setColumnCount(2)   

		self.grp4tab1_tableWidget.setItem(0,0, QTableWidgetItem("Name")) 
		self.grp4tab1_tableWidget.setItem(0,1, QTableWidgetItem("Value")) 
		self.grp4tab1_tableWidget.setItem(1,0, QTableWidgetItem("NDVI")) 
		self.grp4tab1_tableWidget.setItem(2,0, QTableWidgetItem("Index 2")) 
		self.grp4tab1_tableWidget.setItem(3,0, QTableWidgetItem("Index 3")) 
		self.grp4tab1_tableWidget.setItem(4,0, QTableWidgetItem("Index 4")) 
		self.grp4tab1_tableWidget.setItem(5,0, QTableWidgetItem("Index 5")) 
		self.grp4tab1_tableWidget.setItem(6,0, QTableWidgetItem("Index 6")) 
		self.grp4tab1_tableWidget.setItem(7,0, QTableWidgetItem("Index 7")) 
		self.grp4tab1_tableWidget.setItem(8,0, QTableWidgetItem("Index 8")) 
		self.grp4tab1_tableWidget.setItem(9,0, QTableWidgetItem("Index 9")) 
		self.grp4tab1_tableWidget.setItem(10,0, QTableWidgetItem("Index 10")) 
		
		self.grp4tab1_tableWidget.horizontalHeader().setStretchLastSection(True) 
		self.grp4tab1_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
		self.grp4tab1_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
	def populate_grp4_tab2(self):
		self.grp4tab2 = QWidget()


		self.grp4tab2sub1 = QGroupBox("Spectrum Adjustment")
		self.grp4tab2sub2 = QGroupBox("Variable(Band) Editor")
		self.grp4tab2sub3 = QGroupBox("Equation creator")
		self.populate_grp4tab2sub1()
		self.populate_grp4tab2sub2()
		self.populate_grp4tab2sub3()

		self.grp4tab2.layout = QGridLayout(self)
		self.grp4tab2.layout.addWidget(self.grp4tab2sub1, 0,1)
		self.grp4tab2.layout.addWidget(self.grp4tab2sub2, 0,2)
		self.grp4tab2.layout.addWidget(self.grp4tab2sub3, 0,3)
		self.grp4tab2.setLayout(self.grp4tab2.layout)
		pass

	def populate_grp4tab2sub1(self):
		self.grp4tab2sub1_leafThreshold = QLineEdit()
		self.grp4tab2sub1_whitThreshold = QLineEdit()
		self.grp4tab2sub1_BG = QLineEdit()
		self.grp4tab2sub1_leafThreshold.setValidator( QDoubleValidator(0, 255, 8) )
		self.grp4tab2sub1_whitThreshold.setValidator( QDoubleValidator(0, 255, 8) )
		self.grp4tab2sub1_BG.setValidator( QDoubleValidator(0, 16, 8) )
		self.grp4tab2sub1_canvas = MplCanvas1(self, width=2, height=2, dpi=100)
		self.grp4tab2sub1_calc = QPushButton("1. Calculate ⬇")

		self.grp4tab2sub1_eqimg = QLabel(self)
		pixmap = QPixmap(self.imgsDir_grp4tab2sub1_img)
		self.grp4tab2sub1_eqimg.setPixmap(pixmap) #pixmap.scaledToHeight(200)
		# self.resize(pixmap.width()/100,pixmap.height()/100)

		# Optional, resize window to image size


		self.grp4tab2sub1.layout = QGridLayout(self)
		self.grp4tab2sub1.layout.addWidget(QLabel('LT: Leaf Threshold'),       0,0)
		self.grp4tab2sub1.layout.addWidget(self.grp4tab2sub1_leafThreshold,    0,1)
		self.grp4tab2sub1.layout.addWidget(QLabel('WT: White Threshold'),      1,0)
		self.grp4tab2sub1.layout.addWidget(self.grp4tab2sub1_whitThreshold,    1,1)
		self.grp4tab2sub1.layout.addWidget(QLabel('BG value'),                 2,0)
		self.grp4tab2sub1.layout.addWidget(self.grp4tab2sub1_BG,               2,1)
		self.grp4tab2sub1.layout.addWidget(self.grp4tab2sub1_calc,             3,1)

		self.grp4tab2sub1.layout.addWidget(self.grp4tab2sub1_eqimg,            0,2,4,1)
		self.grp4tab2sub1.layout.addWidget(self.grp4tab2sub1_canvas,	       4,0,1,3)
		# self.grp4tab2sub1.layout.addWidget(QLabel('2'),       0,1,2,1)
		# self.grp4tab2sub1.layout.addWidget(QLabel('3'),		  1,0)
		self.grp4tab2sub1.setLayout(self.grp4tab2sub1.layout)
		pass
	def populate_grp4tab2sub2(self):
		self.grp4tab2_tableWidgetVar = QTableWidget()
		self.grp4tab2_create_tableWidgetVar()

		# self.grp4tab2_tableWidgetVal = QTableWidget()
		# self.grp4tab2_create_tableWidgetVal()

		self.grp4tab2sub2layout = QGridLayout(self)
		self.grp4tab2sub2layout.addWidget(self.grp4tab2_tableWidgetVar,     0,0)
		# self.grp4tab2sub2layout.addWidget(self.grp4tab2_tableWidgetVal,     0,1)
		# self.grp4tab2sub2layout.setColumnStretch(0, 10)
		# self.grp4tab2sub2layout.setColumnStretch(1, 0)
		self.grp4tab2sub2.setLayout(self.grp4tab2sub2layout)



	def populate_grp4tab2sub3(self):
		self.grp4tab2sub3_equationCanvas = MplCanvas2(self, width=2, height=2, dpi=100)
		self.grp4tab2sub3_equationEdit = QLineEdit()
		self.grp4tab2sub3_equationEdit.textChanged.connect(self.doSomething)
		self.grp4tab2sub3_equationCalcVal = QLineEdit()
		self.grp4tab2sub3_equationCalcBtn = QPushButton(">>")


		self.grp4tab2sub3layout = QGridLayout(self)
		self.grp4tab2sub3layout.addWidget(QLabel("Write Equation"),           0,0)
		self.grp4tab2sub3layout.addWidget(self.grp4tab2sub3_equationEdit,     1,0)
		self.grp4tab2sub3layout.addWidget(self.grp4tab2sub3_equationCalcBtn,  1,1)
		self.grp4tab2sub3layout.addWidget(self.grp4tab2sub3_equationCalcVal,  1,2)
		self.grp4tab2sub3layout.addWidget(self.grp4tab2sub3_equationCanvas,   2,0,1,3)
		self.grp4tab2sub3.setLayout(self.grp4tab2sub3layout)

		pass

	def doSomething(self):
		print("doSomething")
		print(self.grp4tab2sub3_equationEdit.text())
		self.update_equation(self.grp4tab2sub3_equationEdit.text())

	def grp4tab2_create_tableWidgetVar(self): 
		self.grp4tab2_tableWidgetVar.setRowCount(50)
		self.grp4tab2_tableWidgetVar.setColumnCount(3)   
		self.grp4tab2_tableWidgetVar.setItem(0,0, QTableWidgetItem("Var Name")) 
		self.grp4tab2_tableWidgetVar.setItem(0,1, QTableWidgetItem("Expression")) 
		self.grp4tab2_tableWidgetVar.setItem(0,2, QTableWidgetItem("Value")) 
		self.grp4tab2_tableWidgetVar.horizontalHeader().setStretchLastSection(True) 
		self.grp4tab2_tableWidgetVar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

	# def grp4tab2_create_tableWidgetVal(self): 
	# 	self.grp4tab2_tableWidgetVal.setRowCount(50)
	# 	self.grp4tab2_tableWidgetVal.setColumnCount(1)   
	# 	self.grp4tab2_tableWidgetVal.setItem(0,0, QTableWidgetItem("Var Name")) 
	# 	self.grp4tab2_tableWidgetVal.setItem(0,1, QTableWidgetItem("Expression")) 
	# 	self.grp4tab2_tableWidgetVal.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# self.grp4tab2_tableWidgetVal.horizontalHeader().setStretchLastSection(True) 
		# self.grp4tab2_tableWidgetVal.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 



	#this when changeing the colormap FAMILY get changed
	def on_comboColormapIndexGroup(self):
		tmpGrpName = self.comboIndexGroup.currentText()
		print(tmpGrpName)
		print("self.cmapNames[tmpGrpName]", self.cmapNames[tmpGrpName])
		self.comboColormap.clear()
		for cmap_name in self.cmapNames[tmpGrpName]:
			self.comboColormap.addItem(cmap_name)



	#add initially colormap to the combox
	def for_initializing_combobox(self):
		for cmap_category in self.cmapNames:
			self.comboIndexGroup.addItem(cmap_category)


	#read helper file (from the last usage)
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

		
		# self.comboIndex.setCurrentIndex(self.indexOfIndexData)
		



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

	def update_plot_single(self):
		print('tyrign redraw')
		try:
			theta = self.Azimuth * np.pi / 180.

			ndvi1 = self.ndvi - np.min(self.ndvi)
			colors = ndvi1/np.max(ndvi1)
			r = np.array(self.pitch) #somethings

			self.canvas_single.axes.cla() #cla()  # Clear the canvas.
			self.canvas_single.axes1.cla() #cla()  # Clear the canvas.

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

			print(theta.shape, r.shape)

			r1 = 90 - np.array(r1)
			theta1 = np.array(theta1)
			c = self.canvas_single.axes.scatter(theta1, r1, c=colors, s=r1*1.2, alpha=1) # 
			self.forThe2nd(self.ndvi)
			self.canvas_single.draw()
			self.timer.stop()
			print("somethign")
		except :
			print('error length are diffrernt')
			self.timer.stop()



	def update_equation(self, str_eq):
		print('tyrign redraw')
		try:
			rc('text', usetex=True)
			rc('font', family='serif')
			self.grp4tab2sub3_equationCanvas.axes.cla() 
			c = self.grp4tab2sub3_equationCanvas.axes.text(0.0,0.4, '$' + str_eq + '$', fontsize=30) # 
			self.grp4tab2sub3_equationCanvas.axes.axis('off')
			self.grp4tab2sub3_equationCanvas.draw()

			# self.timer.stop()
			# print("somethign")
		except :
			print('errorasdfasdf ahsdfk')
			# self.timer.stop()

	def onChange_grp4tabwidget(self):
		print("somehting changed in onChange_grp4tabwidget")



	#add index names to the grp4 tab1 (stock indexes)
	def grp4tab1_cbox_stockIndexs_init(self):
		self.grp4tab1_cbox_stockIndexs.addItem("Index 1: NDVI")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 2")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 3")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 4")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 5")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 6")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 7")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 8")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 9")
		self.grp4tab1_cbox_stockIndexs.addItem("Index 10")