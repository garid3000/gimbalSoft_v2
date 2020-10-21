from _2EARGB_3d_full import *
from new_3_2dRGB_plane_1 import *
dr = "C:/Users/Garid/Documents/gimbalSoft/19_1221_newer/13h_ARRgood"
dr = 'C:/Users/Garid/Documents/gimbalSoft/New/2019-12-20/14h_ザルディbad'

eargb = EARGB(dr)
p2d = project_2d(dr, show = True, peri = True)


p2d.savePeriImg()
p2d.saveIndexImg()