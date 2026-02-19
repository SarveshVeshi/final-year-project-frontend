import sys
import os
import subprocess
import time
import requests
import socket
import signal

PID_FILE = ".server.pid"
PORT = 5000
HOST = "127.0.0.1"

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, port)) == 0

def start_server():
    if is_port_in_use(PORT):
        print(f"FAILED: Port {PORT} is already in use. Server may already be running.")
        return

    print("Starting HandSignify Server...")
    
    # Path to the virtual environment python
    venv_python = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        venv_python = "python" # Fallback

    # Start the server in a new detached process
    if os.name == 'nt':
        # Windows detached process
        DETACHED_PROCESS = 0x00000008
        process = subprocess.Popen(
            [venv_python, "app.py"],
            creationflags=DETACHED_PROCESS,
            close_fds=True
        )
    else:
        # Unix/Mac detached process
        process = subprocess.Popen(
            [venv_python, "app.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

    # Save PID
    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))

    # Wait for server to start (MediaPipe/TensorFlow take ~10-15 seconds to load)
    print("Waiting for server to initialize (this may take 10-15 seconds)...")
    time.sleep(15)
    if is_port_in_use(PORT):
        print("Server started successfully.")
        print(f"Access it at http://{HOST}:{PORT}")
    else:
        print("FAILED: Server did not start correctly.")
        print("Try running 'python app.py' directly to see error messages.")

def stop_server():
    if not is_port_in_use(PORT):
        print("Server is already stopped (Port 5000 is free).")
        # Clean up stale PID file if it exists
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        return

    print("Stopping HandSignify Server gracefully...")
    
    try:
        # 1. Try internal shutdown route
        response = requests.post(f"http://{HOST}:{PORT}/shutdown", timeout=5)
        if response.status_code == 200:
            print("Shutdown signal sent successfully.")
        else:
            print("Graceful shutdown route returned an error. Using system signals.")
            raise Exception("Internal shutdown failed")
    except Exception as e:
        # 2. Fallback to killing the process if route fails
        print(f"Graceful route failed: {e}. Using system fallback.")
        if os.path.exists(PID_FILE):
            with open(PID_FILE, "r") as f:
                try:
                    pid = int(f.read().strip())
                    if os.name == 'nt':
                        # Windows specific process termination
                        os.system(f"taskkill /F /PID {pid}")
                    else:
                        os.kill(pid, signal.SIGTERM)
                    print(f"Process {pid} terminated.")
                except ValueError:
                    print("Stale or invalid PID file.")
        else:
            # Final fallback: generic taskkill on windows if port is still occupied
            if os.name == 'nt':
                os.system(f"taskkill /F /IM python.exe /FI \"WINDOWTITLE eq *HandSignify*\"")
                print("Force-stopped server using taskkill.")

    # Verification loop
    max_retries = 5
    for i in range(max_retries):
        time.sleep(1)
        if not is_port_in_use(PORT):
            print("Server stopped successfully.")
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
            return
    
    print("WARNING: Server might still be closing background tasks. Port is still occupied.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_server.py [start|stop]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "start":
        start_server()
    elif command == "stop":
        stop_server()
    else:
        print(f"Unknown command: {command}")
        print("Valid commands: start, stop")
