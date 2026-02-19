# HandSignify — Setup Guide

Step-by-step setup for Windows, macOS, and Linux.

---

## Requirements

| Item | Requirement |
|------|-------------|
| **Python** | 3.10 or 3.11 (3.12 supported; 3.13 may need alternate dependencies) |
| **OS** | Windows 10+, macOS 10.15+, or Linux |
| **Webcam** | Required for real-time detection |

---

## 1. Clone the Repository

```bash
git clone https://github.com/SarveshVeshi/final-year-project-version-2.git
cd final-year-project-version-2
```

---

## 2. Create Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If execution policy blocks scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (Command Prompt)

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Environment Variables

Copy the example file and edit:

### Windows

```powershell
copy .env.example .env
notepad .env
```

### macOS / Linux

```bash
cp .env.example .env
nano .env
```

**Required variables:**

- `SECRET_KEY` — A random string (e.g. 32+ characters)
- `MAIL_USERNAME` — Your SMTP email (for password reset)
- `MAIL_PASSWORD` — SMTP app password

---

## 5. Train the Model (Required Before First Run)

The app needs `models/model.p`. You must either train it or obtain it:

```bash
# 1. Collect training images (requires webcam)
python scripts/collect_imgs.py

# 2. Create dataset from images
python scripts/create_dataset.py

# 3. Train and save model
python scripts/train_classifier.py
```

See `models/README.md` for details and alternatives.

---

## 6. Verify Environment

```bash
python scripts/verify_environment.py
```

Resolve any reported errors before running the app.

---

## 7. Run the Backend

### Option A: Direct run (foreground)

```bash
python app.py
```

### Option B: Background (Windows)

```powershell
.\server.bat start
# ...
.\server.bat stop
```

### Option C: Background (macOS / Linux)

```bash
# Start
nohup python app.py > server.log 2>&1 &

# Stop (or use manage_server.py)
python manage_server.py stop
```

Open **http://127.0.0.1:5000** in a browser.

---

## 8. Test the Health Endpoint

With the server running:

```bash
python test_health.py
```

Expected output includes:
- `imports_successful`
- `model_loaded_successfully` (if model exists)
- `database_found` or `database_not_found`
- `app_import_failed` if requests is missing (install via `pip install requests`)

---

## 9. WebSocket

Flask-SocketIO is used for real-time predictions.

- **Connection:** Automatic when the feed page loads
- **Namespace:** `/`
- **Events:** `prediction`, `stable_prediction`
- **Mode:** `threading` by default (no extra setup)

To use eventlet instead, set in `.env`:
```
SOCKETIO_ASYNC_MODE=eventlet
```
Requires compatible dependency versions (see `requirements_stable.txt`).

---

## Quick Reference

| Step | Command |
|------|---------|
| Activate venv (Win) | `.\.venv\Scripts\Activate.ps1` |
| Activate venv (Mac/Linux) | `source .venv/bin/activate` |
| Install deps | `pip install -r requirements.txt` |
| Verify | `python scripts/verify_environment.py` |
| Run server | `python app.py` |
| Test health | `python test_health.py` |
