from torch.utils.data.dataset import Dataset
from copy import deepcopy
import numpy as np
import torch
import torch.torch_version 
import cv2
import csv
from skimage import morphology
import shutil
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard import SummaryWriter
from matplotlib import pyplot
#from MyModel import MnistModel

class FingerVainDataSet(Dataset):
  def __init__(self,rootDir) -> None:
    self.step = 0
    super().__init__()
    self.FileList = []
    with open(f"{rootDir}/data.csv",mode="r",encoding="utf8") as csvFile:
      reader = csv.reader(csvFile)
      next(reader)            #读掉表头
      for row in reader:
        self.FileList.append((f"{rootDir}/{row[0]}_{row[1]}_{row[2]}_{row[3]}_roi.bmp",(int(row[0])-1)*2+int(row[2][1])-1))  #样本编号成数字，其中每两个编号代表一个人的两个不同的手指

  def __imgPrepoocess(self,img,target):
    wd = img.shape[1]
    ht = img.shape[0]
    # 在这里写上预处理代码
    img = (255*(img.astype(float)-img.min()) / (img.max() - img.min())).astype("uint8")
    #img = self.__getRoi(img,0.8,0.3)      #查找感兴趣区域
    img = 
    img = cv2.resize(img,dsize=(300,100),interpolation=cv2.INTER_LINEAR)    #训练需要图像大小相同，统一缩放
    img = torch.from_numpy(img)           #从numpy转换成张量（用来部署到显卡）

    #return img.float()
    return img

  # 获取裁切区域
  def __getRoi(self,img:np.ndarray,edgeThread:float,kSizeRate:float):    #图像，边缘亮度钳制，核大小
    wd = img.shape[1]
    ht = img.shape[0]
    cutUp = 0;cutDown=ht;cutLeft=0;cutRight=wd    #裁切点 
    # 纵向裁切
    midXPos = wd // 2                             #求中心纵线位置
    midXHist = img[:,midXPos]                     #获取纵线的亮度变化
    midXHist = self.__Average1D(midXHist,0.1)     #一维均值滤波
    midXHist = midXHist.astype(float) / 255       #规格化到0.0~1.0
    # 输出图像纵向裁切，利用中线值
    for i in range(ht):                           #从上扫描，遇到低于阈值的点停止
      if(midXHist[i] < edgeThread): 
        cutUp = i;break
    for i in range(ht-1,-1,-1):                   #从下扫描，遇到低于阈值的点停止
      if(midXHist[i] < edgeThread): 
        cutDown = i + 1;break
    
    # 横向裁切
    referimg = img[15:ht-15,0:wd-50]                     #去除上下和右侧的亮区作为参考图像
    referimg = cv2.equalizeHist(referimg)                #直方图均衡化
    referimg = ((referimg.astype(float) / 255) ** 10 * 255).astype("uint8")    #伽马，降低暗区的权重
    sumYHist = np.sum(referimg,axis=0)                   #获取纵向投影直方图
    sumYHist = self.__Average1D(sumYHist,0.1)            #一维均值滤波
    sumYHist = sumYHist.astype(float) / sumYHist.max()   #规格化到0.0~1.0

    # pyplot.plot(sumYHist)
    # pyplot.show()
    # 输出图像横向裁切，利用参考投影直方图
    maxValues = []                                    #查找所有极值点
    for i in range(1,referimg.shape[1]-1):            #从左扫描，遇到峰值点
      if(sumYHist[i] >= sumYHist[i-1] and sumYHist[i] >= sumYHist[i+1]):  #找到极值点（或拐点）
        lUp =False; rUp = False
        if(sumYHist[i-1]==sumYHist[i+1]):     #如果左右界相同，就需要比较以免选取到拐点
          for L in range(1,i+1):
            if(sumYHist[i-L] < sumYHist[i-1]):lUp = True;break;
            elif(sumYHist[i-L] > sumYHist[i-1]):break;
          for R in range(1,referimg.shape[1]-i):
            if(sumYHist[i+R] > sumYHist[i+R]):lUp = True;break;
            elif(sumYHist[i+R] < sumYHist[i+R]):break;
          if(not (lUp and rUp)):
            continue      #是拐点，继续循环
        maxValues.append(i)

    maxValuesIdx = np.argsort(maxValues)
    cutLeft = maxValues[maxValuesIdx[0]]
    cutRight = maxValues[maxValuesIdx[1]]

    if(cutLeft > cutRight):
      cutLeft,cutRight = cutRight,cutLeft
    
    img = img[cutUp:cutDown,cutLeft:cutRight]     #cv2没有裁切函数，需要使用numpy切片实现
    if(cutUp >= cutDown):print("上下裁切错误")
    if(cutLeft >= cutRight):print("左右裁切错误")
    return img

  # 一维均值滤波
  def __Average1D(self,arr:np.ndarray,windowSize:int)->np.ndarray:
    arr = arr.astype(float)
    arrLen = arr.shape[0]
    cov1dSize = int((windowSize * arrLen) // 2)
    cov1dres = np.zeros(arr.shape)                            #用来接收一维卷积结果
    for i in range(-cov1dSize,cov1dSize+1,1):               
      posX = np.clip(np.arange(i,arrLen+i),0,arrLen-1)        #求坐标数组用来取坐标
      cov1dres += arr[posX]                                   #卷积累加
    return cov1dres / (cov1dSize * 2 + 1)                     #计算平均值            

  def __contest(self,img:np.ndarray,pow:float):               #S形对比度增强函数，利用指数/对数函数
    if(pow == 1):return img
    mapping = np.arange(0,256)
    #指数模式
    if(pow >= 1):
      Map = np.clip(np.round((np.power(pow,(np.arange(0,128).astype(np.float64))/127)-1)/(pow-1)*127),0,127)
    #对数模式
    else:
      pow = 1 / pow
      Map = np.clip((np.round((np.log(np.arange(0,128).astype(np.float64)/(127/(pow-1))+1)/np.log(pow))*127)),0,127)
    mapping[0:128] = Map
    mapping[255:127:-1] = -Map+255
    mapping = mapping.astype("uint8")
    return mapping[img]

  def __getitem__(self, index):
    img = cv2.imread(self.FileList[index][0],flags=cv2.IMREAD_GRAYSCALE)
    img = self.__imgPrepoocess(img,self.FileList[index][1])
    img = img.unsqueeze(0)
    img = img.repeat_interleave(3,0)
    return img, self.FileList[index][1]
      
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
