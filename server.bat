@echo off
if "%1"=="" goto usage
.\.venv\Scripts\python.exe manage_server.py %1
goto :eof

:usage
echo Usage: server [start^|stop]
echo.
echo Examples:
echo   server start  - Starts the HandSignify server
echo   server stop   - Stops the HandSignify server
