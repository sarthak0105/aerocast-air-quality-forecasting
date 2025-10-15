# 🌐 Website Loading Fix Guide

## 🚨 **Problem**: Website not loading in browser

### **❌ Common Issues:**
1. Using `http://0.0.0.0:8000/` (won't work in browser)
2. Server not starting properly
3. Port conflicts
4. Firewall blocking connections

## ✅ **SOLUTION: Use These Working Methods**

### **Method 1: Simple Python Script (Recommended)**
```bash
python scripts/simple_start.py
```

### **Method 2: Double-Click Batch File (Windows)**
```
Double-click: START_AEROCAST.bat
```

### **Method 3: Manual Command**
```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

## 🌐 **CORRECT URLs to Use:**

### ✅ **WORKING URLs:**
- **Main Dashboard**: http://localhost:8000
- **Main Dashboard**: http://127.0.0.1:8000
- **Historical**: http://localhost:8000/static/historical.html
- **Analytics**: http://localhost:8000/static/analytics.html
- **Settings**: http://localhost:8000/static/settings.html
- **API Docs**: http://localhost:8000/docs

### ❌ **DON'T USE:**
- ~~http://0.0.0.0:8000~~ (Won't work in browser)
- ~~http://0.0.0.0:8000/static/index.html~~ (Won't work)

## 🔧 **Troubleshooting Steps:**

### **Step 1: Check if Server is Running**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000
```

### **Step 2: Kill Existing Processes**
```bash
# Kill processes on port 8000
for /f "tokens=5" %a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %a
```

### **Step 3: Start Fresh**
```bash
python scripts/simple_start.py
```

### **Step 4: Test in Browser**
Open: http://localhost:8000

## 🎯 **Quick Fix Commands:**

### **Windows Command Prompt:**
```cmd
cd "C:\path\to\your\AeroCast\project"
python scripts/simple_start.py
```

### **Windows PowerShell:**
```powershell
cd "C:\path\to\your\AeroCast\project"
python scripts/simple_start.py
```

## 📊 **What Should Happen:**

1. **Server starts** on http://127.0.0.1:8000
2. **Browser opens automatically** (or you open manually)
3. **Main dashboard loads** with beautiful interface
4. **You can navigate** to different pages
5. **Predictions work** when you click "Get Forecast"

## 🌟 **Expected Output:**
```
🚀 Starting AeroCast server...
✅ Server process started successfully!

🎉 SUCCESS! AeroCast is now running!

🌐 OPEN THESE LINKS IN YOUR BROWSER:
   📊 Main Dashboard: http://localhost:8000
   📈 Historical Analysis: http://localhost:8000/static/historical.html
   📊 Analytics Dashboard: http://localhost:8000/static/analytics.html

🔗 MAIN LINK: http://localhost:8000
```

## 🔍 **If Still Not Working:**

### **Check 1: Are you in the right directory?**
```bash
# You should see these folders:
dir
# Should show: api, static, src, scripts, etc.
```

### **Check 2: Is Python working?**
```bash
python --version
# Should show Python 3.x
```

### **Check 3: Are dependencies installed?**
```bash
pip install -r requirements.txt
```

### **Check 4: Test API directly**
```bash
# Start server manually
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

# Then open: http://localhost:8000
```

## 🎉 **Success Indicators:**

✅ **Server starts without errors**
✅ **Browser opens to beautiful dashboard**
✅ **You can see the map and charts**
✅ **Navigation links work**
✅ **"Get Forecast" button generates predictions**

## 📞 **Still Need Help?**

If the website still won't load:

1. **Try the batch file**: Double-click `START_AEROCAST.bat`
2. **Check firewall**: Make sure port 8000 isn't blocked
3. **Try different browser**: Chrome, Firefox, Edge
4. **Check antivirus**: Some antivirus blocks local servers

## 🎯 **Bottom Line:**

**Use http://localhost:8000 (NOT http://0.0.0.0:8000)**

The `0.0.0.0` address is for server binding, but browsers need `localhost` or `127.0.0.1` to connect properly.