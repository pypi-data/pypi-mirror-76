import pickle

def SaveDict(Obj,Fname):
	'''
	This function saves the contents of a python dict object into a 
	binary file using pickle.
	
	Inputs:
		Obj: python dict object
		Fname: path to output file.
	
	'''
	f = open(Fname,'wb')
	pickle.dump(Obj,f,pickle.HIGHEST_PROTOCOL)
	f.close()
	
