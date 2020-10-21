import os
import numpy as np
import PIL.Image
import sys	
from file_reader import *

class cropper(object):
	"""docstring for ClassName"""
	def __init__(self, dir):
		super(cropper, self).__init__()
		self.dir = dir
		self.dirCrop = dir + '/cropped'
		self.dirComp = dir + '/compiled'
		self.meta = readMdata(dir)
		self.numShots = len(self.meta)
		self.mkdir()

	def mkdir(self):
		try:
			os.mkdir(self.dirComp)
		except:
			pass
		try:
			os.mkdir(self.dirCrop)
		except:
			pass
			
	def crop_1_shot(self, id):
		# im = PIL.Image.open(self.meta[id].pics_dir).crop((595-120, 430, 595+120, 670))
		# im = PIL.Image.open(self.meta[id].pics_dir).crop((475, 430, 715, 670))
		im = PIL.Image.open(self.meta[id].pics_dir).crop((515-120, 585-120, 515+120, 585+120))
		self.meta[id].crop_img_dir = self.dirCrop + '/' + self.meta[id].id + '_crop_1010.jpg'
		im.save(self.meta[id].crop_img_dir)
		# imgs.append(subDir + '/' + fname.split('.')[0] + '_crop_1010.jpeg')
		# print(self.meta[id].id)
		pass
	def crop_all(self):
		for i in range(self.numShots):
			print(self.meta[i].id)
			self.crop_1_shot(i)

	def compile_all_index(self):
		ndvi = np.zeros((self.numShots, 10))
		for i in range(self.numShots):
			tmp = np.genfromtxt(self.meta[i].spec_dir, delimiter=",")
			ndvi[i,:] = tmp
		np.save(self.dirComp + '/NDVI', ndvi)

	def updateMeta(self):
		directory = self.dir
		with open(directory + '/meta/about.meta', 'wb') as config_dictionary_file:
			pickle.dump(self.meta, config_dictionary_file)
		return self.meta
