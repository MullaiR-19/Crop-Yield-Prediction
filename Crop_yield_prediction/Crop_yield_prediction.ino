void setup() {
  Serial.begin(9600);
}

void loop() {
  int soil = map(analogRead(A0),0,1023,0,100);        
  float temp = 29.3;                
  float hum = 65.5;                 
  int lux = analogRead(A1);         

  Serial.print(soil);
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(hum);
  Serial.print(",");
  Serial.println(lux);

  delay(2000);
}
