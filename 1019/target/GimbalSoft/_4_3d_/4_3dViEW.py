import os, sys
import numpy as np
from vpython import *
# import PIL.Image
import time
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colors

cos = np.cos
sin = np.sin
matmul = np.matmul


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

def pngRefresher():
    FILE = open('3dViewHelper.dat')
    LinesOfFile = FILE.readlines()
    print(LinesOfFile)
    subDir = LinesOfFile[0].replace('\n', '').replace('\r', '')
    cmapanme = LinesOfFile[1].replace('\n', '').replace('\r', '')
    indexMaxVal = float(LinesOfFile[2].replace('\n', '').replace('\r', ''))
    indexMinVal = float(LinesOfFile[3].replace('\n', '').replace('\r', ''))
    indexOfindex = int(LinesOfFile[4].replace('\n', '').replace('\r', ''))
    pic = True
    colorNormFunc = mpl.colors.Normalize(vmin=indexMinVal,vmax=indexMaxVal)

    print(cmapanme)
    cmapFunc = plt.get_cmap(cmapanme)
    NDVI = np.load(subDir + '/compiled/NDVI.npy')
    indexValData = NDVI[:,indexOfindex]


    # fig = plt.Figure(figsize=(8, 8), dpi=100)
    # axes1 = fig.add_subplot(111)    

    fig, axes1 = plt.subplots()

    N, bins, patches = axes1.hist(indexValData, bins=50, orientation="horizontal")
    fracs = N / N.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    for thisfrac, thispatch in zip(fracs, patches):
        if (thispatch.xy[1] > indexMaxVal):
            color = (0.3,0.3,0.3)
        elif (thispatch.xy[1] < indexMinVal):
            color = (0.1,0.1,0.1)
        else:
            tmp = thispatch.xy[1]
            tmp = (tmp - indexMinVal)/(indexMaxVal - indexMinVal)
            # color = plt.cm.RdYlGn(tmp)
            color = cmapFunc(tmp)

        thispatch.set_facecolor(color)
    axes1.plot([0,30], [indexMaxVal, indexMaxVal])
    axes1.plot([0,30], [indexMinVal, indexMinVal])

    # fig.colorbar(orientation='vertical')
    fraction = .1
    norm = mpl.colors.Normalize(vmin=indexMinVal, vmax=indexMaxVal)
    cbar = axes1.figure.colorbar(
                mpl.cm.ScalarMappable(norm=norm, cmap=cmapanme),
                ax=axes1, pad=.05,  fraction=fraction)#extend='both',
    plt.savefig('cmap.png')



#reading file
FILE = open('3dViewHelper.dat')
LinesOfFile = FILE.readlines()
print(LinesOfFile)
subDir = LinesOfFile[0].replace('\n', '').replace('\r', '')
cmapanme = LinesOfFile[1].replace('\n', '').replace('\r', '')
vmax = float(LinesOfFile[2].replace('\n', '').replace('\r', ''))
vmin = float(LinesOfFile[3].replace('\n', '').replace('\r', ''))
indexOfindex = int(LinesOfFile[4].replace('\n', '').replace('\r', ''))
pic = True
colorNormFunc = mpl.colors.Normalize(vmin=vmin,vmax=vmax)

print(cmapanme)
cmapFunc = plt.get_cmap(cmapanme)

pngRefresher()

scene = canvas(width=640, height=480)
tmp1 = box(pos=vector(0,0,0), axis=vector(0,1,0), length=6.40, height=4.80, width=0.01, texture='cmap.png', up=vector(0,1,0))
        





print("cmapanme", cmapanme)
print(subDir)
files = os.listdir(subDir)
files.sort()
imgs = []



# sys.exit()

y = [s for s in files if ('.json' in s)]
imgs = [(subDir + '\\cropped\\' + s) for s in  os.listdir(subDir + '\\cropped') if ('_crop_1010.' in s)]

