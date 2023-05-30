#include <Servo.h>
#include <Wire.h>

int door_status = 1;  //0 = fechada,      1= aberta
int servoPin = 6;     // choose the pin for the servo
Servo x;
int pirPin = 2;              // choose the input pin (for PIR sensor)
int pirStateCurrent;         // we start, assuming no motion detected
int pirStatePrevious;        // we start, assuming no motion detected
int val = 0;                 // variable for reading the pin status
int lookingForMovement = 0;  // varible before/after rpi
unsigned long startTime;
int test1 = 0;
void setup() {
  Serial.begin(9600);
  x.attach(servoPin);
  x.write(0);
  pinMode(pirPin, INPUT);
  pirStateCurrent = LOW;
  pirStatePrevious = LOW;
  delay(20000);  // declare sensor as input
  //Serial.println("Scouting");
}


void abrir() {
  if (door_status == 0) {
    x.write(0);
    door_status = 1;
    //Serial.println("cmd_open");
    pirStatePrevious = LOW;
    delay(3000);
  }
  test1 = 0;
  lookingForMovement = 0;
}

void fechar() {
  if (door_status == 1) {
    x.write(105);  //90 = posição da porta fechada
    door_status = 0;
    //Serial.println("cmd_close");
    //pirStatePrevious = LOW;
    delay(2000);
  }
  lookingForMovement = 1;
}


void fechar2() {
  if (door_status == 1) {
    x.write(105);  //90 = posição da porta fechada
    door_status = 0;
    lookingForMovement = 1;
    Serial.println("cmd_autoclose");
    //pirStatePrevious = LOW;
    delay(2000);
  }
  lookingForMovement = 1;
}


void loop() {
  //initial state
  //readSerialPort();
  //delay(2000;
  /*delay(10000);
  Serial.println("cmd_detected");
  Serial.println("cmd_detected");
  Serial.println("cmd_detected");
  Serial.flush();*/
  if (lookingForMovement == 0 && door_status == 1) {
    int test = readSerialPort();
    //Serial.println(test);
    if (test == 1) {
    } else if (test == 0 && test1 == 0) {
      //cmd_Serial.println("here");
      pirStateCurrent = digitalRead(pirPin);  // read input value
      //pirState = HIGH;
      if (pirStateCurrent == HIGH && pirStatePrevious == LOW) {
        test1 = 1;
        Serial.println("cmd_detected");
        Serial.flush();
        //Serial.println("HERE");
        startTime = millis();
      }
    } else if (test1 == 1) {
      //Serial.println("AQUIIII");
      unsigned long currentTime = millis();
      unsigned long elapsedTime = currentTime - startTime;
      //Serial.println(currentTime + " " + elapsedTime);
      if (elapsedTime >= 10000) {
        //Serial.println("Time expired");
        fechar2();
        //abrir();
        lookingForMovement = 1;
      } else {
        if (readSerialPort() == 1) {
          lookingForMovement = 1;
        } else {
        }
      }
    }
  }

  //waiting for RPI commands
  else if (lookingForMovement == 1) {
    //Serial.println("AQUI V2");
    readSerialPort();
  }
}

/*void state(){
  if(door_status == 0){
      Serial.println("state_close");
  }
  else if(door_status == 1){
      Serial.println("state_open");    
  }
}*/


int readSerialPort() {
  String msg = "";
  int recebi = 0;
  if (Serial.available()) {
    recebi = 1;
    delay(10);
    while (Serial.available() > 0) {
      msg += (char)Serial.read();
    }
    msg.replace("\n", "");
    msg.replace("\r", "");
    //Serial.println('|' + msg + '|');
    if (msg == "cmd_open") {
      Serial.println("VOU ABRIR e o valor do lookingForMovement é " + String(lookingForMovement));
      abrir();
    } else if (msg == "cmd_close") {
      fechar();
    }
    //Serial.print("Detetou");
    Serial.flush();
  }
  return recebi;
}
