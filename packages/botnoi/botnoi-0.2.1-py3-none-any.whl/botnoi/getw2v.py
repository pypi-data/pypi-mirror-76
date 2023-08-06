import pandas as pd
import glob
from pythainlp.tokenize import word_tokenize
import pickle
import numpy as np
import os
#import pkg_resources
#path = 'botnoiw2v_small.mod'
#modloc = pkg_resources.resource_filename(__name__,path)

#mod = pickle.load(open(modloc))
def sentencevector(sentence,mod):
	wList = word_tokenize(str(sentence),engine='newmm')
	wvec = []
	for w in wList:
		try:
			wvec.append(mod[w])
		except:
			pass
	if len(wvec)==0:
		return np.zeros(50)

	return np.mean(wvec,0)