#include "Ultrasonic.h"


  Ultrasonic::Ultrasonic(byte echo, byte trig) {
    this->echo = echo;
    this->trig = trig;
    init();
  }

  void Ultrasonic::init() {
    pinMode(echo, INPUT);
    pinMode(trig, OUTPUT);
    //Serial.begin(9600);
    Serial.println("Ultrasonic Sensor HC-SR04 Test");  // print some text in Serial Monitor
    Serial.println("with Arduino UNO R3");
  }

  int Ultrasonic::getDistance() {
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    // Sets the ULTRASOINC_TRIG HIGH (ACTIVE) for 10 microseconds
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    // Reads the ULTRASONIC_ECHO, returns the sound wave travel time in microseconds
    duration = pulseIn(echo, HIGH);
    // Calculating the distance
    distance = duration * 0.034 / 2;  // Speed of sound wave divided by 2 (go and back)
    // Displays the distance on the Serial Monitor
   // Serial.print("Distance: ");
  //  Serial.print(distance);
   // Serial.println(" cm");
    delay(5);
    return distance;
  }

