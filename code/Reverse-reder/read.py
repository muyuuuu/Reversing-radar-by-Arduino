###
 # @Author         : lanling
 # @Date           : 2020-04-05 21:34:41
 # @FilePath       : \Reverse-reder\read.py
 # @Github         : https://github.com/muyuuuu
 # @Description    : 读取串口数据
 # @佛祖保佑，永无BUG
###

import serial, time


def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
    return data
