#!/usr/bin/env python3
"""
Check what's using port 8000 and fix it
"""
import subprocess
import socket
import sys

def check_port_8000():
    print("🔍 Checking port 8000...")
    
    # Check if port is available
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 8000))
            print("✅ Port 8000 is available")
            return True
    except OSError:
        print("❌ Port 8000 is in use")
        return False

def find_port_users():
    print("\n🔍 Finding processes using port 8000...")
    try:
        if sys.platform == "win32":
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            for line in lines:
                if ':8000' in line:
                    print(f"Found: {line.strip()}")
        else:
            result = subprocess.run(['lsof', '-i', ':8000'], capture_output=True, text=True)
            print(result.stdout)
    except Exception as e:
        print(f"Error checking processes: {e}")

def kill_port_8000():
    print("\n🔧 Attempting to free port 8000...")
    try:
        if sys.platform == "win32":
            # Kill all python processes
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True)
            print("✅ Killed Python processes")
            
            # Kill specific processes using port 8000
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            for line in lines:
                if ':8000' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        try:
                            subprocess.run(['taskkill', '/f', '/pid', pid], 
                                         capture_output=True, check=True)
                            print(f"✅ Killed process {pid}")
                        except:
                            pass
        else:
            subprocess.run(['pkill', '-f', ':8000'], capture_output=True)
            subprocess.run(['pkill', '-f', 'uvicorn'], capture_output=True)
            print("✅ Killed processes using port 8000")
    except Exception as e:
        print(f"Error killing processes: {e}")

def main():
    print("🔧 AeroCast Port Checker & Fixer")
    print("=" * 40)
    
    if check_port_8000():
        print("\n🎉 Port 8000 is ready! You can start the server now.")
        print("Run: python start_server.py")
    else:
        find_port_users()
        kill_port_8000()
        
        # Check again
        print("\n🔄 Checking port again...")
        if check_port_8000():
            print("\n🎉 Port 8000 is now free! You can start the server.")
            print("Run: python start_server.py")
        else:
            print("\n⚠️ Port 8000 is still busy. Try:")
            print("1. Restart your computer")
            print("2. Use a different port: python -m uvicorn api.main:app --port 8080")
            print("3. Check for other web servers running")

if __name__ == "__main__":
    main()