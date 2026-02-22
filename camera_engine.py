import cv2
import numpy as np
import pickle
import time
import socket
import json
from datetime import datetime

# Standard mediapipe imports
import mediapipe as mp
from mediapipe.solutions import hands as mp_hands
from mediapipe.solutions import drawing_utils as mp_drawing
from mediapipe.solutions import drawing_styles as mp_drawing_styles

# Load the model
try:
    with open('models/model.p', 'rb') as f:
        model_dict = pickle.load(f)
    model = model_dict['model']
    print(f"Engine: Model loaded successfully. Classes: {len(model_dict.get('labels_dict', {}))}")
except Exception as e:
    print(f"Engine Error loading model: {e}")
    model = None

def run_engine():
    print("Camera Engine: Initializing CV2...")
    # Use CAP_DSHOW for faster startup/MJPEG on Windows
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("CRITICAL ERROR: Could not open camera.")
        return

    hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)
    
    # Setup UDP socket to stream JPEGs to Flask
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    flask_address = ('127.0.0.1', 5555)
    
    # TCP socket for predictions
    pred_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pred_address = ('127.0.0.1', 5556)

    print("Camera Engine Running!")
    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue
            
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        predicted_character = None
        try:
            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing_styles.get_default_hand_landmarks_style(),
                                              mp_drawing_styles.get_default_hand_connections_style())
                
                data_aux = []
                x_ = []
                y_ = []
                
                for i in range(len(hand_landmarks.landmark)):
                    x_.append(hand_landmarks.landmark[i].x)
                    y_.append(hand_landmarks.landmark[i].y)
                    
                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))
                    
                input_data = np.asarray(data_aux).reshape(1, -1)
                if model:
                    prediction = model.predict(input_data)
                    predicted_label = prediction[0]
                    predicted_character = str(predicted_label)
                    # Mapping to letter omitted for brevity, will send raw label
                    
                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10
                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
                                
        except Exception as e:
            pass
            
        # Compress aggressively to fit in UDP packet (64KB limit)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
        # Resize to guarantee fit
        small_frame = cv2.resize(frame, (480, 360))
        ret_encode, buffer = cv2.imencode('.jpg', small_frame, encode_param)
        
        if ret_encode:
            frame_bytes = buffer.tobytes()
            # UDP packet size is limited to 65507 bytes.
            if len(frame_bytes) < 65000:
                try:
                    sock.sendto(frame_bytes, flask_address)
                except Exception as e:
                    pass
            
            # Send prediction if exists
            if predicted_character:
                try:
                    pred_sock.sendto(predicted_character.encode('utf-8'), pred_address)
                except Exception:
                    pass
                    
        time.sleep(0.01)

if __name__ == '__main__':
    run_engine()
