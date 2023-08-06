import io
import PIL
import pickle
import requests
from sklearn.preprocessing import normalize
import os
class text():
  def __init__(self,text):
    self.text = text

  def getw2v_light(self):
    from botnoi import getw2v as gw
    modpath = os.path.join(os.path.dirname(gw.__file__),'botnoiw2v_small.mod')
    mod = pickle.load(open(modpath,'rb'))
    #return modpath
    feat = gw.sentencevector(self.text,mod)
    feat = normalize([feat])[0]
    self.w2v_light = feat
    return feat

  def save(self,filename):
    pickle.dump(self,open(filename,'wb'))



