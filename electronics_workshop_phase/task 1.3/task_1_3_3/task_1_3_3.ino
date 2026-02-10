# include <Wire.h>
# include <Adafruit_GFX.h>
# include <Adafruit_SSD1306.h>
# define OLED_Addr 0x3C

int w = 128;
int h = 64;
int sound_sensor = A0;
int sound_val;
int diff;

Adafruit_SSD1306 display(w,h,&Wire,-1);

void display_bar(int reading)
{
  display.clearDisplay();
  for(int i =0; i<h/2+reading;i++)
  {
    for(int j=56; j<65;j++)
    {
      display.drawPixel(j,64-i,WHITE);
    }
  }
  display.display();
}
void setup() {
  // put your setup code here, to run once:
  pinMode(sound_sensor,INPUT);
    Wire.begin();
  Serial.begin(9600);
  if(!display.begin(SSD1306_SWITCHCAPVCC, OLED_Addr))
  {
    Serial.println("oled not detected");
    while(true);
  }
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);

  display.println("Soundlevel    sensor");
  display.display();
  delay(2000);
  display.clearDisplay();
}

void loop() {
  // put your main code here, to run repeatedly:
  sound_val = analogRead(sound_sensor);
  Serial.print(sound_val);
  Serial.print("   ");
  diff = sound_val -569;
  Serial.println(diff);
  diff = map(diff,0,32,-32,32);
  display_bar(diff);
  //Serial.println(diff);
  delay(100);

}
