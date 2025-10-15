#!/usr/bin/env python3
"""
Prepare the project for deployment on Vercel (frontend) and Render (backend)
"""
import os
import json
import subprocess
from pathlib import Path

def create_git_repository():
    """Initialize git repository and prepare for GitHub"""
    print("🔧 Preparing Git repository...")
    
    # Initialize git if not already done
    if not Path(".git").exists():
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")
    
    # Create .gitignore if it doesn't exist
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv/
.env

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Data
data/raw/
data/processed/
models/*.h5
models/*.pkl

# Frontend
frontend/node_modules/
frontend/.next/
frontend/out/
frontend/build/
frontend/.env.local
frontend/.env.production.local
frontend/.env.development.local

# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content.strip())
    
    print("✅ .gitignore created")

def check_requirements():
    """Check if all required files exist"""
    print("🔍 Checking deployment requirements...")
    
    required_files = [
        "requirements.txt",
        "api/main.py",
        "frontend/package.json",
        "frontend/next.config.mjs"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def update_frontend_config():
    """Update frontend configuration for production"""
    print("🔧 Updating frontend configuration...")
    
    # Update package.json scripts
    package_json_path = Path("frontend/package.json")
    with open(package_json_path, "r") as f:
        package_data = json.load(f)
    
    # Ensure build script exists
    if "scripts" not in package_data:
        package_data["scripts"] = {}
    
    package_data["scripts"].update({
        "build": "next build",
        "start": "next start",
        "dev": "next dev",
        "lint": "next lint"
    })
    
    with open(package_json_path, "w") as f:
        json.dump(package_data, f, indent=2)
    
    print("✅ Frontend configuration updated")

def display_deployment_urls():
    """Display the deployment URLs and next steps"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT PREPARATION COMPLETE!")
    print("="*60)
    
    print("\n📋 NEXT STEPS:")
    print("\n1. 📤 PUSH TO GITHUB:")
    print("   git add .")
    print("   git commit -m 'Prepare for deployment'")
    print("   git remote add origin https://github.com/YOUR_USERNAME/delhi-air-quality.git")
    print("   git push -u origin main")
    
    print("\n2. 🌐 DEPLOY BACKEND ON RENDER:")
    print("   • Go to https://render.com")
    print("   • Create new Web Service")
    print("   • Connect your GitHub repo")
    print("   • Use these settings:")
    print("     - Build Command: pip install -r requirements.txt")
    print("     - Start Command: uvicorn api.main:app --host 0.0.0.0 --port $PORT")
    print("     - Python Version: 3.9.18")
    
    print("\n3. ⚡ DEPLOY FRONTEND ON VERCEL:")
    print("   • Go to https://vercel.com")
    print("   • Import your GitHub repo")
    print("   • Set Root Directory: frontend")
    print("   • Add Environment Variable:")
    print("     NEXT_PUBLIC_API_URL = https://your-backend-url.onrender.com")
    
    print("\n4. 🔗 UPDATE CORS:")
    print("   • After getting your Vercel URL, update api/main.py")
    print("   • Add your Vercel URL to allow_origins")
    print("   • Push changes to GitHub")
    
    print("\n📱 EXPECTED URLS:")
    print("   • Frontend: https://your-app-name.vercel.app")
    print("   • Backend: https://your-app-name.onrender.com")
    print("   • API Docs: https://your-app-name.onrender.com/docs")
    
    print("\n📖 For detailed instructions, see: deploy_guide.md")
    print("="*60)

def main():
    """Main deployment preparation function"""
    print("🚀 AeroCast - Air Quality Forecasting Platform - Deployment Preparation")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path("api").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the project root directory")
        return
    
    # Create git repository
    create_git_repository()
    
    # Check requirements
    if not check_requirements():
        print("❌ Please fix missing files before deployment")
        return
    
    # Update frontend config
    update_frontend_config()
    
    # Display next steps
    display_deployment_urls()

if __name__ == "__main__":
    main()