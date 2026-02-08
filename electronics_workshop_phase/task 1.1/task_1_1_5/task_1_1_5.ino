int analog_sound = A0;
int digital_sound = 2;
int led = 13;
int digital_sound_val;
int analog_sound_val;

void setup() {
  // put your setup code here, to run once:
  pinMode(led,OUTPUT);
  pinMode(digital_sound,INPUT);
  pinMode(digital_sound,INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  analog_sound_val = analogRead(analog_sound);
  digital_sound_val = digitalRead(digital_sound);  
  Serial.print("value of sound ");
  Serial.println(analog_sound_val);
  //Serial.print(" which corresponds to ");
  //Serial.println(digital_sound_val);
  if(analog_sound_val >100)
  {
    digitalWrite(led,HIGH);
  }
  else
  {
    digitalWrite(led, LOW);
  }
  delay(100);
}
