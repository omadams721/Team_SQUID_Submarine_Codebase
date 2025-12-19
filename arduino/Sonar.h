#ifndef SONAR_H
#define SONAR_H

#include <Arduino.h>
#include <SoftwareSerial.h>

class Sonar {
  private:
    SoftwareSerial* serial;   // Pointer to SoftwareSerial object
    uint8_t rxPin;
    uint8_t txPin;

  public:
    Sonar(uint8_t rx, uint8_t tx);
    void begin(long baud = 115200);
    int readDistanceMM();
};

#endif
