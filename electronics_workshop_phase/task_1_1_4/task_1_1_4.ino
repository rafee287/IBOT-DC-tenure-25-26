int echopin = 2;
int trigpin = 6;
long duration ;         // variable to store the time taken byt the pulse to reach the reciver 
double distance;          // storing the distance calculated in cm

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);               // setting baud rate 
  Serial.println("serial running");
  Serial.println("distance measuremnts");
  
  pinMode(trigpin, OUTPUT);             // trigger pin generates the pulse
  pinMode(echopin, INPUT);
  delay(500);
  
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
  digitalWrite(trigpin,LOW);  // set initially to low to prevent any unnecessary readings 
  delayMicroseconds(5);                   // delay to avoid collision in serial monitor
  digitalWrite(trigpin,HIGH); // set high to generate pulse
  delayMicroseconds(10);      // generating pulse for 10 microseconds

  // if pulse reached the reciever pin ==> echopin then it becomes HIGH 
  // the pulseIn() function returns the time taken in microsec by the pulse to reach the reciver 
  digitalWrite(trigpin,LOW);
  duration = pulseIn(echopin,HIGH);
  distance = duration * 0.0344/2 ;  
  
  Serial.println(distance);
  delay(1000);


}