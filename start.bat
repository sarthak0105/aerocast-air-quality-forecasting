@echo off
echo 🚀 Starting AeroCast Server...
echo ================================

REM Change to script directory
cd /d "%~dp0"

REM Kill existing processes on port 8000
echo 🔍 Cleaning up port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Killing process %%a
    taskkill /f /pid %%a >nul 2>&1
)

REM Kill all python processes to be safe
taskkill /f /im python.exe >nul 2>&1

echo ✅ Port cleanup complete
echo.

REM Wait a moment
timeout /t 2 /nobreak >nul

echo 🌐 Starting server...
echo 📍 Server will be available at: http://localhost:8000
echo 📍 Press Ctrl+C to stop the server
echo.

REM Start the server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

pause