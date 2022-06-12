from copy import deepcopy
import torchvision
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn
#from MyModel import MnistModel
from Loader import *

if __name__ == '__main__':
  #参数
  miniBatch = 100   #批大小

  #部署GPU
  device = torch.device("cuda")
  #数据
  testSet = FingerVainDataSet("Test",prePorcess=False,fakeTrain=False)     #如果做过预处理将prePorcess设置为False
  verifyLoader = DataLoader(testSet,miniBatch,shuffle=False)
  verifyLen = len(testSet)

  #模型
  #myModel = MnistModel()
  myModel = torchvision.models.vgg16()
  #mish版vgg16需要修改的部分
  for i in range(len(myModel.features)):
    if isinstance(myModel.features[i],nn.ReLU):
      myModel.features[i] = nn.Mish(inplace=True)
  for i in range(len(myModel.classifier)):
    if isinstance(myModel.classifier[i],nn.ReLU):
      myModel.classifier[i] = nn.Mish(inplace=True)

  myModel.classifier[6] = nn.Linear(4096,312)
  myModel.load_state_dict(torch.load("./Models/mish.pth"))
  myModel = myModel.to(device)
  
  #代价函数
  lossFn = nn.CrossEntropyLoss()
  lossFn = lossFn.to(device)

  #参数
  myModel.train(False)
  totalLoss = 0     #总损失
  AvgLoss = 0       #平均损失
  rightRate = 0     #正确率
  rightCount = 0
  with torch.no_grad():
    for data in verifyLoader:
      imgs,targets = data
      imgs = imgs.to(device)
      targets = targets.to(device)
      outputs = myModel(imgs)                     #跑验证集
      result = torch.argmax(outputs,1)            #取最大值
      rightCount += torch.sum(result==targets)    #和标签比较
      loss = lossFn(outputs,targets)              #代价函数
      totalLoss+=loss
      
    print()
    rightRate = rightCount/verifyLen*100
    AvgLoss = totalLoss/(verifyLen/miniBatch)
  print(f"验证损失:{AvgLoss:.3f}，正确率：{rightRate:.2f}%")