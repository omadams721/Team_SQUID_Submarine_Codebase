#ifndef IMU_H
#define IMU_H
#include <Wire.h>
//#include "IMU.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>


class IMU {
public:
    IMU();  // constructor
    void init();
    float getX();
    float getY();
    float getZ();
    //IMUData packageData();
    void test();

private:
    Adafruit_BNO055 bno = Adafruit_BNO055(55);
};

#endif
