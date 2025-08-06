import time
import numpy as np
try:
    import RPi.GPIO as GPIO
    gpio_available = True
except (ImportError, RuntimeError):
    print("WARNING: RPi.GPIO not found or not running on Raspberry Pi. Simulating motor control.")
    gpio_available = False

# Import constants from config
from config import (
    MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD, MOTOR_RIGHT_FORWARD,
    MOTOR_RIGHT_BACKWARD, MOTOR_LEFT_ENABLE, MOTOR_RIGHT_ENABLE,
    ULTRASONIC_TRIG, ULTRASONIC_ECHO, MOTOR_SPEED, TURN_DURATION_S,
    OBSTACLE_DISTANCE_THRESHOLD_CM
)

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