#define PIN_SENSOR A0

void setup(){
  Serial.begin(9600);
}
int valor;
void loop(){
  valor= analogRead(PIN_SENSOR);
  Serial.println(valor);
  delay(1000);
}
