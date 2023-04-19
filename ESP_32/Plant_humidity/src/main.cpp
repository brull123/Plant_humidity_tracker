#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define DELAY_TIME 1000
#define DELAY_LONG 10000
#define PIN_HUMIDITY 34
#define WIFI_SSID "Pe3ny_14D6"
#define WIFI_PSWD "36469635"
// #define WIFI_SSID "Marek"
// #define WIFI_PSWD "123456789"
#define S_BAUD 115200

#define URL_RENDER "https://plant-humidity-tracker.onrender.com/data_post"

#define WIFI_CONNECT_ERROR "WiFi connection error"
#define MPU_CONNECT_ERROR "MPU6050 connection error"
#define MPU_CONNECT_SUCCESS "MPU6050 connected successfully"

int pin_value;
int counter = 0;
DynamicJsonDocument doc(1024);
HTTPClient client;

void setup() {
  Serial.begin(S_BAUD);
  WiFi.begin(WIFI_SSID, WIFI_PSWD);

  delay(DELAY_TIME);

  while(WiFi.status() != WL_CONNECTED){
    Serial.println(WIFI_CONNECT_ERROR);
    delay(DELAY_TIME);
  }

  Serial.println(WiFi.localIP());
  delay(DELAY_TIME);
}

void loop() {
  pin_value = analogRead(PIN_HUMIDITY);
  Serial.println(pin_value);

  if (WiFi.status() == WL_CONNECTED){
    int response_code;

    client.begin(URL_RENDER);
      doc["id"] = counter;
      doc["hum"] = pin_value;

      char output[512];
      serializeJson(doc, output);

      client.addHeader("Content-Type", "application/json");
      response_code = client.PUT(output);

      Serial.print(response_code);
      Serial.print(" ");
      Serial.println(client.getString());
      client.end();
  delay(DELAY_LONG);
  }
}