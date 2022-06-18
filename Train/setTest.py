import os
import shutil
import csv
from typing import List

sourceFile = open("allData.csv","r",encoding="utf8")
trainFile = open("data.csv","w",newline="",encoding="utf8")
testFile = open("../Test/data.csv","w",newline="",encoding="utf8")
#写文件头
head = sourceFile.readline()
trainFile.write(head)
testFile.write(head)

#建立读写器
soruceReader = csv.reader(sourceFile)
trainWriter = csv.writer(trainFile)
testWriter = csv.writer(testFile)
#建立源字典表
samples = {}
for row in soruceReader:
  people = int(row[0])
  finger = int(row[2][1])
  if((people,finger) not in samples):
    samples[(people,finger)] = [row]
  else:
    samples[(people,finger)].append(row)
#取字典的最后两项作为测试集，相当于每个人每个手指有两张图用来测试
for keys in samples:
  trainSample = samples[keys][0:-2]
  trainWriter.writerows(trainSample)
  testSample = samples[keys][-2:]
  testWriter.writerows(testSample)

sourceFile.close()
trainFile.close()
testFile.close()

#移动文件
with open("../Test/data.csv","r",encoding="utf8") as testFp:
  testReader = csv.reader(testFp)
  next(testReader)

  for row in testReader:
    shutil.move(f"data/{row[0]}_{row[1]}_{row[2]}_{row[3]}_roi.bmp","../Test/data")