# Agent Guide — HandSignify

For IDE code agents (e.g. Antigravity, Cursor, Copilot). Use this to analyze the project efficiently.

---

## Entry Point

**`app.py`** — Main application. Start here.

- Lines 1–70: Imports, Flask/SocketIO setup, config
- Lines 80–430: Routes (login, register, dashboard, API)
- Lines 430–440: SocketIO disconnect handler
- Lines 440–580: `generate_frames()` — camera + ML prediction loop
- Lines 598–618: `video_feed`, `shutdown`, `if __name__ == '__main__'`

---

## Key Files to Analyze First

| Order | File                 | Purpose                          |
|-------|----------------------|----------------------------------|
| 1     | `app.py`             | Entry point, routing, SocketIO   |
| 2     | `services/sign_service.py` | Sign video generation     |
| 3     | `manage_server.py`   | Server start/stop                |
| 4     | `scripts/train_classifier.py` | Model training          |

---

## Dependencies

Install with:

```bash
pip install -r requirements.txt
```

Core packages: `flask`, `flask-socketio`, `opencv-python`, `mediapipe`, `scikit-learn`.

---

## Things to Ignore

- **`data/`** — Training images (gitignored, large)
- **`instance/`** — SQLite DB (gitignored)
- **`static/generated_assets/`** — Generated videos (gitignored)
- **`*.mp4`, `*.p`, `*.pickle`** — Large binaries (gitignored)
- **`.venv/`** — Virtual environment
- **`STABILIZATION_REPORT.md`** — Internal notes; not essential for code analysis

---

## Known Constraints

1. **Model required:** `models/model.p` must exist. Train with `scripts/train_classifier.py`.
2. **Single camera:** One webcam stream at a time; disconnect releases it.
3. **Threading mode:** `async_mode='threading'` by default (not eventlet).
4. **Secrets:** `SECRET_KEY` and `MAIL_*` come from `.env`; no hardcoded credentials.

---

## Expected Runtime Behavior

- Server listens on `127.0.0.1:5000`
- Startup can take 10–15 seconds (MediaPipe/model load)
- WebSocket connects on page load; predictions stream in real time
- Graceful shutdown via `POST /shutdown` (localhost only)

---

## Important Configuration Flags

| Variable              | Default    | Effect                                |
|-----------------------|-----------|----------------------------------------|
| `SOCKETIO_ASYNC_MODE` | `threading` | Use `eventlet` only if deps support it |
| `SECRET_KEY`          | (required) | Flask session signing                  |
| `DATABASE_URL`        | sqlite default | Override DB path                   |
| `MAIL_*`              | (optional) | Required for password reset            |

---

## Quick Commands

```bash
python app.py                    # Run server
python manage_server.py start    # Start in background
python manage_server.py stop     # Stop
python scripts/train_classifier.py  # Train model
```
