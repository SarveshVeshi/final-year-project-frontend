# HandSignify — Architecture

A concise overview of how the system works.

---

## Backend Flow

```
Request → Flask → Route Handler → Response
                ↓
         [DB / Services / ML]
```

1. **HTTP:** Flask routes handle pages (render templates) and API endpoints (JSON).
2. **WebSocket:** Flask-SocketIO handles real-time events (predictions, disconnect).
3. **Database:** SQLAlchemy + SQLite for users (login, registration).

---

## Request Lifecycle

### Page Request (e.g. `/feed`)

1. Client requests `/feed`
2. Flask renders `feed.html` with Jinja2
3. Template loads JS that connects to SocketIO and requests `/video_feed`
4. `video_feed()` returns an MJPEG stream via `generate_frames()`
5. `generate_frames()` reads webcam → MediaPipe → model.predict() → emits via SocketIO
6. Client displays video and predictions

### WebSocket Flow

1. Client loads page → Socket.IO connects (namespace `/`)
2. Client requests `/video_feed` (MJPEG HTTP stream)
3. Server runs `generate_frames()` generator:
   - Reads frame from OpenCV
   - Runs MediaPipe hand detection
   - Extracts 42 landmarks, predicts with Random Forest
   - Emits `prediction` and `stable_prediction` via `socketio.emit()`
4. Client disconnects → `handle_disconnect()` releases camera

---

## SocketIO Handling

- **Mode:** `threading` (default) — avoids eventlet/Flask 3 session issues on Windows
- **Config:** `manage_session=False` to prevent session mutation errors
- **Camera:** Shared `cv2.VideoCapture` with `camera_lock`; released on disconnect

---

## ML Model Loading

1. At startup: `pickle.load(open('./models/model.p', 'rb'))` → `model_dict['model']`
2. Model is a scikit-learn `RandomForestClassifier`
3. Input shape: `(1, 42)` — flattened hand landmarks
4. Output: class label (string or int, mapped via `labels_dict`)

---

## Static File Handling

- **Directory:** `static/`
- **Contents:** CSS, JS, images, ASL reference images, generated videos
- **Served by:** Flask `url_for('static', filename='...')`
- **Generated assets:** `static/generated_assets/` — sign videos from `sign_service`

---

## Async Behavior

- **Threading:** Flask-SocketIO uses Python threads; no eventlet/gevent by default
- **Camera loop:** `generate_frames()` is a synchronous generator; each `yield` sends one MJPEG frame
- **SocketIO emit:** From within the generator, `socketio.emit()` pushes predictions to all connected clients

---

## Key Components

| Component      | File              | Role                              |
|----------------|-------------------|-----------------------------------|
| App entry      | `app.py`          | Flask app, routes, SocketIO       |
| Sign service   | `services/sign_service.py` | Generate sign videos      |
| Model          | `models/model.p`  | Trained Random Forest             |
| Server control | `manage_server.py`| Start/stop server process         |
