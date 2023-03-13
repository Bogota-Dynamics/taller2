
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);

}

void loop() {
  while (!Serial.available());

    String input = Serial.readStringUntil('\n');
    float x, y;

    if (sscanf(input.c_str(), "%f,%f", &x, &y) == 2) {
      Serial.print("x = ");
      Serial.print(x);
      Serial.print("y = ");
      Serial.print(y);

      // if x > 0 ...
    }
}
