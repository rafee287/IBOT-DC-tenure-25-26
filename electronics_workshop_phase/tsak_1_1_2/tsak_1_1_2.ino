int sensor = A0;                          // sensor connected here
// int led = LED_BUILTIN;                    // for feedback
int ldr_val;                                  // value to be read by the sensor pin 
int amb =0;


int ambient_light()
{
  double net_light = 0;
  for(int i =0; i<100; i++)
  {
    Serial.println("calibrating....");
    net_light += analogRead(sensor);  
  }
  return net_light/100;
}
void setup() {
  // put your setup code here, to run once:
  pinMode(sensor, INPUT);
  // pinMode(led,OUTPUT);
  Serial.begin(9600);
  amb = ambient_light();
}

void loop() {
  // put your main code here, to run repeatedly:
  ldr_val = analogRead(sensor);
  Serial.print("light intensity: ");
  Serial.print(ldr_val);
  Serial.print( "|| ambient light value");
  Serial.println(amb);
  
  delay(100);
}
