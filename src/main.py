import asyncio
import platform
import time
import sys
import os
import sqlite3
import argparse
import base64
import io
import numpy as np
import cv2
import face_recognition
import requests
from PIL import Image

try:
    import RPi.GPIO as GPIO
    gpio_available = True
except (ImportError, RuntimeError):
    print("WARNING: RPi.GPIO library not found or not running on Raspberry Pi.")
    print("Motor and Sensor functions will be simulated.")
    gpio_available = False

try:
    from picamera2 import Picamera2
    picamera_available = True
except ImportError:
    print("WARNING: Picamera2 library not found. Camera functions will be simulated.")
    picamera_available = False

# Constants
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 27
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 23
MOTOR_LEFT_ENABLE = 18
MOTOR_RIGHT_ENABLE = 24
ULTRASONIC_TRIG = 25
ULTRASONIC_ECHO = 8
MOTOR_SPEED = 0.5
TURN_DURATION_S = 0.5
OBSTACLE_DISTANCE_THRESHOLD_CM = 30
CAMERA_RESOLUTION = (640, 480)
DNN_MODEL_PROTOTXT = "models/dnn_prototxt.txt"
DNN_MODEL_CAFFEMODEL = "models/dnn_caffemodel.caffemodel"
DATABASE_PATH = "data/database.sqlite"
ALERT_APP_URL = "http://YOUR_ALERT_APP_IP:PORT/alert"
FACE_DETECTION_MODEL = "cnn"

# Global Variables
person_net = None
picam2 = None
KNOWN_FACE_ENCODINGS = []
KNOWN_FACE_NAMES = []

def setup_gpio():
    """Sets up GPIO pins for motors and sensors."""
    if not gpio_available:
        print("SIMULATION: Skipping GPIO setup.")
        return
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        motor_pins = [
            MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD,
            MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD,
            MOTOR_LEFT_ENABLE, MOTOR_RIGHT_ENABLE
        ]
        for pin in motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        GPIO.setup(ULTRASONIC_TRIG, GPIO.OUT)
        GPIO.setup(ULTRASONIC_ECHO, GPIO.IN)
    except Exception as e:
        print(f"ERROR during GPIO setup: {e}")
        raise

def cleanup_gpio():
    """Cleans up GPIO settings."""
    if not gpio_available:
        print("SIMULATION: Skipping GPIO cleanup.")
        return
    print("Cleaning up GPIO...")
    try:
        stop_motors()
        GPIO.cleanup()
        print("GPIO cleanup finished.")
    except Exception as e:
        print(f"Error during GPIO cleanup: {e}")

def set_motor_speeds(left_speed, right_speed):
    """Sets motor speeds. Positive for forward, negative for backward."""
    if not gpio_available:
        print(f"SIMULATION: Setting motor speeds: left={left_speed}, right={right_speed}")
        return
    GPIO.output(MOTOR_LEFT_FORWARD, left_speed > 0)
    GPIO.output(MOTOR_LEFT_BACKWARD, left_speed < 0)
    GPIO.output(MOTOR_LEFT_ENABLE, abs(left_speed) > 0)
    GPIO.output(MOTOR_RIGHT_FORWARD, right_speed > 0)
    GPIO.output(MOTOR_RIGHT_BACKWARD, right_speed < 0)
    GPIO.output(MOTOR_RIGHT_ENABLE, abs(right_speed) > 0)

def move_forward():
    """Moves the rover forward."""
    print("Moving forward")
    set_motor_speeds(MOTOR_SPEED, MOTOR_SPEED)

def move_backward():
    """Moves the rover backward."""
    print("Moving backward")
    set_motor_speeds(-MOTOR_SPEED, -MOTOR_SPEED)

def turn_left():
    """Turns the rover left."""
    print("Turning left")
    set_motor_speeds(-MOTOR_SPEED, MOTOR_SPEED)
    time.sleep(TURN_DURATION_S)
    stop_motors()

def turn_right():
    """Turns the rover right."""
    print("Turning right")
    set_motor_speeds(MOTOR_SPEED, -MOTOR_SPEED)
    time.sleep(TURN_DURATION_S)
    stop_motors()

def stop_motors():
    """Stops all motors."""
    print("Stopping motors")
    set_motor_speeds(0, 0)

