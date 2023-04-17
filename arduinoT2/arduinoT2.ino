#define ENC_COUNT_REV 77
#define ENC_IN_RIGHT_A 19
#define ENC_IN_RIGHT_B 8
#define ENC_IN_LEFT_A 18
#define ENC_IN_LEFT_B 9

boolean Direction_right = true;
volatile long right_wheel_pulse_count = 0;
boolean Direction_left = true;
volatile long left_wheel_pulse_count = 0;

int interval = 1000;
long previousMillis = 0;
long currentMillis = 0;

float rpm_right = 0;
float rpm_right_ant = 0;
float rpm_left = 0;
float rpm_left_ant = 0;

int mR1 = 2;
int mR2 = 3; 
int mL1 = 4;
int mL2 = 5;
int pwmR = 6;
int pwmL = 7;

float x, y;

void setup() {
  Serial.begin(250000);
  Serial.setTimeout(1);

  pinMode(ENC_IN_RIGHT_A, INPUT_PULLUP);
  pinMode(ENC_IN_RIGHT_B, INPUT);
  pinMode(ENC_IN_LEFT_A, INPUT_PULLUP);
  pinMode(ENC_IN_LEFT_B, INPUT);

  pinMode(mR1, OUTPUT);
  pinMode(mR2, OUTPUT);
  pinMode(mL1, OUTPUT);
  pinMode(mL2, OUTPUT);
  pinMode(pwmR, OUTPUT);
  pinMode(pwmL, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(ENC_IN_RIGHT_A), right_wheel_pulse, RISING);
  attachInterrupt(digitalPinToInterrupt(ENC_IN_LEFT_A), left_wheel_pulse, RISING);
}

void loop() {
    
    currentMillis = millis();
    if(currentMillis-previousMillis>interval)
    {
      previousMillis = currentMillis;
      rpm_right= (float)(right_wheel_pulse_count*60/ENC_COUNT_REV);
      rpm_left= (float)(left_wheel_pulse_count*60/ENC_COUNT_REV);
      char buffer[20];
      dtostrf(rpm_right, 5, 2, buffer);
      String cadena1 = String(buffer);
      dtostrf(rpm_left, 5, 2, buffer);
      String cadena2 = String(buffer);

      Serial.println(cadena1 + "," + cadena2);

      
      right_wheel_pulse_count = 0;
      left_wheel_pulse_count = 0;
    }
    
    String input = Serial.readString();
    input.trim();
    int commaIndex = input.indexOf(',');
    if (commaIndex >= 0) {
       String str1 = input.substring(0, commaIndex);
       String str2 = input.substring(commaIndex + 1);
       x = str1.toFloat();
       y = str2.toFloat();
    }

      if (x < 0) {
        digitalWrite(mL1, HIGH);
        digitalWrite(mL2, LOW);
        digitalWrite(pwmL, 100);

        digitalWrite(mR1, HIGH);
        digitalWrite(mR2, LOW);
        digitalWrite(pwmR, 100);

        Direction_right = true;
        Direction_left = true;
      }
      else if (x>0){
        digitalWrite(mL2, HIGH);
        digitalWrite(mL1, LOW);
        digitalWrite(pwmL, 100);

        digitalWrite(mR2, HIGH);
        digitalWrite(mR1, LOW);
        digitalWrite(pwmR, 100);

        Direction_right = false;
        Direction_left = false;
      }

      else if (y < 0){
        digitalWrite(mL2, HIGH);
        digitalWrite(mL1, LOW);
        digitalWrite(pwmL, 100);

        digitalWrite(mR2, LOW);
        digitalWrite(mR1, HIGH);
        digitalWrite(pwmR, 70);
        Direction_right = true;
        Direction_left = false;
        
       }

       else if (y > 0){
        digitalWrite(mL2, LOW);
        digitalWrite(mL1, HIGH);
        digitalWrite(pwmL, 100);

        digitalWrite(mR2, HIGH);
        digitalWrite(mR1, LOW);
        digitalWrite(pwmR, 70);

        Direction_right = false;
        Direction_left = true;
       }
      else if (x==0 || y==0){
        digitalWrite(mL1, LOW);
        digitalWrite(mL2, LOW);

        digitalWrite(mR1, LOW);
        digitalWrite(mR2, LOW);
      }
 
}


void right_wheel_pulse(){
 
  if(Direction_right == false){
    right_wheel_pulse_count++;
    }

  else{
    right_wheel_pulse_count--;
    }

}


void left_wheel_pulse(){

  
  if(Direction_left == false){
    left_wheel_pulse_count++;
    }

  else{
    left_wheel_pulse_count--;
    }

    
}
