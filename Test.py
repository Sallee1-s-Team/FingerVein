from copy import deepcopy
import torchvision
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn
from Loader import *
from myModel import MyModel

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
  fingerModel = MyModel()
  # fingerModel = torchvision.models.vgg16()
  # #mish版vgg16需要修改的部分
  # for i in range(len(fingerModel.features)):
  #   if isinstance(fingerModel.features[i],nn.ReLU):
  #     fingerModel.features[i] = nn.Mish(inplace=True)
  # for i in range(len(fingerModel.classifier)):
  #   if isinstance(fingerModel.classifier[i],nn.ReLU):
  #     fingerModel.classifier[i] = nn.Mish(inplace=True)

  fingerModel.classifier[-1] = nn.Linear(512,312)
  fingerModel.load_state_dict(torch.load("./Models/myModel.pth"))
  fingerModel = fingerModel.to(device)
  
  #代价函数
  lossFn = nn.CrossEntropyLoss()
  lossFn = lossFn.to(device)

  #tensorboard写入识别错误的图像
  shutil.rmtree("./TestLog",ignore_errors=True)
  logWriter = SummaryWriter("TestLog")
  #错误图
  wrongImgs = [[]for i in range(312)]
  wrongResult = [[]for i in range(312)]

  #计算精确率和召回率的数组
  TP = [0]*312
  FP = [0]*312
  FN = [0]*312
  TN = [0]*312

  #参数
  fingerModel.train(False)
  totalLoss = 0     #总损失
  AvgLoss = 0       #平均损失
  rightRate = 0     #正确率
  rightCount = 0
  with torch.no_grad():
    for data in verifyLoader:
      imgs,targets = data
      imgs = imgs.to(device)
      targets = targets.to(device)
      outputs = fingerModel(imgs)                     #跑验证集
      result = torch.argmax(outputs,1)            #取最大值
      rightCount += torch.sum(result==targets)    #和标签比较
      loss = lossFn(outputs,targets)              #代价函数
      totalLoss+=loss

      #写入错误图图片
      for i in range(len(result)):
        if result[i] != targets[i]:
          wrongImgs[targets[i]].append(imgs[i].cpu().numpy().tolist())
          wrongResult[targets[i]].append(result[i].item())

      #统计TP/FP/FN/TN
      for i in range(len(targets)):
        if(result[i]==targets[i]):
          TP[targets[i]]+=1
        else:
          FP[result[i]]+=1
          FN[targets[i]]+=1

    TP = np.array(TP)
    FP = np.array(FP)
    FN = np.array(FN)
    TN = np.array(TN)
    TN = verifyLen-TP-FP-FN
    #计算正确率，精确率，召回率，F1分数
    rightRate = rightCount/verifyLen
    accRate = (TP / (TP+FP))
    recallRate = (TP / (TP+FN))
    F1Score = (2*accRate*recallRate)/(accRate+recallRate)
    AvgLoss = totalLoss/(verifyLen/miniBatch)

  #控制台输出测试结果
  print(f"测试损失:{AvgLoss:.3f},总正确率:{rightRate*100:.3f}%")
  print(f"平均精确率：{np.nanmean(accRate)*100:.2f}%，最大精确率：{np.nanmax(accRate)*100:.2f}%,最小精确率：{np.nanmin(accRate)*100:.2f}%")
  print(f"平均召回率：{np.nanmean(recallRate)*100:.2f}%，最大召回率：{np.nanmax(recallRate)*100:.2f}%,最小召回率：{np.nanmin(recallRate)*100:.2f}%")
  print(f"平均F1分数：{np.nanmean(F1Score):.4f}，最大F1分数：{np.nanmax(F1Score):.4f},最小F1分数：{np.nanmin(F1Score):.4f}")

  #写入tensorboard
  for i in range(len(wrongImgs)):
    imgs = torch.from_numpy(np.asarray(wrongImgs[i]).astype(np.uint8))
    if(len(imgs)!=0):
      logWriter.add_images(f"target:{i//2+1},f{i%2+1},\
      res={[f'{item//2+1},f{item%2+1}' for item in wrongResult[i]]}",imgs)
  logWriter.close()