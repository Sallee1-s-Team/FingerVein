import copy
import math
import re
import sys

import cv2
import numpy as np
from Ui_mainWidget import *
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PySide6.QtCore import QEvent
from fingerVainRec import fingerVainRec


class MainWindow(QWidget, Ui_mainWidget):
  def __init__(self, parent=None):
    # 变量
    self.inImg = None     # 原始图像
    self.inQImg = None    # 原始图像的QPixmap
    self.outImg = None    # 输出图像
    self.outQImg = None   # 输出图像的QPixmap
    self.zoomScale = 100  # 缩放比例
    self.target = None    # 标签（如果有的话）
    self.fingerVainTool = fingerVainRec()  # 指静脉套件
    # 初始化
    super(MainWindow, self).__init__(parent)
    self.setupUi(self)
    self.obj_preview_scrollArea.viewport().installEventFilter(self)
    self.obj_output_scrollArea.viewport().installEventFilter(self)

  def setObjEnable(self):
    self.obj_ocr_pushButton.setEnabled(True)
    self.obj_zoom_lineEdit.setEnabled(True)
    self.obj_zoomIn_pushButton.setEnabled(True)
    self.obj_zoomOut_pushButton.setEnabled(True)
    self.obj_zoomReset_pushButton.setEnabled(True)

  def numpy2QPixmap(self,img):
    if(len(img.shape) == 2):
      img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    height, width, channel = img.shape
    bytesPerLine = 3 * width
    qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)

  # 事件过滤器
  def eventFilter(self, obj, event):
    if(obj == self.obj_preview_scrollArea.viewport() or obj == self.obj_output_scrollArea.viewport()):
      #记录鼠标点击的起始坐标
      if(event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton):
        self.mousePosX = event.x()
        self.mousePosY = event.y()
        return True
      
      #监听鼠标拖动事件实现ScrollArea的滚动
      if(event.type() == QEvent.MouseMove and event.buttons() == Qt.LeftButton):
        self.obj_preview_scrollArea.horizontalScrollBar().setValue(
            self.obj_preview_scrollArea.horizontalScrollBar().value() - event.x() + self.mousePosX)
        self.obj_preview_scrollArea.verticalScrollBar().setValue(
            self.obj_preview_scrollArea.verticalScrollBar().value() - event.y() + self.mousePosY)

        self.obj_output_scrollArea.horizontalScrollBar().setValue(
            self.obj_output_scrollArea.horizontalScrollBar().value() - event.x() + self.mousePosX)
        self.obj_output_scrollArea.verticalScrollBar().setValue(
            self.obj_output_scrollArea.verticalScrollBar().value() - event.y() + self.mousePosY)
        self.mousePosX = event.x()
        self.mousePosY = event.y()
        return True
      
      #监听鼠标滚轮事件实现图像缩放
      if(event.type() == QEvent.Wheel):
        if(self.inImg is None or self.outImg is None):
          return False
        elif(event.angleDelta().y() < 0):
          self.zoomScale /= 1.1
        else:
          self.zoomScale *= 1.1
        self.setZoomImg()
        return True
    return False

  # 槽函数
  def onOpenPushButtonClick(self):
    self.filePath = QFileDialog.getOpenFileName(self, "打开图片", "", "Image Files(*.jpg *.png *.bmp)")[0]
    if(self.filePath == ""):
      return
    #重置标签
    self.obj_result_label.setStyleSheet("color:black")
    self.obj_target_label.setStyleSheet("color:black")
    self.obj_result_label.setText("无结果")

    fileName = re.search(r'[^/\\]*$', self.filePath)
    if(re.match(r"\d+_\d+_f[12]_\d+_roi\.bmp", fileName[0]) is not None):
      fileNameSplit = str.split(fileName[0], "_")
      self.target = (int(fileNameSplit[0]),int(fileNameSplit[2][-1]))
      self.obj_target_label.setText(f"志愿者{self.target[0]}号，{'左'if self.target[1] == 1 else '右'}手")
    else:
      self.target = None
      self.obj_target_label.setText("无结果")
    #图片显示
    self.inImg = cv2.imread(self.filePath,flags=cv2.IMREAD_GRAYSCALE)
    self.inQImg = self.numpy2QPixmap(self.inImg)
    self.obj_preview_imageContainer.setPixmap(self.inQImg) # 显示图片

    self.obj_output_imageContainer.clear()                  #清空输出窗口图片
    self.obj_output_imageContainer.setText("无预览")
    self.outQImg = None

    self.obj_zoom_lineEdit.setText("100%"); self.zoomScale = 100  # 重置缩放比例
    self.setObjEnable()  # 启用控件

  def onOcrPushButtonClick(self):
    # 获取识别结果
    result = self.fingerVainTool.getResult(self.inImg)
    # 显示识别结果
    self.obj_result_label.setText(f"志愿者{result[0]}号，{'左'if result[1] == 1 else '右'}手")
    # 如果与标签不匹配，将文本修改为红色
    if(self.target is not None and result != self.target):
      self.obj_result_label.setStyleSheet("color:red")
      self.obj_target_label.setStyleSheet("color:red")
    # 显示特征提取图
    self.outImg = self.fingerVainTool.showImg
    self.outQImg = self.numpy2QPixmap(self.outImg)
    self.obj_output_imageContainer.setPixmap(self.outQImg)

  def onZoomOutPushButtonClick(self):
    self.zoomScale /= 1.1
    self.setZoomImg()

  def onZoomInPushButtonClick(self):
    self.zoomScale *= 1.1
    self.setZoomImg()

  def onZoomResetPushButtonClick(self):
    self.zoomScale = 100
    self.obj_zoom_lineEdit.setText("100%")
    self.obj_preview_imageContainer.setPixmap(self.inQImg)
    self.obj_output_imageContainer.setPixmap(self.outQImg)

  def onZoomLineEditFinished(self):
    lineEditText = self.obj_zoom_lineEdit.text()
    if(lineEditText[-1] == "%"):
      lineEditText = lineEditText[:-1]
    if(str.isdigit(lineEditText)):
      self.zoomScale = int(lineEditText)
      self.setZoomImg()
    else:
      self.obj_zoom_lineEdit.setText(f"{int(self.zoomScale):d}%")

  def setZoomImg(self):
    self.zoomScale = np.clip(self.zoomScale, 5, 3200)
    inTmpImg = self.inQImg.scaled(self.inQImg.width()*self.zoomScale/100,self.inQImg.height()*self.zoomScale/100,Qt.KeepAspectRatio)
    self.obj_preview_imageContainer.setPixmap(inTmpImg)
    
    if(self.outQImg is not None):
      outTmpImg = self.outQImg.scaled(self.outQImg.width()*self.zoomScale/100,self.outQImg.height()*self.zoomScale/100,Qt.KeepAspectRatio)
      self.obj_output_imageContainer.setPixmap(outTmpImg)
    self.obj_zoom_lineEdit.setText(f"{int(self.zoomScale):d}%")


if __name__ == '__main__':
  app = QApplication(sys.argv)
  mainWindow = MainWindow()
  mainWindow.show()
  sys.exit(app.exec_())