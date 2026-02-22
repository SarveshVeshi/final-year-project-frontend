# HandSignify - Complete Dependencies Reference

## Overview
This document provides a comprehensive list of all dependencies used in the HandSignify project, including their versions, purposes, and links.

---

## 1. FRONTEND DEPENDENCIES

### 1.1 CSS Frameworks & UI Libraries

| Dependency | Version | Purpose | CDN Link |
|---|---|---|---|
| **Bootstrap** | 5.3.0 | Responsive grid system, navbar, modals, form controls | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css` |
| **Bootstrap JS** | 5.3.0 | Interactive components (dropdowns, modals, tooltips) | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js` |
| **Lucide Icons** | Latest | Modern SVG icons for buttons and UI elements | `https://unpkg.com/lucide@latest` |

### 1.2 Real-Time Communication

| Dependency | Version | Purpose | CDN Link |
|---|---|---|---|
| **Socket.IO Client** | 4.5.4 | WebSocket communication for live camera feed & sign recognition | `https://cdn.socket.io/4.5.4/socket.io.min.js` |

### 1.3 Browser Native APIs (No Installation Required)

| API | Purpose | Supported Browsers |
|---|---|---|
| **Web Speech API** | Speech recognition & text-to-speech synthesis | Chrome 25+, Edge 79+ |
| **WebRTC (getUserMedia)** | Camera access & video streaming | All modern browsers |
| **Canvas API** | Image processing & rendering | All modern browsers |
| **Fetch API** | Asynchronous HTTP requests | All modern browsers |
| **LocalStorage** | Client-side data persistence | All modern browsers |
| **WebSocket** | Real-time bidirectional communication | All modern browsers |

### 1.4 CSS & Styling Files (Custom)

| File | Location | Purpose |
|---|---|---|
| main.css | `/static/main.css` | Global styles, CSS variables, base elements |
| modern_style.css | `/static/modern_style.css` | Modern design system |
| sign_generator.css | `/static/sign_generator.css` | Converter-specific styles |
| video_styles.css | `/static/video_styles.css` | Camera/video component styling |
| premium_ui.css | `/static/premium_ui.css` | Alternative premium theme (legacy) |

### 1.5 JavaScript Modules (Custom)

| File | Location | Purpose |
|---|---|---|
| main.js | `/static/main.js` | Main application logic & initialization |
| camera-controller.js | `/static/camera-controller.js` | Camera stream management |
| feature-utils.js | `/static/feature-utils.js` | Utility functions & text processing |
| realtime-interaction.js | `/static/realtime-interaction.js` | Socket.IO event handling |
| voice-sign.js | `/static/voice-sign.js` | Speech recognition integration |
| sign-voice.js | `/static/sign-voice.js` | Speech synthesis wrapper |
| premium-animations.js | `/static/premium-animations.js` | Loading animations & transitions |

---

## 2. BACKEND PYTHON DEPENDENCIES

### 2.1 Flask Web Framework (8 packages)

| Package | Version | Purpose | Docs |
|---|---|---|---|
| **Flask** | 3.0.3 | Core web framework, routing, templating | https://flask.palletsprojects.com/ |
| **Flask-Cors** | 4.0.0 | Cross-Origin Resource Sharing support | https://flask-cors.readthedocs.io/ |
| **Flask-SQLAlchemy** | 3.1.1 | Database ORM integration | https://flask-sqlalchemy.palletsprojects.com/ |
| **Flask-Login** | 0.6.3 | User authentication & session management | https://flask-login.readthedocs.io/ |
| **Flask-WTF** | 1.2.1 | Form handling & CSRF protection | https://flask-wtf.readthedocs.io/ |
| **Flask-Bcrypt** | 1.0.1 | Password hashing & security | https://github.com/maxcountryman/flask-bcrypt |
| **Flask-Mail** | 0.9.1 | Email functionality (password reset, verification) | https://pythonhosted.org/Flask-Mail/ |
| **flask-socketio** | 5.3.6 | WebSocket support via Socket.IO | https://python-socketio.readthedocs.io/ |

### 2.2 Machine Learning & Computer Vision (3 packages)

| Package | Version | Purpose | Docs |
|---|---|---|---|
| **OpenCV-Python** | 4.8.0.74 | Image processing, MJPEG streaming, video capture | https://docs.opencv.org/ |
| **MediaPipe** | 0.10.32 | Hand landmark detection (21-point pose estimation) | https://developers.google.com/mediapipe |
| **scikit-learn** | 1.5.2 | Random Forest classifier for sign classification | https://scikit-learn.org/ |

### 2.3 Data Science & Computation (2 packages)

