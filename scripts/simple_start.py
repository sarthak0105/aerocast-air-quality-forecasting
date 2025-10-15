#!/usr/bin/env python3
"""
Simple, reliable start script for AeroCast
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def kill_existing_processes():
    """Kill any existing processes on port 8000"""
    try:
        # Find and kill processes on port 8000
        result = subprocess.run(
            'netstat -ano | findstr :8000',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            pids = set()
            
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        pids.add(pid)
            
            for pid in pids:
                try:
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)
                    print(f"✅ Stopped existing process {pid}")
                except:
                    pass
            
            if pids:
                time.sleep(2)
                print("🧹 Cleaned up existing processes")
    
    except Exception as e:
        print(f"⚠️  Note: {e}")

def start_server():
    """Start the AeroCast server"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🌬️  AeroCast Air Quality Forecasting System            ║
║                                                              ║
║    Starting your beautiful web interface...                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Clean up any existing processes
    kill_existing_processes()
    
    # Start the server
    print("🚀 Starting AeroCast server...")
    print("📁 Working directory:", os.getcwd())
    
    try:
        # Use localhost instead of 0.0.0.0 for Windows compatibility
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "127.0.0.1",  # Use localhost
            "--port", "8000",
            "--reload"
        ]
        
        print("🔧 Starting with command:", " ".join(cmd))
        
        # Start the server process
        process = subprocess.Popen(
            cmd, 
            cwd=Path.cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("⏳ Server starting...")
        
        # Wait a bit for server to start
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Server process started successfully!")
            
            # Show access information
            print(f"""
🎉 SUCCESS! AeroCast is now running!

🌐 OPEN THESE LINKS IN YOUR BROWSER:

   📊 Main Dashboard:
   http://localhost:8000

   📈 Historical Analysis:
   http://localhost:8000/static/historical.html

   📊 Analytics Dashboard:
   http://localhost:8000/static/analytics.html

   ⚙️  Settings Page:
   http://localhost:8000/static/settings.html

   📚 API Documentation:
   http://localhost:8000/docs

🎯 FEATURES:
   ✅ Beautiful air quality dashboard
   ✅ Interactive maps and charts
   ✅ Real-time predictions
   ✅ Historical data analysis
   ✅ Mobile-friendly design

💡 USAGE TIPS:
   • Click on different locations on the map
   • Press "Get Forecast" to see predictions
   • Try the different pages using the navigation
   • The system works with or without trained models

🔗 MAIN LINK: http://localhost:8000

Press Ctrl+C to stop the server when done.
            """)
            
            # Optionally open browser automatically
            try:
                print("🌐 Opening browser automatically...")
                webbrowser.open("http://localhost:8000")
            except:
                print("💡 Please open http://localhost:8000 in your browser manually")
            
            # Keep server running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down server...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print("✅ Server stopped successfully")
        else:
            # Process failed to start
            stdout, stderr = process.communicate()
            print("❌ Server failed to start!")
            print(f"Error output: {stderr}")
            print(f"Standard output: {stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def check_requirements():
    """Check if basic requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if we're in the right directory
    if not Path("api").exists() or not Path("static").exists():
        print("❌ Error: Please run this script from the AeroCast project root directory")
        print("   Make sure you can see 'api' and 'static' folders")
        return False
    
    # Check if main files exist
    if not Path("api/main.py").exists():
        print("❌ Error: api/main.py not found")
        return False
    
    if not Path("static/index.html").exists():
        print("❌ Error: static/index.html not found")
        return False
    
    print("✅ Basic requirements check passed")
    return True

def main():
    """Main entry point"""
    if not check_requirements():
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Make sure you're in the AeroCast project directory")
        print("   2. Check that 'api' and 'static' folders exist")
        print("   3. Try: cd path/to/AeroCast")
        sys.exit(1)
    
    success = start_server()
    
    if not success:
        print("\n❌ Failed to start AeroCast")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Check Python version: python --version")
        print("   3. Try running: python -m uvicorn api.main:app --host 127.0.0.1 --port 8000")
        sys.exit(1)

if __name__ == "__main__":
    main()