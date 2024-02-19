#include <Servo.h>

Servo myservo1;
Servo myservo2;
Servo myservo3;  // Added third servo
String command;

/* testing code 
void setup() {
  myservo1.attach(9);  // Connects the first servo on pin 9
  myservo2.attach(5);  // Connects the second servo on pin 5
  myservo3.attach(2);  // Connects the third servo on pin 2
  Serial.begin(9600);
}

void loop() {
    rotateServo(myservo3, 1);  // Rotate the third servo when "banana" is received
  
}

void rotateServo(Servo myservo, int times) {
  for (int i = 0; i < times; i++) {
    myservo.write(180);
    delay(1000);
    myservo.write(0);
    delay(1000);
  }
}
*/


void setup() {
  myservo1.attach(9);  // Connects the first servo on pin 9
  myservo2.attach(5);  // Connects the second servo on pin 5
  myservo3.attach(2);  // Connects the third servo on pin 2
  myservo1.write(0); // 0 or 180 or 90
  myservo2.write(0); 
  myservo3.write(0);

  Serial.begin(9600);
}



void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    if (command == "garbage") {
      rotateServo(myservo1, 1);  // Rotate the third servo when "banana" is received
    } else if (command == "recycling") {
      rotateServo(myservo2, 1);  // Rotate the second servo when "popcorn" is received
    } else if (command == "compost") {
      rotateServo(myservo3, 1);  // Rotate the first servo when "paper" is received
    }
  }
}

void rotateServo(Servo myservo, int times) {
  for (int i = 0; i < times; i++) {
    myservo.write(180);
    delay(10000); // 10 seconds if time, integrate with display
    myservo.write(0);
  }
}
