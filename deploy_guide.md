# 🚀 Deployment Guide: AeroCast - Air Quality Forecasting Platform

## 📋 **Prerequisites**

1. **GitHub Account** (for code hosting)
2. **Vercel Account** (for frontend deployment)
3. **Render Account** (for backend deployment)
4. **Git installed** on your local machine

---

## 🔧 **Step 1: Prepare Your Code for Deployment**

### **1.1 Create GitHub Repository**

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: AeroCast - Air Quality Forecasting Platform"

# Create repository on GitHub and add remote
git remote add origin https://github.com/YOUR_USERNAME/delhi-air-quality-forecasting.git

# Push to GitHub
git push -u origin main
```

---

## 🌐 **Step 2: Deploy Backend on Render**

### **2.1 Create Render Account**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Connect your GitHub repository

### **2.2 Deploy Backend**

1. **Click "New +" → "Web Service"**
2. **Connect Repository**: Select your GitHub repo
3. **Configure Service**:
   ```
   Name: delhi-air-quality-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Environment Variables**:
   ```
   PYTHON_VERSION = 3.9.18
   PORT = 10000
   ```

5. **Click "Create Web Service"**

6. **Wait for deployment** (5-10 minutes)

7. **Note your backend URL**: `https://your-app-name.onrender.com`

### **2.3 Test Backend**
```bash
# Test your deployed backend
curl https://your-app-name.onrender.com/health
curl https://your-app-name.onrender.com/api/v1/model-status
```

---

## ⚡ **Step 3: Deploy Frontend on Vercel**

### **3.1 Create Vercel Account**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub account

### **3.2 Deploy Frontend**

1. **Click "New Project"**
2. **Import Git Repository**: Select your repo
3. **Configure Project**:
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

4. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL = https://your-backend-url.onrender.com
   NODE_ENV = production
   ```

5. **Click "Deploy"**

6. **Wait for deployment** (3-5 minutes)

7. **Note your frontend URL**: `https://your-app-name.vercel.app`

---

## 🔗 **Step 4: Connect Frontend to Backend**

### **4.1 Update CORS Settings**

Update your backend's CORS settings in `api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-url.vercel.app",  # Your actual Vercel URL
        "http://localhost:3000"  # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

### **4.2 Redeploy Backend**
```bash
git add .
git commit -m "Update CORS for production"
git push origin main
```

Render will automatically redeploy your backend.

---

## ✅ **Step 5: Verify Deployment**

### **5.1 Test Backend Endpoints**
```bash
# Health check
curl https://your-backend-url.onrender.com/health

# Model status
curl https://your-backend-url.onrender.com/api/v1/model-status

# Test prediction
curl -X POST https://your-backend-url.onrender.com/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"latitude": 28.6139, "longitude": 77.2090, "hours": 24}'
```

### **5.2 Test Frontend**
1. Open `https://your-frontend-url.vercel.app`
2. Check all pages load correctly
3. Test forecast generation
4. Verify API calls work

---

## 🎯 **Step 6: Custom Domain (Optional)**

### **6.1 Frontend Custom Domain**
1. In Vercel dashboard → Settings → Domains
2. Add your custom domain
3. Configure DNS records

### **6.2 Backend Custom Domain**
1. In Render dashboard → Settings → Custom Domains
2. Add your custom domain
3. Configure DNS records

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

#### **Backend Issues**
```bash
# Check logs in Render dashboard
# Common fixes:
1. Ensure requirements.txt includes all dependencies
2. Check Python version compatibility
3. Verify environment variables
4. Check CORS settings
```

#### **Frontend Issues**
```bash
# Check build logs in Vercel dashboard
# Common fixes:
1. Ensure NEXT_PUBLIC_API_URL is set correctly
2. Check for TypeScript errors
3. Verify all dependencies are in package.json
4. Check for missing environment variables
```

#### **CORS Issues**
```bash
# If getting CORS errors:
1. Update backend CORS origins
2. Ensure frontend URL is whitelisted
3. Check browser network tab for exact error
```

---

## 📱 **Final URLs**

After successful deployment:

- **🌐 Frontend**: `https://your-app-name.vercel.app`
- **📡 Backend API**: `https://your-app-name.onrender.com`
- **📚 API Docs**: `https://your-app-name.onrender.com/docs`

---

## 🎉 **Success!**

Your Delhi Air Quality Forecasting System is now live! 

### **Features Available**:
- ✅ Real-time air quality forecasting
- ✅ Interactive maps and charts
- ✅ Historical data analysis
- ✅ Performance analytics
- ✅ Mobile-responsive design
- ✅ Professional UI/UX

### **Share Your Project**:
- Frontend: `https://your-app-name.vercel.app`
- API: `https://your-app-name.onrender.com/docs`

---

## 🔄 **Future Updates**

To update your deployed application:

```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push origin main
```

Both Vercel and Render will automatically redeploy when you push to GitHub!