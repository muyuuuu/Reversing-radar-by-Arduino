###
 # @Author         : lanling
 # @Date           : 2020-04-05 21:34:41
 # @LastEditTime: 2020-04-12 18:08:58
 # @FilePath       : \Reverse-reder\read.py
 # @Github         : https://github.com/muyuuuu
 # @Description    : 
 # @佛祖保佑，永无BUG
###
import serial
from time import sleep

def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
        sleep(2)
    return data

s = serial.Serial('COM6', 9600, timeout=0.5)  #/dev/ttyUSB0
if s.isOpen():
    print("open success")
else:
    print("open failed")

# 发送一个数据激活
s.write('A'.encode())
while True:
    data = recv(s)
    if data != b'':
        print("receive : ", data)