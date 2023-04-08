// use this for ESP32
#include <ESP32Servo.h>
// use this for other arduino boards
//#include <Servo.h>

// create servo objects
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

// initialise servo positions
float dataServo1 = 90; // Servo 1 rotation range(dataServo1=0~180)
float dataServo2 = 60; // Servo 2 rotation range(dataServo2=0~180) 
float dataServo3 = 110; // Servo 3 rotation range(dataServo3=0~180)
float dataServo4 = 90; // Servo 4 rotation range(dataServo4=0~180)
float dataServo5 = 90; // Servo 5 rotation range(dataServo5=0~180)
float dataServo6 = 90; // Servo 6 rotation range(dataServo6=0~180)

// declare smoothened values
float refresh_rate = 0.98;

float dataServo1_smooth;
float dataServo1_smooth_prev;

float dataServo2_smooth;
float dataServo2_smooth_prev;

float dataServo3_smooth;
float dataServo3_smooth_prev;

float dataServo4_smooth;
float dataServo4_smooth_prev;

float dataServo5_smooth;
float dataServo5_smooth_prev;

float dataServo6_smooth;
float dataServo6_smooth_prev;

void setup() {
  // serial baud
  Serial.begin(115200);

  // attach to GPIO   
  servo1.attach(13);
  servo2.attach(12);
  servo3.attach(14);
  servo4.attach(27);
  servo5.attach(26);
  servo6.attach(25);

  // initialise servo positions
  servo1.write(dataServo1);
  servo2.write(dataServo2);
  servo3.write(dataServo3);
  servo4.write(dataServo4);
  servo5.write(dataServo5);
  servo6.write(dataServo6);
  }

void loop() {

  while(Serial.available()){
    // get new servo positions from serial communication
    // the rotation degree is denoted by 3 numbers
    // e.g. '090' for 90 degrees
    // 6 servos in total, so a total of 18 numbers
    String input = Serial.readStringUntil('\n');
    dataServo1 = input.substring(0,3).toInt();
    dataServo2 = input.substring(3,6).toInt();
    dataServo3 = input.substring(6,9).toInt();
    dataServo4 = input.substring(9,12).toInt();
    dataServo5 = input.substring(12,15).toInt();
    dataServo6 = input.substring(15,18).toInt();
  }

  // instead of directly writing the new servo positions, write with gradually increasing/decreasing values for smooth motion
  dataServo1_smooth = (dataServo1 * (1-refresh_rate)) + (dataServo1_smooth_prev * refresh_rate);
  dataServo2_smooth = (dataServo2 * (1-refresh_rate)) + (dataServo2_smooth_prev * refresh_rate);
  dataServo3_smooth = (dataServo3 * (1-refresh_rate)) + (dataServo3_smooth_prev * refresh_rate);
  dataServo4_smooth = (dataServo4 * (1-refresh_rate)) + (dataServo4_smooth_prev * refresh_rate);
  dataServo5_smooth = (dataServo5 * (1-refresh_rate)) + (dataServo5_smooth_prev * refresh_rate);
  dataServo6_smooth = (dataServo6 * (1-refresh_rate)) + (dataServo6_smooth_prev * refresh_rate);

  // bookmark previous positions
  dataServo1_smooth_prev = dataServo1_smooth;
  dataServo2_smooth_prev = dataServo2_smooth;
  dataServo3_smooth_prev = dataServo3_smooth;
  dataServo4_smooth_prev = dataServo4_smooth;
  dataServo5_smooth_prev = dataServo5_smooth;
  dataServo6_smooth_prev = dataServo6_smooth;

  // update new servo positions
  servo1.write(dataServo1_smooth);
  servo2.write(dataServo2_smooth);
  servo3.write(dataServo3_smooth);
  servo4.write(dataServo4_smooth);
  servo5.write(dataServo5_smooth);
  servo6.write(dataServo6_smooth);

  // wait for 5 ms; write for 200 times per second for smooth operations
  delay(5);
}
