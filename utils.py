import cv2
import numpy as np
import glob
import os
import pickle
import math
import io
from PIL import Image

def bytesToCv2Image(imageBytes):
  img = Image.open(io.BytesIO(imageBytes))
  return np.asarray(img)

def getCharArray(img):
  if (len(img.shape) == 3):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img = cv2.GaussianBlur(img, (3, 3), 0) # 高斯模糊
  _, img = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)  #对图像进行二值化操作
  imgArray = np.array(img)
  return imgArray[:22, 5:17], imgArray[:22, 17:29], imgArray[:22, 29:41], imgArray[:22, 41:53]

CACHE_FILE = '.cache'

def loadAllData():
  if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'rb') as f:
      data = pickle.load(f)
  else:
    images = np.array([], np.int)
    labels = np.array([], np.int)
    for imageFileName in glob.glob('./trainPictures/*.png'):
      (_, imageName) = os.path.split(imageFileName)
      imageName = os.path.splitext(imageName)[0]
      imageCharArray = getCharArray(cv2.imread(imageFileName))
      for i in range(4):
        images = np.append(images, (imageCharArray[i] / 255).astype('float32'))
        labels = np.append(labels, charToOneHot(imageName[i]))  
    data = (images.reshape(-1, 22 * 12), labels.reshape(-1, 36))
    with open(CACHE_FILE, 'wb') as f:
      f.write(pickle.dumps(data))
  return data

def nextTrainDataBatch(batchSize, images, labels, i):
  i = i % (math.ceil(images.shape[0] / batchSize))
  return images[i * batchSize : i * batchSize + batchSize], labels[i * batchSize : i * batchSize + batchSize]

def charToOneHot(char):
  oneHot = np.zeros(36, np.int)
  ascii = ord(char)
  if ascii >= 97:
    oneHot[ascii - 87] = 1
  else:
    oneHot[ascii - 48] = 1
  return oneHot

def ontHotToChar(ontHot):
  res = np.argmax(ontHot)
  if (res > 9):
    return chr(res + 87)
  return chr(res + 48)

