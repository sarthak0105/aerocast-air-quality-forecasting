"""
FastAPI application for air quality forecasting
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
from typing import List, Optional
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import settings
from api.routes import forecast, health
from src.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AeroCast API - Air Quality Forecasting",
    version="1.0.0",
    description="Advanced AI/ML-based air quality forecasting platform for Delhi NCR",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aerocast-air-quality-forecasting.vercel.app",  # Your Vercel URL
        "https://aerocast-sarthak0105.vercel.app",  # Alternative Vercel URL format
        "http://localhost:3000",  # Keep for local development
        "http://localhost:3001"   # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static files (fallback for old HTML version)
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount React build files if available
if Path("frontend/.next").exists():
    app.mount("/_next", StaticFiles(directory="frontend/.next"), name="next_static")
if Path("frontend/public").exists():
    app.mount("/public", StaticFiles(directory="frontend/public"), name="public")

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(forecast.router, prefix="/api/v1", tags=["forecast"])

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    from config.settings import settings
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.get("/")
async def root():
    """Root endpoint - serve main dashboard"""
    from fastapi.responses import FileResponse
    
    # Try to serve React build first
    react_index = Path("frontend/.next/server/pages/index.html")
    if react_index.exists():
        return FileResponse(str(react_index))
    
    # Fallback to static HTML
    static_index = Path("static/index.html")
    if static_index.exists():
        return FileResponse(str(static_index))
    
    # If neither exists, return a simple message
    return {"message": "Delhi Air Quality Forecasting API", "frontend": "not_found"}

@app.get("/historical")
async def historical():
    """Historical data page"""
    from fastapi.responses import FileResponse
    return FileResponse("static/historical.html")

@app.get("/analytics") 
async def analytics():
    """Analytics page"""
    from fastapi.responses import FileResponse
    return FileResponse("static/analytics.html")

@app.get("/settings")
async def settings_page():
    """Settings page"""
    from fastapi.responses import FileResponse
    return FileResponse("static/settings.html")

@app.get("/api")
async def api_info():
    """API information endpoint"""
    from config.settings import settings
    return {
        "message": "Welcome to AeroCast API - Advanced Air Quality Forecasting",
        "version": settings.VERSION,
        "platform": "AeroCast",
        "docs": "/docs",
        "health": "/health",
        "dashboard": "/",
        "historical": "/historical",
        "analytics": "/analytics", 
        "settings": "/settings"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )