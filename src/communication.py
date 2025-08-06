import requests
import time
from config import ALERT_APP_URL

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