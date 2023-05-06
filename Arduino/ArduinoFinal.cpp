#include <Servo.h>
#include <Wire.h>

int door_status = 1;             //0 = fechada,      1= aberta
int servoPin = 6;                // choose the pin for the servo
Servo x;
int pirPin = 2;                 // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status

void setup() {
  Serial.begin(9600);
  x.attach(servoPin); 
  x.write(0);

  pinMode(pirPin, INPUT);     // declare sensor as input
  Serial.begin(9600);
}


void abrir(){
  x.write(0);
  door_status = 1;
  Serial.println("cmd_open");

}

void fechar(){
  x.write(110); //90 = posição da porta fechada
  door_status=0;
  Serial.println("cmd_close");
}
  

void loop() {
  val = digitalRead(pirPin);  // read input value

  if (val == HIGH) {            

    if (pirState == LOW) {    // passou a detetar movimento (antes nao estava a detetar movimento)
      //Serial.println("Movimento detetado, a fechar porta!");
      pirState = HIGH;

      delay(5000);
      fechar();
      delay(2000); //necessario este delay, pq senao o motor pode nao ter tempo para fechar a porta, antes de começar a receber outros comandos
    }
  } else {
    if (pirState == HIGH){   //parou de detetar movimento
      //Serial.println("Movimento acabado, a abrir porta!");
      abrir();  //apenas quando o utilizar pede para abrir
      pirState = LOW;
    }
  }
  readSerialPort();
  delay(500);
}


void state(){
  if(door == 0){
      Serial.println("state_open");
  }
  else if(door == 1){
      Serial.println("state_close");    
  }
}


void readSerialPort() {
  String msg = "";
  if (Serial.available()) {
      delay(10);
      while (Serial.available() > 0) {
          msg += (char)Serial.read();
      }
      if(msg == "cmd_open"){
        abrir();
      }
      else if(msg == "cmd_close"){
        fechar();
      }
      else if(msg == "cmd_state"){
        state();
      }
      else{
        Serial.println("Not a valid command");
      }
   
      //Serial.print("Detetou");
      Serial.flush();
  }
}

