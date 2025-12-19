#include "Sonar.h"

#define COM 0x55  // Command byte sent to sonar

Sonar::Sonar(uint8_t rx, uint8_t tx)
  : rxPin(rx), txPin(tx) {
  serial = new SoftwareSerial(rxPin, txPin);
}

void Sonar::begin(long baud) {
  serial->begin(baud);
}

// Reads distance in mm, returns -1 if invalid
int Sonar::readDistanceMM() {
  unsigned char buffer[4] = {0};
  uint8_t CS;
  int distanceMM = -1;

  serial->listen();           // Activate this serial port
  serial->write(COM);
  delay(100);

  if (serial->available() > 0) {
    delay(4);
    if (serial->read() == 0xFF) {
      buffer[0] = 0xFF;
      for (int i = 1; i < 4; i++) {
        buffer[i] = serial->read();
      }
      CS = buffer[0] + buffer[1] + buffer[2];
      if (buffer[3] == CS) {
        distanceMM = (buffer[1] << 8) + buffer[2];
      }
    }
  }

  return distanceMM;
}

/*
int Sonar::readDistanceMM() {
  serial->write(command);
  delay(100);

  if (serial->available() > 0) {
    delay(4);
    if (serial->read() == 0xFF) {
      buffer_RTT[0] = 0xFF;
      for (int i = 1; i < 4; i++) {
        buffer_RTT[i] = serial->read();
      }

      CS = buffer_RTT[0] + buffer_RTT[1] + buffer_RTT[2];
      if (buffer_RTT[3] == CS) {
        distanceMM = (buffer_RTT[1] << 8) + buffer_RTT[2];
        return distanceMM;
      }
    }
  }
  return -1;
}*/
