import os
import re
import numpy as np
import cv2
import csv
import random as rd
import PIL

class fakeTrain:
  @staticmethod
  def createFakeTrain():
    with open(f"../Train/data.csv") as realFile:
      realCsv = csv.reader(realFile,skipinitialspace=True)
      next(realCsv)
      samples = {}
      #获取文件名列表
      for row in realCsv:
        people = int(row[0])
        finger = int(row[2][1])
        if((people,finger) not in samples):
          samples[(people,finger)] = [row]
        else:
          samples[(people,finger)].append(row)
      #根据现有文件数量扩增
      for groupImg in samples.values():
        count = len(groupImg)
        for i in range(count,100):
          item = groupImg[i%count]
          fileName = f"../Train/{item[0]}_{item[1]}_{item[2]}_{item[3]}_roi.bmp"
          img = cv2.imread(fileName)
          cv2.imwrite(f"fake_{item[0]}_{item[2]}_{i}.bmp",fakeTrain.makeFakeImg(img))
    
    fakeTrain.getCsv()

  @staticmethod
  def makeFakeImg(img:np.ndarray)->np.ndarray:
    def getRd(base:float,range:float):
      return base + (rd.random() * 2 - 1)*range
    wd = img.shape[1]; ht = img.shape[0]
    #透视变换矩阵
    s = 5
    PerspMat = cv2.getPerspectiveTransform(np.asarray([[0,0],[0,wd],[ht,0],[ht,wd]],dtype="float32"),
      np.asarray([[getRd(0,s),getRd(0,s)],[getRd(0,s),getRd(wd,s)],[getRd(ht,s),getRd(0,s)],[getRd(ht,s),getRd(wd,s)]],dtype="float32"))
    img = cv2.warpPerspective(img,PerspMat,dsize=(wd,ht),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    #伽马变换
    img = np.clip((img.astype(float) / 255) ** getRd(1,0.1) * 255,0,255).astype("uint8")
    #噪点
    noiseMask = np.repeat((np.random.randint(-255,255,size=(ht,wd)) * getRd(0,0.04))[:,:,np.newaxis],3,2)
    img = np.clip((img.astype(float)+ noiseMask),0,255).astype("uint8")
    return img

  @staticmethod
  def getCsv():
    def getFileList(root:str,REpattern:str):
      files = os.listdir(root)
      Pattern = re.compile(REpattern)
      Filterfiles = []
      for file in files:
        if(re.search(Pattern,file) != None):
          Filterfiles.append(file)
      return Filterfiles
    
    fileLists = getFileList(".",r".+\.bmp$")

    with open("data.csv","w",encoding="utf8",newline="")as csvFile:
      csvWriter = csv.writer(csvFile)
      head = ["person","finger","simple"]
      csvWriter.writerow(head)
      for fileName in fileLists:
        fileNos = str.split(fileName,"_")
        fileNos[3] = fileNos[3][:-4]
        csvWriter.writerow(fileNos[1:])


if __name__ == "__main__":
  fakeTrain.createFakeTrain()
  fakeTrain.getCsv()