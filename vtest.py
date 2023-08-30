import base64
from datetime import datetime, timedelta
import os
import sys
import pymysql
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets,uic
import cv2
import numpy as np
import threading

from PyQt5.QtCore import QObject, pyqtSignal

import apprcc_rc



class Stats:

    def __init__(self):
        self.myPath = '/home/pi/Desktop/Xin2005/'
        self.ui = uic.loadUi(self.myPath+'main_2.ui')

        self.timer_camera = QtCore.QTimer()  # 定时器timer_camear为每次从摄像头取画面的间隔
        self.cap = cv2.VideoCapture()


        self.show_camera = self.ui.label_01
        self.open_camera = self.ui.button_01
        self.close_camera = self.ui.button_02
        self.info_text = self.ui.text_01
        self.CAM_NUM=0

        self.open_camera.clicked.connect(self.open_button_clicked)
        self.close_camera.clicked.connect(self.close_button_clicked)
        self.ui.closeButton.clicked.connect(self.ui.close)





    # 点击打开视像头后，启动定时器取画面
    def open_button_clicked(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            self.start_camera()
            self.timer_camera.timeout.connect(self.label_show_camera)  # 若定时器结束，则调用label_show_camera()拍照
            self.open_camera.setEnabled(False)
            self.close_camera.setEnabled(True)

    def label_show_camera(self):
        try:
            flag, image = self.cap.read()  # 从视频流中读取一帧图像给self.image
            imag = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            showImage = QImage(imag.data, imag.shape[1], imag.shape[0], QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.show_camera.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里显示QImag
            self.show_camera.setScaledContents(True)
        except Exception as e:
            print('异常信息为：', e)

    def start_camera(self):
        flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
        if flag == False:  # 如果打开摄像头不成功
            QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确", buttons=QMessageBox.Ok)
        else:
            self.timer_camera.start(50)


    # 关闭摄像头，清空第一个窗口显示的图像
    def close_button_clicked(self):
        self.timer_camera.stop()  # 关闭定时器
        self.cap.release()  # 释放视频流
        self.show_camera.clear()
        self.open_camera.setEnabled(True)
        self.close_camera.setEnabled(False)


  


    

app = QApplication([])
stats = Stats()
stats.ui.showFullScreen()
sys.exit(app.exec_())
