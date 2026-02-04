#include <Servo.h>

int servopin = 3;
Servo servo;


void setup() {
  // put your setup code here, to run once:
  servo.attach(servopin);
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i=0; i<180;i++)
  {
    servo.write(i);
    delay(100);
  }
  for(int i=180;i>0;i--)
  {
    servo.write(i);
    delay(100);
  }
}
