#include <Servo.h>

Servo leftMotor;
Servo rightMotor;

void setup() {
  Serial.begin(9600);
  leftMotor.attach(9);
  rightMotor.attach(10);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'W') {
      // Move forward
      leftMotor.write(180);
      rightMotor.write(0);
    } else if (command == 'S') {
      // Move backward
      leftMotor.write(0);
      rightMotor.write(180);
    } else if (command == 'A') {
      // Turn left
      leftMotor.write(0);
      rightMotor.write(180);
    } else if (command == 'D') {
      // Turn right
      leftMotor.write(180);
      rightMotor.write(0);
    }
  }
}
