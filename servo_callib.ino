#include <Servo.h>

Servo myservo1,myservo2;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos1 = 0;    // variable to store the servo1 position
int pos2 = 0;    // variable to store the servo2 position

void setup() {
  myservo1.attach(10);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(11);  // attaches the servo on pin 9 to the servo object
}   

void loop() {
    myservo1.write(pos1);              // tell servo1 to go to position in variable 'pos1'
    delay(15);                       // waits 15ms for the servo to reach the position

    myservo2.write(pos2);              // tell servo2 to go to position in variable 'pos2'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
