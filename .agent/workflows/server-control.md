---
description: How to start and stop the HandSignify server
---

### Standard Control (Recommended)
You can now use simple commands from the project root:

1. **Start the Server**:
   ```powershell
   ./server start
   ```
   *This starts the server in the background and prevents duplicate instances.*

2. **Stop the Server**:
   ```powershell
   ./server stop
   ```
   *This gracefully shuts down the server and frees up the port.*

### Legacy Control
1. **Direct Run**:
   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```
2. **Batch File**: Double-click `run.bat`.
3. **Manual Stop**: Press `Ctrl + C` in the terminal window.
