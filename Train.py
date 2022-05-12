from copy import deepcopy
import shutil
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn
#from MyModel import MnistModel
from Loader import *

if __name__ == '__main__':
  #部署GPU
  #device = torch.device("cuda")
  #数据
  trainSet = MnistDataSet("Train")
  #verifySet = MnistDataSet("Verify")
  trainLoader= DataLoader(trainSet,150,shuffle=True,num_workers=0,drop_last=True)
  #verifyLoader = DataLoader(verifySet,150,shuffle=False)
  trainLen = len(trainSet)
  """
  verifyLen = len(verifySet)

  #模型
  #myModel = MnistModel()
  myModel = torchvision.models.vgg16()
  myModel.classifier[6] = nn.Linear(4096,15)
  print(myModel)
  myModel = myModel.to(device)
  
  #代价函数
  lossFn = nn.CrossEntropyLoss()
  lossFn = lossFn.to(device)

  #优化器
  learn_rate = 1e-4
  optimizer = torch.optim.Adam(myModel.parameters(),lr = learn_rate)
  scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,mode="min",factor=0.5,patience=100,verbose=True)

  #参数
  train_step = 0
  tset_step = 0

  logWriter = SummaryWriter("TrainLogs")

  i = 0
  totalLoss = 0
  rightRate = 0
  maxRightRate = 0
  wait = 0    #当指定epoth后验证集准确率不再上升，则自动停止训练
  maxwait = 5
  while(True):
    myModel.train(True)
    print(f"==========第{i+1}轮训练开始==========")
    i+=1
    for data in trainLoader:
      imgs,targets = data
      imgs = imgs.to(device)
      targets = targets.to(device)
      outputs = myModel(imgs)
      loss = lossFn(outputs,targets)
      #写日志
      logWriter.add_scalar("train Loss",loss,train_step)
      #优化模型
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()
      scheduler.step(loss)
      train_step+=1

    myModel.train(False)
    print("正在计算训练集准确度")
    trainTotalLoss = 0
    trainRightRate = 0
    trainRightCount = 0
    with torch.no_grad():
      for data in trainLoader:
        imgs,targets = data
        imgs = imgs.to(device)
        targets = targets.to(device)
        outputs = myModel(imgs)                     #跑训练集
        result = torch.argmax(outputs,1)            #取最大值
        trainRightCount += torch.sum(result==targets)     #和标签比较
        loss = lossFn(outputs,targets)              #代价函数
        trainTotalLoss+=loss
      trainRightRate = trainRightCount/trainLen*100
    print(f"训练损失:{trainTotalLoss/(trainLen/150)}，正确率：{trainRightRate:.2f}%")
    logWriter.add_scalar("Train RT",trainRightRate,i)


    print("正在计算验证集准确度")

    rightCount = 0
    with torch.no_grad():
      for data in verifyLoader:
        imgs,targets = data
        imgs = imgs.to(device)
        targets = targets.to(device)
        outputs = myModel(imgs)                     #跑验证集
        result = torch.argmax(outputs,1)            #取最大值
        rightCount += torch.sum(result==targets)     #和标签比较
        loss = lossFn(outputs,targets)              #代价函数
        logWriter.add_images("Test data",imgs,train_step)
        totalLoss+=loss
      rightRate = rightCount/verifyLen*100
    print(f"验证损失:{totalLoss/(verifyLen/150)}，正确率：{rightRate:.2f}%")
    
    logWriter.add_scalar("Test RT",rightRate,i)
    #检测是否要停止训练
    if(rightRate > maxRightRate):
      maxRightRate = rightRate
      wait = 0
      torch.save(myModel.state_dict(),"myModel.pth")    #每训练一轮保存一次参数
    else:
      wait+=1
      if(wait == maxwait):
        logWriter.close()
        exit(0)
  """
  shutil.rmtree("TrainLogs",ignore_errors=True)
  logWriter = SummaryWriter("TrainLogs")
  for batch in trainLoader:
    logWriter.add_images("train images",batch[0],1)
    break
  logWriter.close()