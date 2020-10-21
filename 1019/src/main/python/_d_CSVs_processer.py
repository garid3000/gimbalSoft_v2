import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import sys, os
import json
import pandas as pd
from file_reader import *


class CSVfull(object):
	def __init__(self, dir):
		super(CSVfull, self).__init__()
		self.dir       = dir
		self.datafname = dir + '/compiled/CSV_full.npy'
		self.meta      = readMdata(dir)
		self.numShots  = len(self.meta)
		self.data      = np.zeros((self.numShots, 280, 10))
		self.outCSV    = dir + '/CSV/'
		self.mkCSV()
		self.outDir    = dir + '/CSV/full/'
		self.mkCSV_OUT()


	def processAllshots(self):
		for i in range(self.numShots):
			self.data[i,:,:] = np.array(pd.read_csv(self.meta[i].full_dir))

	def process1shot(self, i):
		self.data[i,:,:] = np.array(pd.read_csv(self.meta[i].full_dir))

	def saveData(self):
		np.save(self.datafname, self.data)

	def isDataMade(self):
		return os.path.isfile(self.datafname)

	def loadData(self):
		self.data = np.load(self.datafname)

	def prepare_data(self):
		if self.isDataMade():
			self.loadData()
		else:
			self.processAllshots()
			self.saveData()

	def mkCSV(self):
		if os.path.isdir(self.outCSV):
			return True

		try:
			os.mkdir(self.outCSV)
			return True
		except:
			return False

	def mkCSV_OUT(self):
		if os.path.isdir(self.outDir):
			return True

		try:
			os.mkdir(self.outDir)
			return True
		except:
			return False

	def plot_1shot(self, i):
		#self.plot_img_full

		lines1234 = []
		legen1234 = []

		data = pd.read_csv(self.meta[i].full_dir)


		fig = plt.figure(figsize = (10,6), dpi=120)
		#if lgwb[0] == '1':
		line_1, = plt.plot(data['WAVELENGTH'], data['LEAF'], 	label ='Leaf'	, color = 'green')
		lines1234.append(line_1)
		legen1234.append('Leaf')
		# if lgwb[1] == '1':
		line_2, = plt.plot(data['WAVELENGTH'], data['GRAY'], 	label ='Gray'	, color = 'gray')
		lines1234.append(line_2)
		legen1234.append('Gray')
		#if lgwb[2] == '1':
		line_3, = plt.plot(data['WAVELENGTH'], data['WHITE'], 	label ='White'	, color = 'orange')
		lines1234.append(line_3)
		legen1234.append('White')
		#if lgwb[3] == '1':
		line_4, = plt.plot(data['WAVELENGTH'], data['BG'], 		label ='BG'		, color = 'blue')
		lines1234.append(line_4)
		legen1234.append('BG')

		plt.xlabel('Wavelenght, nm')
		plt.ylabel('Value')
		plt.title("File: " + self.meta[i].id)
		plt.grid(True)

		plt.legend(lines1234, legen1234)

		plt.savefig(self.outDir + self.meta[i].id +'_full.png')
		plt.close(fig)

		self.meta[i].plot_img_full = self.outDir + self.meta[i].id +'_full.png'

	def updateMeta(self):
		directory = self.dir
		with open(directory + '/meta/about.meta', 'wb') as config_dictionary_file:
			pickle.dump(self.meta, config_dictionary_file)
		return self.meta











