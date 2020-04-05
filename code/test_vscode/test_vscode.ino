#include <SoftwareSerial.h>
// 设置软串口使用的针脚
SoftwareSerial
softSerial(5, 6); //5为RX, 6为TX
void setup() {
  Serial.begin(9600); //设定硬串口波特率
  softSerial.begin(9600); //设定软串口波特率
}
void loop() {
  if (softSerial.available()) { //如果HC-06发来数据
    int k = softSerial.read(); //读取1个字节的数据
    Serial.println(k); //通过硬串口打印输出
  }
}
