from torch.utils.data.dataset import Dataset
from copy import deepcopy
import math
import numpy as np
import torch
import torch.torch_version 
from torch import nn
import cv2
import csv
from skimage import morphology

class MnistDataSet(Dataset):
  def __init__(self,rootDir) -> None:
    super().__init__()
    self.FileList = []
    with open(f"{rootDir}/data.csv",mode="r",encoding="utf8") as csvFile:
      reader = csv.reader(csvFile)
      next(reader)            #读掉表头
      for row in reader:
        self.FileList.append((f"{rootDir}/{row[0]}_{row[1]}_{row[2]}_{row[3]}_roi.bmp",(int(row[0])-1)*2+int(row[2][1])-1))  #样本编号成数字，其中每两个编号代表一个人的两个不同的手指

  def __imgPrepoocess(self,img,target):
    # 在这里写上预处理代码
    
    img = torch.from_numpy(img)
    return img
    
  def __getitem__(self, index):
    img = cv2.imread(self.FileList[index][0],flags=cv2.IMREAD_GRAYSCALE)
    img = self.__imgPrepoocess(img,self.FileList[index][1])
    img = img.unsqueeze(0)
    img = img.repeat_interleave(3,0)
    return img, self.FileList[index][1]
      
  def __len__(self):
    return len(self.FileList)