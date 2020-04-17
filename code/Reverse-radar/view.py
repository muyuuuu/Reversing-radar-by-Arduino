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
    def __init__(self):
        super(GraphicsView, self).__init__()

        # 创建图形容器

        self.setFixedSize(460, 560)

        # 将车库实体化为 宽度450 长度600 大小
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 450, 550)

        # 创建车辆实例
        self.rect = RectItem()

        # 初始化位置为 30 30 车辆宽度 250 长度 400
        self.rect.setRect(0, 0, 240, 300)

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

    def recv(self, serial):
        while True:
            self.sleep(1)
            data = serial.read_all()
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
                self.data = self.recv(self.s)
                self.my_signal.emit(str(self.data))    

    def stop(self):
        self.s.write('S'.encode('utf-8'))

    def forward(self):
        self.s.write('F'.encode('utf-8'))

    def back(self):
        self.s.write('B'.encode('utf-8'))

    def left(self):
        self.s.write('L'.encode('utf-8'))

    def right(self):
        self.s.write('R'.encode('utf-8'))

    def begin(self):
        self.s.write('E'.encode('utf-8'))


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

        btn_lift = QPushButton("解除")
        btn_lift.setFixedSize(100, 80)
        left_layout.addWidget(btn_lift, 0, 2)
        btn_list.append(btn_lift)

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
        left_layout.addWidget(exit_btn, 2, 0)
        btn_list.append(exit_btn)

        btn_back = QPushButton("后退")
        btn_back.setFixedSize(100, 80)
        left_layout.addWidget(btn_back, 2, 1)
        btn_list.append(btn_back)

        btn_slow = QPushButton("减速")
        btn_slow.setFixedSize(100, 80)
        left_layout.addWidget(btn_slow, 2, 2)
        btn_list.append(btn_slow)

        pagelayout.addLayout(left_layout)

        # 右侧开始布局
        right_layout = QVBoxLayout()

        # 右上侧开始布局 ----------------------------------------------
        # 创建左侧的文本编辑器  用于显示距离数字
        left_label = QLabel("左")
        left_label.setFixedSize(28, 30)
        label_list.append(left_label)
        self.left_line = QLineEdit()
        self.left_line.setFixedSize(88, 30)
        lineedit_list.append(self.left_line)

        back_label = QLabel("后")
        back_label.setFixedSize(28, 30)
        label_list.append(back_label)
        self.back_line = QLineEdit()
        self.back_line.setFixedSize(88, 30)
        lineedit_list.append(self.back_line)

        right_label = QLabel("右")
        right_label.setFixedSize(28, 30)
        label_list.append(right_label)
        self.right_line = QLineEdit()
        self.right_line.setFixedSize(88, 30)
        lineedit_list.append(self.right_line)

        top_right_layout = QHBoxLayout()
        top_right_layout.addWidget(left_label)
        top_right_layout.addWidget(self.left_line)
        top_right_layout.addWidget(back_label)
        top_right_layout.addWidget(self.back_line)
        top_right_layout.addWidget(right_label)
        top_right_layout.addWidget(self.right_line)

        for label, line in zip(label_list, lineedit_list):
            label.setFont(font)
            line.setFont(font)

        for btn in btn_list:
            btn.setFont(font)

        # 右侧开始布局 ----------------------------------------------
        #　添加右侧的倒车情景
        g = GraphicsView()
        # g.setFixedSize(450, 550)
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

        btn_start.clicked.connect(self.run)

        exit_btn.clicked.connect(self.exit_)

        self.com = Com()
        self.com.my_signal.connect(self.run)

        # 将按钮与发送数据相关联
        btn_stop.clicked.connect(self.stop)
        btn_left.clicked.connect(self.left)
        btn_right.clicked.connect(self.right)
        btn_forward.clicked.connect(self.forward)
        btn_back.clicked.connect(self.back)

    def back(self):
        self.com.back()

    def left(self):
        self.com.left()

    def right(self):
        self.com.right()

    def stop(self):
        self.com.stop()

    def forward(self):
        self.com.forward()

    def exit_(self):
        self.com.is_on = False

    def update(self, distance):
        pass
        # ql = queue.Queue(2)
        # left = int(self.item.x())
        # qb = queue.Queue(2)
        # back = int(self.item.y())
        # ql.put(left)
        # qb.put(back)
        # if ql.qsize() == 1:
        #     self.left_line.setText(str(left))
        # else:
        #     if left - ql.get() > 1:
        #         self.left_line.setText(str(left))
        # if qb.qsize() == 1:
        #     self.back_line.setText(str(100 - back))
        # else:
        #     if back - qb.get() > 1:
        #         self.back_line.setText(str(100 - back))

    def move_pos(self, scene):
        print(self.dis)
        Left = [i for i in range(30, 32, 2)]
        Center = [i for i in range(32, 34, 2)]
        for it in scene.items():
            self.item = it
            for left, center in zip(Left, Center):
                pos = QPointF(left, center)
                if hasattr(it, 'move_smooth'):
                    it.move_smooth(pos, 500)
                    it._pos_animation.valueChanged.connect(self.update)

    def run(self, distance):
        # 线程开始执行
        self.com.start()
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