| Package | Version | Purpose | Docs |
|---|---|---|---|
| **NumPy** | 1.26.4 | Numerical operations for landmark processing | https://numpy.org/ |
| **Matplotlib** | 3.8.4 | Data visualization (backend only) | https://matplotlib.org/ |

### 2.4 WebSocket & Async Communication (3 packages)

| Package | Version | Purpose | Docs |
|---|---|---|---|
| **python-socketio** | 5.11.4 | Server-side Socket.IO protocol | https://python-socketio.readthedocs.io/ |
| **python-engineio** | 4.9.0 | Engine.IO protocol (Socket.IO transport layer) | https://python-engineio.readthedocs.io/ |
| **eventlet** | 0.35.2 | Async I/O (optional, only if SOCKETIO_ASYNC_MODE=eventlet) | https://eventlet.net/ |

### 2.5 Forms & Validation (2 packages)

| Package | Version | Purpose | Docs |
|---|---|---|---|
| **WTForms** | 3.1.2 | Form creation & validation | https://wtforms.readthedocs.io/ |
| **email-validator** | 2.1.0.post1 | Email validation for forms | https://github.com/JoshData/python-email-validator |

### 2.6 HTTP & Network (1 package)

| Package | Version | Purpose | Docs |
|---|---|---|---|
| **Requests** | 2.32.3 | HTTP client library for API calls | https://requests.readthedocs.io/ |

---

## 3. PYTHON VERSION COMPATIBILITY

### Tested & Supported Versions

```
✅ Python 3.10 - Recommended (Primary development target)
✅ Python 3.11 - Recommended (Stable, well-tested)
✅ Python 3.12 - Supported (Latest features)
❌ Python 3.9  - Not tested (might work with modifications)
❌ Python 2.7  - Not supported (EOL)
```

### Version Notes

- **Python 3.10+** required for full type hints support
- **MediaPipe** requires Python 3.7+
- **OpenCV-Python** requires Python 3.5+
- **NumPy 1.26.4** is the last version supporting Python 3.10; use NumPy 2.0+ for Python 3.12

---

## 4. DEPENDENCY DEPENDENCY TREE

```
Flask (3.0.3)
├── Werkzeug (≥2.3)
├── Jinja2 (≥3.0)
├── click (≥8.1)
├── itsdangerous (≥2.0)
└── importlib-metadata (≥3.6) [Python < 3.10]

Flask-SQLAlchemy (3.1.1)
├── SQLAlchemy (≥2.0)
└── Flask (≥2.3)

flask-socketio (5.3.6)
├── python-socketio (≥5.0.0)
├── Flask (≥0.9)
└── eventlet (≥0.30.0) [optional]

python-socketio (5.11.4)
├── python-engineio (≥4.0.0)
├── aiofiles (for async support)
└── msgpack (for binary protocol)

scikit-learn (1.5.2)
├── NumPy (≥1.19.5)
├── SciPy (≥1.6.0)
├── joblib (≥1.2.0)
└── threadpoolctl (≥3.1.0)

MediaPipe (0.10.32)
├── NumPy (≥1.19.3)
├── absl-py (≥0.47)
├── attrs (≥19.3.0)
├── flatbuffers (≥1.12)
├── matplotlib (≥3.3)
├── protobuf (≥3.20)
└── OpenCV-Python (≥4.5.1) [optional]

OpenCV-Python (4.8.0.74)
├── NumPy (≥1.21.2)
└── libglib2.0-0 [system dependency on Linux]

WTForms (3.1.2)
├── MarkupSafe (≥2.0)
└── typing-extensions [Python < 3.10]
```

---

## 5. INSTALLATION COMMANDS

### Install All Dependencies (Production)

```bash
# Create virtual environment
python -m venv venv_stable

# Activate virtual environment
# Windows:
venv_stable\Scripts\activate
# Linux/Mac:
source venv_stable/bin/activate

# Install from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list
```

### Install Individual Dependencies

```bash
# Flask & Extensions
pip install Flask==3.0.3 Flask-Cors==4.0.0 Flask-SQLAlchemy==3.1.1

# Machine Learning
pip install opencv-python==4.8.0.74 mediapipe==0.10.32 scikit-learn==1.5.2

# WebSocket
pip install flask-socketio==5.3.6 python-socketio==5.11.4

# Forms & Validation
pip install WTForms==3.1.2 email-validator==2.1.0.post1
```

### Development Setup

```bash
# With all extras including type hints
pip install -r requirements.txt
pip install mypy black flake8  # Optional: dev tools
```

---

## 6. VERSION PINNING & COMPATIBILITY

### Why Exact Versions?

- **Reproducibility**: Ensures consistent behavior across environments
- **Stability**: Prevents breaking changes from minor/patch updates
- **Testing**: All versions have been tested together
- **Security**: Verifies no known vulnerabilities in pinned versions