def get_distance_cm():
    """Measures distance using ultrasonic sensor."""
    if not gpio_available:
        print("SIMULATION: Returning random distance for testing.")
        return np.random.uniform(10, 100)
    try:
        GPIO.output(ULTRASONIC_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(ULTRASONIC_TRIG, False)
        start_time = time.time()
        while GPIO.input(ULTRASONIC_ECHO) == 0:
            start_time = time.time()
        while GPIO.input(ULTRASONIC_ECHO) == 1:
            end_time = time.time()
        duration = end_time - start_time
        distance = (duration * 34300) / 2  # Speed of sound in cm/s
        return distance
    except Exception as e:
        print(f"Error measuring distance: {e}")
        return float('inf')

def check_obstacle():
    """Checks for obstacles within threshold distance."""
    distance = get_distance_cm()
    if distance < OBSTACLE_DISTANCE_THRESHOLD_CM:
        print(f"Obstacle DETECTED at {distance:.1f} cm")
        return True
    return False

def load_dnn_model():
    """Loads the DNN model for person detection."""
    global person_net
    try:
        if os.path.exists(DNN_MODEL_PROTOTXT) and os.path.exists(DNN_MODEL_CAFFEMODEL):
            person_net = cv2.dnn.readNetFromCaffe(DNN_MODEL_PROTOTXT, DNN_MODEL_CAFFEMODEL)
        else:
            print("ERROR: Model files not found")
            print(f"Expected: {DNN_MODEL_PROTOTXT}")
            print(f"Expected: {DNN_MODEL_CAFFEMODEL}")
            person_net = None
    except cv2.error as e:
        print(f"ERROR loading person detection model: {e}")
        person_net = None

def load_known_faces_from_db():
    """Loads known face encodings and names from SQLite database."""
    global KNOWN_FACE_ENCODINGS, KNOWN_FACE_NAMES
    KNOWN_FACE_ENCODINGS = []
    KNOWN_FACE_NAMES = []
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, face_encoding FROM registered_personnel")
        rows = cursor.fetchall()
        for row in rows:
            name, encoding_blob = row
            encoding = np.frombuffer(encoding_blob, dtype=np.float64)
            if encoding.shape == (128,):
                KNOWN_FACE_NAMES.append(name)
                KNOWN_FACE_ENCODINGS.append(encoding)
            else:
                print(f"Warning: Invalid encoding for {name}")
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def setup_database_for_enrollment():
    """Creates the database table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registered_personnel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                face_encoding BLOB NOT NULL UNIQUE,
                image_filename TEXT
            )
        """)
        conn.commit()
        print(f"Database {DATABASE_PATH} checked/created")
        return conn
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def enroll_single_face(db_conn, image_path, name):
    """Enrolls a single face into the database."""
    try:
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1, model='cnn')
        if not face_locations:
            print(f"ERROR: No face found in {os.path.basename(image_path)}. Skipping.")
            return False
        if len(face_locations) > 1:
            print(f"WARNING: Multiple faces ({len(face_locations)}) found in {os.path.basename(image_path)}. Using the largest one.")
            def face_area(loc):
                top, right, bottom, left = loc
                return (bottom - top) * (right - left)
            face_locations = [max(face_locations, key=face_area)]
        face_encoding = face_recognition.face_encodings(image, face_locations)[0]
        encoding_blob = face_encoding.tobytes()
        cursor = db_conn.cursor()
        cursor.execute(
            "INSERT INTO registered_personnel (name, face_encoding, image_filename) VALUES (?, ?, ?)",
            (name, encoding_blob, os.path.basename(image_path))
        )
        db_conn.commit()
        print(f"Successfully enrolled {name} from {os.path.basename(image_path)}")
        return True
    except sqlite3.IntegrityError:
        print(f"INFO: This exact face encoding might already exist for {name} or another person. Skipping.")
        return False
    except FileNotFoundError:
        print(f"ERROR: Image file not found: {image_path}")
        return False
    except Exception as e:
        print(f"ERROR processing image {os.path.basename(image_path)}: {e}")
        return False

