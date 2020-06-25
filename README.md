# 毕设题目

学校官网暂时进不去了，找不到原题，大概意思是做一个倒车雷达。

# TodoList

## Submodule

1. ~~完成电机功能。(缺少电机驱动模块L298N)~~
2. ~~完成超声波HC-SR04测距并在1602显示的功能。~~
3. ~~完成手机蓝牙控制小车前进后退功能。(缺少蓝牙模块，考虑ESP8266 wifi模块)~~
4. ~~事实证明，还是用HC-05蓝牙模块吧。~~
5. ~~绘制倒车影象(PyQt5)~~

## Function Module

1. ~~超声波测距，蓝牙将距离信息发送回PC~~
2. ~~电脑端上位机控制小车~~
3. ~~PWM减速~~
4. ~~逻辑功能实现：倒车减速、遇到障碍物制动、解除制动后才能控制小车~~
5. ~~实现倒车与动画的统一~~

# Intro

1. `code/Reverse-radar`：`view.py`是上位机软件，`Reverse-radar.ino`是`Arduino`端的代码；
2. `code`其他文件夹都是测试代码；

# 缺陷

1. 倒车时开启雷达，雷达检测到阈值后车辆仍在移动，有一定误差；
2. 超声波测距的误差很大；
3. 每次使用必须重启，必须重新连接蓝牙；
4. 没有倒车雷达的实时动画；
5. 无法根据当前倒车场景的车库实时调整动画中的车辆的大小、方向（确切来说，没有标准的正向，所以也没有实现斜方向的倒车，但在`rotation-test.py`中有所体现）；
6. 其他功能均实现，所以 85 分，毕设结束。

# 更加通俗的解释

https://muyuuuu.github.io/2020/04/18/reverse-radar-begin/
