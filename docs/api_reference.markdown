# TerraRecon API Reference

This document provides an overview of the key functions and classes in the TerraRecon project’s Python modules, located in the `src/` directory.

## src/motor_control.py
Handles motor control and ultrasonic sensor-based obstacle detection.

- **setup_gpio()**
  - **Description**: Initializes GPIO pins for motors and sensors.
  - **Parameters**: None
  - **Returns**: None
- **cleanup_gpio()**
  - **Description**: Cleans up GPIO settings, stopping motors.
  - **Parameters**: None
  - **Returns**: None
- **set_motor_speeds(left_speed, right_speed)**
  - **Description**: Sets motor speeds (positive for forward, negative for backward).
  - **Parameters**:
    - `left_speed` (float): Speed for left motors.
    - `right_speed` (float): Speed for right motors.
  - **Returns**: None
- **move_forward()**, **move_backward()**, **turn_left()**, **turn_right()**
  - **Description**: Controls rover movement.
  - **Parameters**: None
  - **Returns**: None
- **get_distance_cm()**
  - **Description**: Measures distance using ultrasonic sensor.
  - **Returns**: Distance in centimeters (float).
- **check_obstacle()**
  - **Description**: Checks for obstacles within threshold distance.
  - **Returns**: Boolean (True if obstacle detected).

## src/sensor_fusion.py
Manages sensor fusion for navigation.

- **SensorFusion** (class)
  - **__init__()**: Initializes LIDAR and ultrasonic data storage.
  - **update_lidar_data(point_cloud)**: Updates LIDAR point cloud.
    - **Parameters**: `point_cloud` (numpy array): 3D point cloud data.
  - **update_ultrasonic_data()**: Updates ultrasonic sensor data.
  - **fuse_sensors()**: Combines sensor data for obstacle detection.
    - **Returns**: Boolean (True if obstacle detected).
  - **get_navigation_decision()**: Returns navigation decision ("STOP" or "MOVE_FORWARD").

## src/vision_processing.py
Handles AI-based person and face detection.

- **VisionProcessor** (class)
  - **__init__()**: Initializes DNN model for person detection.
  - **load_dnn_model()**: Loads Caffe model from `models/`.
  - **process_frame(frame, known_face_encodings, known_face_names)**:
    - **Description**: Processes a frame for person and face detection.
    - **Parameters**:
      - `frame` (numpy array): Input video frame.
      - `known_face_encodings` (list): List of known face encodings.
      - `known_face_names` (list): List of names corresponding to encodings.
    - **Returns**:
      - Processed frame with annotations.
      - Boolean (True if unknown person detected).
      - Base64-encoded image for alerts (or None).

## src/communication.py
Manages RF-based alert communication.

- **send_alert(image_base64)**
  - **Description**: Sends an alert with a base64-encoded image to the configured URL.
  - **Parameters**:
    - `image_base64` (str): Base64-encoded image data.
  - **Returns**: None

## src/config.py
Defines configuration constants.

- **Constants**:
  - Motor and sensor pins (e.g., `MOTOR_LEFT_FORWARD`, `ULTRASONIC_TRIG`).
  - Motor control parameters (e.g., `MOTOR_SPEED`, `TURN_DURATION_S`).
  - Camera settings (e.g., `CAMERA_RESOLUTION`).
  - Model paths (e.g., `DNN_MODEL_PROTOTXT`).
  - Database and alert settings (e.g., `DATABASE_PATH`, `ALERT_APP_URL`).

## Usage
Import these modules in `src/main.py` or scripts to control the rover. Example:
```python
from motor_control import move_forward, check_obstacle
from vision_processing import VisionProcessor
```

See `docs/user_manual.md` for detailed usage instructions.