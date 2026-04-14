import cv2
import numpy as np
import time
import threading
import pyttsx3
import dlib
from scipy.spatial import distance
from tensorflow.keras.models import load_model
from alerts import send_alert

# ================= VOICE ENGINE =================
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak_async(text):
    def speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=speak, daemon=True).start()

# ================= LOAD MODEL =================
model = load_model("models/drowsiness_model.h5")

IMG_SIZE = 128
CLASS_NAMES = ['Closed_Eyes', 'No_yawn', 'Open_Eyes', 'Yawn']

# ================= EAR SETUP =================
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

LEFT_EYE = list(range(36, 42))
RIGHT_EYE = list(range(42, 48))

EAR_THRESHOLD = 0.25
EAR_FRAMES = 20
ear_counter = 0

# ================= ALERT COOLDOWN =================
last_alert_time = 0
ALERT_COOLDOWN = 10  # seconds

# ================= EAR FUNCTION =================
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# ================= MAIN FUNCTION =================
def detect_drowsiness():
    global ear_counter, last_alert_time

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ---------- ML PREDICTION ----------
        img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img, verbose=0)
        class_id = np.argmax(prediction)
        label = CLASS_NAMES[class_id]

        # ---------- EAR DETECTION ----------
        faces = detector(gray)

        for face in faces:
            shape = predictor(gray, face)
            shape = np.array([[shape.part(i).x, shape.part(i).y] for i in range(68)])

            leftEye = shape[LEFT_EYE]
            rightEye = shape[RIGHT_EYE]

            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            if ear < EAR_THRESHOLD:
                ear_counter += 1
            else:
                ear_counter = 0

            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # ---------- HYBRID DECISION ----------
        current_time = time.time()

        if (
            ear_counter > EAR_FRAMES
            and label in ["Closed_Eyes", "Yawn"]
            and current_time - last_alert_time > ALERT_COOLDOWN
        ):
            message = "⚠️ Driver drowsiness detected! Please take a break."

            send_alert(message)
            speak_async(message)

            last_alert_time = current_time
            ear_counter = 0

        # ---------- DISPLAY ----------
        cv2.putText(frame, f"State: {label}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Smart Driver Safety AI", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
