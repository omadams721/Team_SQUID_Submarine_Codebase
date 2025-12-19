#include "Mailman.h"

// Constructor calls init()
Mailman::Mailman() {
    init();
}

void Mailman::init() {
    Serial.println("Mailman is off to work!");
}

void Mailman::test(int count) {
    StaticJsonDocument<256> doc;

    // Create a JSON array with a test message
    JsonArray test_array = doc.createNestedArray("test");
    String message = "Hello from Pi " + String(count);
    test_array.add(message);

    // Serialize JSON to UART
    serializeJson(doc, Serial);
    Serial.println(); // newline for readability
}

void Mailman::sendDataToPi(float ax, float ay, float az, float sonar_distance) {
    StaticJsonDocument<256> doc;
    Serial.println("sending data");
    
    // IMU section
    JsonObject imuObj = doc.createNestedObject("imu");
    imuObj["ax"] = ax;
    imuObj["ay"] = ay;
    imuObj["az"] = az;

    // Sonar section
    JsonObject sonarObj = doc.createNestedObject("sonar");
    sonarObj["distance"] = sonar_distance;

    // Send JSON over Serial
    serializeJson(doc, Serial);
    Serial.println();
}
