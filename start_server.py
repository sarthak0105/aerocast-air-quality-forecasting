#!/usr/bin/env python3
"""
AeroCast Server - Single Authentic Startup Method
Run this file to start the complete AeroCast application
"""
import os
import sys
import subprocess
import socket
import time
from pathlib import Path

def kill_port_processes(port):
    """Kill processes using the specified port"""
    print(f"🔍 Checking for processes on port {port}...")
    try:
        if os.name == 'nt':  # Windows
            # Find processes using the port
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            pids = []
            
            for line in lines:
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        pids.append(pid)
            
            # Kill the processes
            for pid in pids:
                try:
                    subprocess.run(['taskkill', '/f', '/pid', pid], 
                                 capture_output=True, check=True)
                    print(f"✅ Killed process {pid}")
                except:
                    pass
                    
            # Also try killing all python processes (safer approach)
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True)
        else:  # Unix/Linux/Mac
            subprocess.run(['pkill', '-f', f':{port}'], capture_output=True)
            subprocess.run(['pkill', '-f', 'uvicorn'], capture_output=True)
    except Exception as e:
        print(f"⚠️ Port cleanup warning: {e}")

def check_port_available(port):
    """Check if port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except:
        return False

def find_available_port(start_port=8000):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + 10):
        if check_port_available(port):
            return port
    return None

def main():
    print("🚀 Starting AeroCast Server...")
    print("=" * 50)
    
    # Set working directory to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print(f"📁 Working from: {project_root}")
    
    # Handle port conflicts
    target_port = 8000
    kill_port_processes(target_port)
    
    # Wait a moment for processes to die
    time.sleep(2)
    
    # Find available port
    if not check_port_available(target_port):
        print(f"⚠️ Port {target_port} still busy, finding alternative...")
        available_port = find_available_port(target_port)
        if available_port:
            target_port = available_port
            print(f"✅ Using port {target_port}")
        else:
            print("❌ No available ports found")
            return
    
    print("✅ Port ready")
    print(f"\n🌐 Starting FastAPI server on port {target_port}...")
    print(f"📍 AeroCast will be available at: http://localhost:{target_port}")
    print("📍 All pages accessible from main dashboard navigation")
    print("\n⚡ Server starting... Please wait...")
    print("=" * 50)
    
    try:
        # Start the server using uvicorn
        cmd = [
            sys.executable, '-m', 'uvicorn', 
            'api.main:app',
            '--host', '0.0.0.0',
            '--port', str(target_port),
            '--reload'
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Trying alternative startup method...")
        
        # Alternative method - direct uvicorn import
        try:
            import uvicorn
            uvicorn.run(
                "api.main:app",
                host="0.0.0.0",
                port=target_port,
                reload=False
            )
        except Exception as e2:
            print(f"❌ Alternative method failed: {e2}")
            print("\n🔧 Manual startup:")
            print(f"python -m uvicorn api.main:app --host 0.0.0.0 --port {target_port}")

if __name__ == "__main__":
    main()