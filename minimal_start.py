#!/usr/bin/env python3
"""
Minimal server - bypasses all complex imports
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np

# Change to project directory
os.chdir(Path(__file__).parent)

# Add src to path for model service
sys.path.append(str(Path(__file__).parent))

# Create minimal FastAPI app
app = FastAPI(title="AeroCast", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/historical")
async def historical():
    return FileResponse("static/historical.html")

@app.get("/analytics")
async def analytics():
    return FileResponse("static/analytics.html")

@app.get("/settings")
async def settings():
    return FileResponse("static/settings.html")

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "AeroCast server is running"}

@app.get("/api")
async def api_info():
    return {
        "message": "AeroCast API",
        "version": "1.0.0",
        "status": "running"
    }

# FORECAST API ENDPOINTS
@app.get("/api/v1/current")
async def get_current_forecast(
    lat: float = Query(..., ge=28.4, le=28.9),
    lon: float = Query(..., ge=76.8, le=77.5),
    hours: int = Query(24, ge=1, le=48)
):
    """Get current air quality forecast"""
    try:
        # Import model service
        from src.services.fast_model_service import fast_model_service
        
        # Get predictions
        prediction_result = fast_model_service.predict(lat, lon, hours)
        
        # Format response
        forecast_times = [
            (datetime.utcnow() + timedelta(hours=i)).isoformat() 
            for i in range(1, hours + 1)
        ]
        
        forecasts = []
        for pollutant, values in prediction_result['predictions'].items():
            forecasts.append({
                "pollutant": f"{pollutant}_forecast",
                "values": values,
                "unit": "μg/m³"
            })
        
        return {
            "location": {
                "latitude": lat,
                "longitude": lon,
                "city": "Delhi"
            },
            "forecast_time": datetime.utcnow().isoformat(),
            "forecast_horizon": hours,
            "forecasts": forecasts,
            "metadata": {
                "model_version": "v2.0",
                "forecast_times": forecast_times
            }
        }
        
    except Exception as e:
        print(f"Forecast error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate forecast")

@app.get("/api/v1/model-status")
async def get_model_status():
    """Get model status"""
    try:
        from src.services.fast_model_service import fast_model_service
        model_info = fast_model_service.get_model_info()
        
        return {
            "status": "intelligent_fallback",
            "model_name": "Fast Prediction Engine",
            "accuracy": "70%",
            "description": "Ultra-fast location-aware predictions",
            "loaded_models": model_info['loaded_models'],
            "model_count": model_info['model_count']
        }
    except Exception as e:
        return {
            "status": "error",
            "model_name": "Unknown",
            "accuracy": "Unknown",
            "description": f"Error: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 Starting AeroCast Minimal Server...")
    print("📍 Available at: http://localhost:8000")
    print("⚡ Starting now...")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )