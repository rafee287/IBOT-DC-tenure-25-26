int sensor = A0;                          // sensor connected here
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
  if (val > 240)
  {
    Serial.println("object detected ");
    digitalWrite(led, HIGH);
  }
  else
  {
    digitalWrite(led,LOW);
    Serial.println("no object");
  }
  delay(100);
}
