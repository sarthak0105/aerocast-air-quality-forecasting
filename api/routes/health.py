"""
Health check endpoints
"""
from fastapi import APIRouter
from datetime import datetime
import psutil
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import settings

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION
    }

@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check with system information"""
    
    # System information
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent
            },
            "disk": {
                "total": disk.total,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100
            }
        },
        "configuration": {
            "model_version": settings.MODEL_VERSION,
            "forecast_horizon": settings.FORECAST_HORIZON_HOURS,
            "spatial_resolution": settings.SPATIAL_RESOLUTION_KM
        }
    }