def process_frame_for_persons_and_faces(frame):
    """Processes a frame for person and face detection."""
    h, w = frame.shape[:2]
    if h == 0 or w == 0:
        print("Warning: Received empty frame")
        return frame, False, None
    try:
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        person_net.setInput(blob)
        detections = person_net.forward()
        unknown_detected_in_frame = False
        alert_image = None
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = box.astype("int")
                person_roi = frame[startY:endY, startX:endX]
                if person_roi.size == 0:
                    continue
                rgb_roi = cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_roi, model=FACE_DETECTION_MODEL)
                if face_locations:
                    face_encodings = face_recognition.face_encodings(rgb_roi, face_locations)
                    face_names_in_roi = []
                    roi_contains_unknown = False
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(KNOWN_FACE_ENCODINGS, face_encoding)
                        name = "Unknown"
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = KNOWN_FACE_NAMES[first_match_index]
                        else:
                            roi_contains_unknown = True
                            unknown_detected_in_frame = True
                        face_names_in_roi.append(name)
                    for (top, right, bottom, left), name in zip(face_locations, face_names_in_roi):
                        top_abs, right_abs, bottom_abs, left_abs = top + startY, right + startX, bottom + startY, left + startX
                        color = (0, 0, 255) if name == "Unknown" else (255, 0, 0)
                        cv2.rectangle(frame, (left_abs, top_abs), (right_abs, bottom_abs), color, 2)
                        cv2.rectangle(frame, (left_abs, bottom_abs - 20), (right_abs, bottom_abs), color, cv2.FILLED)
                        cv2.putText(frame, name, (left_abs, bottom_abs - 5), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    if roi_contains_unknown and alert_image is None:
                        pil_img = Image.fromarray(rgb_roi)
                        buf = io.BytesIO()
                        pil_img.save(buf, format="JPEG", quality=85)
                        alert_image = base64.b64encode(buf.getvalue()).decode()
        return frame, unknown_detected_in_frame, alert_image
    except Exception as e:
        print(f"Error processing frame: {e}")
        return frame, False, None

def send_alert(image_base64):
    """Sends an alert with image to the specified URL."""
    try:
        payload = {
            'message': 'ALERT: Unknown person detected by rover unit',
            'timestamp': time.time(),
            'image_base64': image_base64
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(ALERT_APP_URL, json=payload, headers=headers)
        response.raise_for_status()
        print("Alert sent successfully.")
    except requests.RequestException as e:
        print(f"Network error sending alert: {e}")
    except Exception as e:
        print(f"Error preparing or sending alert: {e}")

async def initialize_rover():
    """Initializes rover systems."""
    print("Initializing Rover Systems...")
    setup_gpio()
    load_dnn_model()
    load_known_faces_from_db()
    global picam2
    if picamera_available:
        try:
            picam2 = Picamera2()
            cam_config = picam2.create_still_configuration(main={"size": CAMERA_RESOLUTION})
            picam2.configure(cam_config)
            picam2.start()
            print("Camera initialized successfully.")
            return True
        except Exception as e:
            print(f"ERROR: Failed to initialize camera: {e}")
            picam2 = None
            return False
    else:
        print("Camera disabled (picamera2 library not found).")
        return False

async def run_rover_loop():
    """Main operational loop for the rover."""
    if not await initialize_rover():
        print("Rover initialization failed. Exiting.")
        return
    print("Starting Rover Surveillance Loop (Press Ctrl+C to stop)...")
    last_alert_sent_time = 0
    display_window_available = os.environ.get("DISPLAY") is not None
    try:
        while True:
            if check_obstacle():
                stop_motors()
                print("Obstacle detected! Maneuvering...")
                move_backward()
                time.sleep(0.5)
                stop_motors()
                if np.random.rand() < 0.5:
                    turn_left()
                else:
                    turn_right()
            else:
                move_forward()
            try:
                frame = picam2.capture_array("main")
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"Error capturing frame: {e}")
                time.sleep(0.5)
                continue
            processed_frame, unknown_found, alert_img = process_frame_for_persons_and_faces(frame_bgr)
            if unknown_found and (time.time() - last_alert_sent_time) > 10:
                if alert_img:
                    send_alert(alert_img)
                    last_alert_sent_time = time.time()
                    time.sleep(5)
            if display_window_available:
                try:
                    cv2.imshow("Rover View", processed_frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        print("Quit key pressed.")
                        break
                except cv2.error as e:
                    if "display" in str(e).lower():
                        print("Display window closed or unavailable. Disabling imshow.")
                        display_window_available = False
                    else:
                        print(f"cv2.imshow error: {e}")
            await asyncio.sleep(0.05)
    except KeyboardInterrupt:
        print("Ctrl+C detected. Initiating shutdown...")
    finally:
        print("Initiating shutdown sequence...")
        if picam2:
            print("Stopping camera...")
            picam2.stop()
        if display_window_available:
            print("Closing OpenCV windows...")
            cv2.destroyAllWindows()
        cleanup_gpio()
        print("Rover shutdown complete.")

async def main():
    """Main entry point for Pyodide compatibility."""
    await run_rover_loop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Defense Surveillance Rover")
    parser.add_argument("--enroll", action="store_true", help="Run the face enrollment process instead of the main rover loop")
    args = parser.parse_args()
    if args.enroll:
        run_enrollment_process()
    else:
        if not os.path.exists(DNN_MODEL_PROTOTXT) or not os.path.exists(DNN_MODEL_CAFFEMODEL):
            print("ERROR: Person detection model files are missing.")
            print(f"Ensure {DNN_MODEL_PROTOTXT} and {DNN_MODEL_CAFFEMODEL} exist.")
            sys.exit(1)
        if ALERT_APP_URL == "http://YOUR_ALERT_APP_IP:PORT/alert":
            print("WARNING: The ALERT_APP_URL is set to its default value.")
            print("Alerts will not be sent until this is configured correctly.")
            time.sleep(3)
        if platform.system() == "Emscripten":
            asyncio.ensure_future(main())
        else:
            asyncio.run(main())