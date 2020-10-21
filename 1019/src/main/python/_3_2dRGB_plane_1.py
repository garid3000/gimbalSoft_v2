import sys, os
import numpy as np
import PIL.Image
import PIL.ImageDraw
import time
import matplotlib.pyplot as plt

import imageio
# from skimage.draw import polygon,polygon_perimeter, polygon2mask
from file_reader import *


class project_2d(object):
	def __init__(self, dir, show = False, peri = False):
		super(project_2d, self).__init__()
		self.dir = dir
		self.meta     = readMdata(dir)
		self.show = show
		self.peri = peri

		self.heightPole = 100
		self.fnm = 0
		self.fname = self.dir + '/compiled/EA_RGB_full.npy'
		self.fname1= self.dir + '/compiled/EA_fov.npy'
		self.EA_fov = np.load(self.fname1)

		self.init_calc()
		self.outDir = self.dir + '/compiled/2d.jpg'
		self.outDir_p = self.dir + '/compiled/2d_p.jpg'
		self.outDir_f = self.dir + '/compiled/2d_f.jpg'

		self.EA_RGB = np.load(self.fname)
		self.R   = 5* np.tan(-self.EA_RGB[:,0])
		self.A   = self.EA_RGB[:,1]
		self.RGB = self.EA_RGB[:,2:]

		self.field = np.zeros((4010,4010,3), dtype = np.uint8)



	def init_calc(self):
		self.fov_1 = self.EA_fov[:,0:2]
		self.fov_2 = self.EA_fov[:,2:4]
		self.fov_3 = self.EA_fov[:,4:6]
		self.fov_4 = self.EA_fov[:,6:8]

		self.fov_1R = 5 * np.tan(-self.fov_1[:,0])
		self.fov_2R = 5 * np.tan(-self.fov_2[:,0])
		self.fov_3R = 5 * np.tan(-self.fov_3[:,0])
		self.fov_4R = 5 * np.tan(-self.fov_4[:,0])

		self.fov_1A = self.fov_1[:,1]
		self.fov_2A = self.fov_2[:,1]
		self.fov_3A = self.fov_3[:,1]
		self.fov_4A = self.fov_4[:,1]

		fovState = False


		self.fov_1R[np.where(self.fov_1R>40)] = 40
		self.fov_2R[np.where(self.fov_2R>40)] = 40
		self.fov_3R[np.where(self.fov_3R>40)] = 40
		self.fov_4R[np.where(self.fov_4R>40)] = 40

		self.fov_1R[np.where(self.fov_1R<0)] = 0
		self.fov_2R[np.where(self.fov_2R<0)] = 0
		self.fov_3R[np.where(self.fov_3R<0)] = 0
		self.fov_4R[np.where(self.fov_4R<0)] = 0

		self.polar2x1 = self.fov_1R[:] * np.cos(self.fov_1A[:]) * 50 + 2005
		self.polar2y1 = self.fov_1R[:] * np.sin(self.fov_1A[:]) * 50 + 2005

		self.polar2x2 = self.fov_2R[:] * np.cos(self.fov_2A[:]) * 50 + 2005
		self.polar2y2 = self.fov_2R[:] * np.sin(self.fov_2A[:]) * 50 + 2005

		self.polar2x3 = self.fov_3R[:] * np.cos(self.fov_3A[:]) * 50 + 2005
		self.polar2y3 = self.fov_3R[:] * np.sin(self.fov_3A[:]) * 50 + 2005

		self.polar2x4 = self.fov_4R[:] * np.cos(self.fov_4A[:]) * 50 + 2005
		self.polar2y4 = self.fov_4R[:] * np.sin(self.fov_4A[:]) * 50 + 2005
		          

	def calc_stage1(self):
		self.verRadius = 35
		index = np.where(abs(self.R-self.verRadius)<5)
		self.polar2x = self.R[index] * np.cos(self.A[index]) * 50 + 2005
		self.polar2y = self.R[index] * np.sin(self.A[index]) * 50 + 2005

		for q in range(-5,5,1):
			for qq in range(-5,5,1):
				self.field[self.polar2x.astype(int)+q, self.polar2y.astype(int)+qq,:] = self.RGB[index]#/255.



	def calc_stage2(self):
		self.verRadius = 26
		index = np.where(abs(self.R-self.verRadius)<4)
		self.polar2x = self.R[index] * np.cos(self.A[index]) * 50 + 2005
		self.polar2y = self.R[index] * np.sin(self.A[index]) * 50 + 2005

		for q in range(-4,4,1):
			for qq in range(-4,4,1):
				self.field[self.polar2x.astype(int)+q, self.polar2y.astype(int)+qq,:] = self.RGB[index]#/255.


	def calc_stage3(self):
		self.verRadius = 19
		index = np.where(abs(self.R-self.verRadius)<3)
		self.polar2x = self.R[index] * np.cos(self.A[index]) * 50 + 2005
		self.polar2y = self.R[index] * np.sin(self.A[index]) * 50 + 2005

		for q in range(-3,3,1):
			for qq in range(-3,3,1):
				self.field[self.polar2x.astype(int)+q, self.polar2y.astype(int)+qq,:] = self.RGB[index]#/255.


	def calc_stage4(self):
		self.verRadius = 12
		index = np.where(abs(self.R-self.verRadius)<4)
		self.polar2x = self.R[index] * np.cos(self.A[index]) * 50 + 2005
		self.polar2y = self.R[index] * np.sin(self.A[index]) * 50 + 2005

		for q in range(-2,2,1):
			for qq in range(-2,2,1):
				self.field[self.polar2x.astype(int)+q, self.polar2y.astype(int)+qq,:] = self.RGB[index]#/255.
	
	def calc_stage5(self):
		self.verRadius = 4
		index = np.where(abs(self.R-self.verRadius)<4)
		self.polar2x = self.R[index] * np.cos(self.A[index]) * 50 + 2005
		self.polar2y = self.R[index] * np.sin(self.A[index]) * 50 + 2005

		q = 0
		qq= 0
		self.field[self.polar2x.astype(int)+q, self.polar2y.astype(int)+qq,:] = self.RGB[index]#/255.

	def calc_allStages(self):
		self.calc_stage1()
		self.calc_stage2()
		self.calc_stage3()
		self.calc_stage4()
		self.calc_stage5()

	def addPeri(self):
		self.image2 = PIL.Image.fromarray(self.field)
		draw = PIL.ImageDraw.Draw(self.image2)


		for i123 in range(self.polar2x1.shape[0]):
			c = np.array([self.polar2x1[i123].astype(int), self.polar2x2[i123].astype(int), self.polar2x4[i123].astype(int), self.polar2x3[i123].astype(int)])
			r = np.array([self.polar2y1[i123].astype(int), self.polar2y2[i123].astype(int), self.polar2y4[i123].astype(int), self.polar2y3[i123].astype(int)])
			print('rc', r, c)
			onePerim = [(r[0],c[0]),
						(r[1],c[1]),
						(r[2],c[2]),
						(r[3],c[3]),
						(r[0],c[0])]
			draw.line(onePerim, fill=(255, 255, 0), width=5)


		# pass
		# for i123 in range(self.polar2x1.shape[0]):    
		# 	r = np.array([self.polar2x1[i123].astype(int), self.polar2x2[i123].astype(int), self.polar2x4[i123].astype(int), self.polar2x3[i123].astype(int)])
		# 	c = np.array([self.polar2y1[i123].astype(int), self.polar2y2[i123].astype(int), self.polar2y4[i123].astype(int), self.polar2y3[i123].astype(int)])
		# 	#             rr, cc = polygon(r, c)
		# 	rr, cc = polygon_perimeter(r, c, shape=self.field.shape, clip=True)
		# 	self.field[rr, cc, :] = np.array([0,255,255])
			
		# 	rr, cc = polygon_perimeter(r+1, c, shape=self.field.shape, clip=True)
		# 	self.field[rr, cc, :] = np.array([0,255,255])
			
		# 	rr, cc = polygon_perimeter(r+2, c, shape=self.field.shape, clip=True)
		# 	self.field[rr, cc, :] = np.array([0,255,255])


		# 	# self.field[rr, cc, :] = np.array([0,255,255])
		# 	rr, cc = polygon_perimeter(r, c+1, shape=self.field.shape, clip=True)
		# 	self.field[rr, cc, :] = np.array([0,255,255])
		# 	rr, cc = polygon_perimeter(r, c+2, shape=self.field.shape, clip=True)
		# 	self.field[rr, cc, :] = np.array([0,255,255])

	def addColor(self):
		self.image3 = PIL.Image.fromarray(self.field)
		draw = PIL.ImageDraw.Draw(self.image3)


		for i123 in range(self.polar2x1.shape[0]):
			c = np.array([self.polar2x1[i123].astype(int), self.polar2x2[i123].astype(int), self.polar2x4[i123].astype(int), self.polar2x3[i123].astype(int)])
			r = np.array([self.polar2y1[i123].astype(int), self.polar2y2[i123].astype(int), self.polar2y4[i123].astype(int), self.polar2y3[i123].astype(int)])
			print('rc', r, c)
			onePerim = [(r[0],c[0]),
						(r[1],c[1]),
						(r[2],c[2]),
						(r[3],c[3]),
						(r[0],c[0])]
			draw.polygon(onePerim, fill=(45, 100, 45), outline=(255, 255, 0))

		pass
		# mask = 0
		# for i123 in range(self.polar2x1.shape[0]):    
		# 	r = np.array([self.polar2x1[i123].astype(int), self.polar2x2[i123].astype(int), self.polar2x4[i123].astype(int), self.polar2x3[i123].astype(int)])
		# 	c = np.array([self.polar2y1[i123].astype(int), self.polar2y2[i123].astype(int), self.polar2y4[i123].astype(int), self.polar2y3[i123].astype(int)])
		# 	nxutils.pnpoly(r, c, xyverts)
		# 	polygon = np.array(
		# 					[[r[0], c[0]], 
		# 					 [r[1], c[1]], 
		# 					 [r[2], c[2]], 
		# 					 [r[3], c[3]]])
		# 	mask = np.logical_or(mask, polygon2mask((4010,4010), polygon))
			
		# 	print('adding Color')
		# self.field[:, :, 0] = mask*255
		# self.field[:, :, 1] = mask*255
		# self.field[:, :, 2] = mask*255

	def showImg(self):
		plt.figure(figsize = (15,15))
		plt.imshow(self.field)
		plt.show()

	def saveImg(self):
		imageio.imwrite(self.outDir, self.field)
		

	def savePeriImg(self):
		self.addPeri()
		# imageio.imwrite(self.outDir_p, self.field)
		self.image2.save(self.outDir_p, quality=95)

	def saveFullImg(self):
		self.addPeri()
		# imageio.imwrite(self.outDir_f, self.field)
		self.image3.save(self.outDir_f, quality=95)
		
	def updateMeta(self):
		directory = self.dir
		with open(directory + '/meta/about.meta', 'wb') as config_dictionary_file:
			pickle.dump(self.meta, config_dictionary_file)
		return self.meta