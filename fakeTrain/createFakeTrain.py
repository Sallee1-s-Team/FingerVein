import cv2
import csv

def createFakeTrain():
  with open(f"../Train/data.csv") as realFile:
    realCsv = csv.reader(realFile,skipinitialspace=True)
    next(realCsv)
    samples = {}
    for row in realCsv:
      people = int(row[0])
      finger = int(row[2][1])
      if((people,finger) not in samples):
        samples[(people,finger)] = 1
      else:
        samples[(people,finger)] += 1
    print(samples)


if __name__ == "__main__":
  createFakeTrain()