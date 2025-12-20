# Team_SQUID_Submarine_Codebase
This repository contains the software stack for an intelligent submersible vehicle developed as part of a robotics course project. The goal of the project is to design and implement an autonomous underwater system capable of propulsion, sensing, communication, and actuation in a challenging aquatic environment.

The system uses a distributed embedded architecture, with a Raspberry Pi handling high-level sensing, data processing, and control logic, and an Arduino managing low-level motor control and real-time hardware interfacing.

# Project Goals
The vehicle is designed to address the following core challenges:
1. Precise and autonomous motion control
2. Reliable underwater depth and distance sensing
3. Robust communication between embedded subsystems
4. Modular software design for iterative testing and expansion

# System Architecture
Raspberry Pi (High-Level Control)
1. Interfaces directly with multiple underwater ultrasonic sensors via hardware UART
2. Performs distance decoding and depth estimation
3. Implements autonomous depth-holding logic
4. Sends structured control commands to the Arduino
5. Logs sensor data for calibration and analysis
6. Provides manual teleoperation for testing and debugging

Arduino (Low-Level Control)
1. Receives JSON-formatted commands over serial
2. Controls motor drivers and propulsion hardware
3. Interfaces with onboard sensors such as IMU (optional)
4. Executes real-time actuation commands

# Repository Structure
├── teleop_keyboard.py        # Keyboard-based manual control (W/A/S/D + depth commands)<br>
├── depth_control.py          # Autonomous depth-holding using sonar feedback<br>
├── sonar_logger.py           # Multi-sonar data logging and calibration tool<br>
├── arduino/                  # Arduino firmware (motor control, command parsing)<br>
│   └── *.ino<br>
├── README.md<br>

# Key Features

- Autonomous depth control using underwater ultrasonic sensors
- Manual override and teleoperation via keyboard input
- Multi-sonar support for front, bottom, and rear sensing
- JSON-based serial communication for clarity and robustness
- Real-time sensor logging for debugging and calibration
- Designed for operation in underwater environments where GPS and RF are unavailable

# Hardware Requirements
1. Raspberry Pi (with multiple enabled UART interfaces)
2. Arduino or compatible microcontroller
3. DFRobot Underwater Ultrasonic Obstacle Avoidance Sensors (3 m range)
4. Motor drivers and DC thrusters
5. Common ground between all devices
6. Appropriate power supply for underwater operation

# Usage
1. Manual Teleoperation
Use keyboard input to directly command the vehicle for testing:<br>
`python3 teleop_control.py`<br>
Controls include forward, backward, turning, stop, and project-specific depth commands.<br>
2. Autonomous Depth Control<br>
Runs closed-loop depth control using a downward-facing sonar:<br>
`python3 depth_control.py`<br>
The Raspberry Pi continuously monitors depth and sends corrective commands to maintain a desired range.<br>
3. Sonar Data Logging<br>
Logs time-stamped sonar readings to a file for calibration and analysis:<br>
`python3 distance_detection.py`<br>
Data is saved in CSV format for easy plotting and inspection.<br>

# Communication Protocol
Commands sent to the Arduino are JSON-formatted for readability and robustness:
`{
  "cmd": "w"
}`
This approach simplifies debugging and allows for future extension of command types.

# Educational Outcomes
This project focuses on:
1. Embedded systems communication
2. Underwater sensing and perception
3. Autonomous control logic
4. Hardware/software co-design
5. Debugging real-world robotic systems

# Notes
- UART ports must be enabled and free of system services on the Raspberry Pi
- Only one process may access a serial port at a time
- Sonar readings may return None when no valid echo is detected

# Future Work
- Enhanced control strategies
- Obstacle avoidance behaviors
- Sensor fusion with IMU data
- Autonomous navigation and mission execution

# License
This project was developed for educational purposes as part of UMD ENEE408V course.
