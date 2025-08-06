# TerraRecon: Autonomous Military Surveillance Rover


**TerraRecon** is a cutting-edge autonomous surveillance rover engineered to transform military and defense operations. Developed as a Bachelor of Technology project at SRM Institute of Science and Technology, Ramapuram, TerraRecon integrates advanced artificial intelligence, robust RF communication, and a terrain-adaptive chassis to deliver real-time threat detection, precise environment mapping, and autonomous navigation. Designed for critical applications such as border security, perimeter monitoring, and tactical patrolling, it minimizes human risk while maximizing operational efficiency through a scalable, energy-efficient platform.

## Project Theme and Innovations

TerraRecon redefines autonomous surveillance with a fusion of state-of-the-art technologies:

- **AI-Driven Threat Detection**: Employs the YOLO (You Only Look Once) algorithm for real-time person detection, coupled with the `face_recognition` library for high-accuracy facial identification (128D face encodings). Unknown individuals trigger immediate alerts, enhancing situational awareness.
- **Autonomous Navigation**: Combines LIDAR (e.g., RPLIDAR A1) for 3D environment mapping, GPS (e.g., NEO-6M) for geolocation, and ultrasonic sensors (e.g., HC-SR04) for obstacle detection within a 30 cm threshold, enabling robust navigation across challenging terrains.
- **Secure RF Communication**: Utilizes RF modules (e.g., NRF24L01) to transmit base64-encoded images of detected threats to a remote server, ensuring secure, long-range data transfer in mission-critical scenarios.
- **Hardware Efficiency**: Powered by a Raspberry Pi 4 (4GB/8GB RAM) with a modular, 3D-printed chassis featuring terrain-adaptive tracks, optimized for low-power operation and durability.
- **Modular Software Architecture**: Built on the Robot Operating System (ROS) and Python, with a modular codebase (`src/motor_control.py`, `src/vision_processing.py`, etc.) for extensibility and ease of maintenance.

This project showcases the potential of AI and robotics to revolutionize defense surveillance, offering a scalable solution for real-world deployment.

## Prerequisites

### Hardware
- **Raspberry Pi 4**: 4GB or 8GB RAM for processing AI and sensor data.
- **LIDAR Sensor**: RPLIDAR A1 or equivalent for 3D environment mapping.
- **Infrared Camera**: Raspberry Pi NoIR Camera Module for low-light vision.
- **Ultrasonic Sensor**: HC-SR04 for obstacle detection.
- **GPS Module**: NEO-6M for precise geolocation.
- **DC Motors and Driver**: L298N driver with four DC motors for mobility.
- **Chassis**: 3D-printed with modular tracks for terrain adaptability.
- **RF Module**: NRF24L01 for long-range communication.
- **Power Supply**: 12V battery pack with a 5V regulator for Raspberry Pi.

### Software
- **Operating System**: Raspberry Pi OS (latest, 32-bit or 64-bit).
- **Python**: Version 3.8 or higher.
- **Dependencies**: Listed in `requirements.txt` (e.g., `opencv-python`, `face_recognition`, `RPi.GPIO`, `picamera2`).
- **Pre-trained Models**: Caffe-based DNN model files (`models/dnn_prototxt.txt`, `models/dnn_caffemodel.caffemodel`), such as MobileNet-SSD or YOLOv3.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ashwinrajesh2005/TerraRecon.git
   cd TerraRecon
   ```

2. **Run Setup Script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   - Installs Python dependencies.
   - Creates `data/logs/` and `data/faces/` directories.
   - Initializes the SQLite database (`data/database.sqlite`).

3. **Add Pre-trained Model Files**:
   - Download a Caffe-compatible model (e.g., MobileNet-SSD) from [OpenCV DNN testdata](https://github.com/opencv/opencv_extra/tree/master/testdata/dnn).
   - Rename files to `dnn_prototxt.txt` and `dnn_caffemodel.caffemodel` and place them in `models/`.
   - Refer to `models/README.md` for detailed instructions.

4. **Configure RF Communication**:
   - Update `ALERT_APP_URL` in `src/config.py` with your server’s address (e.g., `http://192.168.1.100:8080/alert`).

## Hardware Setup

