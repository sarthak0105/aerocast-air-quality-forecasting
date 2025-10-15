#!/usr/bin/env python3
"""
Start both backend API and React frontend together
"""

import os
import sys
import subprocess
import time
import threading
import signal
from pathlib import Path

class FullSystemStarter:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.project_root = Path(__file__).parent.parent
        
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🌬️  AeroCast Full System Startup                        ║
║                                                              ║
║    🚀 Backend API + React Frontend                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def check_prerequisites(self):
        """Check if all prerequisites are available"""
        print("🔍 Checking prerequisites...")
        
        # Check Python
        try:
            python_version = sys.version.split()[0]
            print(f"✅ Python {python_version}")
        except:
            print("❌ Python not found")
            return False
            
        # Check Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js {result.stdout.strip()}")
            else:
                print("❌ Node.js not found")
                return False
        except FileNotFoundError:
            print("❌ Node.js not found")
            return False
            
        # Check frontend directory
        frontend_dir = self.project_root / "frontend"
        if not frontend_dir.exists():
            print("❌ Frontend directory not found")
            return False
        print("✅ Frontend directory found")
        
        # Check if frontend dependencies are installed
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Installing frontend dependencies...")
            try:
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
                print("✅ Frontend dependencies installed")
            except subprocess.CalledProcessError:
                print("❌ Failed to install frontend dependencies")
                return False
        else:
            print("✅ Frontend dependencies already installed")
            
        return True
        
    def kill_existing_processes(self):
        """Kill any existing processes on ports 8000 and 3000"""
        print("🧹 Cleaning up existing processes...")
        
        ports = [8000, 3000]
        for port in ports:
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
                            print(f"✅ Killed process {pid} on port {port}")
                        except:
                            pass
                            
                    if pids:
                        time.sleep(2)  # Wait for processes to die
                        
            except Exception as e:
                print(f"⚠️  Error cleaning port {port}: {e}")
                
    def start_backend(self):
        """Start the FastAPI backend"""
        print("🚀 Starting backend API server...")
        
        try:
            cmd = [
                sys.executable, "-m", "uvicorn", 
                "api.main:app", 
                "--host", "127.0.0.1",
                "--port", "8000",
                "--reload"
            ]
            
            self.backend_process = subprocess.Popen(
                cmd, 
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            print("✅ Backend API starting on http://localhost:8000")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
            
    def start_frontend(self):
        """Start the React frontend"""
        print("⚛️  Starting React frontend...")
        
        try:
            frontend_dir = self.project_root / "frontend"
            
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            print("✅ React frontend starting on http://localhost:3000")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
            
    def wait_for_services(self):
        """Wait for both services to be ready"""
        print("⏳ Waiting for services to start...")
        
        # Wait for backend
        backend_ready = False
        for i in range(30):
            try:
                import requests
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    backend_ready = True
                    print("✅ Backend API is ready!")
                    break
            except:
                time.sleep(1)
                
        if not backend_ready:
            print("⚠️  Backend may still be starting...")
            
        # Wait a bit for frontend
        print("⏳ Frontend is starting (this may take a moment)...")
        time.sleep(5)
        print("✅ Frontend should be ready!")
        
    def print_access_info(self):
        """Print access information"""
        info = """
🎉 FULL SYSTEM READY!

🌐 ACCESS POINTS:

   ⚛️  REACT FRONTEND (Modern UI):
   → http://localhost:3000                    # Main Dashboard
   → http://localhost:3000/historical        # Historical Analysis
   → http://localhost:3000/analytics         # Analytics Dashboard
   → http://localhost:3000/settings          # Settings Page

   🌐 HTML FRONTEND (Alternative):
   → http://localhost:8000                    # Static HTML Dashboard
   → http://localhost:8000/static/historical.html
   → http://localhost:8000/static/analytics.html

   🔌 BACKEND API:
   → http://localhost:8000/docs               # API Documentation
   → http://localhost:8000/health             # Health Check

🎯 FEATURES READY:
   ✅ Real-time air quality predictions
   ✅ Interactive charts and visualizations
   ✅ Model status monitoring
   ✅ Location-based forecasting
   ✅ Historical data analysis
   ✅ Professional UI with React + TypeScript

🚀 RECOMMENDED:
   Start with the React frontend at http://localhost:3000
   for the best modern development experience!

Press Ctrl+C to stop both services.
        """
        print(info)
        
    def cleanup(self):
        """Clean up processes"""
        print("\n🛑 Shutting down services...")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend stopped")
            except:
                try:
                    self.frontend_process.kill()
                except:
                    pass
                    
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend stopped")
            except:
                try:
                    self.backend_process.kill()
                except:
                    pass
                    
        print("✅ All services stopped")
        
    def run(self):
        """Main execution"""
        self.print_banner()
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("❌ Prerequisites not met. Please install missing components.")
            return False
            
        # Clean up existing processes
        self.kill_existing_processes()
        
        # Start services
        if not self.start_backend():
            return False
            
        if not self.start_frontend():
            self.cleanup()
            return False
            
        # Wait for services
        self.wait_for_services()
        
        # Show access info
        self.print_access_info()
        
        # Wait for user interrupt
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()
            
        return True

def main():
    """Main entry point"""
    starter = FullSystemStarter()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        starter.cleanup()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    success = starter.run()
    if not success:
        print("❌ Failed to start full system")
        sys.exit(1)

if __name__ == "__main__":
    main()