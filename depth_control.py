"""
Depth Control Script for Underwater Robot 

This script runs on a Raspberry Pi and performs the following tasks:
1. Interfaces directly with multiple DFRobot underwater ultrasonic sonars
   over hardware UART (ttyAMA* devices).
2. Periodically triggers each sonar, reads the binary distance response,
   and converts the measurement to centimeters.
3. Uses one designated sonar (typically the downward-facing sonar) to
   estimate vehicle depth.
4. Implements a simple depth-holding controller with hysteresis to avoid
   oscillation.
5. Sends motion commands to an Arduino over USB serial using
   JSON-formatted messages.

The Raspberry Pi is responsible for:
- High-level sensing (sonar processing)
- Control logic (depth decisions)
- Command generation

The Arduino is responsible for:
- Low-level motor control
- Executing commands received as JSON (e.g., dive, surface, stop)

--------------------
HARDWARE ASSUMPTIONS
--------------------
- Raspberry Pi with multiple enabled UARTs (e.g., UART3/4/5).
- DFRobot Underwater Ultrasonic Sensors (3 m range) connected via UART.
- Sonars respond to a single-byte trigger (0x55) and return a 4-byte frame:
    [0xFF][DIST_H][DIST_L][CHECKSUM]
- Common ground between Raspberry Pi and all sonars.
- Arduino connected over USB (e.g., /dev/ttyACM0).

--------------------
CONFIGURATION
--------------------
- SONAR_PORTS: List of UART device paths for each sonar.
- DEPTH_SONAR_INDEX: Index of the sonar used for depth measurement.
- MIN_DEPTH / MAX_DEPTH: Desired depth range in centimeters.
- HYSTERESIS: Deadband to prevent rapid command switching.
- BAUD rate must match both the sonar and Arduino configuration.

--------------------
USAGE
--------------------
1. Ensure all UARTs are enabled in /boot/config.txt and no serial getty
   services are using the ports.
2. Connect sonars and Arduino.
3. Make the script executable:
      chmod +x depth_control.py
4. Run:
      ./depth_control.py
5. Observe sonar readings and JSON commands printed to the terminal.

Press Ctrl+C to safely exit and close all serial ports.
"""

#!/usr/bin/env python3
import sys
import json
import serial
import time

# === CONFIGURATION ===
SONAR_PORTS = ["/dev/ttyAMA5", "/dev/ttyAMA3", "/dev/ttyAMA4"]
BAUD = 115200
ARDUINO_PORT = "/dev/ttyACM0"

# Depth control parameters
MIN_DEPTH = 40  # cm - too shallow
MAX_DEPTH = 35 # cm - too deep
DEPTH_SONAR_INDEX = 1  # which sonar measures depth (0=front, 1=bottom, 2=back)

# Hysteresis to prevent oscillation
HYSTERESIS = 5  # cm

def read_sonar(ser):
    """Read a distance measurement from a DFRobot underwater sonar."""
    ser.write(b'\x55')
    time.sleep(0.1)
    if ser.in_waiting < 4:
        return None
    data = ser.read(4)
    if len(data) == 4 and data[0] == 0xFF:
        high, low, checksum = data[1], data[2], data[3]
        if (0xFF + high + low) & 0xFF == checksum:
            distance = (high << 8) + low
            distance_cm = distance / 10.0  # convert mm to cm
            # Return None if distance is 0 (no reading)
            return distance_cm if distance_cm > 0 else None
    return None

def send_command(ser, cmd):
    """Send a command to the Arduino."""
    payload = {"cmd": cmd}
    json_data = json.dumps(payload)
    ser.write((json_data + "\n").encode('utf-8'))
    print(f"📤 Sent: {json_data}")

def main():
    # Connect to sonar sensors
    sonars = []
    for port in SONAR_PORTS:
        try:
            s = serial.Serial(port, BAUD, timeout=0.1)
            sonars.append(s)
            print(f"✅ Connected to sonar on {port}")
        except Exception as e:
            print(f"⚠️ Could not open sonar {port}: {e}")
            sonars.append(None)  # Keep index alignment
    
    # Connect to Arduino
    try: 
        arduino = serial.Serial(ARDUINO_PORT, BAUD, timeout=0.1)
        print(f"✅ Connected to Arduino on {ARDUINO_PORT}")
    except Exception as e:
        print(f"⚠️ Could not open Arduino {ARDUINO_PORT}: {e}")
        return

    current_state = "neutral"  # Track current command to avoid spam
    last_valid_depth = None  # Track last valid reading

    try:
        while True:
            # Read sonar distances
            distances = []
            for i, s in enumerate(sonars):
                if s is not None:
                    dist = read_sonar(s)
                    distances.append(dist)
                else:
                    distances.append(None)
            
            print(f"🌊 Sonar distances: {distances}")

            # Check depth from the designated sonar
            if len(distances) > DEPTH_SONAR_INDEX:
                depth = distances[DEPTH_SONAR_INDEX]
                
                # Only act on valid readings (not None and not 0)
                if depth is not None and depth > 0:
                    last_valid_depth = depth  # Store for reference
                    
                    # Too shallow - need to dive
                    if depth > MIN_DEPTH - HYSTERESIS:
                        if current_state != "diving":
                            send_command(arduino, "k")  # Dive command
                            current_state = "diving"
                    
                    # Too deep - need to surface
                    elif depth < MAX_DEPTH + HYSTERESIS:
                        if current_state != "surfacing":
                            send_command(arduino, "i")  # Surface command
                            current_state = "surfacing"
                    
                    # In good range - maintain
                    elif MAX_DEPTH <= depth <= MIN_DEPTH:
                        if current_state != "neutral":
                            send_command(arduino, "j")  # Neutral/stop command
                            current_state = "neutral"
                else:
                    print(f"⚠️ Invalid depth reading: {depth} (last valid: {last_valid_depth})")

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n🛑 Exiting due to keyboard interrupt.")
    finally:
        for s in sonars:
            if s is not None:
                s.close()
        arduino.close()

if __name__ == "__main__":
    main()