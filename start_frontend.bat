@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║    🎨 AeroCast Frontend Server                              ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📁 Starting frontend server...
echo 🌐 Frontend will be available at: http://localhost:8080
echo.
echo Available pages:
echo   • http://localhost:8080/index.html (Main Dashboard)
echo   • http://localhost:8080/historical.html (Historical Analysis)
echo   • http://localhost:8080/analytics.html (Analytics Dashboard)
echo   • http://localhost:8080/settings.html (Settings)
echo.
echo ⚠️  Note: API calls will fail since backend is not running
echo    The frontend will show 'System offline' status
echo.
echo Press Ctrl+C to stop the server
echo.

cd static
python -m http.server 8080