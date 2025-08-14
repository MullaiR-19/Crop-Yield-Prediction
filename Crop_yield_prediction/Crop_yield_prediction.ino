#include <DHT.h>
#include <Servo.h>

Servo myServo_1;
Servo myServo_2;

#define DHTPIN 12      // DHT11 sensor pin
#define LED_PIN 4      // LED pin 13
#define RELAY_PIN 11    // Relay Pin 6
#define SERVO_PIN_1 3   // Main Servo 3
#define SERVO_PIN_2 5  //Sprinkler Servo 5

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  myServo_1.attach(SERVO_PIN_1);
  myServo_2.attach(SERVO_PIN_2);

  myServo_1.write(100);
  myServo_2.write(40);
}

void loop() {
  int soil = map(analogRead(A0), 1023, 0, 0, 100);  // Soil moisture %
  float temp = dht.readTemperature();               // Temperature (°C)
  float hum = dht.readHumidity();                   // Humidity (%)
  int lux = analogRead(A5);                         // Light intensity (raw)

  // Check if DHT reading failed
  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT read failed");
    temp = 36;
    hum = 70;
  }

  // Send data to Serial
  Serial.print(soil);
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(hum);
  Serial.print(",");
  Serial.println(1023 - lux);

  // Blink LED for 100ms
  digitalWrite(LED_PIN, HIGH);
  delay(50);
  digitalWrite(LED_PIN, LOW);

  delay(2000);  // Wait before next reading

  if (Serial.available()) {
    char cmd = Serial.read();
    //    Serial.print("CMD: ");
    //    Serial.print(cmd);
    if (cmd == 'W') {
      myServo_1.write(100);
      Serial.print("Servo running");
      sprinkle();
      for (int i = 100; i >= 35; i--) {
        myServo_1.write(i);
        delay(15);
      }

      sprinkle();
      for (int i = 35; i <= 165; i++) {
        myServo_1.write(i);
        delay(15);
      }

      sprinkle();
      for (int i = 165; i >= 100; i--) {
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
  for (int i = 40; i <= 140; i++) {
    myServo_2.write(i);
    delay(40);
  }
  for (int i = 140; i >= 40; i--) {
    myServo_2.write(i);
    delay(40);
  }
  digitalWrite(RELAY_PIN, LOW);
  delay(200);
}
