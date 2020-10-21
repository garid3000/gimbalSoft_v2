import os
import numpy as np
from numpy import cos, sin, tan, matmul
import PIL.Image
import time 
import json
from file_reader import *



def R(u, t): #rotational matrix
	t = t*np.pi/180    
	rx = np.array((
	    (    cos(t) + u[0]**2 * (1-cos(t)) ,  
	         u[0] * u[1] * (1-cos(t)) - u[2] * sin(t),
	         u[0] * u[2] * (1-cos(t)) + u[1] * sin(t)
	    ),
	    
	    
	    (    u[1] * u[0] * (1-cos(t)) + u[2] * sin(t), 
	         cos(t) + u[1]**2 * (1-cos(t)) ,  
	         u[1] * u[2] * (1-cos(t)) - u[0] * sin(t)
	    ),
	    
	    
	    (    u[2] * u[0] * (1-cos(t)) - u[1] * sin(t), 
	         u[2] * u[1] * (1-cos(t)) + u[0] * sin(t),
	         cos(t) + u[2]**2 * (1-cos(t))
	    )
	))

	return rx

def xyz2ea(coor):
	xplane = coor[:,:,0]
	yplane = coor[:,:,1]
	zplane = coor[:,:,2]
	xzplane = np.sqrt(xplane**2 + zplane**2)
	ea = np.zeros((coor.shape[0], coor.shape[1], 2))
	ea[:,:,0] = np.arctan( xzplane /yplane)
	ea[:,:,1] = np.arctan2(-xplane, zplane)
	return ea


