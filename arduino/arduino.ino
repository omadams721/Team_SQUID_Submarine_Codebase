#include <ArduinoJson.h>
#include "IMU.h"
#include "Ultrasonic.h"
#include "Drivetrain.h"
#include "Mailman.h"


// === MOTOR PINS ===
#define EN_A 9
#define X_LEFT_1 8
#define X_LEFT_2 7
#define EN_B 3
#define X_RIGHT_1 5
#define X_RIGHT_2 4


#define Z_LEFT_1 13
#define Z_LEFT_2 12
#define Z_RIGHT_1 10
#define Z_RIGHT_2 9


// === IMU ===
#define imu_SDA A4
#define imu_SCL A5


// === OBJECTS ===
//Note: Enable does not matter for motors
Drivetrain X_subby(X_LEFT_1, X_LEFT_2, X_RIGHT_1, X_RIGHT_2, EN_A, EN_B);
Drivetrain Z_subby(Z_LEFT_1, Z_LEFT_2, Z_RIGHT_1, Z_RIGHT_2, EN_A, EN_B);

Mailman mailman;
//IMU imu_sensor;


// === VARIABLES ===
float ax, ay, az;
float sonar_distance;
String inputBuffer = "";  // stores incoming JSON lines


void setup() {
  Serial.begin(115200);
  Serial.println("🤖 Submarine online!");


  mailman.init();


  ax = ay = az = 0;
  sonar_distance = 0;
}


void loop() {
  // --- READ IMU + SEND TELEMETRY ---
 // ax = imu_sensor.getX();
  //ay = imu_sensor.getY();
  //az = imu_sensor.getZ();


 // mailman.sendDataToPi({ax, ay, az}, {sonar_distance});


  // --- RECEIVE JSON COMMANDS ---
  handleSerialCommands();


  delay(100); // adjust rate as needed
}


// === FUNCTION: Handle incoming JSON from Pi ===
void handleSerialCommands() {
  while (Serial.available()) {
    char c = Serial.read();


    // accumulate characters until newline
    if (c == '\n') {
      if (inputBuffer.length() > 0) {
        processJsonCommand(inputBuffer);
        inputBuffer = "";
      }
    } else {
      inputBuffer += c;
    }
  }
}


// === FUNCTION: Parse JSON and execute ===
void processJsonCommand(const String &jsonString) {
  StaticJsonDocument<128> doc;


  DeserializationError error = deserializeJson(doc, jsonString);
  if (error) {
    Serial.print("⚠️ JSON parse error: ");
    Serial.println(error.c_str());
    return;
  }


  // Expecting: {"cmd": "w"}
  if (doc.containsKey("cmd")) {
    String cmd = doc["cmd"].as<String>();
    cmd.toLowerCase();


    if (cmd == "w") {
      X_subby.forward();
      Serial.println("🏁 Forward");
    } else if (cmd == "s") {
      X_subby.backward();
      Serial.println("⬅️  Backward");
    } else if (cmd == "a") {
      X_subby.rotateLeft();
      Serial.println("↩️  Left");
    } else if (cmd == "d") {
      X_subby.rotateRight();
      Serial.println("↪️  Right");
    } else if (cmd == "p") {
      X_subby.stopMoving();
      Z_subby.stopMoving();
      Serial.println("⛔ Stop");
    } if (cmd == "i") {
      Z_subby.forward();
      Serial.println("🏁 Forward");
    } else if (cmd == "k") {
      Z_subby.backward();
      Serial.println("⬅️  Backward");
    } else if (cmd == "j") {
      Z_subby.rotateLeft();
      Serial.println("↩️  Left");
    } else if (cmd == "l") {
      Z_subby.rotateRight();
      Serial.println("↪️  Right");
    }
    else {
      Serial.print("❓ Unknown command: ");
      Serial.println(cmd);
    }
  }
}
