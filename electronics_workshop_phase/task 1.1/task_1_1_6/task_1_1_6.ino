// this is code for ir flame sensor
// the code is simple because the feedback led is available on the module itslef

int sensor = 2;                          // sensor connected here
int led = LED_BUILTIN;                    // for feedback
int val;                                  // value to be read by the sensor pin 
void setup() {
  // put your setup code here, to run once:
  pinMode(sensor, INPUT);
  pinMode(led,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = analogRead(sensor);
  Serial.println(val);
  
  delay(100);
}
