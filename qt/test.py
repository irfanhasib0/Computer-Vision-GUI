# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
#pip install PyOpenGL PyOpenGL_accelerate
#pip install PyQt5

from PyQt5 import QtCore, QtGui, QtWidgets
#import pyqtgraph as pg
#import cv2
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
from flow import *
from copy import deepcopy

def image2qt(rgbImage):
    h, w, ch = rgbImage.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
    return p
    
    
class Thread(QThread):
    changePixmap = pyqtSignal(QImage,QImage)
    def run(self):
        cap = cv2.VideoCapture(0)
        flow = OpticalFlow()
        self.show = False
        while True:
            ret, frame = cap.read()
            flow_1,flow_2 = flow.get_flow(frame)
            if ret and self.show:
                # https://stackoverflow.com/a/55468544/6622587
                flow_1 = cv2.cvtColor(flow_1, cv2.COLOR_BGR2RGB)
                p1 = image2qt(flow_1)
                p2 = image2qt(flow_2)
                self.changePixmap.emit(p1,p2)

                
class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        
    def initUI(self):
        
        self.gview_1 = QtWidgets.QGraphicsView(self)
        self.gview_1.setGeometry(20,220,480,320)
        self.gview_1.label = QtWidgets.QLabel(self)
        self.gview_1.label.move(20, 220)
        self.gview_1.label.resize(480, 320)
        p = image2qt(np.zeros((320,480,3),dtype=np.uint8))
        self.gview_1.label.setPixmap(QPixmap.fromImage(p))
        
        
        self.gview_2 = QtWidgets.QGraphicsView(self)
        self.gview_2.setGeometry(540,220,480,320)
        self.gview_2.label = QtWidgets.QLabel(self)
        self.gview_2.label.move(540, 220)
        self.gview_2.label.resize(480, 320)
        p = image2qt(np.zeros((320,480,3),dtype=np.uint8))
        self.gview_2.label.setPixmap(QPixmap.fromImage(p))
        
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        
    @pyqtSlot(QImage,QImage)
    def setImage(self, image1,image2):
        self.gview_1.label.setPixmap(QPixmap.fromImage(image1))
        self.gview_2.label.setPixmap(QPixmap.fromImage(image2))
    
    #@pyqtSlot(str)
    def run_clicked(self):
        self.th.show = True
        print("run clicked")
        
    def stop_clicked(self):
        self.th.show = False
        p = image2qt(np.zeros((320,480,3),dtype=np.uint8))
        self.gview_1.label.setPixmap(QPixmap.fromImage(p))
        self.gview_2.label.setPixmap(QPixmap.fromImage(p))
        
    	
    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(1045, 694)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(290, 620, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        self.start = QtWidgets.QPushButton(self)
        self.start.setGeometry(QtCore.QRect(30, 650, 89, 25))
        self.start.setObjectName("pushButton")
        self.start.clicked.connect(self.run_clicked)
        
        self.stop = QtWidgets.QPushButton(self)
        self.stop.setGeometry(QtCore.QRect(130, 650, 89, 25))
        self.stop.setObjectName("pushButton_2")
        self.stop.clicked.connect(self.stop_clicked)
        
        self.openGLWidget = QtWidgets.QOpenGLWidget(self)
        self.openGLWidget.setGeometry(QtCore.QRect(80, 30, 901, 131))
        self.openGLWidget.setObjectName("openGLWidget")
        
        self.gview_2 = QtWidgets.QGraphicsView(self)
        self.gview_2.setGeometry(QtCore.QRect(540, 220, 480, 320))
        self.initUI()
        
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(50, 620, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        
        self.lcdNumber = QtWidgets.QLCDNumber(self)
        self.lcdNumber.setGeometry(QtCore.QRect(100, 190, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self)
        self.lcdNumber_2.setGeometry(QtCore.QRect(640, 190, 64, 23))
        self.lcdNumber_2.setObjectName("lcdNumber_2")

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.start.setText(_translate("Dialog", "run"))
        self.stop.setText(_translate("Dialog", "stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi()
    #ui.initUI()
    #Dialog.show()
    sys.exit(app.exec_())