### Updating Dependencies Safely

```bash
# Check for outdated packages
pip list --outdated

# Update specific package (test thoroughly first)
pip install --upgrade Flask==3.1.0

# Generate updated requirements
pip freeze > requirements.txt
```

---

## 7. OPTIONAL DEPENDENCIES

### Conditional Installation

| Condition | Package | Version | Installation |
|---|---|---|---|
| If using eventlet async | eventlet | 0.35.2 | `pip install eventlet==0.35.2` |
| Production WSGI server | gunicorn | 21.2.0 | `pip install gunicorn==21.2.0` |

### Enable Eventlet (Optional)

```bash
# Set environment variable
export SOCKETIO_ASYNC_MODE=eventlet  # Linux/Mac
set SOCKETIO_ASYNC_MODE=eventlet     # Windows

# Or add to .env file
echo "SOCKETIO_ASYNC_MODE=eventlet" >> .env
```

---

## 8. TROUBLESHOOTING COMMON DEPENDENCY ISSUES

### Issue: MediaPipe Installation Fails

**Solution**: Install build tools first
```bash
# Windows
pip install --upgrade pip setuptools wheel
pip install mediapipe==0.10.32

# Linux
sudo apt-get install build-essential python3-dev
pip install mediapipe==0.10.32
```

### Issue: Flask-SocketIO Connection Issues

**Solution**: Ensure Python ≥ 3.10
```bash
python --version
# If < 3.10, upgrade Python and create new venv
```

### Issue: NumPy Version Conflict

**Solution**: Check compatibility
```bash
pip install --upgrade numpy==1.26.4
# Or for Python 3.12+:
pip install numpy==2.0.0
```

### Issue: OpenCV Requires System Libraries

**Solution**: Install system dependencies
```bash
# Ubuntu/Debian
sudo apt-get install libsm6 libxext6 libxrender-dev

# macOS
brew install opencv

# Windows (usually automatic via wheel)
pip install opencv-python==4.8.0.74
```

---

## 9. SECURITY CONSIDERATIONS

### Dependency Scanning

```bash
# Check for known vulnerabilities
pip install safety
safety check

# Generate SBOM (Software Bill of Materials)
pip install pip-audit
pip-audit
```

### Recommendations

- ✅ Keep dependencies updated (run `pip install --upgrade -r requirements.txt` monthly)
- ✅ Use virtual environments to isolate dependencies
- ✅ Pin exact versions in requirements.txt
- ✅ Review security advisories for critical packages
- ⚠️ Avoid installing from unnamed/untrusted sources

---

## 10. DEPLOYMENT REQUIREMENTS

### Minimum for Production

```bash
Flask==3.0.3
Flask-Cors==4.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
Flask-Bcrypt==1.0.1
flask-socketio==5.3.6
python-socketio==5.11.4
opencv-python==4.8.0.74
mediapipe==0.10.32
scikit-learn==1.5.2
numpy==1.26.4
WTForms==3.1.2
email-validator==2.1.0.post1
requests==2.32.3
```

### Docker Deployment Requirements

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

---

## 11. DEPENDENCY LICENSES

| Package | License | Note |
|---|---|---|
| Flask | BSD-3-Clause | Open source |
| Bootstrap | MIT | Open source |
| OpenCV | Apache 2.0 | Open source |
| MediaPipe | Apache 2.0 | Open source, requires attribution |
| scikit-learn | BSD-3-Clause | Open source |
| NumPy | BSD-3-Clause | Open source |
| WTForms | BSD-3-Clause | Open source |
| Requests | Apache 2.0 | Open source |
| Socket.IO | MIT | Open source |

---

## 12. VERSION RELEASE HISTORY

```
Project: HandSignify
Created: February 2026
Last Updated: February 22, 2026

Flask: 3.0.3 (Released Jan 2024)
MediaPipe: 0.10.32 (Released Sep 2023)
scikit-learn: 1.5.2 (Released June 2024)
Bootstrap: 5.3.0 (Released Aug 2023)
Socket.IO: 4.5.4 (Released Dec 2022)
```

---

## 13. SUPPORT & DOCUMENTATION

### Quick Links

- **Requirements.txt**: [/requirements.txt](requirements.txt)
- **Frontend Report**: [FRONTEND_REPORT.md](FRONTEND_REPORT.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Setup Guide**: [SETUP.md](SETUP.md)

### Getting Help

1. Check dependency version: `pip show package-name`
2. Check package documentation links in table above
3. Common issues section (Section 8)
4. GitHub issues: https://github.com/SarveshVeshi/final-year-project-frontend

---

**Report Generated**: February 22, 2026  
**Last Updated**: February 22, 2026  
**Total Dependencies Documented**: 24 Python packages + Unlimited Browser APIs
