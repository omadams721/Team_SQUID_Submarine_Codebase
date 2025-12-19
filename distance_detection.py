"""
Multi-Sonar Data Logger for Underwater Robot (Raspberry Pi)

This script runs on a Raspberry Pi and is used to interface with multiple
DFRobot underwater ultrasonic sonars over hardware UART. It continuously
triggers each sonar, reads the returned binary distance frames, converts the
measurements to centimeters, and logs the data to a file for offline analysis
and debugging.

The primary purpose of this script is:
- Validate sonar wiring and UART configuration
- Collect synchronized distance measurements from multiple sonars
- Record time-stamped sonar data for plotting, calibration, and testing

Unlike the control script, this file does NOT send motor commands or perform
control logic. It is intended purely for sensing and data logging.

--------------------
HARDWARE ASSUMPTIONS
--------------------
- Raspberry Pi with multiple enabled UARTs (e.g., UART3, UART4, UART5)
- DFRobot Underwater Ultrasonic Obstacle Avoidance Sensors (3 m range)
- Sonars connected via UART (TX/RX crossed, common ground)
- Sonars powered from appropriate supply (typically 5V)

--------------------
DATA FORMAT
--------------------
Each sonar returns a 4-byte binary frame:
    [0xFF][DIST_H][DIST_L][CHECKSUM]

Distance is computed as:
    distance_mm = (DIST_H << 8) + DIST_L
    distance_cm = distance_mm / 10.0

Logged file format (CSV):
    timestamp, sonar_0, sonar_1, sonar_2

Timestamps are recorded in ISO-8601 format.

--------------------
CONFIGURATION
--------------------
- SONAR_PORTS: List of UART device paths corresponding to each sonar.
- BAUD: Serial baud rate (must match sonar configuration).
- LOG_FILE: Output file path for logged data (CSV by default).

--------------------
USAGE
--------------------
1. Ensure UART overlays are enabled and no serial getty services are running.
2. Connect all sonars and power them on.
3. Make the script executable:
      chmod +x sonar_logger.py
4. Run:
      python3 distance_detection.py
5. Observe live sonar readings printed to the terminal.
6. Press Ctrl+C to stop logging safely.

--------------------
NOTES
--------------------
- If a sonar returns no data, its value may appear as "None" in the log.
- This script flushes the log file on every write to prevent data loss.
- Designed for calibration, debugging, and sensor characterization prior
  to integration with closed-loop control or ROS 2.
"""

#!/usr/bin/env python3
import sys
import termios
import tty
import json
import serial
import time
from datetime import datetime

# === CONFIGURATION ===
SONAR_PORTS = ["/dev/ttyAMA5", "/dev/ttyAMA3", "/dev/ttyAMA4"]
BAUD = 115200
LOG_FILE = "sonar_data.csv"  # Change to .json if you prefer JSON format

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
            return distance / 10.0  # convert mm to cm
    return None

def main():
    # connect to sonar sensors
    sonars = []
    for port in SONAR_PORTS:
        try:
            s = serial.Serial(port, BAUD, timeout=0.1)
            sonars.append(s)
            print(f"✅ Connected to sonar on {port}")
        except Exception as e:
            print(f"⚠️ Could not open {port}: {e}")

    # Open log file and write header
    with open(LOG_FILE, 'a') as log_file:
        # Write header if file is empty/new
        log_file.write("timestamp,sonar_0,sonar_1,sonar_2\n")
        print(f"📝 Logging data to {LOG_FILE}")

        try:
            while True:
                # read sonar distances
                distances = []
                for i, s in enumerate(sonars):
                    dist = read_sonar(s)
                    distances.append(dist)
                
                if distances:
                    timestamp = datetime.now().isoformat()
                    print(f"🌊 Sonar distances: {distances}")
                    
                    # Write to file: timestamp, dist0, dist1, dist2
                    log_line = f"{timestamp},{distances[0]},{distances[1]},{distances[2]}\n"
                    log_file.write(log_line)
                    log_file.flush()  # Ensure data is written immediately

                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\n🛑 Exiting due to keyboard interrupt.")
        finally:
            for s in sonars:
                s.close()
            print(f"✅ Data saved to {LOG_FILE}")

if __name__ == "__main__":
    import select
    main()