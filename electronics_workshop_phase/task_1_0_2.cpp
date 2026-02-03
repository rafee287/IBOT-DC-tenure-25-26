#include <Arduino.h>
int led = LED_BUILTIN;
void setup()
{
  pinMode(LED_BUILTIN,OUTPUT);
}
void loop()
{
  for(int i =0; i<255;i+=10)
  {
    analogWrite(led,i);
    delay(100);
  }
  for(int i =255; i>0;i-=10)
  {
    analogWrite(led,i);
    delay(100);
  }
}

