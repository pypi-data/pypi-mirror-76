import io
import PIL
import pickle
import requests
from sklearn.preprocessing import normalize
class text():
  def __init__(self,text):
    self.text = text

  def getw2v_light(self):
    from botnoi import getw2v as gw
    feat = gw.sentencevector(self.text)
    feat = normalize([feat])[0]
    self.w2v_light = feat
    return feat

  def save(self,filename):
    pickle.dump(self,open(filename,'wb'))



