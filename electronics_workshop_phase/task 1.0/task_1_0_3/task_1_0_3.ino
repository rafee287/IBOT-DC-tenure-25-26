#include <Arduino.h>
int led = LED_BUILTIN;
int led_state =0;
int button = 8;
int button_state =0;
int button_last =0;
int debounce = 50;

void setup()
{
  pinMode(LED_BUILTIN,OUTPUT);
  pinMode(button, INPUT);
}
void loop()
{
  button_state = digitalRead(button);
  if (button_state==0 && button_last==1)
  {
    led_state=!led_state;
    digitalWrite(led,led_state);
  
  }
  button_last = button_state;
  delay(debounce);

}

