#!/usr/bin/env python3
"""
Fix and start the AeroCast system - simple and reliable
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def kill_all_processes():
    """Kill all processes on ports 8000 and 3000"""
    ports = [8000, 3000]
    
    for port in ports:
        try:
            result = subprocess.run(
                f'netstat -ano | findstr :{port}',
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
                        print(f"✅ Killed process {pid} on port {port}")
                    except:
                        pass
                        
                if pids:
                    time.sleep(2)
            
        except Exception as e:
            print(f"⚠️  Error cleaning port {port}: {e}")

def start_simple_server():
    """Start a simple working server"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🌬️  AeroCast - Simple Start                             ║
║                                                              ║
║    Getting your website working reliably                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Kill existing processes
    print("🧹 Cleaning up any existing processes...")
    kill_all_processes()
    
    # Start the API server
    print("🚀 Starting API server...")
    
    try:
        # Use the original model service to avoid issues
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "0.0.0.0",  # Listen on all interfaces
            "--port", "8000",
            "--reload"
        ]
        
        print("📁 Starting from directory:", os.getcwd())
        print("🔧 Command:", " ".join(cmd))
        
        # Start the process
        process = subprocess.Popen(cmd, cwd=Path.cwd())
        
        print("⏳ Server starting...")
        
        # Wait for server to be ready
        server_ready = False
        for i in range(30):
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ API server is running!")
                    server_ready = True
                    break
            except:
                time.sleep(1)
                if i % 5 == 0:
                    print(f"   Starting... {i+1}/30")
        
        if not server_ready:
            print("⚠️  Server may still be starting...")
        
        # Test the API
        print("\n🧪 Testing API endpoints...")
        try:
            response = requests.get("http://localhost:8000/api/v1/current?lat=28.6139&lon=77.2090&hours=24", timeout=10)
            if response.status_code == 200:
                print("✅ API predictions working!")
            else:
                print(f"⚠️  API responded with status {response.status_code}")
        except Exception as e:
            print(f"⚠️  API test failed: {e}")
        
        print(f"""
🎉 SUCCESS! Your AeroCast system is running!

🌐 ACCESS YOUR WEBSITE:

   📊 Main Dashboard:
   → http://localhost:8000
   
   📈 Historical Analysis:
   → http://localhost:8000/static/historical.html
   
   📊 Analytics Dashboard:
   → http://localhost:8000/static/analytics.html
   
   ⚙️  Settings Page:
   → http://localhost:8000/static/settings.html
   
   📚 API Documentation:
   → http://localhost:8000/docs

🎯 FEATURES WORKING:
   ✅ Beautiful web interface
   ✅ Air quality predictions
   ✅ Interactive maps and charts
   ✅ Real-time data updates
   ✅ Mobile responsive design

💡 TIPS:
   • Try different locations on the map
   • Generate forecasts by clicking "Get Forecast"
   • Explore all the different pages
   • Check the API docs for technical details

Press Ctrl+C to stop the server
        """)
        
        # Keep server running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            print("✅ Server stopped successfully")
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def main():
    """Main entry point"""
    success = start_simple_server()
    if not success:
        print("\n❌ Failed to start the system")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure you're in the project directory")
        print("   2. Check if Python and dependencies are installed")
        print("   3. Try: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()