#include <Servo.h>
#include <Wire.h>

int door_status = 1;             //0 = fechada,      1= aberta
int servoPin = 6;                // choose the pin for the servo
Servo x;
int pirPin = 2;                 // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status
int lookingForMovement = 0;                 // varible before/after rpi
unsigned long startTime;
int test1 = 0;
void setup() {
  Serial.begin(9600);
  x.attach(servoPin); 
  x.write(0);

  pinMode(pirPin, INPUT);     // declare sensor as input
}


void abrir(){
  x.write(0);
  door_status = 1;
  pirState = LOW;
  lookingForMovement=0;
  Serial.println("cmd_open");
  delay(3000);
}

void fechar(){
  x.write(105); //90 = posição da porta fechada
  door_status=0;
  Serial.println("cmd_close");
  delay(2000);
}
  

void loop() {
  //initial state
  //fechar();
  if(lookingForMovement == 0 && door_status == 1){
    int test = readSerialPort();
    //Serial.println(test);
    if(test == 1){
    }else if (test == 0 && test1 == 0){
      val = digitalRead(pirPin);  // read input value
      //Serial.println(val);
      if(val == HIGH){
        if (pirState == LOW) { 
          //Serial.println("HERE");
          startTime = millis();
          test1 = 1;
          Serial.println("cmd_detected");
          pirState = HIGH;
        }
       }
    }else if(test1 == 1){   
        //Serial.println("AQUIIII");
        unsigned long currentTime = millis();
        unsigned long elapsedTime = currentTime - startTime;
        //Serial.println(currentTime + " " + elapsedTime);
        if(elapsedTime >= 5000){
          Serial.println("Time expired");
          fechar();
          abrir();
          lookingForMovement = 1;
        }else{
          if(readSerialPort() == 1){
            lookingForMovement = 1;
          }else{
            
          }
        }
    }
   }
   
   //waiting for RPI commands
   else if(lookingForMovement == 1){
    //Serial.println("AQUI V2");
    readSerialPort();
  }
}

void state(){
  if(door_status == 0){
      Serial.println("state_close");
  }
  else if(door_status == 1){
      Serial.println("state_open");    
  }
}


int readSerialPort() {
  String msg = "";
  int recebi = 0 ;
  if (Serial.available()) {
      recebi = 1;
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
  return recebi;
}