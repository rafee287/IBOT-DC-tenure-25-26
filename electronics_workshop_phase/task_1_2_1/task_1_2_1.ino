int pin = 6;
int freq = 1000;
void setup() {
  // put your setup code here, to run once:
  pinMode(pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  tone(pin,freq,1000);
  delay(1000);


}
