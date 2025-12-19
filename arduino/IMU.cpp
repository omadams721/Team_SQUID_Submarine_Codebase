#include "IMU.h"

IMU::IMU() {
    init();
}

void IMU::init(){
  Adafruit_BNO055 bno = Adafruit_BNO055(55);
  Serial.println("Orientation Sensor Test"); Serial.println("");
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  delay(1000);
  bno.setExtCrystalUse(true);
}

float IMU::getX(){
  sensors_event_t event; 
  bno.getEvent(&event);
  return event.orientation.x;
}

float IMU::getY(){
  sensors_event_t event; 
  bno.getEvent(&event);
  return event.orientation.y;
}

float IMU::getZ(){
  sensors_event_t event; 
  //bno.getEvent(&event);
  return event.orientation.z;
}

//IMUData IMU::packageData(){
  //IMUData imu;
  //imu.gx = getX();
  //imu.gy = getY();
  //imu.gz = getZ();
  //return imu
//}
void IMU::test(){
  sensors_event_t event; 
  //bno.getEvent(&event);
  
  /* Display the floating point data */
  Serial.print("{");
  Serial.print("\"x\":"); Serial.print(event.orientation.x, 4); Serial.print(",");
  Serial.print("\"y\":"); Serial.print(event.orientation.y, 4); Serial.print(",");
  Serial.print("\"z\":"); Serial.print(event.orientation.z, 4);
  Serial.println("}");
}
