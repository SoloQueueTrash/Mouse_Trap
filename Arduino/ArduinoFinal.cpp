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

Servo doorMotor;
unsigned long movementTime;

void registerMovement() {
  interrupt = true;
}

void setup() {
  Serial.begin(BAUD_RATE);
  doorMotor.attach(SERVO_PIN);
  doorMotor.write(MOTOR_OPEN_POSITION);
  pinMode(PIR_PIN, INPUT);
  delay(DELAY_SENSOR_READY);
  attachInterrupt(digitalPinToInterrupt(PIR_PIN), registerMovement, RISING);
}


void openDoor() {
  if (!doorOpen) {
    doorMotor.write(MOTOR_OPEN_POSITION);
    doorOpen = true;
    interrupt = false;
    delay(DELAY_OPEN_MOVEMENT);
  }
  movementDetected = false;
  lookingForMovement = false;
}

void closeDoor() {
  if (doorOpen) {
    doorMotor.write(MOTOR_CLOSED_POSITION);
    doorOpen = false;
    delay(DELAY_CLOSE_MOVEMENT);
  }
  lookingForMovement = true;
}


void autoCloseDoor() {
  if (doorOpen) {
    doorMotor.write(MOTOR_CLOSED_POSITION);
    doorOpen = false;
    lookingForMovement = true;
    Serial.println("cmd_autoclose");
    delay(DELAY_CLOSE_MOVEMENT);
  }
  lookingForMovement = true;
}


void loop() {
  if (!lookingForMovement && doorOpen) {
    int test = readSerialPort();
    if (test == 1) return;
    if (!movementDetected) {
      if (interrupt) {
        movementDetected = true;
        Serial.println("cmd_detected");
        Serial.flush();
        movementTime = millis();
      }
    } else if (movementDetected) {
      unsigned long currentTime = millis();
      unsigned long elapsedTime = currentTime - movementTime;
      if (elapsedTime >= TIMEOUT_AUTO_CLOSE) {
        autoCloseDoor();
        lookingForMovement = true;
      } else {
        if (readSerialPort() == 1) {
          lookingForMovement = true;
        } else {
        }
      }
    }
  }
}

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
    if (msg == "cmd_open") {
      Serial.println("VOU ABRIR e o valor do lookingForMovement é " + String(lookingForMovement));
      openDoor();
    } else if (msg == "cmd_close") {
      closeDoor();
    }
    Serial.flush();
  }
  return recebi;
}
