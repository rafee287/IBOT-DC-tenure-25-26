# include <Wire.h>
# include <Adafruit_GFX.h>
# include <Adafruit_SSD1306.h>

int w = 128;
int h = 64;

# define OLED_Addr 0x3C

Adafruit_SSD1306 display(w,h,&Wire,-1);

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(9600);
  if(!display.begin(SSD1306_SWITCHCAPVCC, OLED_Addr))
  {
    Serial.println("oled not detected");
    while(true);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);

  display.println("Hello world");
  display.display();
}

void loop() {
  // put your main code here, to run repeatedly:

}
