#include <Servo.h>
#include <Wire.h>

#define BAUD_RATE 9600

#define PIR_PIN 2
#define SERVO_PIN 6

#define MOTOR_OPEN_POSITION 0
#define MOTOR_CLOSED_POSITION 105

#define TIMEOUT_AUTO_CLOSE 10000
#define DELAY_SENSOR_READY 20000
#define DELAY_OPEN_MOVEMENT 3000
#define DELAY_CLOSE_MOVEMENT 2000

bool doorOpen = true;
bool lookingForMovement = false;
bool movementDetected = false;
bool interrupt = false;

Servo x;
int val = 0;  // variable for reading the pin status
unsigned long startTime;

void registerMovement() {
  interrupt = true;
}

void setup() {
  Serial.begin(BAUD_RATE);
  x.attach(SERVO_PIN);
  x.write(MOTOR_OPEN_POSITION);
  pinMode(PIR_PIN, INPUT);
  delay(DELAY_SENSOR_READY);  // declare sensor as input
  attachInterrupt(digitalPinToInterrupt(PIR_PIN), registerMovement, RISING);
  //Serial.println("Scouting");
}


void abrir() {
  if (!doorOpen) {
    x.write(MOTOR_OPEN_POSITION);
    doorOpen = true;
    //Serial.println("cmd_open");
    interrupt = false;
    delay(DELAY_OPEN_MOVEMENT);
  }
  movementDetected = false;
  lookingForMovement = false;
}

void fechar() {
  if (doorOpen) {
    x.write(MOTOR_CLOSED_POSITION);  //90 = posição da porta fechada
    doorOpen = false;
    //Serial.println("cmd_close");
    //pirStatePrevious = LOW;
    delay(DELAY_CLOSE_MOVEMENT);
  }
  lookingForMovement = true;
}


void fechar2() {
  if (doorOpen) {
    x.write(MOTOR_CLOSED_POSITION);  //90 = posição da porta fechada
    doorOpen = false;
    lookingForMovement = true;
    Serial.println("cmd_autoclose");
    //pirStatePrevious = LOW;
    delay(DELAY_CLOSE_MOVEMENT);
  }
  lookingForMovement = true;
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
  if (!lookingForMovement && doorOpen) {
    int test = readSerialPort();
    //Serial.println(test);
    if (test == 1) {
    } else if (test == 0 && !movementDetected) {
      //cmd_Serial.println("here");
      if (interrupt) {
        movementDetected = true;
        Serial.println("cmd_detected");
        Serial.flush();
        //Serial.println("HERE");
        startTime = millis();
      }
    } else if (movementDetected) {
      //Serial.println("AQUIIII");
      unsigned long currentTime = millis();
      unsigned long elapsedTime = currentTime - startTime;
      //Serial.println(currentTime + " " + elapsedTime);
      if (elapsedTime >= TIMEOUT_AUTO_CLOSE) {
        //Serial.println("Time expired");
        fechar2();
        //abrir();
        lookingForMovement = true;
      } else {
        if (readSerialPort() == 1) {
          lookingForMovement = true;
        } else {
        }
      }
    }
  }

  //waiting for RPI commands
  else if (lookingForMovement) {
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
