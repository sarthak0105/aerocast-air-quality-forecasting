#!/usr/bin/env python3
"""
Clean start script - kills existing processes and starts fresh
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def kill_processes_on_port(port):
    """Kill processes using the specified port"""
    try:
        # Find processes using the port
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
            
            # Kill the processes
            for pid in pids:
                try:
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)
                    print(f"✅ Killed process {pid}")
                except:
                    pass
                    
            if pids:
                time.sleep(2)  # Wait for processes to die
                print(f"🧹 Cleaned up {len(pids)} processes on port {port}")
            else:
                print(f"✅ Port {port} is already free")
        else:
            print(f"✅ Port {port} is free")
            
    except Exception as e:
        print(f"⚠️  Error cleaning port {port}: {e}")

def start_simple_server():
    """Start a simple working server"""
    print("🚀 Starting Air Quality Forecasting System...")
    
    # Kill any existing processes on port 8000
    kill_processes_on_port(8000)
    
    # Start the server
    try:
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "127.0.0.1",  # Use localhost only
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ]
        
        print("📁 Starting from directory:", os.getcwd())
        print("🔧 Command:", " ".join(cmd))
        
        # Start the process
        process = subprocess.Popen(cmd, cwd=Path.cwd())
        
        print("⏳ Server starting...")
        print("🌐 Once started, access at: http://localhost:8000")
        print("📊 Main dashboard: http://localhost:8000")
        print("📈 Historical: http://localhost:8000/static/historical.html")
        print("📊 Analytics: http://localhost:8000/static/analytics.html")
        print("⚙️  Settings: http://localhost:8000/static/settings.html")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop the server")
        
        # Wait for the process
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            print("✅ Server stopped")
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🌬️  Delhi Air Quality Forecasting System                ║
║                                                              ║
║    🧹 Clean Start - Fixing Port Issues                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    start_simple_server()