'''
File: view.py
Project: Reverse-reder
File Created: Monday, 6th April 2020 11:58:29 am
Author: lanling (https://github.com/muyuuuu)
-----------
Last Modified: Monday, 13th April 2020 11:25:58 pm
Modified By: lanling (https://github.com/muyuuuu)
Copyright 2020 - 2020 NCST, NCST
-----------
--佛祖保佑，永无BUG--
'''

import sys, time, random, queue, qdarkstyle, serial, threading
from PyQt5.QtCore import (Qt, QPointF, QRectF, QVariantAnimation,
                          QAbstractAnimation, QTimer, QObject, QThread,
                          pyqtSignal)
from PyQt5.QtGui import QColor, QPen, QBrush, QFont
from PyQt5.QtWidgets import (QApplication, QGraphicsRectItem, QGraphicsScene,
                             QGraphicsView, QMainWindow, QGridLayout, QFrame,
                             QSplitter, QWidget, QTextEdit, QVBoxLayout,
                             QPushButton, QGraphicsItem, QHBoxLayout, QLabel,
                             QLineEdit, QGridLayout)
from functools import partial


# 读取串口数据的类
class Com(QThread):
    my_signal = pyqtSignal(str)

    def __init__(self):
        super(Com, self).__init__()
        self.data = ""
        self.is_on = True   # 1
        self.s = serial.Serial(port='COM6',
                                baudrate=9600,
                                stopbits=serial.STOPBITS_ONE)

    def recv(self):
        while True:
            self.sleep(1)
            data = self.s.readline()
            if data == '':
                continue
            else:
                break
        return data

    def run(self):
        while self.is_on:   # 2
            if self.s.isOpen():
                print("open success")
            else:
                print("open failed")

            while True:
                self.data = self.recv()
                self.my_signal.emit(str(self.data))    

    def stop(self):
        self.s.write(b"2")

    def forward(self):
        self.s.write(b"0")

    def back(self):
        self.s.write(b"1")

    def left(self):
        self.s.write(b"3")

    def right(self):
        self.s.write(b"4")

    def begin(self):
        self.s.write(b"5")

    def lift_exit(self):
        self.s.write(b"6")


# 主窗口的类
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # 设置文字的字体
        font = QFont()
        font.setFamily("Microsoft Yahei")
        font.setPointSize(11)

        self.setFixedSize(800, 650)

        # 统一设置按钮的字体
        btn_list = []
        label_list = []
        lineedit_list = []

        # 设置题目和状态栏
        self.setWindowTitle("倒车雷达模拟软件")

        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("安全驾驶~")

        # 整体布局从
        pagelayout = QHBoxLayout()

        # 左侧开始布局
        left_layout = QGridLayout()

        btn_start = QPushButton("倒车")
        btn_start.setFixedSize(100, 80)
        left_layout.addWidget(btn_start, 3, 1)
        btn_list.append(btn_start)

        btn_forward = QPushButton("前进")
        btn_forward.setFixedSize(100, 80)
        left_layout.addWidget(btn_forward, 0, 1)
        btn_list.append(btn_forward)

        btn_left = QPushButton("左转")
        btn_left.setFixedSize(100, 80)
        left_layout.addWidget(btn_left, 1, 0)
        btn_list.append(btn_left)

        btn_stop = QPushButton("停车")
        btn_stop.setFixedSize(100, 80)
        left_layout.addWidget(btn_stop, 1, 1)
        btn_list.append(btn_stop)

        btn_right = QPushButton("右转")
        btn_right.setFixedSize(100, 80)
        left_layout.addWidget(btn_right, 1, 2)
        btn_list.append(btn_right)

        exit_btn = QPushButton("退出")
        exit_btn.setFixedSize(100, 80)
        left_layout.addWidget(exit_btn, 0, 2)
        btn_list.append(exit_btn)

        btn_back = QPushButton("后退")
        btn_back.setFixedSize(100, 80)
        left_layout.addWidget(btn_back, 2, 1)
        btn_list.append(btn_back)

        # btn_slow = QPushButton("减速")
        # btn_slow.setFixedSize(100, 80)
        # left_layout.addWidget(btn_slow, 2, 2)
        # btn_list.append(btn_slow)

        pagelayout.addLayout(left_layout)

        for label, line in zip(label_list, lineedit_list):
            label.setFont(font)
            line.setFont(font)

        for btn in btn_list:
            btn.setFont(font)


        # 设置最终的窗口布局与控件-------------------------------------
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        btn_start.clicked.connect(self.test_)
        btn_start.clicked.connect(self.run)
        exit_btn.clicked.connect(self.lift_run)

        self.com = Com()
        self.com.my_signal.connect(self.run)

        # 将按钮与发送数据相关联
        btn_stop.clicked.connect(self.stop)
        btn_left.clicked.connect(self.left)
        btn_right.clicked.connect(self.right)
        btn_forward.clicked.connect(self.forward)
        btn_back.clicked.connect(self.back)

        self.flag = 0
        self.flag1 = 0
        self.dis = 0
        self.com.start()
        
    def lift_run(self):
        self.com.lift_exit()

    def back(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def stop(self):
        pass

    def forward(self):
        pass

    def test_(self):
        if (self.flag == 1):
            self.flag = 0

    def run(self, data):
        print(data)
        if (self.flag == 0):
            self.com.begin()
            self.flag = 1
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())