import cv2
import mediapipe as mp
import numpy as np
import time
from flask import Flask, Response, jsonify
from flask_cors import CORS

# Explicitly import mediapipe submodules
from mediapipe.solutions import hands as mp_hands
from mediapipe.solutions import drawing_utils as mp_drawing
from mediapipe.solutions import drawing_styles as mp_drawing_styles

app = Flask(__name__)
CORS(app) # Allow main app to reach us

# Global state
latest_prediction = "None"
camera_busy = False

def get_camera():
    # Use CAP_DSHOW for fastest startup on Windows
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap

def generate_frames():
    global latest_prediction, camera_busy
    
    if camera_busy:
        return
    camera_busy = True

    try:
        cap = get_camera()
        if not cap.isOpened():
            yield b"Error: Could not open camera."
            return

        # MediaPipe Hands setup
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

            while True:
                success, frame = cap.read()
                if not success:
                    break

                # Process MediaPipe
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                prediction = "None"
                if results.multi_hand_landmarks:
                    prediction = "Hand Detected" # Replace with actual model prediction if available
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                
                latest_prediction = prediction

                # Encode frame
                ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                # Small sleep to yield CPU
                time.sleep(0.01)

    finally:
        if 'cap' in locals():
            cap.release()
        camera_busy = False

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/prediction')
def get_prediction():
    return jsonify({'prediction': latest_prediction})

if __name__ == '__main__':
    print("Camera Engine Server Starting on Port 5001...")
    # NOTE: We use threaded=True so multiple browser instances don't block each other
    app.run(host='127.0.0.1', port=5001, threaded=True, debug=False)
