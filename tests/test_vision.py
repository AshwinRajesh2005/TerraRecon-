import unittest
import numpy as np
import cv2
from vision_processing import VisionProcessor

class TestVisionProcessing(unittest.TestCase):
    def setUp(self):
        self.vision_processor = VisionProcessor()
        # Create a dummy frame (640x480, BGR)
        self.test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.known_face_encodings = []
        self.known_face_names = []

    def test_load_dnn_model(self):
        # Check if model loading attempted (actual model files may not exist)
        self.assertIsNotNone(self.vision_processor.person_net, "DNN model should be initialized or None if files missing")
        # Note: Cannot fully test without actual model files

    def test_process_frame(self):
        frame, unknown_detected, alert_image = self.vision_processor.process_frame(
            self.test_frame, self.known_face_encodings, self.known_face_names
        )
        self.assertIsInstance(frame, np.ndarray)
        self.assertIsInstance(unknown_detected, bool)
        self.assertTrue(alert_image is None or isinstance(alert_image, str))

if __name__ == '__main__':
    unittest.main()