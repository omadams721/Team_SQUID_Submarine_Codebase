"""
Keyboard Teleoperation Interface for Underwater Robot (Raspberry Pi)

This script runs on a Raspberry Pi and provides a simple
keyboard-based teleoperation interface for an Arduino-controlled robot.
It captures single key presses from the terminal,
packages them into JSON-formatted commands, and sends them over a serial
connection to the Arduino.

The primary purpose of this script is:
- Manual testing and debugging of motor control
- Direct teleoperation during bench tests or pool tests
- Verifying serial communication and command parsing on the Arduino

--------------------
HOW IT WORKS
--------------------
- The script reads raw keyboard input using termios/tty (non-blocking, no Enter).
- Valid control keys are converted into a JSON message of the form:
      {"cmd": "<key>"}
- The JSON string is sent over USB serial to the Arduino.
- Optional status or debug messages sent back from the Arduino are printed
  to the terminal.

--------------------
SUPPORTED COMMANDS
--------------------
The following keys are recognized and forwarded to the Arduino:

Movement:
- w : forward
- s : backward
- a : rotate left (about z axis)
- d : rotate right (about z axis)
- p : stop all motors

Depth / State Commands (project-specific):
- i: up
- k: down 
- j: rotate left (about x axis)
- l: rotate right (about x axis)


Exit:
- q : quit the program safely

The exact behavior of each command is defined by the Arduino firmware.

--------------------
HARDWARE ASSUMPTIONS
--------------------
- Arduino (or Teensy) connected to the Raspberry Pi via USB
- Serial device appears as /dev/ttyACM0 (may vary by system)
- Common baud rate between Pi and Arduino (default: 115200)

--------------------
CONFIGURATION
--------------------
- PORT: Serial device for the Arduino connection
- BAUD: Serial baud rate (must match Arduino code)

--------------------
USAGE
--------------------
1. Connect the Arduino to the Raspberry Pi via USB.
2. Ensure no other program is using the serial port.
3. Make the script executable:
      chmod +x teleop_keyboard.py
4. Run:
      python3 teleop_control.py
5. Use the keyboard to send commands.
6. Press 'q' to exit cleanly.
"""

#!/usr/bin/env python3
import sys
import termios
import tty
import json
import serial
import time

# === CONFIGURATION ===
PORT = "/dev/ttyACM0"   # Update this for your Arduino (e.g., COM3 on Windows)
BAUD = 115200

def getch():
    """Read a single key press (no Enter required)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=0.1)
        print(f"✅ Connected to {PORT} at {BAUD} baud.")
    except Exception as e:
        print(f"❌ Could not open serial port: {e}")
        return
    print("Use W/A/S/D to control, Q to quit.\n")

    try:
        while True:
            key = getch().lower()
            if key in ["w", "a", "s", "d", "p", "i", "j", "k", "l"]:
                payload = {"cmd": key}
                json_data = json.dumps(payload)
                ser.write((json_data + "\n").encode('utf-8'))
                print(f"📤 Sent: {json_data}")
            elif key == "q":
                print("👋 Exiting...")
                break
            # Optional: read any response from Arduino
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                if response:
                    print(f"🔄 Arduino: {response}")
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt detected. Exiting.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
