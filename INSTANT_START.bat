@echo off
echo 🚀 AeroCast Instant Start
echo ========================

REM Kill any existing python processes
taskkill /f /im python.exe >nul 2>&1

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

echo ⚡ Starting server on port 8000...
echo 📍 Open browser to: http://localhost:8000
echo.

REM Start server directly
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

pause