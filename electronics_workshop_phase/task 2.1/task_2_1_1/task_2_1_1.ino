#include <WiFi.h>

const char* ssid = "ssid";
const char* password = "password";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(5,OUTPUT);

  delay(10);

  // connecting to wifi

  Serial.print("connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid,password);

  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Wifi connected");
  Serial.print("ip address:");
  Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:

}
