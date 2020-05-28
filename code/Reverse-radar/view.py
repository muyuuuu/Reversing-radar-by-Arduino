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
import math


class RectItem(QGraphicsRectItem):
    def __init__(self, rect=QRectF()):
        super(RectItem, self).__init__(rect)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self._pos_animation = QVariantAnimation()
        self._pos_animation.valueChanged.connect(self.setPos)

    def move_smooth(self, end, duration):
        if self._pos_animation.state() == QAbstractAnimation.Running:
            self._pos_animation.stop()
        self._pos_animation.setDuration(duration)
        self._pos_animation.setStartValue(self.pos())
        self._pos_animation.setEndValue(end)
        self._pos_animation.start()


# 负责绘制车辆的类
class GraphicsView(QGraphicsView):
    def __init__(self, width, height):
        super(GraphicsView, self).__init__()

        # 创建图形容器

        self.setFixedSize(460, 560)

        # 将车库实体化为 宽度450 长度600 大小
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 450, 550)

        # 创建车辆实例
        self.rect = RectItem()

        # 初始化位置为 30 30 车辆宽度 250 长度 400
        self.rect.setRect((450 - width) / 2, 0, width, height)

        # 创建颜色刷子
        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(QColor(124, 214, 175))

        # 给车身上色
        self.rect.setBrush(brush1)

        # 将车身添加到容器中 即放到车库里
        self.scene.addItem(self.rect)

        # 设置当前场景
        self.setScene(self.scene)


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

    def lift(self):
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
        left_layout.addWidget(btn_start, 0, 0)
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

        pagelayout.addLayout(left_layout)

        # 右侧开始布局
        right_layout = QVBoxLayout()

        # 右上侧开始布局 ----------------------------------------------
        # 创建左侧的文本编辑器  用于显示距离数字

        back_label = QLabel("后方距离")
        back_label.setFixedSize(90, 30)
        label_list.append(back_label)
        self.back_line = QLineEdit()
        self.back_line.setFixedSize(180, 30)
        lineedit_list.append(self.back_line)

        top_right_layout = QHBoxLayout()
        top_right_layout.addWidget(back_label)
        top_right_layout.addWidget(self.back_line)

        for label, line in zip(label_list, lineedit_list):
            label.setFont(font)
            line.setFont(font)

        for btn in btn_list:
            btn.setFont(font)

        # 右侧开始布局 ----------------------------------------------
        #　添加右侧的倒车情景
        self.width = 240
        self.height = 300
        g = GraphicsView(self.width, self.height)
        self.car = g.rect
        self.scene = g.scene

        # print(self.scene.x())
        right_layout.addLayout(top_right_layout)
        right_layout.addWidget(g)
        pagelayout.addLayout(right_layout)

        # 设置最终的窗口布局与控件-------------------------------------
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        btn_start.clicked.connect(self.update_begin)
        btn_start.clicked.connect(self.run)
        exit_btn.clicked.connect(self.lift)

        self.com = Com()
        self.com.my_signal.connect(self.run)

        # 将按钮与发送数据相关联
        btn_stop.clicked.connect(self.stop)
        btn_left.clicked.connect(self.left)
        btn_right.clicked.connect(self.right)
        btn_forward.clicked.connect(self.forward)
        btn_back.clicked.connect(self.back)

        self.flag = 0
        self.dis = 0
        self.flag1 = 0
        self.left_angle = 5
        self.right_angle = 5

        self.rotate_pos = (self.car.pos().x() + self.width / 2, self.car.pos().x() + self.height / 2)

        self.direction = 1

    def lift(self):
        self.com.lift()

    def back(self):
        self.direction = 1
        self.com.back()

    def left(self):
        self.direction = -1
        self.com.left()
        pos = self.rotate_pos
        x, y = pos[0] + self.width / 2, pos[1] + self.height / 2
        self.car.setTransformOriginPoint(QPointF(x, y))
        self.car.setRotation(360 - self.left_angle)
        self.left_angle += 5
        self.right_angle -= 5

    def right(self):
        self.direction = -1
        self.com.right()
        pos = self.rotate_pos
        x, y = pos[0] + self.width / 2, pos[1] + self.height / 2
        self.car.setTransformOriginPoint(QPointF(x, y))
        self.car.setRotation(self.right_angle)
        self.left_angle -= 5
        self.right_angle += 5

    def stop(self):
        self.com.stop()

    def forward(self):
        self.direction = -1
        self.com.forward()

    def update(self, distance):
        self.back_line.setText(str(self.dis)[2:-5] + "cm")

    def move_pos(self, scene):
        if self.dis != False:
            # print(self.dis)
            string = str(self.dis)
            dis = int(string[2:-5])
            if dis < 20:
                for it in scene.items():
                    self.item = it
                    if dis < 5:
                        y = 550 - 10 - self.height
                    else:
                        y = 550 - dis * 10 - self.height
                    if self.left_angle == self.right_angle:
                        x = 0
                    if self.left_angle > self.right_angle:
                        x = -(self.left_angle)
                    if self.right_angle > self.left_angle:
                        x = self.right_angle
                    pos = QPointF(x, y - x)
                    # print(self.car.scenePos()
                    if hasattr(it, 'move_smooth'):
                        it.move_smooth(pos, 200)
                        it._pos_animation.valueChanged.connect(self.update)


    # 确定是按钮按下 而不是多线程发来的信号
    def update_begin(self):
        if self.flag1 == 1:
            self.flag1 = 0

    def run(self, distance):
        if self.flag1 == 0:
            self.com.begin()
            self.flag1 = 1
        # 数据线程开始执行
        if self.flag == 0:
            self.com.start()
            self.flag += 1
        self.dis = distance
        wrapper = partial(self.move_pos, self.scene)
        timer = QTimer(interval=5000, timeout=wrapper)
        timer.start()
        wrapper()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())