class CSVcrop(object):
	def __init__(self, dir):
		super(CSVcrop, self).__init__()
		self.dir       = dir
		self.datafname = dir + '/compiled/CSV_crop.npy'
		self.meta      = readMdata(dir)
		self.numShots  = len(self.meta)
		self.data      = np.zeros((self.numShots, 480, 6))
		self.outCSV    = dir + '/CSV/'
		self.mkCSV()
		self.outDir    = dir + '/CSV/crop/'
		self.mkCSV_OUT()


	def processAllshots(self):
		for i in range(self.numShots):
			self.data[i,:,:] = np.array(pd.read_csv(self.meta[i].full_dir))

	def process1shot(self, i):
		self.data[i,:,:] = np.array(pd.read_csv(self.meta[i].full_dir))

	def saveData(self):
		np.save(self.datafname, self.data)

	def isDataMade(self):
		return os.path.isfile(self.datafname)

	def loadData(self):
		self.data = np.load(self.datafname)

	def prepare_data(self):
		if self.isDataMade():
			self.loadData()
		else:
			self.processAllshots()
			self.saveData()

	def mkCSV(self):
		if os.path.isdir(self.outCSV):
			return True

		try:
			os.mkdir(self.outCSV)
			return True
		except:
			return False

	def mkCSV_OUT(self):
		if os.path.isdir(self.outDir):
			return True

		try:
			os.mkdir(self.outDir)
			return True
		except:
			return False

	def plot_1shot(self, i):
		#self.plot_img_full

		data = pd.read_csv(self.meta[i].crop_dir)
		
		lines1234 = []
		legen1234 = []

		fig = plt.figure(figsize = (10,6), dpi=120)
		#if lgwb[0] == '1':
		line_1, = plt.plot(data['WAVELENGTH'], data['LEAF'], 	label ='Leaf'	, color = 'green')
		lines1234.append(line_1)
		legen1234.append('Leaf')
		#if lgwb[1] == '1':
		line_2, = plt.plot(data['WAVELENGTH'], data['GRAY'], 	label ='Gray'	, color = 'gray')
		lines1234.append(line_2)
		legen1234.append('Gray')
		#if lgwb[2] == '1':
		line_3, = plt.plot(data['WAVELENGTH'], data['WHITE'], 	label ='White'	, color = 'orange')
		lines1234.append(line_3)
		legen1234.append('White')
		#if lgwb[3] == '1':
		line_4, = plt.plot(data['WAVELENGTH'], data['BG'], 		label ='BG'		, color = 'blue')
		lines1234.append(line_4)
		legen1234.append('BG')

		plt.xlabel('Wavelenght, nm')
		plt.ylabel('Value')
		plt.title("File: " + self.meta[i].id)
		plt.grid(True)

		plt.legend(lines1234, legen1234)

		plt.savefig(self.outDir + self.meta[i].id +'_crop.png')
		plt.close(fig)
	
		self.meta[i].plot_img_crop = self.outDir + self.meta[i].id +'_crop.png'

	def updateMeta(self):
		directory = self.dir
		with open(directory + '/meta/about.meta', 'wb') as config_dictionary_file:
			pickle.dump(self.meta, config_dictionary_file)
		return self.meta












class CSVspec(object):
	def __init__(self, dir):
		super(CSVspec, self).__init__()
		self.dir       = dir
		self.datafname = dir + '/compiled/CSV_spec.npy'
		self.meta      = readMdata(dir)
		self.numShots  = len(self.meta)
		self.data      = np.zeros((self.numShots, 10, 1))
		self.outCSV    = dir + '/CSV/'
		self.mkCSV()
		self.outDir    = dir + '/CSV/spec/'
		self.mkCSV_OUT()


	def processAllshots(self):
		for i in range(self.numShots):
			self.data[i,:,:] = np.array(pd.read_csv(self.meta[i].full_dir))

	def process1shot(self, i):
		self.data[i,:,:] = np.array(pd.read_csv(self.meta[i].full_dir))

	def saveData(self):
		np.save(self.datafname, self.data)

	def isDataMade(self):
		return os.path.isfile(self.datafname)

	def loadData(self):
		self.data = np.load(self.datafname)

	def prepare_data(self):
		if self.isDataMade():
			self.loadData()
		else:
			self.processAllshots()
			self.saveData()

	def mkCSV(self):
		if os.path.isdir(self.outCSV):
			return True

		try:
			os.mkdir(self.outCSV)
			return True
		except:
			return False

	def mkCSV_OUT(self):
		if os.path.isdir(self.outDir):
			return True

		try:
			os.mkdir(self.outDir)
			return True
		except:
			return False

	def plot_1shot(self, i):
		#self.plot_img_full

		data = pd.read_csv(self.meta[i].spec_dir, header = None)
		data = np.array(data)[0][:9]

		labels = [	 'index1:\n' + "{:.2f}".format(data[0]),
					 'index2:\n' + "{:.2f}".format(data[1]), 
					 'index3:\n' + "{:.2f}".format(data[2]), 
					 'index4:\n' + "{:.2f}".format(data[3]),
					 'index5:\n' + "{:.2f}".format(data[4]), 
					 'index6:\n' + "{:.2f}".format(data[5]), 
					 'index7:\n' + "{:.2f}".format(data[6]), 
					 'index8:\n' + "{:.2f}".format(data[7]), 
					 'index9:\n' + "{:.2f}".format(data[8])]

		fig = plt.figure(figsize = (10,6), dpi=120)
		plt.bar(labels, data)

		plt.xlabel('Index names')
		plt.ylabel('Value')
		plt.title("File: " + self.meta[i].id)
		plt.grid(True)

		plt.savefig(self.outDir + self.meta[i].id +'_spec.png')
		plt.close(fig)


	
		self.meta[i].plot_img_spec = self.outDir + self.meta[i].id +'_spec.png'

	def updateMeta(self):
		directory = self.dir
		with open(directory + '/meta/about.meta', 'wb') as config_dictionary_file:
			pickle.dump(self.meta, config_dictionary_file)
		return self.meta