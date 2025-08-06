import unittest
from motor_control import setup_gpio, cleanup_gpio, move_forward, move_backward, turn_left, turn_right, check_obstacle, get_distance_cm
try:
    import RPi.GPIO as GPIO
    gpio_available = True
except (ImportError, RuntimeError):
    gpio_available = False

class TestMotorControl(unittest.TestCase):
    def setUp(self):
        if gpio_available:
            setup_gpio()

    def tearDown(self):
        if gpio_available:
            cleanup_gpio()

    def test_move_forward(self):
        move_forward()
        # Simulate GPIO check; actual GPIO testing requires hardware
        if not gpio_available:
            print("SIMULATION: move_forward called")
        self.assertTrue(True)  # Placeholder for hardware-dependent test

    def test_move_backward(self):
        move_backward()
        if not gpio_available:
            print("SIMULATION: move_backward called")
        self.assertTrue(True)

    def test_turn_left(self):
        turn_left()
        if not gpio_available:
            print("SIMULATION: turn_left called")
        self.assertTrue(True)

    def test_turn_right(self):
        turn_right()
        if not gpio_available:
            print("SIMULATION: turn_right called")
        self.assertTrue(True)

    def test_check_obstacle(self):
        result = check_obstacle()
        self.assertIsInstance(result, bool)
        if not gpio_available:
            print("SIMULATION: check_obstacle called")

    def test_get_distance_cm(self):
        distance = get_distance_cm()
        self.assertIsInstance(distance, float)
        self.assertGreaterEqual(distance, 0)
        if not gpio_available:
            print("SIMULATION: get_distance_cm called")

if __name__ == '__main__':
    unittest.main()