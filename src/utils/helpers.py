"""
Helper functions for the Air Quality Forecasting System
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Tuple, Union, Optional
import xarray as xr
from pathlib import Path

from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_datetime_from_components(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create datetime column from year, month, day, hour components
    
    Args:
        df: Input dataframe with year, month, day, hour columns
        
    Returns:
        DataFrame with datetime column added
    """
    df = df.copy()
    
    # Create datetime from components
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    
    logger.info(f"Created datetime column for {len(df)} records")
    return df


def create_time_features(df: pd.DataFrame, datetime_col: str = 'datetime') -> pd.DataFrame:
    """
    Create temporal features from datetime column or existing time components
    
    Args:
        df: Input dataframe
        datetime_col: Name of datetime column
        
    Returns:
        DataFrame with additional temporal features
    """
    df = df.copy()
    
    # If datetime column doesn't exist but components do, create it
    if datetime_col not in df.columns and all(col in df.columns for col in ['year', 'month', 'day', 'hour']):
        df = create_datetime_from_components(df)
    
    # Use existing time components if available, otherwise extract from datetime
    if 'hour' not in df.columns and datetime_col in df.columns:
        dt = pd.to_datetime(df[datetime_col])
        df['hour'] = dt.dt.hour
        df['day_of_week'] = dt.dt.dayofweek
        df['day_of_year'] = dt.dt.dayofyear
        df['month'] = dt.dt.month
        df['quarter'] = dt.dt.quarter
        df['year'] = dt.dt.year
        df['day'] = dt.dt.day
    elif 'day_of_week' not in df.columns and datetime_col in df.columns:
        dt = pd.to_datetime(df[datetime_col])
        df['day_of_week'] = dt.dt.dayofweek
        df['day_of_year'] = dt.dt.dayofyear
        df['quarter'] = dt.dt.quarter
    
    # Ensure we have the basic time components
    if 'day_of_week' not in df.columns and datetime_col in df.columns:
        dt = pd.to_datetime(df[datetime_col])
        df['day_of_week'] = dt.dt.dayofweek
    
    # Cyclical features
    if 'hour' in df.columns:
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    
    if 'day_of_week' in df.columns:
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    if 'month' in df.columns:
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    # Boolean features
    if 'day_of_week' in df.columns:
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    if 'hour' in df.columns:
        df['is_rush_hour'] = ((df['hour'].between(7, 9)) | (df['hour'].between(17, 19))).astype(int)
    
    # Season
    if 'month' in df.columns:
        df['season'] = df['month'].map({
            12: 0, 1: 0, 2: 0,  # Winter
            3: 1, 4: 1, 5: 1,   # Spring
            6: 2, 7: 2, 8: 2,   # Summer
            9: 3, 10: 3, 11: 3  # Autumn
        })
    
    logger.info(f"Created temporal features for {len(df)} records")
    return df


def create_lag_features(
    df: pd.DataFrame, 
    columns: List[str], 
    lags: List[int],
    group_col: Optional[str] = None
) -> pd.DataFrame:
    """
    Create lag features for specified columns
    
    Args:
        df: Input dataframe
        columns: Columns to create lags for
        lags: List of lag periods
        group_col: Column to group by (e.g., station_id)
        
    Returns:
        DataFrame with lag features
    """
    df = df.copy()
    
    for col in columns:
        for lag in lags:
            if group_col:
                df[f'{col}_lag_{lag}'] = df.groupby(group_col)[col].shift(lag)
            else:
                df[f'{col}_lag_{lag}'] = df[col].shift(lag)
    
    logger.info(f"Created lag features for columns: {columns}, lags: {lags}")
    return df


def create_rolling_features(
    df: pd.DataFrame,
    columns: List[str],
    windows: List[int],
    group_col: Optional[str] = None
) -> pd.DataFrame:
    """
    Create rolling statistical features
    
    Args:
        df: Input dataframe
        columns: Columns to create rolling features for
        windows: List of window sizes
        group_col: Column to group by
        
    Returns:
        DataFrame with rolling features
    """
    df = df.copy()
    
    for col in columns:
        for window in windows:
            if group_col:
                grouped = df.groupby(group_col)[col]
                df[f'{col}_rolling_mean_{window}'] = grouped.rolling(window).mean()
                df[f'{col}_rolling_std_{window}'] = grouped.rolling(window).std()
                df[f'{col}_rolling_min_{window}'] = grouped.rolling(window).min()
                df[f'{col}_rolling_max_{window}'] = grouped.rolling(window).max()
            else:
                df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window).mean()
                df[f'{col}_rolling_std_{window}'] = df[col].rolling(window).std()
                df[f'{col}_rolling_min_{window}'] = df[col].rolling(window).min()
                df[f'{col}_rolling_max_{window}'] = df[col].rolling(window).max()
    
    logger.info(f"Created rolling features for columns: {columns}, windows: {windows}")
    return df


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
        
    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c


def split_time_series(
    df: pd.DataFrame,
    datetime_col: str,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split time series data chronologically
    
    Args:
        df: Input dataframe
        datetime_col: Name of datetime column
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set
        
    Returns:
        Tuple of (train_df, val_df, test_df)
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1"
    
    df_sorted = df.sort_values(datetime_col)
    n = len(df_sorted)
    
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    
    train_df = df_sorted.iloc[:train_end]
    val_df = df_sorted.iloc[train_end:val_end]
    test_df = df_sorted.iloc[val_end:]
    
    logger.info(f"Split data: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
    
    return train_df, val_df, test_df


def normalize_coordinates(lat: float, lon: float) -> Tuple[float, float]:
    """
    Normalize latitude and longitude to [-1, 1] range
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Normalized (lat, lon)
    """
    norm_lat = lat / 90.0
    norm_lon = lon / 180.0
    return norm_lat, norm_lon


def save_model_metadata(
    model_path: Path,
    metadata: dict,
    filename: str = "metadata.json"
) -> None:
    """
    Save model metadata to JSON file
    
    Args:
        model_path: Path to model directory
        metadata: Dictionary containing metadata
        filename: Name of metadata file
    """
    import json
    
    model_path.mkdir(parents=True, exist_ok=True)
    metadata_path = model_path / filename
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    
    logger.info(f"Saved model metadata to {metadata_path}")


def load_model_metadata(
    model_path: Path,
    filename: str = "metadata.json"
) -> dict:
    """
    Load model metadata from JSON file
    
    Args:
        model_path: Path to model directory
        filename: Name of metadata file
        
    Returns:
        Dictionary containing metadata
    """
    import json
    
    metadata_path = model_path / filename
    
    if not metadata_path.exists():
        logger.warning(f"Metadata file not found: {metadata_path}")
        return {}
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    logger.info(f"Loaded model metadata from {metadata_path}")
    return metadata