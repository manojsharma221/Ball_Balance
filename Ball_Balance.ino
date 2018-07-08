int data=90;
#include <Servo.h>
Servo servo;
void setup() {
Serial.begin(115200); // set the baud rate
Serial.println("Ready"); // print "Ready" once
servo.attach(3);
}
void loop() {
if (Serial.available()){
  data = Serial.read();
}
//Serial.println(data);
servo.write(data);
delay(10);
}