class EARGB(object):
	"""docstring for EARGB"""
	def __init__(self, dir):
		super(EARGB, self).__init__()
		self.dir      = dir
		self.dirComp  = dir + '/compiled'
		self.meta     = readMdata(dir)
		self.numShots = len(self.meta)
		self.pitch    = []
		self.roll     = []
		self.Azimuth  = []
		self.mkdir()
		self.readPRA()
		self.ndvi 	  = None
		self.readNDVI()
		self.ElAzRGB  = np.zeros((240*240*self.numShots, 5))
		
		self.l = self.ElAzRGB.shape[0]
		self.num_crops = self.l // 57600
		self.fov = np.zeros((self.num_crops, 2 * 4))

		self.defualtTen  = 10


	def mkdir(self):
		try:
			os.mkdir(self.dirComp)
		except:
			pass
	def readPRA(self):
		for i in range(self.numShots):
			self.pitch.append(float(self.meta[i].jsonDic['Pitch']))
			self.roll.append(float(self.meta[i].jsonDic['Roll']))
			self.Azimuth.append(float(self.meta[i].jsonDic['Azimuth']))
	def readNDVI(self):		#disclaimer: this is not only NDVI but also all the calculated indexes
		NDVI = np.load(self.dirComp + '/NDVI.npy')
		self.ndvi = NDVI[:,0]

	def save0(self):
		np.save(self.dirComp + '/EA_RGB_full', self.ElAzRGB)
	def save1(self):
		np.save(self.dirComp + '/EA_fov',self.fov)

		#np.save(self.dirComp + '/EA_RGB_full', self.ElAzRGB)
	def calc_1_shot0(self, i):
		#l = l0 * ndvi[i]
		y = - np.sin(self.pitch[i]  * np.pi / 180.)
		x = - np.cos(self.pitch[i]  * np.pi / 180.) * np.cos(self.Azimuth[i]  * np.pi / 180.)
		z = - np.cos(self.pitch[i]  * np.pi / 180.) * np.sin(self.Azimuth[i]  * np.pi / 180.)

		a,b,c = x,y,z
		abc = np.sqrt(a*a + b*b + c*c)
		aa = -a*b / abc
		bb = -(b*b) / abc + 1 
		cc = -c*b / abc

		x0,y0,z0 = x,y,z
		normalVectorPlane = np.array((x0, y0, z0))
		normalVectorPlane/= np.linalg.norm(normalVectorPlane) 

		qx = matmul(R(normalVectorPlane, self.roll[i]), np.array((aa, bb, cc)).reshape(3,1))
		qx = qx/np.linalg.norm(qx)
		aa,bb,cc = qx[0][0],qx[1][0],qx[2][0]

		qx = matmul(R(normalVectorPlane, self.roll[i] + 90), np.array((aa, bb, cc)).reshape(3,1))
		qx = qx/np.linalg.norm(qx)
		aaa,bbb,ccc = qx[0][0],qx[1][0],qx[2][0]

		q = 16
		abc = abc * q
		#         hei = 2 * abc * np.tan(5*np.pi/180)
		#         wid = 2 * abc * np.tan(1*np.pi/180)
		hei = 2 * abc * np.tan(self.defualtTen*np.pi/180)
		wid = 2 * abc * np.tan(self.defualtTen*np.pi/180)

		#             if pic:
		#                 tmp1 = box(pos=vector(x*q,y*q,z*q), axis=vector(x,y,z), length=0.05, height=hei, width=wid, texture=imgs[i], up=vector(aa,bb,cc))
		#             q=8
		#             tmp1 = box(pos=vector(x*q,y*q,z*q), axis=vector(x,y,z), length=0.05, height=.8, width=.8, color = vector(1-ndvi[i],ndvi[i],0), up=vector(aa,bb,cc))



		q = 16
		imgCoordinates = np.zeros((240, 240 , 2))
		imgCoordinates[:,:,0] = np.arange(120, -120, -1).reshape(240,1)/240*hei
		imgCoordinates[:,:,1] = np.arange(-120, 120, 1).reshape(1, 240)/240*wid

		imgCoordinates3D = np.zeros((240, 240 , 3))
		imgCoordinates3D[:,:,:] = np.array([aa,bb,cc])

		imgCoordinatesTMp = np.zeros((240, 240 , 3))
		imgCoordinatesTMp[:,:,0] = imgCoordinates[:,:,0]
		imgCoordinatesTMp[:,:,1] = imgCoordinates[:,:,0]
		imgCoordinatesTMp[:,:,2] = imgCoordinates[:,:,0]

		tmpH =  imgCoordinates3D * imgCoordinatesTMp


		imgCoordinates3D = np.zeros((240, 240 , 3))
		imgCoordinates3D[:,:,:] = np.array([aaa,bbb,ccc])

		imgCoordinatesTMp[:,:,0] = imgCoordinates[:,:,1]
		imgCoordinatesTMp[:,:,1] = imgCoordinates[:,:,1]
		imgCoordinatesTMp[:,:,2] = imgCoordinates[:,:,1]

		tmpV =  imgCoordinates3D * imgCoordinatesTMp
		tmpHV = tmpH + tmpV #end zurgin gol tsegtei haritsangui toolol

		s = np.zeros((240, 240 , 3))
		s[:,:,0] = x*q
		s[:,:,1] = y*q
		s[:,:,2] = z*q
		tmpHV += s #ene toolliin ehees haritsangui baidal

		#         tmp12 = box(pos=vector(tmpHV[0,0,0],tmpHV[0,0,1],tmpHV[0,0,2]), axis=vector(x/ndvi[i],y/ndvi[i],z/ndvi[i]), length=.1, height=.1, width=.1)
		#         tmp12 = box(pos=vector(tmpHV[0,47,0],tmpHV[0,47,1],tmpHV[0,47,2]), axis=vector(x/ndvi[i],y/ndvi[i],z/ndvi[i]), length=.1, height=.1, width=.1)
		#         tmp12 = box(pos=vector(tmpHV[239,0,0],tmpHV[239,0,1],tmpHV[239,0,2]), axis=vector(x/ndvi[i],y/ndvi[i],z/ndvi[i]), length=.1, height=.1, width=.1)

		tmpEA = xyz2ea(tmpHV)

		self.ElAzRGB[57600*(i):57600*(i+1), 0:2] = tmpEA.reshape(57600, 2)
		self.ElAzRGB[57600*(i):57600*(i+1), 2: ] = np.array(PIL.Image.open(self.meta[i].crop_img_dir)).reshape(57600, 3)

	def calc_all_shot(self):
		for i in range(self.numShots):
			self.calc_1_shot0(i)
			self.calc_1_shot1(i)
		self.save0()
		self.save1()

	def calc_1_shot1(self, i):
		tmp = self.ElAzRGB[57600 * i: 57600 * (i+1), :]
		upLe = 0   + 120-24-1
		upRi = 0   + 120+24+1
		boLe = 239*240 + 120-24-1
		boRi = 239*240 + 120+24+1

		self.fov[i, 0:2] = tmp[upLe,:2]
		self.fov[i, 2:4] = tmp[upRi,:2]
		self.fov[i, 4:6] = tmp[boLe,:2]
		self.fov[i, 6:8] = tmp[boRi,:2]
