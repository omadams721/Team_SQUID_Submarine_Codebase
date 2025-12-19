#include "Drivetrain.h"

Drivetrain::Drivetrain(byte lefta, byte leftb, byte rightc, byte rightd, byte en_left, byte en_right) {
  left1 = lefta;
  left2 = leftb;
  right1 = rightc;
  right2 = rightd;
  en_Left = en_left;
  en_Right = en_right;
  pinMode(lefta, OUTPUT);
  pinMode(leftb, OUTPUT);
  pinMode(rightc, OUTPUT);
  pinMode(rightd, OUTPUT);
  pinMode(en_Left, OUTPUT);
  pinMode(en_Right, OUTPUT);
  

}

void Drivetrain::leftForward() {
  digitalWrite(left1, LOW);
  digitalWrite(left2, HIGH);
}

void Drivetrain::rightForward() {
  digitalWrite(right1, HIGH);
  digitalWrite(right2, LOW);
}

void Drivetrain::stopMoving(){
  stopLeft();
  stopRight();
}

void Drivetrain::stopLeft(){
  digitalWrite(left1, LOW);
  digitalWrite(left2, LOW);
}

void Drivetrain::stopRight(){
  digitalWrite(right1, LOW);
  digitalWrite(right2, LOW);
}

void Drivetrain::leftBackward() {
  digitalWrite(left1, HIGH);
  digitalWrite(left2, LOW);
}

void Drivetrain::rightBackward() {
  digitalWrite(right1, LOW);
  digitalWrite(right2, HIGH);
}

void Drivetrain::forward() {
  Serial.println("forward");
  digitalWrite(left1, LOW);
  digitalWrite(left2, HIGH);

  digitalWrite(right1, HIGH);
  digitalWrite(right2, LOW);
  
}

void Drivetrain::backward() {
  Serial.println("backward");
  digitalWrite(left1, HIGH);
  digitalWrite(left2, LOW);

  digitalWrite(right1, LOW);
  digitalWrite(right2, HIGH);

}

void Drivetrain::rotateLeft() {
  stopLeft();
  rightForward();
}

void Drivetrain::rotateRight() {
  leftForward();
  stopRight();
}

void Drivetrain::test() {
  Serial.println("forward");
  digitalWrite(left1, HIGH);
  digitalWrite(left2, LOW);

  digitalWrite(right1, HIGH);
  digitalWrite(right2, LOW);
  delay(1000);
  Serial.println("backward");
  digitalWrite(left1, LOW);
  digitalWrite(left2, HIGH);

  digitalWrite(right1, LOW);
  digitalWrite(right2, HIGH);
  delay(1000);
}
