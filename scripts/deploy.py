#!/usr/bin/env python3
"""
Deployment script for the air quality forecasting system
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking deployment requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or python_version.minor < 8:
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}")
    
    # Check if Docker is available
    try:
        subprocess.run(["docker", "--version"], check=True, 
                      capture_output=True, text=True)
        print("✅ Docker is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Docker not found (optional for local deployment)")
    
    # Check if required files exist
    required_files = [
        "requirements.txt",
        "api/main.py",
        "config/settings.py",
        "docker-compose.yml"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    commands = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install -r requirements.txt", "Installing Python dependencies")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        "models",
        "data",
        "logs",
        "forecasts",
        "static"
    ]
    
    print("\n📁 Setting up directories...")
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created/verified: {directory}")

def deploy_local():
    """Deploy locally using uvicorn"""
    print("\n🚀 Starting local deployment...")
    
    # Set environment variables
    os.environ["PYTHONPATH"] = str(Path.cwd())
    
    # Start the API server
    command = "python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"
    print(f"\n🌐 Starting API server...")
    print(f"Command: {command}")
    print(f"API will be available at: http://localhost:8000")
    print(f"Web interface: http://localhost:8000/static/index.html")
    print(f"API docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        subprocess.run(command, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")

def deploy_docker():
    """Deploy using Docker Compose"""
    print("\n🐳 Starting Docker deployment...")
    
    commands = [
        ("docker-compose build", "Building Docker images"),
        ("docker-compose up -d", "Starting containers")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("\n✅ Docker deployment completed!")
    print("🌐 API available at: http://localhost:8000")
    print("📊 Web interface: http://localhost:8000/static/index.html")
    print("📖 API docs: http://localhost:8000/docs")
    print("\nTo stop: docker-compose down")
    print("To view logs: docker-compose logs -f")
    
    return True

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running tests...")
    
    # Wait a moment for server to start
    import time
    time.sleep(3)
    
    test_command = "python scripts/test_api.py"
    return run_command(test_command, "Running API tests")

def main():
    parser = argparse.ArgumentParser(description="Deploy air quality forecasting system")
    parser.add_argument("--mode", choices=["local", "docker"], default="local",
                       help="Deployment mode")
    parser.add_argument("--skip-deps", action="store_true",
                       help="Skip dependency installation")
    parser.add_argument("--skip-tests", action="store_true",
                       help="Skip running tests")
    
    args = parser.parse_args()
    
    print("🚀 Air Quality Forecasting System Deployment")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Install dependencies
    if not args.skip_deps:
        if not install_dependencies():
            print("\n❌ Dependency installation failed.")
            sys.exit(1)
    
    # Deploy based on mode
    if args.mode == "local":
        deploy_local()
    elif args.mode == "docker":
        if not deploy_docker():
            print("\n❌ Docker deployment failed.")
            sys.exit(1)
        
        # Run tests if not skipped
        if not args.skip_tests:
            run_tests()
    
    print("\n🎉 Deployment completed successfully!")

if __name__ == "__main__":
    main()