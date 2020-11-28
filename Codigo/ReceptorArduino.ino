#define PIN_SENSOR A0

void setup(){
  Serial.begin(115200);
}

void loop(){
  int valor= analogRead(PIN_SENSOR);
  Serial.println(valor);
  delay(1000);
}
