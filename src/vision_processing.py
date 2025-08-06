import cv2
import numpy as np
import face_recognition
from PIL import Image
import io
import base64
from config import DNN_MODEL_PROTOTXT, DNN_MODEL_CAFFEMODEL, FACE_DETECTION_MODEL, CAMERA_RESOLUTION

class VisionProcessor:
    """Handles person and face detection using OpenCV and face_recognition."""
    def __init__(self):
        self.person_net = None
        self.load_dnn_model()

    def load_dnn_model(self):
        """Loads the DNN model for person detection."""
        try:
            if os.path.exists(DNN_MODEL_PROTOTXT) and os.path.exists(DNN_MODEL_CAFFEMODEL):
                self.person_net = cv2.dnn.readNetFromCaffe(DNN_MODEL_PROTOTXT, DNN_MODEL_CAFFEMODEL)
            else:
                print("ERROR: Model files not found")
                print(f"Expected: {DNN_MODEL_PROTOTXT}")
                print(f"Expected: {DNN_MODEL_CAFFEMODEL}")
                self.person_net = None
        except cv2.error as e:
            print(f"ERROR loading person detection model: {e}")
            self.person_net = None

    def process_frame(self, frame, known_face_encodings, known_face_names):
        """Processes a frame for person and face detection."""
        h, w = frame.shape[:2]
        if h == 0 or w == 0:
            print("Warning: Received empty frame")
            return frame, False, None
        try:
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.person_net.setInput(blob)
            detections = self.person_net.forward()
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
                            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                            name = "Unknown"
                            if True in matches:
                                first_match_index = matches.index(True)
                                name = known_face_names[first_match_index]
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