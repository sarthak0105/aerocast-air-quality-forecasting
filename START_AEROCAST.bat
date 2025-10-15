@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║    🌬️  AeroCast Air Quality Forecasting System            ║
echo ║                                                              ║
echo ║    Double-click this file to start your website             ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Starting AeroCast...
echo.

REM Kill any existing processes on port 8000
echo 🧹 Cleaning up any existing processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Stopping process %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo 🔧 Starting server...
echo 📁 Working directory: %CD%
echo.

REM Start the server
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo 🛑 Server stopped.
pause