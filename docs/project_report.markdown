# TerraRecon Project Report

## Overview
**TerraRecon** is an autonomous military surveillance rover developed as a Bachelor of Technology project at SRM Institute of Science and Technology, Ramapuram. It leverages advanced AI and RF technology to enhance defense and security operations, focusing on real-time environment mapping, threat detection, and autonomous navigation. The rover is designed to reduce manual surveillance risks, improve operational efficiency, and provide scalable solutions for applications like border security and autonomous patrolling.

## Objectives
- Develop a robust, terrain-adaptive rover for military surveillance.
- Implement AI-based threat detection using real-time object and facial recognition.
- Enable secure, long-range data transmission via RF communication.
- Create a modular and energy-efficient design for scalability.

## Hardware Design
- **Central Processing Unit**: Raspberry Pi 4, serving as the main controller.
- **Sensors**:
  - LIDAR for environment mapping.
  - Infrared camera for low-light vision.
  - Ultrasonic sensor for obstacle detection.
  - GPS for navigation and positioning.
- **Chassis**: Modular, 3D-printed tracks for terrain adaptability.
- **Motors**: DC motors with drivers for precise movement control.

## Software Architecture
- **Framework**: Robot Operating System (ROS) for modular control and communication.
- **Programming Language**: Python for core logic and AI processing.
- **AI Components**:
  - **Object Detection**: YOLO model (loaded via `models/dnn_prototxt.txt` and `dnn_caffemodel.caffemodel`) for person detection.
  - **Facial Recognition**: `face_recognition` library for identifying known/unknown individuals.
- **Database**: SQLite (`data/database.sqlite`) for storing face encodings.
- **Communication**: RF-based data transmission for sending alerts with base64-encoded images.

## Key Features
- **Autonomous Navigation**: Combines LIDAR, GPS, and ultrasonic sensor data for obstacle avoidance and path planning.
- **Threat Detection**: Detects and identifies persons, flagging unknowns and sending alerts to a remote server.
- **Real-Time Processing**: Processes video feeds at 640x480 resolution for efficient performance on Raspberry Pi.
- **Modular Codebase**: Organized into modules (`src/motor_control.py`, `src/vision_processing.py`, etc.) for maintainability.

## Implementation Details
- **Code Structure**: See `src/` for core modules and `scripts/` for utility scripts.
- **Setup**: Detailed in `docs/hardware_setup.md` and `docs/user_manual.md`.
- **Dependencies**: Listed in `requirements.txt` (e.g., `opencv-python`, `face_recognition`).
- **Testing**: Unit tests in `tests/` for motors, vision, and communication.

## Challenges and Solutions
- **Challenge**: Limited computational resources on Raspberry Pi.
  - **Solution**: Optimized YOLO model (e.g., MobileNet-SSD) for lightweight processing.
- **Challenge**: Reliable obstacle detection in varied terrains.
  - **Solution**: Sensor fusion combining LIDAR and ultrasonic data.
- **Challenge**: Secure data transmission.
  - **Solution**: RF communication with base64-encoded image alerts.

## Future Enhancements
- Integrate thermal imaging for enhanced night operations.
- Add ROS-based multi-rover coordination.
- Implement machine learning for adaptive path planning.
- Enhance RF range and encryption for secure communication.

## Conclusion
TerraRecon demonstrates significant potential for transforming defense operations with its robust, customizable, and energy-efficient design. The project successfully integrates AI, robotics, and communication technologies, providing a scalable solution for autonomous surveillance.

## Authors
- Developed by students at SRM Institute of Science and Technology, Ramapuram.
- Contact: [Insert contact details or GitHub repository link].