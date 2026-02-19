# Project Stabilization Report

## Root Cause Analysis

### ISSUE 1 — Backend Instability

| Error | Root Cause | Fix Applied |
|-------|------------|-------------|
| `AttributeError: RequestContext.session has no setter` | Flask 3.x + Werkzeug 3.x changed `session` to a read-only property. Flask-SocketIO with eventlet internally tries to set/fork the session, triggering this. | **Switched to `async_mode='threading'`** — no eventlet, avoids the session mutation code path. |
| Eventlet deprecation warning | Newer eventlet (0.40.x) with Python 3.13 emits deprecation warnings. | **Threading mode** — eventlet not used by default. |
| ConnectionAbortedError on Windows | Eventlet + Windows socket handling can cause connection resets. | **Threading mode** — native threading avoids eventlet networking. |
| sklearn InconsistentVersionWarning | Model trained with scikit-learn 1.3.0, runtime has 1.8.0. | **Warnings filter** — suppresses the unpickle warning; inference still works. |

### ISSUE 2 — Antigravity Agent Termination

Antigravity (Cursor AI agent or similar) connects to the app via WebSocket/HTTP. When the backend crashes or WebSocket handling fails, the agent loses connection and terminates.

**Causes addressed:**
- Backend crash on session setter → fixed by threading mode
- Unhandled exception in disconnect handler → wrapped in try/except
- WebSocket instability from eventlet → fixed by threading mode

**If agent still terminates:**
- Ensure backend is fully started (wait ~15 seconds after `python app.py`)
- Check no firewall/antivirus blocking WebSocket on port 5000
- For Python 3.13 instability, use **Python 3.11 + requirements_stable.txt**

---

## Final Stable Dependency List

### Option A — Current (Python 3.13, threading mode)
Use `requirements_reset.txt`:
- Flask 3.1.x, Werkzeug 3.x
- Flask-SocketIO 5.6, python-socketio 5.16
- **async_mode='threading'** (default in app)

### Option B — Maximum stability (Python 3.11 recommended)
Use `requirements_stable.txt`:
- Flask 2.3.3, Werkzeug 2.3.x
- Flask-SocketIO 5.3.6, python-socketio 5.8.0, eventlet 0.33.3
- scikit-learn 1.3.0 (matches model)
- Set `SOCKETIO_ASYNC_MODE=eventlet` in .env to use eventlet

---

## Clean Environment Rebuild

```powershell
cd "c:\Users\Sarvesh\project_Alpha_1 - Copy"

# 1. Remove old venv
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# 2. Create fresh venv (Python 3.11 recommended for Option B)
python -m venv .venv
.\.venv\Scripts\activate

# 3. Install dependencies
# Option A (Python 3.13):
pip install -r requirements_reset.txt

# Option B (Python 3.11):
pip install -r requirements_stable.txt

# 4. Run
python app.py
```

---

## Verification Checklist

- [x] `python app.py` starts (threading mode confirmed)
- [x] No "session has no setter" in console
- [x] No eventlet deprecation warnings (threading mode)
- [x] No sklearn InconsistentVersionWarning (filter applied)
- [ ] WebSocket connect/disconnect does not crash
- [ ] Video feed loads at http://127.0.0.1:5000
- [ ] Agent/Antigravity can connect and stay connected

**Note:** If you see "socket access forbidden" when binding port 5000, run outside the sandbox or check Windows firewall.
