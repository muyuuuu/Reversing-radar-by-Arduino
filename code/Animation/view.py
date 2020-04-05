import sys, qdarkstyle, time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush, QFont
from PyQt5.QtWidgets import (QApplication, QGraphicsRectItem, QGraphicsScene,
                             QGraphicsView, QMainWindow, QGridLayout, QFrame,
                             QSplitter, QWidget, QTextEdit, QVBoxLayout, QPushButton)
from multiprocessing import Process, Queue


# 负责绘制车辆的类
class GraphicsView(QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()

        # 创建图形容器
        self.scene = QGraphicsScene()
        # 将车库实体化为 宽度450 长度600 大小
        self.scene.setSceneRect(0, 0, 450, 600)

        # 创建车辆实例
        self.rect = QGraphicsRectItem()
        # 初始化位置为 30 30 车辆宽度 250 长度 400
        self.rect.setRect(30, 30, 250, 400)

        # 创建颜色刷子
        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(QColor(124, 214, 175))

        # 给车身上色
        self.rect.setBrush(brush1)

        # 设置主窗口的背景颜色
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 将车身添加到容器中 即放到车库里
        self.scene.addItem(self.rect)

        # 设置当前场景
        self.setScene(self.scene)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # 装窗口设置大小
        self.setFixedSize(900, 700)

        # 设置文字的字体
        font = QFont()
        font.setFamily("Microsoft Yahei")
        font.setPointSize(11)

        # 设置主窗口风格
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 整体布局
        pagelayout = QVBoxLayout()
        
        # 左侧开始布局 ----------------------------------------------
        left_frame = QFrame(self)
        left_frame.setFrameShape(QFrame.StyledPanel)

        # 创建左侧的文本编辑器  用于显示距离数字
        text = QTextEdit(left_frame)
        text.setFont(font)
        text.setTextColor(QColor(124, 214, 175))
        text.setFixedWidth(350)
        left_layout = QVBoxLayout(left_frame)
        left_layout.addWidget(text)
        
        # 右侧开始布局 ----------------------------------------------
        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)

        #　添加右侧的倒车情景
        self.car = GraphicsView()
        right_layout = QVBoxLayout(right_frame)
        right_layout.addWidget(self.car)
        btn = QPushButton("开始")
        btn.setFont(font)
        btn.setFixedSize(100, 30)
        right_layout.addWidget(btn)

        # 创建窗口分割-----------------------------------------------
        # 左侧添加文本控件
        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(left_frame)
        self.splitter1.setFixedWidth(300)
        # 右侧添加车辆
        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.setFixedWidth(420)
        self.splitter2.addWidget(right_frame)

        # 设置最终的窗口布局与控件-------------------------------------
        widget = QWidget()
        pagelayout.addWidget(self.splitter2)
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        btn.clicked.connect(self.run)

        self.qc = Queue()
        self.ql = Queue()

    def write(self, qc, ql):
        L = [30, 35, 40]
        C = [100, 110, 120]
        # while True: 
        for left, center in zip(L, C):
            qc.put(center)
            ql.put(left)
            time.sleep(1)

    def read(self, qc, ql):
        while True:
            center = qc.get(True)
            left = ql.get(True)
            self.car.rect.setRect(left, center, 250, 400)
    
    def run(self):
        qc = Queue()
        ql = Queue()
        pw = Process(target=self.write, args=(qc, ql))
        pr = Process(target=self.read, args=(qc, ql))
        # 启动子进程pw，写入:
        pw.start()
        # 启动子进程pr，读取:
        pr.start()
        # 等待pw结束:
        pw.join()
        # pr进程里是死循环，无法等待其结束，只能强行终止:
        pr.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())