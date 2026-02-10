# include <Wire.h>
# include <Adafruit_GFX.h>
# include <Adafruit_SSD1306.h>

int w = 128;
int h = 64;
int x=0;
int y=0;
int r = 2;
int r_val;
int l = 3;
int l_val;
int u = 4;
int u_val;
int d = 5;
int d_val;
int shift =8;
# define OLED_Addr 0x3C

Adafruit_SSD1306 display(w,h,&Wire,-1);

// helper function to draw a 8x8 grid using the top left corner as reference 
void draw_walker(int t_l_x,int t_l_y){
  for(int i =0; i<8;i++){
    for(int j =0; j<8;j++){
      display.drawPixel((((t_l_x+i)%w)+w)%w,(((t_l_y+j)%h)+h)%h,WHITE);
    }
  }
  display.display();
}

// helper function to move the grid by one pixel
void move_right(int t_l_x,int t_l_y,int shift){
  display.clearDisplay();
  draw_walker(t_l_x+shift,t_l_y);
  
}
void move_left(int t_l_x,int t_l_y,int shift){
  display.clearDisplay();
  draw_walker(t_l_x-shift,t_l_y);
}
void move_up(int t_l_x,int t_l_y,int shift){
  display.clearDisplay();
  draw_walker(t_l_x,t_l_y-shift);
}
void move_down(int t_l_x,int t_l_y,int shift){
  display.clearDisplay();
  draw_walker(t_l_x-1,t_l_y+shift);
}

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

  display.println("GRID WALKER");
  display.display();
  delay(2000);
  display.clearDisplay();
  
  pinMode(r,INPUT);
  pinMode(l,INPUT);
  pinMode(u,INPUT);
  pinMode(d,INPUT);
  draw_walker(x,y);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  r_val = digitalRead(r);
  l_val = digitalRead(l);
  u_val = digitalRead(u);
  d_val = digitalRead(d);
  
  if(r_val == LOW)
  {
    move_right(x,y,shift);
    x+=shift;
  }
  else if(l_val == LOW)
  {
    move_left(x,y,shift);
    x-=shift;
  }
  else if(u_val == LOW)
  {
    move_up(x,y,shift);
    y-=shift;
  }
  else if(d_val == LOW)
  {
    move_down(x,y,shift);
    y+=shift;
  }
  
  delay(100);

}

