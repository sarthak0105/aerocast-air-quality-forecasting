#!/usr/bin/env python3
"""
Enhanced deployment script for React/Next.js frontend conversion
"""
import os
import sys
import subprocess
import time
import json
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"🔧 Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Node.js
    try:
        result = run_command("node --version", check=False)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/")
            return False
    except:
        print("❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/")
        return False
    
    # Check npm/pnpm
    npm_available = False
    pnpm_available = False
    
    try:
        result = run_command("npm --version", check=False)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
            npm_available = True
    except:
        pass
    
    try:
        result = run_command("pnpm --version", check=False)
        if result.returncode == 0:
            print(f"✅ pnpm: {result.stdout.strip()}")
            pnpm_available = True
    except:
        pass
    
    if not npm_available and not pnpm_available:
        print("❌ Neither npm nor pnpm found. Please install Node.js.")
        return False
    
    return True

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("📦 Installing frontend dependencies...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    # Check if pnpm is available and pnpm-lock.yaml exists
    if Path("frontend/pnpm-lock.yaml").exists():
        try:
            run_command("pnpm --version", check=False)
            print("🔧 Using pnpm for installation...")
            run_command("pnpm install", cwd="frontend")
            return True
        except:
            print("⚠️ pnpm not available, falling back to npm...")
    
    # Use npm
    print("🔧 Using npm for installation...")
    run_command("npm install", cwd="frontend")
    return True

def build_frontend():
    """Build the React/Next.js frontend"""
    print("🏗️ Building React/Next.js frontend...")
    
    # Check if pnpm is available
    try:
        run_command("pnpm --version", check=False)
        if Path("frontend/pnpm-lock.yaml").exists():
            run_command("pnpm run build", cwd="frontend")
            return True
    except:
        pass
    
    # Use npm
    run_command("npm run build", cwd="frontend")
    return True

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    
    # Check if virtual environment exists
    venv_paths = ["venv", ".venv", "env"]
    python_cmd = "python"
    
    for venv_path in venv_paths:
        if Path(venv_path).exists():
            if os.name == 'nt':  # Windows
                python_cmd = f"{venv_path}\\Scripts\\python"
            else:  # Unix/Linux/macOS
                python_cmd = f"{venv_path}/bin/python"
            break
    
    # Install Python dependencies if requirements.txt exists
    if Path("requirements.txt").exists():
        print("📦 Installing Python dependencies...")
        run_command(f"{python_cmd} -m pip install -r requirements.txt")
    
    # Start the backend server
    print("🌐 Starting backend server on http://localhost:8000...")
    backend_process = subprocess.Popen([
        python_cmd, "-m", "uvicorn", "api.main:app", 
        "--host", "0.0.0.0", "--port", "8000", "--reload"
    ])
    
    return backend_process

def start_frontend():
    """Start the React/Next.js frontend"""
    print("🚀 Starting React/Next.js frontend...")
    
    # Check if pnpm is available
    try:
        run_command("pnpm --version", check=False)
        if Path("frontend/pnpm-lock.yaml").exists():
            print("🌐 Starting frontend server on http://localhost:3000...")
            frontend_process = subprocess.Popen([
                "pnpm", "run", "dev"
            ], cwd="frontend")
            return frontend_process
    except:
        pass
    
    # Use npm
    print("🌐 Starting frontend server on http://localhost:3000...")
    frontend_process = subprocess.Popen([
        "npm", "run", "dev"
    ], cwd="frontend")
    
    return frontend_process

def create_proxy_config():
    """Create a simple proxy configuration for development"""
    proxy_config = {
        "name": "air-quality-proxy",
        "version": "1.0.0",
        "description": "Proxy server for air quality app",
        "main": "proxy.js",
        "scripts": {
            "start": "node proxy.js"
        },
        "dependencies": {
            "http-proxy-middleware": "^2.0.6",
            "express": "^4.18.2",
            "cors": "^2.8.5"
        }
    }
    
    proxy_js = '''
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Enable CORS
app.use(cors());

// Serve static files from Next.js build
app.use(express.static(path.join(__dirname, 'frontend/.next/static')));

// Proxy API requests to FastAPI backend
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8000',
  changeOrigin: true,
  pathRewrite: {
    '^/api': '/api'
  }
}));

// Proxy health endpoint
app.use('/health', createProxyMiddleware({
  target: 'http://localhost:8000',
  changeOrigin: true
}));

// Serve Next.js app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/.next/server/pages/index.html'));
});

app.listen(PORT, () => {
  console.log(`🚀 Proxy server running on http://localhost:${PORT}`);
  console.log('📡 API requests proxied to http://localhost:8000');
  console.log('🌐 Frontend served from Next.js build');
});
'''
    
    # Write proxy configuration
    with open("proxy-package.json", "w") as f:
        json.dump(proxy_config, f, indent=2)
    
    with open("proxy.js", "w") as f:
        f.write(proxy_js)
    
    print("📝 Created proxy configuration files")

def main():
    """Main deployment function"""
    print("🎯 Delhi Air Quality Forecasting - React/Next.js Deployment")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed!")
        sys.exit(1)
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        print("❌ Frontend dependency installation failed!")
        sys.exit(1)
    
    # Build frontend
    try:
        build_frontend()
        print("✅ Frontend build completed successfully!")
    except Exception as e:
        print(f"⚠️ Frontend build failed: {e}")
        print("🔄 Continuing with development mode...")
    
    # Create proxy config
    create_proxy_config()
    
    print("\n🚀 Starting services...")
    print("=" * 40)
    
    # Start backend
    backend_process = start_backend()
    time.sleep(3)  # Give backend time to start
    
    # Start frontend
    frontend_process = start_frontend()
    time.sleep(2)  # Give frontend time to start
    
    print("\n✅ Deployment completed successfully!")
    print("=" * 50)
    print("🌐 Access your application:")
    print("   • Frontend (React/Next.js): http://localhost:3000")
    print("   • Backend API: http://localhost:8000")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("\n📊 Available Pages:")
    print("   • Dashboard: http://localhost:3000/")
    print("   • Historical: http://localhost:3000/historical")
    print("   • Analytics: http://localhost:3000/analytics")
    print("   • Settings: http://localhost:3000/settings")
    print("\n🎉 Your React/Next.js conversion is ready!")
    print("Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ All services stopped. Goodbye!")

if __name__ == "__main__":
    main()