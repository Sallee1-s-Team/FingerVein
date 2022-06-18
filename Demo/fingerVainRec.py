import copy
import math
import os
import shutil

import cv2
import numpy as np
import skimage.morphology as mp
import torch
import torchvision

from myModel import MyModel
from torch import nn
from matplotlib import pyplot

class fingerVainRec:
  # 如果需要打包成单独的程序，则需要手动提供模型路径
  # 以下代码摘自Loader.py,Test.py
  def __init__(self,modelPath="../Models/myModel.pth"):
    # 模型
    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    self.myModel = MyModel()
    
    self.myModel.classifier[6] = nn.Linear(512,312)
    self.myModel.load_state_dict(torch.load(modelPath))
    self.myModel = self.myModel.to(self.device)
    self.myModel.train(False)
    # 代价函数
    self.lossFn = nn.CrossEntropyLoss()
    self.lossFn = self.lossFn.to(self.device)

  def getResult(self,img):
    self.showImg = copy.deepcopy(img)
    self.testImg = copy.deepcopy(img)
    self.showImg,self.testImg = self.__imgPreprocess(self.testImg)
    self.testImg = np.repeat(self.testImg[np.newaxis,np.newaxis,:,:],3,axis=1)
    self.testImg = torch.from_numpy(np.asarray(self.testImg)).type(torch.float)
    return self.test()

  def __imgPreprocess(self,img):
    wd = img.shape[1];ht = img.shape[0]
    oriImg = copy.deepcopy(img)            #复制原图用来叠底
    img = oriImg[15:ht-15,75:wd-100]       #裁剪
    img = cv2.equalizeHist(img)            #直方图均衡化
    img = cv2.blur(img,ksize=(5,5))
    img = cv2.Laplacian(img,-1,ksize=3)
    img = cv2.medianBlur(img,ksize=7)      #中值滤波
    img = cv2.equalizeHist(img)            #直方图均衡化
    img = np.where(img < 50,False,True)    #二值化
    img = mp.remove_small_objects(img,min_size=16)      #丢弃小连通图
    img = mp.closing(img,selem=mp.disk(3)) #闭运算
    img = mp.skeletonize(img)              #骨架
    img = mp.dilation(img,selem=mp.square(3))
    img = img.astype("uint8")*255

    #展示图片，叠加血管图
    showImg = copy.deepcopy(oriImg)
    showImg = cv2.cvtColor(showImg,cv2.COLOR_GRAY2RGB)
    showImg[15:ht-15,75:wd-100,0] = np.where(img == 255,0,showImg[15:ht-15,75:wd-100,0])
    showImg[15:ht-15,75:wd-100,1] = np.where(img == 255,255,showImg[15:ht-15,75:wd-100,1])
    showImg[15:ht-15,75:wd-100,2] = np.where(img == 255,0,showImg[15:ht-15,75:wd-100,2])
    showImg = cv2.rectangle(showImg,(75,15),(wd-100,ht-15),(0,0,255),2)

    #测试图片
    testImg = cv2.blur(img,ksize=(5,5))
    testImg = ((1 - (testImg / testImg.max()))*oriImg[15:ht-15,75:wd-100]).astype("uint8")    #叠加在原图上

    return showImg,testImg

  def test(self):
    #数据
    testSet = self.testImg
    testSet = testSet.to(self.device)

    with torch.no_grad():
      output = self.myModel(testSet)                 #跑测试集
      output = torch.argmax(output).item()         #取最大值
    return (output // 2 + 1, output % 2 + 1)

if __name__ == "__main__":
  img = cv2.imread("../Test/1_6_f1_1_roi.bmp",flags=cv2.IMREAD_GRAYSCALE)
  fvr = fingerVainRec()
  print(fvr.getResult(img))
  pyplot.imshow(fvr.showImg)
  pyplot.show()