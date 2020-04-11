int input3 = 9; // 定义uno的pin 9 向 input3 输出
int input4 = 10; // 定义uno的pin 10 向 input4 输出

void setup() {
       //  Serial.begin (9600);
       //初始化各IO,模式为OUTPUT 输出模式
       pinMode(input3,OUTPUT);
       pinMode(input4,OUTPUT);
 
}
 
void loop() {
  //forward 向前转
  digitalWrite(input3,HIGH); //给高电平
  digitalWrite(input4,LOW);  //给低电平
 
}