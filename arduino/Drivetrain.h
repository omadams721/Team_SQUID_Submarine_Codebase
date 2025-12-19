#ifndef DRIVETRAIN_H
#define DRIVETRAIN_H
#include <Arduino.h>


class Drivetrain{
  private:
    int x;
    int y;
    int speed = 255; //Speed ranges from 0 to 255
    
    byte left1;
    byte left2;
    byte right1;
    byte right2;
    byte en_Left;
    byte en_Right;
    
    public:

    Drivetrain(byte left1, byte left2, byte right1, byte right2, byte enA, byte enB);

    void leftForward();
    void rightForward();

    void stopMoving();
    void stopLeft();
    void stopRight();
    
    void leftBackward();
    void rightBackward();

    

    void forward();
    void backward();
    void rotateLeft();
    void rotateRight();

    void test();
};



#endif
