from copy import deepcopy
from math import ceil

import torchvision.models as models
import torch

import numpy as np
from torch import Tensor
from torch import nn

class MyModel(nn.Module):
  def __init__(self) -> None:
    super(MyModel,self).__init__()
    self.feature = nn.Sequential(
      #32x3
      nn.Conv2d(3,32,3,1,1),    nn.Mish(inplace=True),
      nn.Conv2d(32,32,3,1,1),   nn.Mish(inplace=True),
      nn.Conv2d(32,32,3,1,1),   nn.Mish(inplace=True),
      nn.MaxPool2d(2),
      #64x3
      nn.Conv2d(32,64,3,1,1),   nn.Mish(inplace=True),
      nn.Conv2d(64,64,3,1,1),   nn.Mish(inplace=True),
      nn.Conv2d(64,64,3,1,1),   nn.Mish(inplace=True),
      nn.MaxPool2d(2),
      #128x3
      nn.Conv2d(64,128,3,1,1),  nn.Mish(inplace=True),
      nn.Conv2d(128,128,3,1,1), nn.Mish(inplace=True),
      nn.Conv2d(128,128,3,1,1), nn.Mish(inplace=True),
      nn.MaxPool2d(2)
    )
    #规格化输出为8x8
    self.avgpool = nn.AdaptiveAvgPool2d((8,8))
    self.classifier = nn.Sequential(
      nn.Linear(128*8*8,512),    nn.Mish(inplace=True),nn.Dropout(0.5),
      nn.Linear(512,512),       nn.Mish(inplace=True),nn.Dropout(0.5),
      nn.Linear(512,10)
    )
  
  def forward(self,x:Tensor)->Tensor:
    x = self.feature(x)
    x = self.avgpool(x)
    x = torch.flatten(x,1)
    x = self.classifier(x)
    return x

if __name__ == "__main__":
  fingerModel = MyModel()
  #fingerModel = models.vgg16()
  fingerModel.classifier[-1] = nn.Linear(512,312)
  print(fingerModel)

  #测试模型输出
  input = torch.ones((64,3,64,64))
  output = fingerModel(input)
  print(output.shape)