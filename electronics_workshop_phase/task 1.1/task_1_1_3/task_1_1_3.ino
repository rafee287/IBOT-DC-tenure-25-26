int pirsensor = 4;                          // sensor connected here
int led = LED_BUILTIN;                    // for feedback
int val;                                  // value to be read by the sensor pin 
void setup() {
  // put your setup code here, to run once:
  pinMode(pirsensor, INPUT);
  pinMode(led,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = digitalRead(pirsensor);
  
  if (val == HIGH)
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
