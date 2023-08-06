import pandas as pd
import glob
from pythainlp.tokenize import word_tokenize
import pickle
import numpy as np

mod = pickle.load(open('botnoi/botnoiw2v_small.mod','rb'))
def sentencevector(sentence):
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