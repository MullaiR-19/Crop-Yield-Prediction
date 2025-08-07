#include <DHT.h>

#define DHTPIN 12       // DHT11 sensor pin
#define DHTTYPE DHT11   // DHT11 type
#define LED_PIN 2      // LED pin 13
#define RELAY_PIN 6    // Relay Pin 6

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
}

void loop() {
  int soil = map(analogRead(A0), 0, 1023, 0, 100);    // Soil moisture %
  float temp = dht.readTemperature();                 // Temperature (°C)
  float hum = dht.readHumidity();                     // Humidity (%)
  int lux = analogRead(A5);                           // Light intensity (raw)

  // Check if DHT reading failed
  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT read failed");
    return;
  }

  // Send data to Serial
  Serial.print(soil);
  Serial.print(",");
  Serial.print(temp - 1);
  Serial.print(",");
  Serial.print(hum - 10);
  Serial.print(",");
  Serial.println(1023 - lux);

  // Blink LED for 100ms
  digitalWrite(LED_PIN, HIGH);
  delay(50);
  digitalWrite(LED_PIN, LOW);

  delay(2000);  // Wait before next reading

  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'W') {
      digitalWrite(RELAY_PIN, HIGH);
      delay(10000); // 10 seconds
      digitalWrite(RELAY_PIN, LOW);
    }
  }
}
