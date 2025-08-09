#include <DHT.h>
#include <Servo.h>

Servo myServo_1;
Servo myServo_2;

#define DHTPIN 12      // DHT11 sensor pin
#define DHTTYPE DHT11  // DHT11 type
#define LED_PIN 2      // LED pin 13
#define RELAY_PIN 6    // Relay Pin 6
#define SERVO_PIN_1    // Main Servo 3
#define SERVO_PIN_2    //Sprinkler Servo 5


DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  myServo_1.attach(SERVO_PIN_1);
  myServo_2.attach(SERVO_PIN_2);

  myServo_1.write(90);
  myServo_2.write(30);
}

void loop() {
  int soil = map(analogRead(A0), 0, 1023, 0, 100);  // Soil moisture %
  float temp = dht.readTemperature();               // Temperature (°C)
  float hum = dht.readHumidity();                   // Humidity (%)
  int lux = analogRead(A5);                         // Light intensity (raw)

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
      myServo_1.write(90);

      sprinkle();
      for (int i = 90; i >= 10; i--) {
        myServo_1.write(i);
        delay(15);
      }

      sprinkle();
      for (int i = 10; i <= 170; i++) {
        myServo_1.write(i);
        delay(15);
      }

      sprinkle();
      for (int i = 170; i >= 90; i--) {
        myServo_1.write(i);
        delay(15);
      }

      delay(1000);
      digitalWrite(RELAY_PIN, LOW);
    }
  }
}

//Sprinkler head rotate function
void sprinkle() {
  digitalWrite(RELAY_PIN, HIGH);
  for (i = 30; i <= 150; i++) {
    myServo_2.write(i);
    dela(40);
  }
  for (i = 150; i < = 30; i--) {
    myServo_2.write(i);
    dela(40);
  }
  digitalWrite(RELAY_PIN, LOW);
  delay(200);
}
