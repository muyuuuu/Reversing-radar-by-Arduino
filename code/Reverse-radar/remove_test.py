'''
File: test_rotation.py
Project: Reverse-radar
File Created: Friday, 17th April 2020 11:12:09 pm
Author: lanling (https://github.com/muyuuuu)
-----------
Last Modified: Friday, 17th April 2020 11:12:36 pm
Modified By: lanling (https://github.com/muyuuuu)
Copyright 2020 - 2020 NCST, NCST
-----------
@ 佛祖保佑，永无BUG--
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


# 主窗口的类
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)


        # 整体布局从
        pagelayout = QHBoxLayout()

        # 左侧开始布局
        left_layout = QGridLayout()
        btn_start = QPushButton("倒车")
        btn_start.setFixedSize(100, 80)
        left_layout.addWidget(btn_start, 0, 0)


        # 右侧开始布局
        right_layout = QVBoxLayout()

        # 右侧开始布局 ----------------------------------------------
        #　添加右侧的倒车情景
        g = GraphicsView()
        # g.setFixedSize(450, 550)
        self.car = g.rect
        self.scene = g.scene

        # print(self.scene.x())
        right_layout.addWidget(g)
        pagelayout.addLayout(left_layout)
        pagelayout.addLayout(right_layout)

        # 设置最终的窗口布局与控件-------------------------------------
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        btn_start.clicked.connect(self.run)

    def move_pos(self, scene):
        Left = [i for i in range(30, 32, 2)]
        Center = [i for i in range(32, 34, 2)]
        for it in scene.items():
            self.item = it
            for left, center in zip(Left, Center):
                pos = QPointF(left, center)
                if hasattr(it, 'move_smooth'):
                    it.move_smooth(pos, 500)

    def run(self, distance):
        wrapper = partial(self.move_pos, self.scene)
        timer = QTimer(interval=5000, timeout=wrapper)
        timer.start()
        wrapper()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())