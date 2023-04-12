#define ENC_COUNT_REV 620
#define ENC_IN_RIGHT_A 2
#define ENC_IN_RIGHT_B 4

boolean Direction_right = true;
volatile long right_wheel_pulse_count = 0;

int interval = 1000;
long previousMillis = 0;
long currentMillis = 0;

float rpm_right = 0;

void setup() {

  Serial.begin(9600);

  pinMode(ENC_IN_RIGHT_A, INPUT_PULLUP);
  pinMode(ENC_IN_RIGHT_B, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENC_IN_RIGHT_A), right_wheel_pulse, RISING);

}

void loop() {

  currentMillis = millis();

  if(currentMillis-previousMillis>interval)
    {
      previousMillis = currentMillis;
      rpm_right= (float)(right_wheel_pulse_count*60/ENC_COUNT_REV);
      
      Serial.print(" Pulses: ");
      Serial.println(right_wheel_pulse_count);
      Serial.print(" RPM: ");
      Serial.println(rpm_right);

      right_wheel_pulse_count = 0;
    }
}


void right_wheel_pulse(){
  
  int val=digitalRead(ENC_IN_RIGHT_B);

  if(val == LOW){

    Direction_right = false;
    }

  else{
    Direction_right = true;
    }

  if(val == LOW){

    right_wheel_pulse_count++;
    }

  else{
    right_wheel_pulse_count--;
    }

    
  
  }
