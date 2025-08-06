import sqlite3
import face_recognition
import os
from config import DATABASE_PATH

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

def run_enrollment_process(image_folder="data/faces"):
    """Enrolls faces from a folder of images."""
    db_conn = setup_database_for_enrollment()
    if not db_conn:
        print("Failed to set up database. Exiting.")
        return
    for filename in os.listdir(image_folder):
        if filename.endswith((".jpg", ".png")):
            image_path = os.path.join(image_folder, filename)
            base_name = os.path.splitext(filename)[0]
            name = ''.join(filter(str.isalpha, base_name.split('_')[0]))
            if not name:
                print(f"Could not extract a valid name from {filename}! Skipping.")
                continue
            enroll_single_face(db_conn, image_path, name)
    db_conn.close()

if __name__ == "__main__":
    run_enrollment_process()