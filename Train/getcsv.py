import os
import re
import csv


def getFileList(root:str,REpattern:str):
  files = os.listdir(root)
  Pattern = re.compile(REpattern)
  Filterfiles = []
  for file in files:
    if(re.search(Pattern,file) != None):
      Filterfiles.append(file)
  return Filterfiles

if __name__ == "__main__":
  FileLists = getFileList("data/",r".+\.bmp$")
  head = ["person","simple","finger","times"]

  with open("allData.csv","w",encoding="utf8",newline="")as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(head)
    for fileName in FileLists:
      fileNos = str.split(fileName,"_")
      csvWriter.writerow(fileNos[:-1])