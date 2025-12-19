#ifndef MAILMAN_H
#define MAILMAN_H

#include <Arduino.h>
#include <ArduinoJson.h>


// Define the Mailman class
class Mailman {
public:
    Mailman();  // constructor
    void init();
    void test(int count);
    void sendDataToPi(float ax, float ay, float az, float sonar_distance);
};

#endif
