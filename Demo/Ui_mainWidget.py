# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_mainWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_mainWidget(object):
    def setupUi(self, mainWidget):
        if not mainWidget.objectName():
            mainWidget.setObjectName(u"mainWidget")
        mainWidget.resize(800, 600)
        mainWidget.setMinimumSize(QSize(320, 240))
        font = QFont()
        font.setStyleStrategy(QFont.PreferDefault)
        mainWidget.setFont(font)
        self.gridLayout_2 = QGridLayout(mainWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget_2 = QWidget(mainWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.obj_zoomOut_pushButton = QPushButton(self.widget_2)
        self.obj_zoomOut_pushButton.setObjectName(u"obj_zoomOut_pushButton")
        self.obj_zoomOut_pushButton.setEnabled(False)
        self.obj_zoomOut_pushButton.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout.addWidget(self.obj_zoomOut_pushButton)

        self.obj_zoom_lineEdit = QLineEdit(self.widget_2)
        self.obj_zoom_lineEdit.setObjectName(u"obj_zoom_lineEdit")
        self.obj_zoom_lineEdit.setEnabled(False)
        self.obj_zoom_lineEdit.setMinimumSize(QSize(0, 0))
        self.obj_zoom_lineEdit.setMaximumSize(QSize(64, 16777215))
        self.obj_zoom_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.obj_zoom_lineEdit)

        self.obj_zoomIn_pushButton = QPushButton(self.widget_2)
        self.obj_zoomIn_pushButton.setObjectName(u"obj_zoomIn_pushButton")
        self.obj_zoomIn_pushButton.setEnabled(False)
        self.obj_zoomIn_pushButton.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout.addWidget(self.obj_zoomIn_pushButton)

        self.obj_zoomReset_pushButton = QPushButton(self.widget_2)
        self.obj_zoomReset_pushButton.setObjectName(u"obj_zoomReset_pushButton")
        self.obj_zoomReset_pushButton.setEnabled(False)
        self.obj_zoomReset_pushButton.setMinimumSize(QSize(0, 0))
        self.obj_zoomReset_pushButton.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout.addWidget(self.obj_zoomReset_pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout_2.addWidget(self.widget_2, 3, 0, 1, 3)

        self.obj_result_groupBox = QGroupBox(mainWidget)
        self.obj_result_groupBox.setObjectName(u"obj_result_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.obj_result_groupBox.sizePolicy().hasHeightForWidth())
        self.obj_result_groupBox.setSizePolicy(sizePolicy)
        self.obj_result_groupBox.setMinimumSize(QSize(64, 40))
        self.obj_result_groupBox.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout = QVBoxLayout(self.obj_result_groupBox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.obj_result_scrollArea = QScrollArea(self.obj_result_groupBox)
        self.obj_result_scrollArea.setObjectName(u"obj_result_scrollArea")
        self.obj_result_scrollArea.setFrameShape(QFrame.NoFrame)
        self.obj_result_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.obj_result_scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.obj_result_scrollArea.setWidgetResizable(True)
        self.obj_rssult_scrollAreaWidgetContents = QWidget()
        self.obj_rssult_scrollAreaWidgetContents.setObjectName(u"obj_rssult_scrollAreaWidgetContents")
        self.obj_rssult_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 346, 69))
        self.verticalLayout_4 = QVBoxLayout(self.obj_rssult_scrollAreaWidgetContents)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.obj_result_label = QLabel(self.obj_rssult_scrollAreaWidgetContents)
        self.obj_result_label.setObjectName(u"obj_result_label")
        font1 = QFont()
        font1.setPointSize(24)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.obj_result_label.setFont(font1)

        self.verticalLayout_4.addWidget(self.obj_result_label)

        self.obj_result_scrollArea.setWidget(self.obj_rssult_scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.obj_result_scrollArea)


        self.gridLayout_2.addWidget(self.obj_result_groupBox, 5, 0, 2, 1)

        self.obj_target_groupBox = QGroupBox(mainWidget)
        self.obj_target_groupBox.setObjectName(u"obj_target_groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.obj_target_groupBox.sizePolicy().hasHeightForWidth())
        self.obj_target_groupBox.setSizePolicy(sizePolicy1)
        self.obj_target_groupBox.setMinimumSize(QSize(60, 40))
        self.obj_target_groupBox.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout_5 = QVBoxLayout(self.obj_target_groupBox)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.obj_target_scrollArea = QScrollArea(self.obj_target_groupBox)
        self.obj_target_scrollArea.setObjectName(u"obj_target_scrollArea")
        self.obj_target_scrollArea.setFrameShape(QFrame.NoFrame)
        self.obj_target_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.obj_target_scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.obj_target_scrollArea.setWidgetResizable(True)
        self.obj_target_scrollAreaWidgetContents = QWidget()
        self.obj_target_scrollAreaWidgetContents.setObjectName(u"obj_target_scrollAreaWidgetContents")
        self.obj_target_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 345, 69))
        self.verticalLayout_8 = QVBoxLayout(self.obj_target_scrollAreaWidgetContents)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.obj_target_label = QLabel(self.obj_target_scrollAreaWidgetContents)
        self.obj_target_label.setObjectName(u"obj_target_label")
        self.obj_target_label.setFont(font1)

        self.verticalLayout_8.addWidget(self.obj_target_label)

        self.obj_target_scrollArea.setWidget(self.obj_target_scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.obj_target_scrollArea)


        self.gridLayout_2.addWidget(self.obj_target_groupBox, 5, 1, 2, 1)

        self.obj_open_pushButton = QPushButton(mainWidget)
        self.obj_open_pushButton.setObjectName(u"obj_open_pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.obj_open_pushButton.sizePolicy().hasHeightForWidth())
        self.obj_open_pushButton.setSizePolicy(sizePolicy2)
        self.obj_open_pushButton.setMinimumSize(QSize(24, 0))
        self.obj_open_pushButton.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_2.addWidget(self.obj_open_pushButton, 5, 2, 1, 1)

        self.obj_output_groupBox = QGroupBox(mainWidget)
        self.obj_output_groupBox.setObjectName(u"obj_output_groupBox")
        self.verticalLayout_6 = QVBoxLayout(self.obj_output_groupBox)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.obj_output_scrollArea = QScrollArea(self.obj_output_groupBox)
        self.obj_output_scrollArea.setObjectName(u"obj_output_scrollArea")
        self.obj_output_scrollArea.setFrameShape(QFrame.NoFrame)
        self.obj_output_scrollArea.setFrameShadow(QFrame.Sunken)
        self.obj_output_scrollArea.setLineWidth(1)
        self.obj_output_scrollArea.setWidgetResizable(True)
        self.obj_output_scrollAreaWidgetContents = QWidget()
        self.obj_output_scrollAreaWidgetContents.setObjectName(u"obj_output_scrollAreaWidgetContents")
        self.obj_output_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 780, 210))
        self.verticalLayout_7 = QVBoxLayout(self.obj_output_scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.obj_output_imageContainer = QLabel(self.obj_output_scrollAreaWidgetContents)
        self.obj_output_imageContainer.setObjectName(u"obj_output_imageContainer")
        self.obj_output_imageContainer.setCursor(QCursor(Qt.OpenHandCursor))
        self.obj_output_imageContainer.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.obj_output_imageContainer)

        self.obj_output_scrollArea.setWidget(self.obj_output_scrollAreaWidgetContents)

        self.verticalLayout_6.addWidget(self.obj_output_scrollArea)


        self.gridLayout_2.addWidget(self.obj_output_groupBox, 2, 0, 1, 3)

        self.obj_preview_groupBox = QGroupBox(mainWidget)
        self.obj_preview_groupBox.setObjectName(u"obj_preview_groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.obj_preview_groupBox)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.obj_preview_scrollArea = QScrollArea(self.obj_preview_groupBox)
        self.obj_preview_scrollArea.setObjectName(u"obj_preview_scrollArea")
        self.obj_preview_scrollArea.setFrameShape(QFrame.NoFrame)
        self.obj_preview_scrollArea.setFrameShadow(QFrame.Sunken)
        self.obj_preview_scrollArea.setLineWidth(1)
        self.obj_preview_scrollArea.setWidgetResizable(True)
        self.obj_preview_scrollAreaWidgetContents = QWidget()
        self.obj_preview_scrollAreaWidgetContents.setObjectName(u"obj_preview_scrollAreaWidgetContents")
        self.obj_preview_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 780, 210))
        self.verticalLayout_2 = QVBoxLayout(self.obj_preview_scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.obj_preview_imageContainer = QLabel(self.obj_preview_scrollAreaWidgetContents)
        self.obj_preview_imageContainer.setObjectName(u"obj_preview_imageContainer")
        self.obj_preview_imageContainer.setCursor(QCursor(Qt.OpenHandCursor))
        self.obj_preview_imageContainer.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.obj_preview_imageContainer)

        self.obj_preview_scrollArea.setWidget(self.obj_preview_scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.obj_preview_scrollArea)


        self.gridLayout_2.addWidget(self.obj_preview_groupBox, 0, 0, 1, 3)

        self.obj_ocr_pushButton = QPushButton(mainWidget)
        self.obj_ocr_pushButton.setObjectName(u"obj_ocr_pushButton")
        self.obj_ocr_pushButton.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.obj_ocr_pushButton.sizePolicy().hasHeightForWidth())
        self.obj_ocr_pushButton.setSizePolicy(sizePolicy3)
        self.obj_ocr_pushButton.setMinimumSize(QSize(24, 0))

        self.gridLayout_2.addWidget(self.obj_ocr_pushButton, 6, 2, 1, 1)


        self.retranslateUi(mainWidget)
        self.obj_open_pushButton.clicked.connect(mainWidget.onOpenPushButtonClick)
        self.obj_ocr_pushButton.clicked.connect(mainWidget.onOcrPushButtonClick)
        self.obj_zoomOut_pushButton.clicked.connect(mainWidget.onZoomOutPushButtonClick)
        self.obj_zoomIn_pushButton.clicked.connect(mainWidget.onZoomInPushButtonClick)
        self.obj_zoomReset_pushButton.clicked.connect(mainWidget.onZoomResetPushButtonClick)
        self.obj_zoom_lineEdit.editingFinished.connect(mainWidget.onZoomLineEditFinished)

        QMetaObject.connectSlotsByName(mainWidget)
    # setupUi

    def retranslateUi(self, mainWidget):
        mainWidget.setWindowTitle(QCoreApplication.translate("mainWidget", u"\u6307\u9759\u8109\u8bc6\u522b", None))
        self.obj_zoomOut_pushButton.setText(QCoreApplication.translate("mainWidget", u"\u7f29\u5c0f", None))
        self.obj_zoom_lineEdit.setText(QCoreApplication.translate("mainWidget", u"100%", None))
        self.obj_zoomIn_pushButton.setText(QCoreApplication.translate("mainWidget", u"\u653e\u5927", None))
        self.obj_zoomReset_pushButton.setText(QCoreApplication.translate("mainWidget", u"\u91cd\u7f6e", None))
        self.obj_result_groupBox.setTitle(QCoreApplication.translate("mainWidget", u"\u8bc6\u522b\u7ed3\u679c", None))
        self.obj_result_label.setText(QCoreApplication.translate("mainWidget", u"\u65e0\u7ed3\u679c", None))
        self.obj_target_groupBox.setTitle(QCoreApplication.translate("mainWidget", u"\u6807\u7b7e\uff08\u5982\u679c\u6709\uff09", None))
        self.obj_target_label.setText(QCoreApplication.translate("mainWidget", u"\u65e0\u7ed3\u679c", None))
        self.obj_open_pushButton.setText(QCoreApplication.translate("mainWidget", u"\u6253\u5f00", None))
        self.obj_output_groupBox.setTitle(QCoreApplication.translate("mainWidget", u"\u7279\u5f81\u63d0\u53d6", None))
        self.obj_output_imageContainer.setText(QCoreApplication.translate("mainWidget", u"\u65e0\u9884\u89c8", None))
        self.obj_preview_groupBox.setTitle(QCoreApplication.translate("mainWidget", u"\u539f\u56fe", None))
        self.obj_preview_imageContainer.setText(QCoreApplication.translate("mainWidget", u"\u65e0\u9884\u89c8", None))
        self.obj_ocr_pushButton.setText(QCoreApplication.translate("mainWidget", u"\u8bc6\u522b", None))
    # retranslateUi

