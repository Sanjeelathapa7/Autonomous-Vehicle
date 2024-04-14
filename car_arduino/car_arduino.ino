// #include <Servo.h>

// Servo servo; // Create a servo object

// void setup()
// {
//   servo.attach(9);    // Attach the servo to pin 9
//   Serial.begin(9600); // Initialize serial communication
// }
// a
// void loop()
// {
//   if (Serial.available() > 0)
//   {
//     int angle = Serial.parseInt(); // Read the angle from serial
//     servo.write(angle);            // Set the servo angle
//   }
// }


#include <Servo.h>

// Pin Definitions
const int throttlePin = 9;  // PWM pin connected to ESC signal input

// Constants
const int minThrottle = 1000; // Minimum throttle value (in microseconds)
const int maxThrottle = 2000; // Maximum throttle value (in microseconds)
const int neutralThrottle = 1500; // Neutral throttle value (in microseconds)

Servo esc; // Create a servo object

void setup() {
  // Attach the ESC to the throttle pin
  esc.attach(throttlePin);
  
  // Set the throttle to neutral position at start
  esc.writeMicroseconds(neutralThrottle);
  
  // Wait for the ESC to initialize
  delay(5000);
}

void loop() {
  // Move forward at full throttle for 2 seconds
  esc.writeMicroseconds(maxThrottle);
  delay(2000);
  
  // Stop for 1 second
  esc.writeMicroseconds(neutralThrottle);
  delay(1000);
  
  // Move in reverse at full throttle for 2 seconds
  esc.writeMicroseconds(minThrottle);
  delay(2000);
  
  // Stop for 1 second
  esc.writeMicroseconds(neutralThrottle);
  delay(1000);
}
