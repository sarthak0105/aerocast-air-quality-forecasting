"""
Feature engineering for air quality forecasting
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Union
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer, KNNImputer

from config.settings import settings
from src.utils.logger import get_logger
from src.utils.helpers import (
    create_time_features, 
    create_lag_features, 
    create_rolling_features,
    haversine_distance
)
from src.preprocessing.data_quality import DataQualityEnhancer

logger = get_logger(__name__)


class FeatureEngineer:
    """Feature engineering pipeline for air quality data"""
    
    def __init__(self):
        self.scalers = {}
        self.imputers = {}
        self.feature_names = []
        self.target_columns = settings.TARGET_VARIABLES
        self.data_quality_enhancer = DataQualityEnhancer()
        
    def create_meteorological_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create comprehensive derived meteorological features
        
        Args:
            df: Input dataframe with meteorological variables
            
        Returns:
            DataFrame with additional meteorological features
        """
        df = df.copy()
        
        # Wind-based features (u, v, w components already provided)
        if 'u_forecast' in df.columns and 'v_forecast' in df.columns:
            # Calculate horizontal wind speed and direction
            df['wind_speed'] = np.sqrt(df['u_forecast']**2 + df['v_forecast']**2)
            df['wind_direction'] = np.arctan2(df['v_forecast'], df['u_forecast']) * 180 / np.pi
            df['wind_direction'] = (df['wind_direction'] + 360) % 360  # Convert to 0-360 degrees
            
            # Wind direction categories (8 cardinal directions)
            df['wind_dir_N'] = np.cos(np.radians(df['wind_direction']))
            df['wind_dir_E'] = np.sin(np.radians(df['wind_direction']))
            
            # Wind speed categories
            df['wind_speed_category'] = pd.cut(
                df['wind_speed'], 
                bins=[0, 2, 5, 10, 15, float('inf')],
                labels=[0, 1, 2, 3, 4]  # Calm, Light, Moderate, Strong, Very Strong
            ).astype(float)
            
            # Wind power (cubic relationship)
            df['wind_power'] = df['wind_speed'] ** 3
            
            # Turbulence indicators
            df['wind_shear'] = df['u_forecast'].diff().abs() + df['v_forecast'].diff().abs()
        
        # Vertical wind component features
        if 'w_forecast' in df.columns:
            df['vertical_wind_abs'] = np.abs(df['w_forecast'])
            df['vertical_stability'] = np.where(df['w_forecast'] > 0, 1, -1)  # Upward/downward motion
            df['vertical_wind_squared'] = df['w_forecast'] ** 2
            
            # Atmospheric mixing potential
            if 'wind_speed' in df.columns:
                df['mixing_potential'] = df['wind_speed'] * np.abs(df['w_forecast'])
        
        # Temperature-based features (assuming T_forecast is in Kelvin or Celsius)
        if 'T_forecast' in df.columns:
            # If temperature is in Kelvin, convert to Celsius
            if df['T_forecast'].mean() > 100:  # Likely Kelvin
                df['temp_celsius'] = df['T_forecast'] - 273.15
            else:
                df['temp_celsius'] = df['T_forecast']
            
            # Temperature categories
            df['temp_category'] = pd.cut(
                df['temp_celsius'],
                bins=[-float('inf'), 0, 10, 20, 30, 40, float('inf')],
                labels=[0, 1, 2, 3, 4, 5]  # Very Cold, Cold, Cool, Warm, Hot, Very Hot
            ).astype(float)
            
            # Temperature gradients (thermal stability)
            df['temp_gradient'] = df['temp_celsius'].diff()
            df['temp_gradient_abs'] = np.abs(df['temp_gradient'])
            
            # Diurnal temperature variation indicators
            df['temp_sin_daily'] = np.sin(2 * np.pi * df.get('hour', 0) / 24)
            df['temp_cos_daily'] = np.cos(2 * np.pi * df.get('hour', 0) / 24)
        
        # Specific humidity features
        if 'q_forecast' in df.columns:
            df['humidity_log'] = np.log(df['q_forecast'] + 1e-8)  # Log transform for better distribution
            df['humidity_sqrt'] = np.sqrt(df['q_forecast'])
            
            # Relative humidity approximation (if temperature available)
            if 'temp_celsius' in df.columns:
                # Saturation vapor pressure (Tetens formula)
                es = 0.6108 * np.exp(17.27 * df['temp_celsius'] / (df['temp_celsius'] + 237.3))
                # Convert specific humidity to mixing ratio then to vapor pressure
                mixing_ratio = df['q_forecast'] / (1 - df['q_forecast'] + 1e-8)
                # Approximate relative humidity
                df['relative_humidity_approx'] = np.minimum(100, (mixing_ratio / (es + 1e-8)) * 100)
                
                # Dew point approximation
                df['dew_point_approx'] = df['temp_celsius'] - ((100 - df['relative_humidity_approx']) / 5)
                
                # Vapor pressure deficit
                df['vpd'] = es - (df['relative_humidity_approx'] / 100 * es)
        
        # Atmospheric stability indicators
        if 'wind_speed' in df.columns and 'w_forecast' in df.columns:
            df['atmospheric_stability'] = df['w_forecast'] / (df['wind_speed'] + 0.1)
            
            # Richardson number approximation (stability parameter)
            if 'temp_gradient' in df.columns:
                df['richardson_number'] = (df['temp_gradient'] / (df['temp_celsius'] + 273.15)) / (df['wind_speed'] + 0.1)**2
        
        # Boundary layer indicators
        if 'temp_celsius' in df.columns and 'wind_speed' in df.columns:
            # Monin-Obukhov length approximation
            df['stability_parameter'] = df['temp_celsius'] / (df['wind_speed'] + 0.1)**2
            
            # Convective velocity scale
            if 'w_forecast' in df.columns:
                df['convective_velocity'] = (np.abs(df['w_forecast']) * df['temp_celsius'])**(1/3)
        
        # Pressure-related features (if available)
        if 'pressure' in df.columns or 'p_forecast' in df.columns:
            pressure_col = 'pressure' if 'pressure' in df.columns else 'p_forecast'
            df['pressure_gradient'] = df[pressure_col].diff()
            df['pressure_tendency'] = df[pressure_col].rolling(window=3).mean().diff()
        
        # Solar radiation proxies (based on time of day and season)
        if 'hour' in df.columns and 'month' in df.columns:
            # Solar elevation angle approximation
            day_of_year = df.get('day_of_year', df['month'] * 30)  # Rough approximation
            solar_declination = 23.45 * np.sin(np.radians(360 * (284 + day_of_year) / 365))
            
            # Assuming latitude around Delhi (28.6°N)
            latitude = 28.6
            hour_angle = 15 * (df['hour'] - 12)
            
            solar_elevation = np.arcsin(
                np.sin(np.radians(latitude)) * np.sin(np.radians(solar_declination)) +
                np.cos(np.radians(latitude)) * np.cos(np.radians(solar_declination)) * np.cos(np.radians(hour_angle))
            )
            
            df['solar_elevation'] = np.degrees(solar_elevation)
            df['solar_radiation_proxy'] = np.maximum(0, np.sin(solar_elevation))
            
            # Photochemical activity indicator
            df['photochemical_potential'] = df['solar_radiation_proxy'] * (df['temp_celsius'] + 273.15) / 300
        
        # Interaction features
        if 'temp_celsius' in df.columns and 'wind_speed' in df.columns:
            # Heat index approximation
            df['heat_index'] = df['temp_celsius'] + 0.5 * (df['relative_humidity_approx'] - 50) / 10
            
            # Wind chill approximation
            df['wind_chill'] = 13.12 + 0.6215 * df['temp_celsius'] - 11.37 * (df['wind_speed'] * 3.6)**0.16 + 0.3965 * df['temp_celsius'] * (df['wind_speed'] * 3.6)**0.16
        
        logger.info("Created comprehensive meteorological features")
        return df
    
    def create_satellite_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create satellite-based features
        
        Args:
            df: Input dataframe with satellite variables
            
        Returns:
            DataFrame with additional satellite features
        """
        df = df.copy()
        
        # NO2 satellite features
        if 'NO2_satellite' in df.columns:
            df['NO2_satellite_log'] = np.log(df['NO2_satellite'] + 1e-8)
            df['NO2_satellite_sqrt'] = np.sqrt(np.maximum(0, df['NO2_satellite']))
        
        # HCHO satellite features
        if 'HCHO_satellite' in df.columns:
            df['HCHO_satellite_log'] = np.log(df['HCHO_satellite'] + 1e-8)
            df['HCHO_satellite_sqrt'] = np.sqrt(np.maximum(0, df['HCHO_satellite']))
        
        # Ratio features (already provided but can enhance)
        if 'ratio_satellite' in df.columns:
            df['ratio_satellite_log'] = np.log(df['ratio_satellite'] + 1e-8)
            df['ratio_satellite_inv'] = 1 / (df['ratio_satellite'] + 1e-8)
        
        # Cross-satellite features
        if 'NO2_satellite' in df.columns and 'HCHO_satellite' in df.columns:
            df['NO2_HCHO_product'] = df['NO2_satellite'] * df['HCHO_satellite']
            df['NO2_HCHO_diff'] = df['NO2_satellite'] - df['HCHO_satellite']
            
            # Alternative ratio calculation
            df['NO2_HCHO_ratio_alt'] = df['NO2_satellite'] / (df['HCHO_satellite'] + 1e-8)
        
        logger.info("Created satellite features")
        return df
    
    def create_pollution_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create pollution-related features
        
        Args:
            df: Input dataframe with pollution forecast variables
            
        Returns:
            DataFrame with pollution features
        """
        df = df.copy()
        
        # Ratios between forecast pollutants
        if 'NO2_forecast' in df.columns and 'O3_forecast' in df.columns:
            df['NO2_O3_forecast_ratio'] = df['NO2_forecast'] / (df['O3_forecast'] + 1e-6)
            df['O3_NO2_forecast_ratio'] = df['O3_forecast'] / (df['NO2_forecast'] + 1e-6)
        
        # Air Quality Index approximation for forecasts
        if 'NO2_forecast' in df.columns:
            df['NO2_forecast_aqi_category'] = pd.cut(
                df['NO2_forecast'], 
                bins=[0, 40, 80, 180, 280, float('inf')],
                labels=[0, 1, 2, 3, 4]  # Good, Satisfactory, Moderate, Poor, Very Poor
            ).astype(float)
        
        if 'O3_forecast' in df.columns:
            df['O3_forecast_aqi_category'] = pd.cut(
                df['O3_forecast'],
                bins=[0, 50, 100, 168, 208, float('inf')],
                labels=[0, 1, 2, 3, 4]
            ).astype(float)
        
        # Satellite vs Forecast comparison features
        if 'NO2_satellite' in df.columns and 'NO2_forecast' in df.columns:
            df['NO2_satellite_forecast_ratio'] = df['NO2_satellite'] / (df['NO2_forecast'] + 1e-6)
            df['NO2_satellite_forecast_diff'] = df['NO2_satellite'] - df['NO2_forecast']
        
        # Combined pollution index
        if 'NO2_forecast' in df.columns and 'O3_forecast' in df.columns:
            # Normalized combined index (0-1 scale)
            no2_norm = df['NO2_forecast'] / (df['NO2_forecast'].max() + 1e-6)
            o3_norm = df['O3_forecast'] / (df['O3_forecast'].max() + 1e-6)
            df['combined_pollution_index'] = (no2_norm + o3_norm) / 2
        
        logger.info("Created pollution features")
        return df
    
    def handle_missing_values(
        self, 
        df: pd.DataFrame, 
        strategy: str = 'knn',
        n_neighbors: int = 5
    ) -> pd.DataFrame:
        """
        Handle missing values in the dataset
        
        Args:
            df: Input dataframe
            strategy: Imputation strategy ('mean', 'median', 'knn')
            n_neighbors: Number of neighbors for KNN imputation
            
        Returns:
            DataFrame with imputed values
        """
        df = df.copy()
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        if strategy == 'knn':
            imputer = KNNImputer(n_neighbors=n_neighbors)
            df[numeric_columns] = imputer.fit_transform(df[numeric_columns])
            self.imputers['knn'] = imputer
        else:
            imputer = SimpleImputer(strategy=strategy)
            df[numeric_columns] = imputer.fit_transform(df[numeric_columns])
            self.imputers[strategy] = imputer
        
        logger.info(f"Handled missing values using {strategy} strategy")
        return df
    
    def scale_features(
        self, 
        df: pd.DataFrame, 
        method: str = 'standard',
        exclude_columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Scale numerical features
        
        Args:
            df: Input dataframe
            method: Scaling method ('standard', 'minmax')
            exclude_columns: Columns to exclude from scaling
            
        Returns:
            DataFrame with scaled features
        """
        df = df.copy()
        exclude_columns = exclude_columns or []
        
        # Get numeric columns excluding targets and specified columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        columns_to_scale = [col for col in numeric_columns 
                           if col not in self.target_columns + exclude_columns]
        
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
        self.scalers[method] = scaler
        
        logger.info(f"Scaled features using {method} scaling")
        return df
    
    def create_sequences(
        self,
        df: pd.DataFrame,
        sequence_length: int = 24,
        forecast_horizon: int = 1,
        target_columns: Optional[List[str]] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for time series modeling
        
        Args:
            df: Input dataframe
            sequence_length: Length of input sequences
            forecast_horizon: Number of steps to forecast
            target_columns: Target variable columns
            
        Returns:
            Tuple of (X, y) arrays
        """
        target_columns = target_columns or self.target_columns
        feature_columns = [col for col in df.columns if col not in target_columns]
        
        X, y = [], []
        
        for i in range(len(df) - sequence_length - forecast_horizon + 1):
            # Input sequence
            X_seq = df[feature_columns].iloc[i:i + sequence_length].values
            
            # Target sequence
            y_seq = df[target_columns].iloc[
                i + sequence_length:i + sequence_length + forecast_horizon
            ].values
            
            X.append(X_seq)
            y.append(y_seq)
        
        X = np.array(X)
        y = np.array(y)
        
        logger.info(f"Created sequences: X shape {X.shape}, y shape {y.shape}")
        return X, y
    
    def fit_transform(
        self,
        df: pd.DataFrame,
        create_sequences: bool = False,
        sequence_length: int = 24,
        forecast_horizon: int = 1
    ) -> Union[pd.DataFrame, Tuple[np.ndarray, np.ndarray]]:
        """
        Complete enhanced feature engineering pipeline
        
        Args:
            df: Input dataframe
            create_sequences: Whether to create sequences for time series
            sequence_length: Length of input sequences
            forecast_horizon: Number of steps to forecast
            
        Returns:
            Processed dataframe or sequence arrays
        """
        logger.info("Starting enhanced feature engineering pipeline")
        
        # Create datetime and temporal features
        if 'datetime' in df.columns or all(col in df.columns for col in ['year', 'month', 'day', 'hour']):
            df = create_time_features(df)
        
        # Create meteorological features
        df = self.create_meteorological_features(df)
        
        # Create satellite features
        df = self.create_satellite_features(df)
        
        # Create pollution features
        df = self.create_pollution_features(df)
        
        # Create lag features
        lag_columns = [col for col in self.target_columns if col in df.columns]
        if lag_columns:
            df = create_lag_features(df, lag_columns, [1, 2, 3, 6, 12, 24, 48])
        
        # Create rolling features
        if lag_columns:
            df = create_rolling_features(df, lag_columns, [3, 6, 12, 24, 48])
        
        # Apply comprehensive data quality enhancement
        logger.info("Applying comprehensive data quality enhancement...")
        df = self.data_quality_enhancer.enhance_data_quality(
            df,
            handle_outliers=True,
            smooth_data=True,
            create_robust_stats=True,
            create_interactions=True,
            create_lags=True,
            scaling_method='robust'
        )
        
        # Store feature names (excluding target columns)
        self.feature_names = [col for col in df.columns if col not in self.target_columns]
        
        # Remove any remaining infinite or extremely large values
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # Final imputation for any remaining missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
        
        logger.info(f"Enhanced feature engineering completed. Total features: {len(self.feature_names)}")
        logger.info(f"Data shape: {df.shape}")
        
        if create_sequences:
            return self.create_sequences(df, sequence_length, forecast_horizon)
        else:
            return df
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform new data using fitted scalers and imputers
        
        Args:
            df: Input dataframe
            
        Returns:
            Transformed dataframe
        """
        df = df.copy()
        
        # Apply same transformations as in fit_transform
        if 'datetime' in df.columns or all(col in df.columns for col in ['year', 'month', 'day', 'hour']):
            df = create_time_features(df)
        
        df = self.create_meteorological_features(df)
        df = self.create_satellite_features(df)
        df = self.create_pollution_features(df)
        
        # Create lag features (same as in fit_transform)
        lag_columns = [col for col in self.target_columns if col in df.columns]
        if lag_columns:
            df = create_lag_features(df, lag_columns, [1, 2, 3, 6, 12, 24])
        
        # Create rolling features (same as in fit_transform)
        if lag_columns:
            df = create_rolling_features(df, lag_columns, [3, 6, 12, 24])
        
        # Handle missing values using fitted imputer
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # Ensure we have the same columns as during fit
        missing_cols = set(self.feature_names) - set(df.columns)
        if missing_cols:
            logger.warning(f"Missing columns during transform: {missing_cols}")
            # Add missing columns with zeros
            for col in missing_cols:
                df[col] = 0.0
        
        # Select only the features that were used during fit
        feature_cols = [col for col in self.feature_names if col in df.columns]
        
        if 'knn' in self.imputers:
            df[feature_cols] = self.imputers['knn'].transform(df[feature_cols])
        
        if 'standard' in self.scalers:
            columns_to_scale = [col for col in feature_cols 
                               if col not in self.target_columns]
            df[columns_to_scale] = self.scalers['standard'].transform(df[columns_to_scale])
        
        return df