// tripwire task
// int laser = 6;
// void setup() {
//   // put your setup code here, to run once:
//   pinMode(laser,OUTPUT);
// }

// void loop() {
//   // put your main code here, to run repeatedly:
//   digitalWrite(laser,HIGH);
//   delay(1000);
//   digitalWrite(laser,LOW);
//   delay(1000);
// }

// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int laser = 6;
int ldr = A0;
int val;
int buzzer = 7;
void setup() {
  // put your setup code here, to run once:
  pinMode(laser,OUTPUT);
  digitalWrite(laser,HIGH);
  pinMode(ldr,INPUT);
  pinMode(buzzer,OUTPUT);
  Serial.begin(9600);
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Tripwire");
  lcd.setCursor(0,1);
  // lcd.print("Rafee");

}

void loop() {
  // put your main code here, to run repeatedly:
  val = analogRead(ldr);
  //Serial.println(val);
  if(val>40)
  {
    Serial.println("connection broken");
    lcd.print("interference");
    tone(buzzer,1000);
  }
  else{
    Serial.println("connection intact");
    lcd.print("no interference");
    noTone(buzzer);
  }
  lcd.setCursor(0,1);
  delay(100);
}
