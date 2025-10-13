"""
Configuration settings for the Air Quality Forecasting System
"""
import os
from pathlib import Path
from typing import List, Optional
try:
    from pydantic_settings import BaseSettings
    from pydantic import validator
except ImportError:
    from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Air Quality Forecasting System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/airquality"
    REDIS_URL: str = "redis://localhost:6379"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Model Configuration
    MODEL_VERSION: str = "v2.0"
    FORECAST_HORIZON_HOURS: int = 48
    SPATIAL_RESOLUTION_KM: float = 1.0
    BATCH_SIZE: int = 256  # Larger batch size for stability
    LEARNING_RATE: float = 0.0003  # Lower learning rate for better convergence
    
    # Data Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    RAW_DATA_PATH: Path = BASE_DIR / "data" / "raw"
    PROCESSED_DATA_PATH: Path = BASE_DIR / "data" / "processed"
    MODEL_PATH: Path = BASE_DIR / "models"
    LOG_PATH: Path = BASE_DIR / "logs"
    
    # Geographic Configuration (Delhi NCR)
    DELHI_BBOX_MIN_LAT: float = 28.4
    DELHI_BBOX_MAX_LAT: float = 28.9
    DELHI_BBOX_MIN_LON: float = 76.8
    DELHI_BBOX_MAX_LON: float = 77.5
    
    # Target Variables (what we want to predict)
    TARGET_VARIABLES: List[str] = ["O3_forecast", "NO2_forecast"]
    
    # Actual target columns in training data
    ACTUAL_TARGET_VARIABLES: List[str] = ["O3_target", "NO2_target"]
    
    # Enhanced Feature Configuration
    METEOROLOGICAL_FEATURES: List[str] = [
        "T_forecast", "q_forecast", "u_forecast", "v_forecast", "w_forecast",
        "wind_speed", "wind_direction", "atmospheric_stability", "mixing_potential",
        "temp_celsius", "relative_humidity_approx", "solar_radiation_proxy"
    ]
    
    SATELLITE_FEATURES: List[str] = [
        "NO2_satellite", "HCHO_satellite", "ratio_satellite",
        "NO2_satellite_log", "HCHO_satellite_log", "NO2_HCHO_product"
    ]
    
    TEMPORAL_FEATURES: List[str] = [
        "year", "month", "day", "hour", "day_of_week", "season", "is_weekend", "is_holiday",
        "traffic_intensity", "photochemical_activity", "winter_pollution_factor"
    ]
    
    # Advanced Model Parameters
    SEQUENCE_LENGTH: int = 72  # 3 days of hourly data
    LSTM_UNITS: int = 256
    NUM_LSTM_LAYERS: int = 4
    ATTENTION_HEADS: int = 12
    DROPOUT_RATE: float = 0.3
    USE_ATTENTION: bool = True
    USE_CNN_FEATURES: bool = True
    USE_BIDIRECTIONAL: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "air_quality_forecasting"
    
    # API Keys (will be loaded from environment)
    NASA_EARTHDATA_USERNAME: Optional[str] = None
    NASA_EARTHDATA_PASSWORD: Optional[str] = None
    ECMWF_API_KEY: Optional[str] = None
    OPENWEATHER_API_KEY: Optional[str] = None
    
    @validator("RAW_DATA_PATH", "PROCESSED_DATA_PATH", "MODEL_PATH", "LOG_PATH")
    def create_directories(cls, v):
        """Create directories if they don't exist"""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields from environment


# Global settings instance
settings = Settings()