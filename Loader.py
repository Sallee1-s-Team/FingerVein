import os
import random
from torch.utils.data.dataset import Dataset
from copy import deepcopy
import numpy as np
import torch
import cv2
import csv
from skimage import morphology as mp
import shutil
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard import SummaryWriter
from matplotlib import pyplot
#from MyModel import MnistModel


class FingerVainDataSet(Dataset):
  def __init__(self,rootDir,prePorcess = True,fakeTrain = True) -> None:
    self.rootDir = rootDir
    super().__init__()
    # 生成文件列表
    self.FileList = []
    with open(f"{self.rootDir}/data.csv",mode="r",encoding="utf8") as csvFile:
      reader = csv.reader(csvFile)
      next(reader)            #读掉表头
      for row in reader:
        self.FileList.append((f"{self.rootDir}/data/{row[0]}_{row[1]}_{row[2]}_{row[3]}_roi.bmp",(int(row[0])-1)*2+int(row[2][1])-1))  #样本编号成数字，其中每两个编号代表一个人的两个不同的手指

    self.lenFileList = len(self.FileList);i = 0

    if(prePorcess == True):
      # 预处理，放在临时文件夹里
      shutil.rmtree(f"Temp/{self.rootDir}",ignore_errors=True)
      if(f"Temp/{rootDir}" not in os.listdir("Temp")):
        os.makedirs(f"Temp/{rootDir}/data",exist_ok=True)
              
      for file in self.FileList:
        img = cv2.imread(file[0],flags=0)
        img = self.__imgPreprocess(img)     #实际预处理代码
        cv2.imwrite(f"Temp/{file[0]}",img)
        i+=1
        print(f"\r预处理数据集\"{rootDir}\"中，进度{i / self.lenFileList * 100:.2f}%",flush=True,end="")
      print()

    # 生成假数据集列表
    self.fakeFileList = []
    self.lenFakeFileList = 0
    if(fakeTrain):
      with open(f"fakeTrain/data.csv",mode="r",encoding="utf8") as csvFile:
        reader = csv.reader(csvFile)
        next(reader)            #读掉表头
        for row in reader:
          self.fakeFileList.append((f"fakeTrain/data/fake_{row[0]}_{row[1]}_{row[2]}.bmp",(int(row[0])-1)*2+int(row[1][1])-1))  #样本编号成数字，其中每两个编号代表一个人
      self.lenFakeFileList = len(self.fakeFileList);i = 0
      if(prePorcess == True):
        # 预处理，放在临时文件夹里
        shutil.rmtree(f"Temp/fakeTrain",ignore_errors=True)
        if(f"Temp/fakeTrain" not in os.listdir("Temp")):
          os.makedirs(f"Temp/fakeTrain/data",exist_ok=True)      
        for file in self.fakeFileList:
          img = cv2.imread(file[0],flags=0)
          img = self.__imgPreprocess(img)     #实际预处理代码
          cv2.imwrite(f"Temp/{file[0]}",img)
          i+=1
          print(f"\r预处理数据集\"fakeTrain\"中，进度{i / self.lenFakeFileList * 100:.2f}%",flush=True,end="")
        print()

  def __imgPreprocess(self,img):        
    wd = img.shape[1];ht = img.shape[0]
    img = img[15:ht-15,75:wd-100]          #裁剪
    oriImg = deepcopy(img)                 #复制原图用来叠底
    wd = img.shape[1];ht = img.shape[0]
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
    img = cv2.blur(img,ksize=(5,5))        #加粗&模糊骨架
    img = ((1 - (img / img.max()))*oriImg).astype("uint8")    #叠加在原图上
    return img

  
  def __getitem__(self, index):
    if(index < self.lenFileList):     #读取的是真数据集
      img = cv2.imread(f"Temp/{self.FileList[index][0]}",flags=cv2.IMREAD_GRAYSCALE)
      img = torch.from_numpy(img)           #从numpy转换成张量（用来部署到显卡）
      img = img.unsqueeze(0)
      img = img.repeat_interleave(3,0)
      return img.float(), self.FileList[index][1]
    else:          #读取的是假数据集
      index = index - self.lenFileList
      img = cv2.imread(f"Temp/{self.fakeFileList[index][0]}",flags=cv2.IMREAD_GRAYSCALE)
      img = torch.from_numpy(img)           #从numpy转换成张量（用来部署到显卡）
      img = img.unsqueeze(0)
      img = img.repeat_interleave(3,0)
      return img.float(), self.fakeFileList[index][1]
      
  def __len__(self):
    return self.lenFileList + self.lenFakeFileList



if __name__ == '__main__':
  #参数
  miniBatch = 64   #批大小
  #数据
  trainSet = FingerVainDataSet("Train",prePorcess=False,fakeTrain=True)
  trainLoader= DataLoader(trainSet,miniBatch,shuffle=False,num_workers=0,drop_last=True)

  trainLen = len(trainSet)

  shutil.rmtree("LoaderLogs",ignore_errors=True)
  logWriter = SummaryWriter("LoaderLogs")
  step = 0
  for miniBatch in trainLoader:
    logWriter.add_images("train images",miniBatch[0],step)
    step+=1
  logWriter.close()
  exit(0)
