###
 # @Author         : lanling
 # @Date           : 2020-04-13 17:07:49
 # @LastEditTime   : 2020-04-13 22:31:25
 # @FilePath       : \Reverse-reder\test.py
 # @Github         : https://github.com/muyuuuu
 # @Description    : PyQt5 多线程测试
 # @佛祖保佑，永无BUG
###

import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()

        self.button = QPushButton('Start', self)
        self.button.clicked.connect(self.count_func)
        self.button_2 = QPushButton('Stop', self)           # 3
        self.button_2.clicked.connect(self.stop_count_func)

        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter)

        self.my_thread = MyThread()
        self.my_thread.my_signal.connect(self.set_label_func)

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.h_layout.addWidget(self.button)
        self.h_layout.addWidget(self.button_2)
        self.v_layout.addWidget(self.label)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def count_func(self):
        self.my_thread.is_on = True         # 5
        self.my_thread.start()

    def set_label_func(self, num):
        self.label.setText(num)

    def stop_count_func(self):              # 4
        self.my_thread.is_on = False
        self.my_thread.count = 0


class MyThread(QThread):
    my_signal = pyqtSignal(str)

    def __init__(self):
        super(MyThread, self).__init__()
        self.count = 0
        self.is_on = True   # 1

    def run(self):
        while self.is_on:   # 2
            print(self.count)
            self.count += 1
            self.my_signal.emit(str(self.count))
            self.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())