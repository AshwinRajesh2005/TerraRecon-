from motor_control import setup_gpio, cleanup_gpio, move_forward, move_backward, turn_left, turn_right, check_obstacle
import time

def test_hardware():
    """Tests motor and sensor functionality."""
    print("Starting hardware tests...")
    setup_gpio()
    try:
        print("Testing forward movement...")
        move_forward()
        time.sleep(1)
        print("Testing backward movement...")
        move_backward()
        time.sleep(1)
        print("Testing left turn...")
        turn_left()
        time.sleep(1)
        print("Testing right turn...")
        turn_right()
        time.sleep(1)
        print("Testing obstacle detection...")
        if check_obstacle():
            print("Obstacle detected during test.")
        else:
            print("No obstacle detected during test.")
        print("Hardware tests completed.")
    finally:
        cleanup_gpio()

if __name__ == "__main__":
    test_hardware()