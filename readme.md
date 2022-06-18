# 指静脉文件说明

## 文件列表

* 数据集代码，在Train文件夹中
  * getcsv.py 自动生成文件列表的csv文件
  * setTest.py 自动划分训练集和测试集，并生成csv文件
  * createFakeTrain 自动生成伪训练集，并生成csv文件

使用前只需要将训练集放到**Train/data**中，即可依次执行上述文件完成操作

* 训练代码，在根目录中
  * Loader.py 用于读取并预处理数据，处理好的数据将会保存到Temp中
  * MyModel.py 自己在今天（6月18日）尝试写的模型，目前效果已经和vgg16相当
  * Train.py 训练的主代码，模型会保存到Model.pth，日志（loss曲线）会保存到TrainLog
  * Test.py 测试的主代码，会输出模型的多项指标，日志（混淆图片）保存到TestLog

* 展示程序，在Demo文件夹中
  * fingerVainRec.py 后端部分，上述代码的整合，默认使用myModel模型
  * main.py 前端功能实现部分
  * Ui_mainWidget.py 前端样式部分

* 其他
  * Models附带了自己今天（6月18日）训练的模型，答辩用的vgg16模型太大，没有放
  * Logs附带了对应的损失曲线
