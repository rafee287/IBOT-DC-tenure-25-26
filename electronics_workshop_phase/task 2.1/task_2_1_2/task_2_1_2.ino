#include <WiFi.h>
#include <WebServer.h>

// --- Wi-Fi Credentials ---
const char* ssid = "instiwifi"; 
#define EAP_IDENTITY "rollno"   //  (usually the same as username)
#define EAP_USERNAME "rollno"    
#define EAP_PASSWORD "passwrd"   

// --- Hardware Setup ---
const int ledPin = 5; // Built-in LED on most ESP32 boards

// Create the web server on port 80
WebServer server(80);

// --- The HTML Webpage ---
// We use R"rawliteral(...)rawliteral" so we don't have to escape every single quote in the HTML
const char* htmlPage = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>ESP32 LED Control</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: Arial; text-align: center; margin-top: 50px; }
    button { padding: 15px 32px; font-size: 24px; margin: 10px; cursor: pointer; }
    .btn-on { background-color: #4CAF50; color: white; border: none; }
    .btn-off { background-color: #f44336; color: white; border: none; }
  </style>
</head>
<body>
  <h1>ESP32 Control Panel</h1>
  <p>LED is ready.</p>
  <a href="/on"><button class="btn-on">TURN ON</button></a>
  <a href="/off"><button class="btn-off">TURN OFF</button></a>
</body>
</html>
)rawliteral";

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Start with LED off

  // --- Connect to Wi-Fi ---
  Serial.println("Connecting to network...");
  WiFi.disconnect(true);
  WiFi.mode(WIFI_STA); 
  WiFi.begin(ssid, WPA2_AUTH_PEAP, EAP_IDENTITY, EAP_USERNAME, EAP_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected!");
  Serial.print("Go to this IP address in your browser: ");
  Serial.println(WiFi.localIP());

  // --- Setup Web Server Routes ---
  
  // 1. When someone visits the main IP address, show the webpage
  server.on("/", []() {
    server.send(200, "text/html", htmlPage);
  });

  // 2. When someone clicks "TURN ON"
  server.on("/on", []() {
    digitalWrite(ledPin, HIGH); // Turn LED on
    server.send(200, "text/html", htmlPage); // Reload the page
  });

  // 3. When someone clicks "TURN OFF"
  server.on("/off", []() {
    digitalWrite(ledPin, LOW); // Turn LED off
    server.send(200, "text/html", htmlPage); // Reload the page
  });

  // Start the server
  server.begin();
  Serial.println("Web server started!");
}

void loop() {
  // This line keeps the server listening for incoming requests from your phone
  server.handleClient();
}