- Assemble the rover according to `docs/hardware_setup.md`.
- Connect components to Raspberry Pi GPIO pins:
  - Motors: GPIO 17, 27, 22, 23 (forward/backward), 18, 24 (enable).
  - Ultrasonic sensor: GPIO 25 (trigger), 8 (echo).
  - Camera, LIDAR, GPS, and RF module as specified.
- Test hardware connectivity:
  ```bash
  python scripts/test_hardware.py
  ```

## Usage

1. **Enroll Authorized Faces**:
   - Place images of authorized personnel in `data/faces/` (e.g., `john_doe.jpg`).
   - Run:
     ```bash
     python scripts/enroll_faces.py
     ```
   - Names are extracted from filenames (e.g., `john_doe.jpg` → "JohnDoe").

2. **Run Autonomous Surveillance**:
   ```bash
   python src/main.py
   ```
   - Initiates the rover’s main loop: navigation, obstacle avoidance, person detection, and threat alerts.
   - Press `Ctrl+C` to stop or `q` to close the video feed (if displayed on a monitor).

3. **Monitor Alerts**:
   - Unknown persons detected trigger alerts with base64-encoded images sent to `ALERT_APP_URL`.
   - Debug logs are saved in `data/logs/` for analysis.

4. **Run Tests**:
   ```bash
   python -m unittest discover tests/
   ```
   - Validates motor control, vision processing, and communication modules.

## Adding the Rover Image

To enhance the GitHub page with a visual of the TerraRecon rover:

1. **Add the Image**:
   - Place your rover image (e.g., `terracrecon_rover.jpg`) in the `images/` directory:
     ```bash
     mkdir images
     mv terracrecon_rover.jpg images/
     ```
   - Commit and push:
     ```bash
     git add images/terracrecon_rover.jpg
     git commit -m "Add TerraRecon rover image"
     git push
     ```

2. **Verify Image Display**:
   - The image is embedded in this README with:
     ```markdown
     <p align="center">
       <img src="images/terracrecon_rover.jpg" alt="TerraRecon Rover" width="600">
     </p>
     ```
   - The `width="600"` ensures a prominent yet balanced size, and `<p align="center">` centers the image with whitespace for visual clarity.

3. **Alternative: External Hosting**:
   - If the image doesn’t display or you prefer external hosting, upload it to a service like Imgur and update the Markdown:
     ```markdown
     <p align="center">
       <img src="https://i.imgur.com/your-image-link.jpg" alt="TerraRecon Rover" width="600">
     </p>
     ```

4. **Image Suggestions**:
   - Use a high-quality photo of the assembled rover or a 3D-rendered diagram showing the chassis, sensors, and tracks.
   - Recommended dimensions: ~800x600 pixels for clear rendering on GitHub.
   - If you need an image generated, provide a description (e.g., “3D-printed rover with LIDAR and camera on a rugged terrain”), and I can suggest a prompt for an AI image generation tool.

## Troubleshooting

- **Camera Not Working**: Ensure `picamera2` is installed (`pip install picamera2`) and the camera is properly connected to the Raspberry Pi camera port.
- **Model Loading Errors**: Verify `models/dnn_prototxt.txt` and `dnn_caffemodel.caffemodel` exist and match (e.g., both for MobileNet-SSD).
- **GPIO Issues**: Check wiring (see `docs/hardware_setup.md`) and run scripts with `sudo` if permission errors occur.
- **Alert Failures**: Confirm `ALERT_APP_URL` is correct and the server is accessible.
- Detailed troubleshooting is available in `docs/user_manual.md`.

## Contributing

We welcome contributions to enhance TerraRecon! To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request on GitHub.

Please include unit tests in `tests/` and update documentation in `docs/` for new features.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Authors

- Developed by students at SRM Institute of Science and Technology, Ramapuram.
- Contact: https://github.com/ashwinrajesh2005/TerraRecon.

## Acknowledgments

- Built using [Robot Operating System (ROS)](https://www.ros.org/), [OpenCV](https://opencv.org/), and [face_recognition](https://github.com/ageitgey/face_recognition).
- Inspired by advancements in autonomous robotics and AI-driven defense technologies.