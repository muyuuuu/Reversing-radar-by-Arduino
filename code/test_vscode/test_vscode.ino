/*** 
 * @Author         : lanling
 * @Date           : 2020-02-06 17:15:20
 * @LastEditTime: 2020-04-12 17:34:28
 * @FilePath       : \test_vscode\test_vscode.ino
 * @Github         : https://github.com/muyuuuu
 * @Description    : 
 * @佛祖保佑，永无BUG
 */

#include <SoftwareSerial.h>   // 引用库
//定义蓝牙模块引脚
SoftwareSerial BT(7, 8); // 接HC05发送脚与D8接口连接，HC05接收脚与D9接口连接
char val;  // 存储接收的数据
void setup() {
       Serial.begin(9600);   
       Serial.println("BT is ready!");
       // 如果是HC-06，改成38400；
       BT.begin(9600);
}
void loop() {
       // 把串口监视器接收到的数据发送给蓝牙模块
       if (Serial.available()) {
              val = Serial.read();
              BT.print(val);
       }
       // 把蓝牙模块接收到的数据发送到串口监视器
       if (BT.available()) {
              val = BT.read();
              Serial.print(val);
       }
}