pitch = []
roll  = []
Azimuth = []
for yy in y:
    fname = subDir + '/' + yy.split('.')[0] + '.json'
    file = open(fname, 'r', encoding = 'utf-8')
    JsonDict = json.loads(file.read())
    # print(JsonDict['Pitch'], JsonDict['Roll'], JsonDict['Azimuth'] )
    pitch.append(float(JsonDict['Pitch']))
    roll.append(float(JsonDict['Roll']))
    Azimuth.append(float(JsonDict['Azimuth']))
    print(float(JsonDict['Pitch']), float(JsonDict['Roll']), float(JsonDict['Azimuth']))
# print(imgs)
# sys.exit()


NDVI = np.load(subDir + '/compiled/NDVI.npy')
ndvi = NDVI[:,indexOfindex]



#creating the 3d canvas
scene = canvas(width=1000, height=800)
tmp = arrow(pos=vector(0,0,0), axis=vector(0,-5,0), shaftwidth=0.05)

num = len(pitch)
print(num, len(imgs))

#ElAzRGB = np.zeros((240*48*num, 5))
ElAzRGB = np.zeros((240*240*num, 5))

for i in range(num):
    #l = l0 * ndvi[i]
    y = - np.sin(pitch[i]  * np.pi / 180.)
    x = - np.cos(pitch[i]  * np.pi / 180.) * np.cos(Azimuth[i]  * np.pi / 180.)
    z = - np.cos(pitch[i]  * np.pi / 180.) * np.sin(Azimuth[i]  * np.pi / 180.)


    a,b,c = x,y,z
    abc = np.sqrt(a*a + b*b + c*c)
    aa = -a*b / abc
    bb = -(b*b) / abc + 1 
    cc = -c*b / abc

    x0,y0,z0 = x,y,z
    normalVectorPlane = np.array((x0, y0, z0))
    normalVectorPlane/= np.linalg.norm(normalVectorPlane) 


    qx = matmul(R(normalVectorPlane, roll[i]), np.array((aa, bb, cc)).reshape(3,1))
    qx = qx/np.linalg.norm(qx)
    aa,bb,cc = qx[0][0],qx[1][0],qx[2][0]

    qx = matmul(R(normalVectorPlane, roll[i] + 90), np.array((aa, bb, cc)).reshape(3,1))
    qx = qx/np.linalg.norm(qx)
    aaa,bbb,ccc = qx[0][0],qx[1][0],qx[2][0]

    q = 16
    abc = abc * q
    #         hei = 2 * abc * np.tan(5*np.pi/180)
    #         wid = 2 * abc * np.tan(1*np.pi/180)
    hei = 2 * abc * np.tan(10*np.pi/180)
    wid = 2 * abc * np.tan(10*np.pi/180)

    if pic:
        tmp1 = box(pos=vector(x*q,y*q,z*q), axis=vector(x,y,z), length=0.05, height=hei, width=wid, texture=imgs[i], up=vector(aa,bb,cc))
        print(i, '\t', imgs[i], hei, wid)
    q=8

    # tmp1 = box(pos=vector(x*q,y*q,z*q), axis=vector(x,y,z), length=0.05, height=.8, width=.8, color = vector(1-ndvi[i],ndvi[i],0), up=vector(aa,bb,cc))
    # print("ndvi[i]", ndvi[i])
    if(ndvi[i] > vmax ):
        _r,_g,_b = 0.6,0.6,0.6
    elif(ndvi[i] < vmin):
        _r,_g,_b = 0.3,0.3,0.3
    else:    
        _r,_g,_b,_a = cmapFunc(colorNormFunc(ndvi[i]))
    tmp1 = box(pos=vector(x*q,y*q,z*q), axis=vector(x,y,z), length=0.05, height=.8, width=.8, color = vector(_r,_g,_b), up=vector(aa,bb,cc))



    q = 16


T = text(text=subDir, align='center', color=color.green, height=0.3)






