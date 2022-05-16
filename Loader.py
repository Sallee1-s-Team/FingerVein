import os
from torch.utils.data.dataset import Dataset
from copy import deepcopy
import numpy as np
import torch
import torch.torch_version 
import cv2
import csv
from skimage import morphology as mp
import shutil
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard import SummaryWriter
from matplotlib import pyplot
#from MyModel import MnistModel

class FingerVainDataSet(Dataset):
  def __init__(self,rootDir) -> None:
    self.rootDir = rootDir
    super().__init__()
    # 生成文件列表
    self.FileList = []
    with open(f"{self.rootDir}/data.csv",mode="r",encoding="utf8") as csvFile:
      reader = csv.reader(csvFile)
      next(reader)            #读掉表头
      for row in reader:
        self.FileList.append((f"{self.rootDir}/{row[0]}_{row[1]}_{row[2]}_{row[3]}_roi.bmp",(int(row[0])-1)*2+int(row[2][1])-1))  #样本编号成数字，其中每两个编号代表一个人的两个不同的手指

    # 预处理，放在临时文件夹里
    shutil.rmtree(f"Temp/{self.rootDir}",ignore_errors=True)
    if(f"Temp/{rootDir}" not in os.listdir("Temp")):
      os.mkdir(f"Temp/{rootDir}")      
    for file in self.FileList:
      img = cv2.imread(file[0],flags=0)
      img = self.__imgPrepoocess(img)     #实际预处理代码
      cv2.imwrite(f"Temp/{file[0]}",img)


  def __imgPrepoocess(self,img):
    wd = img.shape[1];ht = img.shape[0]
    img = img[15:ht-15,75:wd-100]          #裁剪
    # oriImg = deepcopy(img)                 #复制原图用来叠底
    # wd = img.shape[1];ht = img.shape[0]
    # img = cv2.equalizeHist(img)            #直方图均衡化
    # img = cv2.blur(img,ksize=(5,5))
    # img = cv2.Laplacian(img,-1,ksize=3)
    # img = cv2.medianBlur(img,ksize=7)      #中值滤波
    # img = cv2.equalizeHist(img)            #直方图均衡化
    # img = np.where(img < 50,False,True)    #二值化
    # img = mp.remove_small_objects(img,min_size=16)      #丢弃小连通图
    # img = mp.closing(img,selem=mp.disk(3)) #闭运算
    # img = mp.skeletonize(img)              #骨架
    # img = mp.dilation(img,selem=mp.square(3))
    # img = img.astype("uint8")*255
    # img = cv2.blur(img,ksize=(5,5))        #加粗&模糊骨架
    # img = ((1 - (img / img.max()))*oriImg).astype("uint8")    #叠加在原图上
    return img

  def __gamma(self,img,gammaVal):         #伽马变换
    return ((img.astype(float) / 255) ** gammaVal * 255).astype("uint8")

  # 一维均值滤波
  def __average1D(self,arr:np.ndarray,windowSize:int)->np.ndarray:
    arr = arr.astype(float)
    arrLen = arr.shape[0]
    cov1dSize = int((windowSize * arrLen) // 2)
    cov1dres = np.zeros(arr.shape)                            #用来接收一维卷积结果
    for i in range(-cov1dSize,cov1dSize+1,1):               
      posX = np.clip(np.arange(i,arrLen+i),0,arrLen-1)        #求坐标数组用来取坐标
      cov1dres += arr[posX]                                   #卷积累加
    return cov1dres / (cov1dSize * 2 + 1)                     #计算平均值            

  def __contest(self,img:np.ndarray,val:float):               #S形对比度增强函数，利用指数/对数函数
    mapping = np.arange(0,256)
    Map = ((np.arange(0,128) / 127) ** val * 127).astype("uint8")
    mapping[0:128] = Map
    mapping[255:127:-1] = -Map+255
    mapping = mapping.astype("uint8")
    return mapping[img]

  def __getitem__(self, index):
    img = cv2.imread(f"Temp/{self.FileList[index][0]}",flags=cv2.IMREAD_GRAYSCALE)
    img = torch.from_numpy(img)           #从numpy转换成张量（用来部署到显卡）
    img = img.unsqueeze(0)
    img = img.repeat_interleave(3,0)
    return img.float(), self.FileList[index][1]
      
  def __len__(self):
    return len(self.FileList)



if __name__ == '__main__':
  #参数
  batch = 200   #批大小
  #数据
  trainSet = FingerVainDataSet("Train")
  trainLoader= DataLoader(trainSet,batch,shuffle=True,num_workers=0,drop_last=True)

  trainLen = len(trainSet)

  shutil.rmtree("TrainLogs",ignore_errors=True)
  logWriter = SummaryWriter("TrainLogs")
  for batch in trainLoader:
    logWriter.add_images("train images",batch[0],1)
    break
  logWriter.close()
  exit(0)
  
  trainSet = FingerVainDataSet("Train")
  shutil.rmtree("TrainLogs",ignore_errors=True)
  logWriter = SummaryWriter("TrainLogs")
  logWriter.add_image("testImg",trainSet[0][0])
  logWriter.close()
