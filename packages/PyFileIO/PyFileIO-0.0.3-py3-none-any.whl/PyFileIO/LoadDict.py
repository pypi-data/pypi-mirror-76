import os
import pickle

def LoadDict(Fname):
	'''
	Loads a python dict object from a file.
	
	Inputs:
		Fname: file name and path.
		
	Output:
		python dict object.
	'''
	if not os.path.isfile(Fname):
		print('File not found')
		return None
	
	f = open(Fname,'rb')
	Obj = pickle.load(f)
	f.close()
	return Obj
