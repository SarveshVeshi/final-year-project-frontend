# HandSignify — AI-Powered Sign Language Detection

A web application that detects and translates American Sign Language (ASL) gestures in real time using computer vision and machine learning.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Project Purpose](#project-purpose)
- [Tech Stack](#tech-stack)
- [Architecture Overview](#architecture-overview)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running Locally](#running-locally)
- [API Routes](#api-routes)
- [WebSocket](#websocket)
- [Model Usage](#model-usage)
- [Reproducibility](#reproducibility)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)

---

## Problem Statement

Deaf and hard-of-hearing individuals face communication barriers in daily interactions. Real-time sign language recognition can bridge this gap by converting hand gestures into text and speech, enabling more inclusive communication without specialized hardware.

---

## Project Purpose

HandSignify provides:

- **Real-time ASL detection** via webcam using MediaPipe and a Random Forest classifier
- **User authentication** with secure login, registration, and password reset
- **Sign-to-text converter** for translating gestures into typed text
- **Sign-to-video generator** for converting text into skeletal sign animations
- **Voice integration** for text-to-speech output of recognized signs

---

## Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Backend     | Flask, Flask-SocketIO, SQLAlchemy    |
| Frontend    | HTML5, Vanilla CSS, JavaScript       |
| ML/CV       | MediaPipe, OpenCV, scikit-learn      |
| Auth        | Flask-Login, Flask-Bcrypt            |
| Database    | SQLite                               |

---

## Architecture Overview

```
┌─────────────┐     HTTP/WS      ┌─────────────┐     ┌──────────────┐
│   Browser   │ ◄──────────────► │   Flask     │ ◄──►│  MediaPipe   │
│  (Webcam)   │                  │   app.py    │     │  + RF Model  │
└─────────────┘                  └─────────────┘     └──────────────┘
                                        │
                                        ▼
                                ┌──────────────┐
                                │   SQLite DB  │
                                └──────────────┘
```

- **Flask** serves pages and REST endpoints
- **Flask-SocketIO** streams real-time predictions to the client
- **MediaPipe** extracts hand landmarks; **Random Forest** classifies gestures
- **SQLite** stores user accounts

---

## Folder Structure

```
.
├── app.py                 # Main Flask app & entry point
├── manage_server.py       # Start/stop server utility
├── server.bat             # Windows start/stop script
├── run.bat                # Direct run (foreground)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
│
├── models/                # ML model storage (see models/README.md)
├── scripts/               # Training & data collection
│   ├── train_classifier.py
│   ├── collect_imgs.py
│   └── create_dataset.py
│
├── services/              # Business logic
│   └── sign_service.py    # Sign video generation
│
├── static/                # CSS, JS, images, videos
├── templates/             # Jinja2 HTML templates
├── data/                  # Training images (gitignored)
└── instance/              # SQLite DB (gitignored)
```

---

## Installation

### Prerequisites

- Python 3.10 or 3.11 (3.13 supported; 3.11 recommended for stability)
- Webcam

### Steps

```powershell
# Clone
git clone https://github.com/SarveshVeshi/final-year-project-version-2.git
cd final-year-project-version-2

# Virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac

# Dependencies
pip install -r requirements.txt

# Environment
copy .env.example .env     # Windows
# cp .env.example .env     # Linux/Mac
# Edit .env with your SECRET_KEY and MAIL_* credentials

# Train model (required before first run)
python scripts/train_classifier.py
```

---

## Environment Setup

Copy `.env.example` to `.env` and set:

| Variable       | Description                    | Required |
|----------------|--------------------------------|----------|
| SECRET_KEY     | Flask secret (e.g. random 32 chars) | Yes      |
| MAIL_USERNAME  | SMTP email                     | For password reset |
| MAIL_PASSWORD  | SMTP app password              | For password reset |
| DATABASE_URL   | Override DB path               | No       |

---

## Running Locally

### Option 1: Server script (recommended)

```powershell
.\server.bat start   # Start in background
.\server.bat stop    # Stop
```

### Option 2: Direct run

```powershell
.\.venv\Scripts\activate
python app.py
```

Open **http://127.0.0.1:5000**

---

## API Routes

| Method | Route                    | Description                    |
|--------|--------------------------|--------------------------------|
| GET    | /                        | Home / welcome                 |
| GET    | /feed                    | Camera feed page               |
| GET    | /sign-text-converter     | Sign-to-text tool              |
| GET    | /voice-converter         | Voice input tool               |
| GET    | /sign-language           | Sign language reference        |
| POST   | /generate_sign_video_api | Generate sign video from text  |
| GET/POST | /login                 | Login                          |
| GET/POST | /register              | Registration                   |
| GET/POST | /logout                | Logout                         |
| GET/POST | /dashboard             | User dashboard                 |
| GET    | /video_feed             | MJPEG camera stream            |
| POST   | /shutdown               | Graceful shutdown (localhost)  |

---

## WebSocket

Flask-SocketIO provides real-time prediction streaming.

- **Namespace:** `/`
- **Events emitted:**
  - `prediction` — Per-frame gesture predictions
  - `stable_prediction` — Prediction after stability threshold
- **Events received:**
  - `disconnect` — Client disconnect (releases camera)

Default async mode is **threading** (stable on Windows/Flask 3.x). Set `SOCKETIO_ASYNC_MODE=eventlet` in `.env` for eventlet (requires compatible dependency set).

---

## Model Usage

- **Input:** 42-dimensional hand landmark features from MediaPipe
- **Output:** Class labels (A–Z, Hello, Thank You, I Love you, etc.)
- **Storage:** `models/model.p` (pickle; generated by `scripts/train_classifier.py`)
- **Training:** See `models/README.md` and `scripts/train_classifier.py`

---

## Reproducibility

### Required Python Version

- **3.10** or **3.11** (recommended)
- **3.12** supported
- **3.13** supported with threading mode (some packages may need alternate versions)

### Supported Operating Systems

- Windows 10+
- macOS 10.15+
- Linux (Ubuntu 20.04+, Fedora, etc.)

### Hardware Requirements

| Resource | Minimum |
|----------|---------|
| **CPU** | x64; no GPU required |
| **RAM** | 4 GB |
| **Webcam** | Required for real-time detection |
| **Disk** | ~500 MB (including dependencies and model) |

### Known Issues

- **sklearn version mismatch:** Model trained with scikit-learn 1.3.0; runtime 1.5+ may show `InconsistentVersionWarning`. Inference still works.
- **Flask 3 + eventlet:** Use `async_mode='threading'` (default) on Flask 3.x to avoid session setter errors.
- **Windows port binding:** If port 5000 fails, check firewall or use a different port in `app.py`.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Model file not found` | Train model: `scripts/collect_imgs.py` → `create_dataset.py` → `train_classifier.py` |
| Port already in use | Change port in `app.py` or stop the other process |
| Camera not detected | Ensure webcam is connected and not in use by another app |
| Import errors on startup | Run `python scripts/verify_environment.py` to diagnose |

See `SETUP.md` for detailed setup steps.

---

## Known Limitations

- Model must be trained before first run (`scripts/train_classifier.py`)
- Single camera stream; concurrent users share one feed
- ASL-focused; limited to trained vocabulary
- Password reset requires valid SMTP configuration

---

## Future Improvements

- [ ] Multi-user camera sessions
- [ ] Expand gesture vocabulary
- [ ] Export sessions to text/transcript
- [ ] Mobile-responsive UI
- [ ] Docker deployment

---

## License

Educational / academic use.

---

© 2026 HandSignify
