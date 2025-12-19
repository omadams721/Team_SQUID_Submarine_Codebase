#ifndef ULTRASONIC_H
#define ULTRASONIC_H
#include <Arduino.h>
class Ultrasonic{

private:
  byte echo;
  byte trig;
  long duration;
  int distance;

public:
Ultrasonic(byte echo, byte trig);

void init();

int getDistance();

};
#endif