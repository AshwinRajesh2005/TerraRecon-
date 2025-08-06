# TerraRecon User Manual

This manual provides instructions for setting up, running, and operating the TerraRecon autonomous surveillance rover.

## Prerequisites
- **Hardware**: Assembled rover (see `docs/hardware_setup.md`).
- **Software**:
  - Raspberry Pi OS (latest version).
  - Python 3.8+.
  - Dependencies listed in `requirements.txt`.
  - Pre-trained model files in `models/` (see `models/README.md`).
- **Network**: Configured alert server URL in `src/config.py`.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TerraRecon.git
   cd TerraRecon
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python scripts/setup_database.py
   ```
4. Place model files (`dnn_prototxt.txt`, `dnn_caffemodel.caffemodel`) in `models/`.
5. Update `src/config.py` with the correct alert server URL.

## Running the Rover
1. **Test Hardware**:
   ```bash
   python scripts/test_hardware.py
   ```
   - Verifies motor and sensor functionality.
2. **Enroll Faces**:
   ```bash
   python scripts/enroll_faces.py
   ```
   - Place face images in `data/faces/` (e.g., `john_doe.jpg`).
   - Names are derived from filenames (e.g., `john_doe.jpg` → "JohnDoe").
3. **Run Main Loop**:
   ```bash
   python src/main.py
   ```
   - Starts autonomous surveillance, including navigation, person detection, and alerts.
   - Press `Ctrl+C` to stop.
   - If a display is available, press `q` to quit the video feed.

## Operation
- **Navigation**: The rover moves forward unless an obstacle is detected (within 30 cm), then it stops, moves backward, and turns randomly.
- **Threat Detection**: Detects persons using YOLO and identifies faces using `face_recognition`. Unknown faces trigger alerts sent to `ALERT_APP_URL`.
- **Logs**: Debug logs are stored in `data/logs/` (create this directory if missing).
- **Database**: Face encodings are stored in `data/database.sqlite`.

## Troubleshooting
- **No camera feed**: Ensure `picamera2` is installed and the camera is connected.
- **Model errors**: Verify `models/dnn_prototxt.txt` and `dnn_caffemodel.caffemodel` exist.
- **GPIO errors**: Check wiring and permissions (run with `sudo` if needed).
- **Alert failures**: Confirm `ALERT_APP_URL` is correct and the server is reachable.

## Safety Notes
- Ensure the rover operates in a safe environment to avoid collisions.
- Monitor battery levels to prevent unexpected shutdowns.
- Test in a controlled area before deploying in the field.