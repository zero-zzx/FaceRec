import base64
from datetime import datetime, timedelta
import os
import sys
import pymysql
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PySide2.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets,uic
import cv2
import numpy as np
import threading

from PyQt5.QtCore import QObject, pyqtSignal
#from PySide2.QtUiTools import QUiLoader

import remote_mysql

import use_baidu_api
import apprcc_rc
import print_paper

class MySignals(QObject):
    text_show=pyqtSignal(str)


class Stats:

    def __init__(self):
        self.myPath = './'
        # self.ui = uic.loadUi(self.myPath+'show_image.ui')
        # self.ui = uic.loadUi(self.myPath + 'main_1.ui')
        self.ui = uic.loadUi(self.myPath+'main_2.ui')
        # self.ui = QUiLoader().load('main_1.ui')

        self.ms=MySignals()
        self.timer_camera = QtCore.QTimer()  # 定时器timer_camear为每次从摄像头取画面的间隔
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.count_img = 0
        self.count_none = 0
        self.token = '0'

        self.show_camera = self.ui.label_01
        self.open_camera = self.ui.button_01
        self.close_camera = self.ui.button_02
        self.info_text = self.ui.text_01

        self.open_camera.clicked.connect(self.open_button_clicked)
        self.close_camera.clicked.connect(self.close_button_clicked)
        self.ms.text_show.connect(self.print_to_text)

        # self.close_camera.setEnabled(False)
        self.ui.minButton.clicked.connect(self.ui.showMinimized)
        # self.ui.maxButton.clicked.connect(self.max_or_restore)
        # self.ui.maxButton.animateClick(10)
        self.ui.closeButton.clicked.connect(self.ui.close)

    def max_or_restore(self):
        if self.ui.maxButton.isChecked():
            self.ui.showMaximized()
        else:
            self.ui.showNormal()

    # 点击打开视像头后，启动定时器取画面
    def open_button_clicked(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            self.start_camera()
            self.face_cascase = cv2.CascadeClassifier(self.myPath+'haarcascade_frontalface_alt2.xml')
            self.timer_camera.timeout.connect(self.label_show_camera)  # 若定时器结束，则调用label_show_camera()拍照
            self.open_camera.setEnabled(False)
            self.close_camera.setEnabled(True)


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


    def label_show_camera(self):
        try:
            flag, self.image = self.cap.read()  # 从视频流中读取一帧图像给self.image
            imag = self.paint_rectangle(self.image)
            imag = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            showImage = QImage(imag.data, imag.shape[1], imag.shape[0], QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.show_camera.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里显示QImag
            self.show_camera.setScaledContents(True)
        except Exception as e:
            print('异常信息为：', e)

        # try:
        #     flag, self.image = self.cap.read()  # 从视频流中读取一帧图像给self.image
        #     self.image=self.Scale(self.image)
        #     imag = self.paint_rectangle(self.image)
        #     imag = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        #     showImage = QImage(imag.data, imag.shape[1], imag.shape[0], QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        #     self.show_camera.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里显示QImag
        # except:
        #     print("label_show_camrea---->err")
        #     pass

    # 绘制人脸框
    def paint_rectangle(self, image):
        try:
            image_upload=image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascase.detectMultiScale(gray, 1.3, 3)

            cnt=0
            for (x, y, w, h) in faces:
                # 在窗口当中标识人脸 画一个矩形
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cnt+=1
            #print(cnt)

            if(cnt==1):
                self.count_img+=1
                if(self.count_img%25==1):
                    cv2.imwrite(self.myPath+'image.jpg', image_upload)
                    # cv2.imwrite(self.myPath+'image_show.jpg', image)
                    self.recognition()
                    #print("uploading...")
                    self.count_none=0
            else:
                self.count_none+=1
                if(self.count_none>=100):
                    self.count_none=0
                    self.print_to_text("信息学院学生打卡")
            return image
        except:
            print("paint_rectangle---->err")
            pass

    def recognition(self):
        try:
            self.thread = threading.Thread(target=self.getInfoFromImage, args=())
            self.thread.start()

        except:
            print("recognition----->err")
            pass

    def getInfoFromImage(self):
        try:
            '''
            img = open(self.myPath+'/zzx.jpg', 'rb')
            my_text = use_aliyun_api.use_aliyun_api(img)
            number = my_text['MatchList'][0]['FaceItems'][0]['EntityId']
            score = my_text['MatchList'][0]['FaceItems'][0]['Score']
            score*=100
            print(number, score)
            '''

            img = 'image.jpg'
            #print(self.myPath+format(img))
            with open(self.myPath+format(img), 'rb') as f:
                base64_data = base64.b64encode(f.read())
                img = base64_data.decode()
                #print('token',self.token)
                my_text = use_baidu_api.baidu_api(img,self.token)
                #print('mytext',my_text)
                #print(my_text["error_code"])
                if(my_text["error_code"]==0):
                    number = my_text["result"]['user_list'][0]['user_id']
                    score = my_text["result"]['user_list'][0]['score']

                    #print(number)
                    #print(score)
                    if(score>80):
                        p = remote_mysql.use_mysql('select * from xin2005 where id="{}"'.format(number))
                        #print(p["name"], p["sex"], p["class_bel"])
                        now = datetime.now()  # 获取当前日期和时间
                        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
                        last_time=p["check_in_time"]
                        score=p["score"]
                        last_day = datetime.now() + timedelta(hours=-10)
                        if(last_day>last_time):
                            score=score+1
                        str="学号：{}\n姓名：{}\n性别：{}\n班级：{}\n签到时间：{}\n您已累计签到{}天".format(p["id"],p["name"],p["sex"],p["class_bel"],current_time,score)
                        remote_mysql.use_mysql("update xin2005 set check_in_time='{}',score={} where id='{}'".format(current_time,score,number))
                        #print("update xin2005 set check_in_time='{}',score={} where id='{}'".format(current_time,score,number))
                        print_paper.Print_paper(str)
                        self.ms.text_show.emit(str)
                    else:
                        self.ms.text_show.emit('人脸识别度低，请将正脸正对屏幕')
                elif(my_text["error_code"]==110):
                    # {'error_code': 110, 'error_msg': 'Access token invalid or no longer valid'}
                    self.token=use_baidu_api.get_Token()
                elif(my_text["error_code"]==17):
                    self.ms.text_show.emit('人脸识别次数已达上限，请联系管理员')

        except:
            print("getIngoFromImage-------->err")
            pass


    def print_to_text(self,str):
        self.info_text.setText(str)


    # def Print_paper(self,str):
        # print_paper.print_paper(str)


app = QApplication([])
stats = Stats()
# stats.ui.show()
stats.ui.showFullScreen()
sys.exit(app.exec_())