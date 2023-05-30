#include <Servo.h>

#define BAUD_RATE 9600

#define PIR_PIN 2
#define SERVO_PIN 6

#define MOTOR_OPEN_POSITION 0
#define MOTOR_CLOSED_POSITION 105

#define TIMEOUT_AUTO_CLOSE 10000
#define DELAY_SENSOR_READY 20000
#define DELAY_OPEN_MOVEMENT 3000
#define DELAY_CLOSE_MOVEMENT 2000

enum state_t { OPEN,
               CLOSED,
               WAITING };

bool interrupt = false;

state_t currentState;

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

  currentState = OPEN;
}


void openDoor() {
  doorMotor.write(MOTOR_OPEN_POSITION);
  delay(DELAY_OPEN_MOVEMENT);
}

void closeDoor() {
  doorMotor.write(MOTOR_CLOSED_POSITION);
  delay(DELAY_CLOSE_MOVEMENT);
}

void loop() {
  String command = readSerialPort();
  switch (currentState) {
    case OPEN:
      if (command == "cmd_close") {
        closeDoor();
        currentState = CLOSED;
      } else if (interrupt) {
        interrupt = false;
        currentState = WAITING;
        movementTime = millis();
        Serial.println("cmd_detected");
      }
      return;
    case CLOSED:
      if (command == "cmd_open") {
        openDoor();
        currentState = OPEN;
      }
      return;
    case WAITING:
      if (command == "cmd_open") {
        openDoor();
        currentState = OPEN;
      } else if (command == "cmd_close") {
        closeDoor();
        currentState = CLOSED;
      } else if (millis() - movementTime >= TIMEOUT_AUTO_CLOSE) {
        closeDoor();
        currentState = CLOSED;
        Serial.println("cmd_autoclose");
      }
      return;
  }
}

String readSerialPort() {
  String msg = "";
  if (Serial.available()) {
    delay(10);
    while (Serial.available() > 0) {
      msg += (char)Serial.read();
    }
    msg.trim();
    Serial.flush();
  }
  return msg;
}
