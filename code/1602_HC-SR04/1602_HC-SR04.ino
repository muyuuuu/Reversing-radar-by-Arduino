#include <LiquidCrystal.h>

int trigPin = 11;    //Trig
int echoPin = 12;    //Echo
long duration, cm;
 
const int rs = 7, en = 6, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lcd.begin(16, 2);
  lcd.clear();
}
 
void loop()
{
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  duration = pulseIn(echoPin, HIGH);
 
  // convert the time into a distance
  cm = (duration/2) / 29.1;
  cm = int(cm);
  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("L:");
  
  lcd.setCursor(8, 0);
  lcd.print("R:");

  lcd.setCursor(5, 1);
  lcd.print("C:");
  lcd.print(cm);
  lcd.print("cm");

  delay(500);
}
