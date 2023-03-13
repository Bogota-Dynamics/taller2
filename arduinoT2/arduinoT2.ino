
int mR1 = 2;
int mR2 = 3;
int mL1 = 4;
int mL2 = 5;
int pwmR = 6;
int pwmL = 7;


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);

  pinMode(mR1, OUTPUT);
  pinMode(mR2, OUTPUT);
  pinMode(mL1, OUTPUT);
  pinMode(mL2, OUTPUT);
  pinMode(pwmR, OUTPUT);
  pinMode(pwmL, OUTPUT);
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

      if (x > 0) {
        digitalWrite(mL1, HIGH);
        digitalWrite(mL2, LOW);
        digitalWrite(pwmL, 70);

        digitalWrite(mR1, HIGH);
        digitalWrite(mR2, LOW);
        digitalWrite(pwmR, 70);
      }
   }
}
