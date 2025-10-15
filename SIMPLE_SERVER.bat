@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║    🌐 AeroCast Simple Server                               ║
echo ║                                                              ║
echo ║    Using Python's built-in HTTP server                      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if static directory exists
if not exist "static" (
    echo ❌ Error: 'static' directory not found!
    echo    Make sure you're in the AeroCast project directory
    pause
    exit /b 1
)

echo ✅ Found static directory
echo 📁 Serving files from static folder
echo.

REM Kill any existing processes on port 8000
echo 🧹 Cleaning up port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo 🚀 Starting simple HTTP server on port 8000...
echo.
echo 🌐 Your website will be available at:
echo    http://localhost:8000
echo.
echo ✨ FEATURES:
echo    ✅ Beautiful web interface
echo    ✅ All HTML pages work
echo    ✅ CSS styling applied
echo    ✅ Interactive maps
echo    ✅ No complex setup needed
echo.
echo Press Ctrl+C to stop the server
echo.

REM Change to static directory and start server
cd static
python -m http.server 8000

echo.
echo 🛑 Server stopped.
pause