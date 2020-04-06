// 后方超声波 **************************************
int trigBack = 13;
int echoBack = A0;
// 右侧超声波 **************************************
int trigRight = 8;
int echoRight = A1;
// 左侧超声波 **************************************
int trigLeft = 2;
int echoLeft = A2;
// 设置蓝牙的连接 **********************************
String str = "";
// 后侧超声波
long cmB, cmR, cmL;

void setup() {
	// 设置硬件串口通信的波特率
	Serial.begin(9600);
	// 定义后侧超声波的输入输出模式 *******************
	pinMode(trigBack, OUTPUT);
	pinMode(echoBack, INPUT);
	// 定义右侧超声波的输入输出模式 *******************
  	pinMode(trigRight, OUTPUT);
  	pinMode(echoRight, INPUT); 
	// 定义左侧超声波的输入输出模式 *******************
  	pinMode(trigLeft, OUTPUT);
  	pinMode(echoLeft, INPUT); 	  
}
 
void loop()
{
	// 后方超声波开启 **********************************************
	digitalWrite(trigBack, LOW);
	delayMicroseconds(5);
	digitalWrite(trigBack, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigBack, LOW);
	// 计算后方超声波的距离
	cmB = (pulseIn(echoBack, HIGH) / 2) / 29.1;

	// 右侧超声波开启 **********************************************
	digitalWrite(trigRight, LOW);
	delayMicroseconds(5);
	digitalWrite(trigRight, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigRight, LOW);
	// 计算后方超声波的距离
	cmR = (pulseIn(echoRight, HIGH) / 2) / 29.1;

	// 左侧超声波开启 **********************************************
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
	if (Serial.available() > 0) 
	{
		delay(500);
		Serial.print(str);
		delay(500);
	}
	delay(2000);
	str = "";
}
