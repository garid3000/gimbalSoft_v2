import sys
import os
import json
import pickle


def slashChanger(someString):
	tmp = ''
	for char in someString:
		if char == '\\':
			tmp += '/'
		else:
			tmp +=char
	return tmp

class fileRegister(object):
	"""docstring for fileRegister"""
	def __init__(self, arg):
		super(fileRegister, self).__init__()
		self.arg = arg




class singleShot(object):
	"""docstring for singleShot"""
	def __init__(self, id, pics_dir, json_dir, crop_dir, full_dir, spec_dir):
		super(singleShot, self).__init__()
		self.id       = id
		self.pics_dir = pics_dir
		self.json_dir = json_dir
		self.crop_dir = crop_dir
		self.full_dir = full_dir
		self.spec_dir = spec_dir
		self.crop_img_dir = None

		self.plot_img_full = None
		self.plot_img_crop = None
		self.plot_img_spec = None


		file = open(self.json_dir, 'r', encoding = 'utf-8')
		self.jsonDic = json.loads(file.read())
		file.close()

def refreshFolder(directory):
	directory = slashChanger(directory)
	print(directory)
	try:
		fnames = [s for s in os.listdir(directory) if os.path.isfile(directory + '/' + s) and '.jpeg' in s]
	except:
		return []
	print(fnames)
	fnames.sort()
	Fnames = [directory + '/' + s for s in fnames]

	mainThing = []
	for fname in fnames:
		tmp_pic_dir = directory + '/' + fname
		ID = fname.split('.')[0]
		tmp_json_dir = directory + '/' + ID + '.json' 		if os.path.isfile(directory + '/' + ID + '.json') else None
		tmp_crop_dir = directory + '/' + ID + '_crop.csv' 	if os.path.isfile(directory + '/' + ID + '_crop.csv') else None
		tmp_full_dir = directory + '/' + ID + '_full.csv' 	if os.path.isfile(directory + '/' + ID + '_full.csv') else None
		tmp_spec_dir = directory + '/' + ID + '_spec_NDVI.csv' if os.path.isfile(directory + '/' + ID + '_spec_NDVI.csv') else None
		mainThing.append(singleShot(ID, tmp_pic_dir, tmp_json_dir, tmp_crop_dir, tmp_full_dir, tmp_spec_dir))
	
	try:
		os.mkdir(directory + "/meta")
	except:
		pass

	with open(directory + '/meta/about.meta', 'wb') as config_dictionary_file:
		pickle.dump(mainThing, config_dictionary_file)
	return mainThing

def readMdata(directory):
	if (os.path.isfile(directory + '/meta/about.meta')):
		try:
			with open(directory + '/meta/about.meta', 'rb') as config_dictionary_file:
				mainThing = pickle.load(config_dictionary_file)
			return mainThing
		except:
			return None
	return refreshFolder(directory)
# refreshFolder(sys.aasdrgv[1])