int led = 2;
int freq = 1000;
void setup() {
  // put your setup code here, to run once:
  ledcAttach(led,freq,12);
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i =0; i<4096;i++)
  {
    ledcWrite(led,i);
  }
  for(int i =4095; i>0;i--)
  {
    ledcWrite(led,i);
  }

}
