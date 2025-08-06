import unittest
from communication import send_alert
from config import ALERT_APP_URL

class TestCommunication(unittest.TestCase):
    def test_send_alert(self):
        # Use a dummy base64 string
        dummy_image = "data:image/jpeg;base64,/9j/4AAQSkZJRg=="
        # Cannot fully test without a valid ALERT_APP_URL
        if ALERT_APP_URL == "http://YOUR_ALERT_APP_IP:PORT/alert":
            print("WARNING: ALERT_APP_URL not configured. Skipping network test.")
            self.assertTrue(True)
        else:
            try:
                send_alert(dummy_image)
                self.assertTrue(True)
            except Exception as e:
                print(f"Alert test failed: {e}")
                self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()