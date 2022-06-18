from copy import deepcopy
import torchvision
import shutil
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn
#from MyModel import MnistModel
from Loader import *
from myModel import MyModel

if __name__ == '__main__':
  #参数
  learn_rate = 1e-3   #学习率
  miniBatch = 50      #批大小
  miniBatchCount = 10  #梯度累加次数

  #部署GPU
  device = torch.device("cuda")
  #数据
  trainSet = FingerVainDataSet("Train",prePorcess=False,fakeTrain=True)      #如果做过预处理将prePorcess设置为False
  verifySet = FingerVainDataSet("Test",prePorcess=False,fakeTrain=False)     #如果做过预处理将prePorcess设置为False
  trainLoader= DataLoader(trainSet,miniBatch,shuffle=True,num_workers=0,drop_last=True)
  verifyLoader = DataLoader(verifySet,miniBatch,shuffle=False)

  trainLen = len(trainSet)
  verifyLen = len(verifySet)

  #模型
  fingerModel = MyModel()
  #fingerModel = torchvision.models.vgg16()
  #将vgg16模型中的ReLU换成mish
  # for i in range(len(fingerModel.features)):
  #   if isinstance(fingerModel.features[i],nn.ReLU):
  #     fingerModel.features[i] = nn.Mish(inplace=True)
  # for i in range(len(fingerModel.classifier)):
  #   if isinstance(fingerModel.classifier[i],nn.ReLU):
  #     fingerModel.classifier[i] = nn.Mish(inplace=True)

  fingerModel.classifier[-1] = nn.Linear(512,312)
  print(fingerModel)
  fingerModel = fingerModel.to(device)
  #代价函数
  lossFn = nn.CrossEntropyLoss()
  lossFn = lossFn.to(device)

  #优化器
  optimizer = torch.optim.Adam(fingerModel.parameters(),lr = learn_rate)
  scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,mode="min",factor=0.5,patience=100,verbose=True)

  #参数
  train_step = 0
  tset_step = 0

  #写训练日志
  shutil.rmtree("TrainLog",ignore_errors=True)
  logWriter = SummaryWriter("TrainLog")

  i = 0
  maxRt = 0         #最小损失
  wait = 0          #超时次数
  maxwait = 10       #最大超时

  while(True):
    optimizer.zero_grad()   #清除上一次最后累计的梯度
    fingerModel.train(True)
    print(f"==========第{i+1}轮训练开始==========")
    i+=1
    batchCount = trainLen // miniBatch    #计算有多少个batch，用来计算进度
    batchi = 0           #用来计算进度
    miniBatchNo = 1      #梯度累加次数
    totalLoss = 0       #梯度累加的总梯度
    for data in trainLoader:
      imgs,targets = data
      imgs = imgs.to(device)
      targets = targets.to(device)
      outputs = fingerModel(imgs)
      AvgLoss = lossFn(outputs,targets)
      AvgLoss = AvgLoss / miniBatchCount
      totalLoss += AvgLoss
      #梯度累加&优化模型
      AvgLoss.backward()
      if(miniBatchNo < miniBatchCount):
        miniBatchNo+=1
      else:
        logWriter.add_scalar("train Loss",totalLoss,train_step)
        optimizer.step()
        scheduler.step(totalLoss)
        optimizer.zero_grad()
        miniBatchNo = 1
        totalLoss = 0
        train_step+=1
      batchi+=1
      print(f"\r训练中，进度{(batchi / batchCount)*100:.2f}%",flush=True,end="")
    print()



    fingerModel.train(False)
    print("正在计算训练集准确度")
    trainTotalLoss = 0
    trainAvgLoss = 0
    trainRightRate = 0
    trainRightCount = 0
    with torch.no_grad():
      batchCount = trainLen // miniBatch
      batchi = 0        #用来输出测试进度
      for data in trainLoader:
        imgs,targets = data
        imgs = imgs.to(device)
        targets = targets.to(device)
        outputs = fingerModel(imgs)                           #跑训练集
        result = torch.argmax(outputs,1)                  #取最大值
        trainRightCount += torch.sum(result==targets)     #和标签比较
        loss = lossFn(outputs,targets)                    #代价函数
        trainTotalLoss+=loss
        batchi += 1
        print(f"\r测试中，进度{(batchi / batchCount)*100:.2f}%",flush=True,end="")
      print()
      trainRightRate = trainRightCount/trainLen*100
      trainAvgLoss = trainTotalLoss/(trainLen/miniBatch)
    print(f"训练损失:{trainAvgLoss:.3f}，正确率：{trainRightRate:.2f}%")
    logWriter.add_scalar("Train RT",trainRightRate,i)

    print("正在计算验证集准确度")
    totalLoss = 0     #总损失
    AvgLoss = 0       #平均损失
    rightRate = 0     #正确率
    rightCount = 0
    with torch.no_grad():
      batchCount = verifyLen // miniBatch + 1
      batchi = 0        #用来输出测试进度
      for data in verifyLoader:
        imgs,targets = data
        imgs = imgs.to(device)
        targets = targets.to(device)
        outputs = fingerModel(imgs)                     #跑验证集
        result = torch.argmax(outputs,1)            #取最大值
        rightCount += torch.sum(result==targets)    #和标签比较
        loss = lossFn(outputs,targets)              #代价函数
        logWriter.add_images("Test data",imgs,train_step)
        totalLoss+=loss
        batchi += 1
        print(f"\r测试中，进度{(batchi / batchCount)*100:.2f}%",flush=True,end="")
      print()
      rightRate = rightCount/verifyLen*100
      AvgLoss = totalLoss/(verifyLen/miniBatch)
    print(f"验证损失:{AvgLoss:.3f}，正确率：{rightRate:.2f}%")
    
    logWriter.add_scalar("Test RT",rightRate,i)
    #检测是否要停止训练
    if(rightRate > maxRt):
      maxRt = rightRate
      wait = 0
      torch.save(fingerModel.state_dict(),"Model.pth")    #每训练一轮保存一次参数
    else:
      wait+=1
      if(wait == maxwait):
        logWriter.close()
        exit(0)