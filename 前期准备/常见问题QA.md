记录一些技术关键点，方便论文凑字数。

### 开发环境配置

- 安装 `Arduino IDE` 为编译器。https://www.arduino.cc/en/main/software
- 在 `VSCode` 中安装 `Arduino` 插件并配置所安装的 `Arduino.exe` 的路径，本电脑为：`C:\Program Files (x86)\Arduino` ，为主要编辑环境。

### 上拉电阻与下拉电阻

上拉电阻：稳定电平读入；增加 `CPU` 输出的电流。
下拉电阻：分流；稳定电平读入。
参考图：https://blog.csdn.net/tennysonsky/article/details/45174981

### pinMode

[pinMode说明](http://www.taichi-maker.com/homepage/reference-index/arduino-code-reference/pinmode/)

### digitalWrite

[digitalWrite说明](http://www.taichi-maker.com/homepage/reference-index/arduino-code-reference/digitalwrite/)

### delayMicroseconds

[单位是毫秒](http://www.taichi-maker.com/homepage/reference-index/arduino-code-reference/delaymicroseconds/)

### pulseIn

[检测电平持续时间](http://www.taichi-maker.com/homepage/reference-index/arduino-code-reference/pulsein/)

