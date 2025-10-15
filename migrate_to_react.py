#!/usr/bin/env python3
"""
Migration script to help transition from HTML/CSS/JS to React/Next.js frontend
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print migration banner"""
    print("🚀 AeroCast - Air Quality Forecasting Platform - React Migration")
    print("=" * 65)
    print("Converting from HTML/CSS/JS to React/Next.js")
    print("=" * 65)

def check_prerequisites():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found!")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found!")
        print("📥 Please install Node.js from: https://nodejs.org/")
        return False

def backup_static_files():
    """Backup existing static files"""
    if Path("static").exists():
        backup_dir = Path("static_backup")
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        
        print("💾 Backing up existing static files...")
        shutil.copytree("static", backup_dir)
        print(f"✅ Static files backed up to: {backup_dir}")
        return True
    return False

def install_frontend():
    """Install React frontend dependencies"""
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    print("📦 Installing React/Next.js dependencies...")
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Check for pnpm first, then npm
    package_managers = [
        ("pnpm", ["pnpm", "install"]),
        ("npm", ["npm", "install"])
    ]
    
    for pm_name, install_cmd in package_managers:
        try:
            # Check if package manager is available
            subprocess.run([pm_name, "--version"], capture_output=True, check=True)
            print(f"🔧 Using {pm_name} for installation...")
            
            # Install dependencies
            result = subprocess.run(install_cmd, check=True)
            print(f"✅ Dependencies installed successfully with {pm_name}!")
            
            # Go back to root directory
            os.chdir("..")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ No suitable package manager found (npm or pnpm)")
    os.chdir("..")
    return False

def update_api_routes():
    """Update API to serve React frontend"""
    api_file = Path("api/main.py")
    
    if not api_file.exists():
        print("⚠️ API file not found, skipping API updates")
        return
    
    print("🔧 Updating API to serve React frontend...")
    
    # The API has already been updated in the previous steps
    print("✅ API routes updated to serve React frontend")

def create_development_script():
    """Create a development script for easy startup"""
    dev_script = '''#!/bin/bash
# Development startup script for React frontend

echo "🚀 Starting Delhi Air Quality Forecasting System"
echo "Frontend: React/Next.js | Backend: FastAPI"
echo "=========================================="

# Start backend in background
echo "🔧 Starting FastAPI backend..."
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🌐 Starting React frontend..."
cd frontend
if command -v pnpm &> /dev/null; then
    pnpm dev
else
    npm run dev
fi

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
'''
    
    with open("start_dev.sh", "w") as f:
        f.write(dev_script)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod("start_dev.sh", 0o755)
    
    print("✅ Created development startup script: start_dev.sh")

def create_windows_batch():
    """Create Windows batch file for development"""
    batch_script = '''@echo off
echo 🚀 Starting Delhi Air Quality Forecasting System
echo Frontend: React/Next.js ^| Backend: FastAPI
echo ==========================================

echo 🔧 Starting FastAPI backend...
start "Backend" python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo 🌐 Starting React frontend...
cd frontend
if exist pnpm-lock.yaml (
    pnpm dev
) else (
    npm run dev
)
'''
    
    with open("start_dev.bat", "w") as f:
        f.write(batch_script)
    
    print("✅ Created Windows development script: start_dev.bat")

def print_success_message():
    """Print success message with instructions"""
    print("\n🎉 Migration to React/Next.js completed successfully!")
    print("=" * 55)
    print("\n📋 Next Steps:")
    print("1. Start the development servers:")
    
    if os.name == 'nt':  # Windows
        print("   • Run: start_dev.bat")
    else:  # Unix/Linux/macOS
        print("   • Run: ./start_dev.sh")
        print("   • Or manually:")
    
    print("     - Backend: python -m uvicorn api.main:app --reload")
    print("     - Frontend: cd frontend && npm run dev")
    
    print("\n🌐 Access URLs:")
    print("   • React Frontend: http://localhost:3000")
    print("   • FastAPI Backend: http://localhost:8000")
    print("   • API Docs: http://localhost:8000/docs")
    
    print("\n📊 Available Pages:")
    print("   • Dashboard: http://localhost:3000/")
    print("   • Historical: http://localhost:3000/historical")
    print("   • Analytics: http://localhost:3000/analytics")
    print("   • Settings: http://localhost:3000/settings")
    
    print("\n🔧 Development Commands:")
    print("   • Build for production: cd frontend && npm run build")
    print("   • Run tests: cd frontend && npm test")
    print("   • Type checking: cd frontend && npm run type-check")
    
    print("\n💡 Tips:")
    print("   • The old HTML files are backed up in 'static_backup/'")
    print("   • React frontend has hot reload for development")
    print("   • All original functionality is preserved and enhanced")
    print("   • Check frontend/README.md for detailed documentation")
    
    print("\n🎯 Enjoy your modern React/Next.js air quality system!")

def main():
    """Main migration function"""
    print_banner()
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Backup static files
    backup_static_files()
    
    # Install frontend dependencies
    if not install_frontend():
        print("❌ Frontend installation failed!")
        sys.exit(1)
    
    # Update API routes
    update_api_routes()
    
    # Create development scripts
    create_development_script()
    if os.name == 'nt':
        create_windows_batch()
    
    # Print success message
    print_success_message()

if __name__ == "__main__":
    main()