/*
 * File: Reverse-reder.ino
 * Project: Reverse-reder
 * File Created: Sunday, 29th March 2020 7:11:35 pm
 * Author: lanling (https://github.com/muyuuuu)
 * -----------
 * Last Modified: Monday, 13th April 2020 11:29:50 pm
 * Modified By: lanling (https://github.com/muyuuuu)
 * Copyright 2020 - 2020 NCST, NCST
 * -----------
 * @ 佛祖保佑，永无BUG--
 */

// 后方超声波 ------------------------------------
int trigBack = 13;
int echoBack = A0;
// 右侧超声波 ------------------------------------
int trigRight = 8;
int echoRight = A1;
// 左侧超声波 ------------------------------------
int trigLeft = 2;
int echoLeft = A2;
// 右前轮 -----------------------------------------
// 定义 uno 的 pin 11 向 input1 输出
int input1 = 9; 
// 定义 uno 的 pin 12 向 input2 输出
int input2 = 10; 
// 左前轮 -----------------------------------------
// 定义 uno 的 pin 9 向 input3 输出
int input3 = 11; 
// 定义 uno 的 pin 10 向 input4 输出
int input4 = 12; 
// 右后轮 -----------------------------------------
// 定义 uno 的 pin 11 向 input1 输出
int input5 = 3; 
// 定义 uno 的 pin 12 向 input2 输出
int input6 = 4; 
// 左后轮 -----------------------------------------
// 定义 uno 的 pin 9 向 input3 输出
int input7 = 5; 
// 定义 uno 的 pin 10 向 input4 输出
int input8 = 6; 
// 设置蓝牙的连接 -----------------------------------
String str = "";
// 后侧超声波
long cmB, cmR, cmL;

void setup() {
	// 设置硬件串口通信的波特率
	Serial.begin(9600);
	// 定义后侧超声波的输入输出模式 -----------------------------
	pinMode(trigBack, OUTPUT);
	pinMode(echoBack, INPUT);
	// 定义右侧超声波的输入输出模式 -----------------------------
  	pinMode(trigRight, OUTPUT);
  	pinMode(echoRight, INPUT); 
	// 定义左侧超声波的输入输出模式 -----------------------------
  	pinMode(trigLeft, OUTPUT);
	  
  	pinMode(echoLeft, INPUT); 	  
	// 定义所有的电机均为输出模式 ------------------------------
	// 右前
	pinMode(input1, OUTPUT);
	pinMode(input2, OUTPUT);
	// 左前  
	pinMode(input3, OUTPUT);
	pinMode(input4, OUTPUT);
	// 右后
	pinMode(input5, OUTPUT);
	pinMode(input6, OUTPUT);
	// 左后  
	pinMode(input7, OUTPUT);
	pinMode(input8, OUTPUT);
}

// 前进函数 ------------------------------------------
void forward()
{
	// 左前轮
	digitalWrite(input1, LOW); 
	digitalWrite(input2, HIGH);  
	// 右前轮 
	digitalWrite(input3, LOW); 
	digitalWrite(input4, HIGH);
	// 右后轮
	digitalWrite(input5, HIGH);
	digitalWrite(input6, LOW);
	// 左后轮
	digitalWrite(input7, HIGH);
	digitalWrite(input8, LOW);
}

// 停止函数 ------------------------------------------
void stop()
{
	// 左前轮
	digitalWrite(input1, LOW); 
	digitalWrite(input2, LOW);  
	// 右前轮 
	digitalWrite(input3, LOW); 
	digitalWrite(input4, LOW);
	// 右后轮
	digitalWrite(input5, LOW);
	digitalWrite(input6, LOW);
	// 左后轮
	digitalWrite(input7, LOW);
	digitalWrite(input8, LOW);
}

// 后退函数 ------------------------------------------
void back()
{
	// 左前轮
	digitalWrite(input1, HIGH); 
	digitalWrite(input2, LOW);  
	// 右前轮 
	digitalWrite(input3, HIGH); 
	digitalWrite(input4, LOW);
	// 右后轮
	digitalWrite(input5, LOW);
	digitalWrite(input6, HIGH);
	// 左后轮
	digitalWrite(input7, LOW);
	digitalWrite(input8, HIGH);
}

// 左转函数 ------------------------------------------
void left()
{
	// 左前轮
	digitalWrite(input1, LOW); 
	digitalWrite(input2, HIGH);  
	// 左后轮
	digitalWrite(input7, HIGH);
	digitalWrite(input8, LOW);
	// 右前轮 
	digitalWrite(input3, HIGH); 
	digitalWrite(input4, LOW);
	// 右后轮
	digitalWrite(input5, LOW);
	digitalWrite(input6, HIGH);
}

// 右转函数 ------------------------------------------
void right()
{
	// 右前轮 
	digitalWrite(input3, LOW); 
	digitalWrite(input4, HIGH);
	// 右后轮
	digitalWrite(input5, HIGH);
	digitalWrite(input6, LOW);
	// 左前轮
	digitalWrite(input1, HIGH); 
	digitalWrite(input2, LOW);  
	// 左后轮
	digitalWrite(input7, LOW);
	digitalWrite(input8, HIGH);
}

void loop()
{
	// forward();
	// 后方超声波开启 --------------------------------------------
	digitalWrite(trigBack, LOW);
	delayMicroseconds(5);
	digitalWrite(trigBack, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigBack, LOW);
	// 计算后方超声波的距离
	cmB = (pulseIn(echoBack, HIGH) / 2) / 29.1;

	// 右侧超声波开启 --------------------------------------------
	digitalWrite(trigRight, LOW);
	delayMicroseconds(5);
	digitalWrite(trigRight, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigRight, LOW);
	// 计算后方超声波的距离
	cmR = (pulseIn(echoRight, HIGH) / 2) / 29.1;

	// 左侧超声波开启 --------------------------------------------
	digitalWrite(trigLeft, LOW);
	delayMicroseconds(5);
	digitalWrite(trigLeft, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigLeft, LOW);
	// 计算后方超声波的距离
	cmL = (pulseIn(echoLeft, HIGH) / 2) / 29.1;

	// 串口输出距离
	str += "B";
	str += cmB;
	str += "R";
	str += cmR;
	str += "L";
	str += cmL;
	str += "O";

	delay(500);
	Serial.println(str);
	// 发送完毕串口数据前都在等待
	Serial.flush();
	delay(500);

	// delay(2000);
	str = "";
}
