"""
Advanced data quality improvement and preprocessing
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.preprocessing import RobustScaler, QuantileTransformer
from sklearn.impute import KNNImputer
from scipy import stats
from scipy.signal import savgol_filter

from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataQualityEnhancer:
    """Advanced data quality enhancement for air quality forecasting"""
    
    def __init__(self):
        self.scalers = {}
        self.transformers = {}
        self.outlier_bounds = {}
        self.quality_stats = {}
        
    def detect_and_handle_outliers(
        self, 
        df: pd.DataFrame, 
        method: str = 'iqr',
        factor: float = 2.5,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Detect and handle outliers using various methods
        
        Args:
            df: Input dataframe
            method: Outlier detection method ('iqr', 'zscore', 'isolation_forest')
            factor: Multiplier for outlier detection threshold
            columns: Columns to check for outliers
            
        Returns:
            DataFrame with outliers handled
        """
        df = df.copy()
        columns = columns or df.select_dtypes(include=[np.number]).columns.tolist()
        
        outlier_counts = {}
        
        for col in columns:
            if col not in df.columns:
                continue
                
            original_count = len(df)
            
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - factor * IQR
                upper_bound = Q3 + factor * IQR
                
                # Store bounds for future use
                self.outlier_bounds[col] = (lower_bound, upper_bound)
                
                # Cap outliers instead of removing them
                df[col] = np.clip(df[col], lower_bound, upper_bound)
                
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                threshold = factor
                
                # Get outlier mask
                outlier_mask = z_scores > threshold
                
                if np.any(outlier_mask):
                    # Replace outliers with median
                    median_val = df[col].median()
                    df.loc[df[col].index[outlier_mask], col] = median_val
                
            elif method == 'isolation_forest':
                from sklearn.ensemble import IsolationForest
                
                # Fit isolation forest
                iso_forest = IsolationForest(contamination=0.1, random_state=42)
                outlier_mask = iso_forest.fit_predict(df[[col]].dropna()) == -1
                
                if np.any(outlier_mask):
                    # Replace outliers with median
                    median_val = df[col].median()
                    df.loc[df[col].dropna().index[outlier_mask], col] = median_val
            
            # Count outliers handled
            outlier_counts[col] = original_count - len(df[df[col].notna()])
        
        logger.info(f"Outlier handling ({method}): {sum(outlier_counts.values())} outliers processed")
        return df
    
    def smooth_time_series(
        self, 
        df: pd.DataFrame, 
        columns: Optional[List[str]] = None,
        window_length: int = 5,
        polyorder: int = 2
    ) -> pd.DataFrame:
        """
        Apply smoothing to time series data to reduce noise
        
        Args:
            df: Input dataframe
            columns: Columns to smooth
            window_length: Length of smoothing window
            polyorder: Polynomial order for Savitzky-Golay filter
            
        Returns:
            DataFrame with smoothed data
        """
        df = df.copy()
        columns = columns or ['O3_forecast', 'NO2_forecast', 'T_forecast', 'q_forecast']
        
        for col in columns:
            if col in df.columns and len(df[col].dropna()) > window_length:
                # Apply Savitzky-Golay filter for smoothing
                try:
                    smoothed = savgol_filter(
                        df[col].ffill().bfill(), 
                        window_length=window_length, 
                        polyorder=polyorder
                    )
                    df[f'{col}_smoothed'] = smoothed
                    
                    # Keep original and add smoothed as additional feature
                    logger.debug(f"Applied smoothing to {col}")
                except Exception as e:
                    logger.warning(f"Could not smooth {col}: {str(e)}")
        
        return df
    
    def create_robust_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create robust statistical features that are less sensitive to outliers
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with robust features
        """
        df = df.copy()
        
        # Robust statistical features for key variables
        key_vars = ['O3_forecast', 'NO2_forecast', 'T_forecast', 'q_forecast', 'wind_speed']
        
        for var in key_vars:
            if var in df.columns:
                # Rolling robust statistics
                for window in [3, 6, 12, 24]:
                    # Median (robust to outliers)
                    df[f'{var}_median_{window}h'] = df[var].rolling(window=window, min_periods=1).median()
                    
                    # Interquartile range
                    df[f'{var}_iqr_{window}h'] = (
                        df[var].rolling(window=window, min_periods=1).quantile(0.75) - 
                        df[var].rolling(window=window, min_periods=1).quantile(0.25)
                    )
                    
                    # Robust standard deviation (using MAD)
                    df[f'{var}_mad_{window}h'] = df[var].rolling(window=window, min_periods=1).apply(
                        lambda x: np.median(np.abs(x - np.median(x)))
                    )
                    
                    # Percentile features
                    df[f'{var}_p10_{window}h'] = df[var].rolling(window=window, min_periods=1).quantile(0.1)
                    df[f'{var}_p90_{window}h'] = df[var].rolling(window=window, min_periods=1).quantile(0.9)
        
        # Cross-variable robust features
        if 'O3_forecast' in df.columns and 'NO2_forecast' in df.columns:
            # Robust correlation features
            for window in [12, 24]:
                df[f'O3_NO2_ratio_median_{window}h'] = (
                    df['O3_forecast'].rolling(window=window, min_periods=1).median() / 
                    (df['NO2_forecast'].rolling(window=window, min_periods=1).median() + 1e-6)
                )
        
        logger.info("Created robust statistical features")
        return df
    
    def apply_advanced_scaling(
        self, 
        df: pd.DataFrame, 
        method: str = 'robust',
        exclude_columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Apply advanced scaling methods that are robust to outliers
        
        Args:
            df: Input dataframe
            method: Scaling method ('robust', 'quantile', 'power')
            exclude_columns: Columns to exclude from scaling
            
        Returns:
            DataFrame with scaled features
        """
        df = df.copy()
        exclude_columns = exclude_columns or ['year', 'month', 'day', 'hour', 'site_id']
        
        # Get numeric columns excluding specified ones
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        columns_to_scale = [col for col in numeric_columns if col not in exclude_columns]
        
        if method == 'robust':
            scaler = RobustScaler()
            df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
            self.scalers['robust'] = scaler
            
        elif method == 'quantile':
            # Quantile transformer to make data more Gaussian
            transformer = QuantileTransformer(output_distribution='normal', random_state=42)
            df[columns_to_scale] = transformer.fit_transform(df[columns_to_scale])
            self.transformers['quantile'] = transformer
            
        elif method == 'power':
            # Power transformer (Yeo-Johnson) for skewed data
            from sklearn.preprocessing import PowerTransformer
            transformer = PowerTransformer(method='yeo-johnson', standardize=True)
            df[columns_to_scale] = transformer.fit_transform(df[columns_to_scale])
            self.transformers['power'] = transformer
        
        logger.info(f"Applied {method} scaling to {len(columns_to_scale)} columns")
        return df
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create sophisticated interaction features
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with interaction features
        """
        df = df.copy()
        
        # Meteorological interactions
        if all(col in df.columns for col in ['T_forecast', 'q_forecast']):
            # Temperature-humidity interaction
            df['temp_humidity_interaction'] = df['T_forecast'] * df['q_forecast']
            df['temp_humidity_ratio'] = df['T_forecast'] / (df['q_forecast'] + 1e-8)
        
        if all(col in df.columns for col in ['wind_speed', 'T_forecast']):
            # Wind-temperature interaction (affects mixing)
            df['wind_temp_interaction'] = df['wind_speed'] * df['T_forecast']
            df['thermal_wind_ratio'] = df['T_forecast'] / (df['wind_speed'] + 0.1)
        
        # Pollution-meteorology interactions
        if all(col in df.columns for col in ['NO2_satellite', 'wind_speed']):
            # Pollution dispersion potential
            df['NO2_dispersion_potential'] = df['NO2_satellite'] / (df['wind_speed'] + 0.1)
        
        if all(col in df.columns for col in ['solar_radiation_proxy', 'T_forecast', 'NO2_satellite']):
            # Photochemical reaction potential
            df['photochemical_reaction_potential'] = (
                df['solar_radiation_proxy'] * df['T_forecast'] * df['NO2_satellite']
            )
        
        # Temporal interactions
        if 'hour' in df.columns:
            # Rush hour indicators
            df['morning_rush'] = ((df['hour'] >= 7) & (df['hour'] <= 10)).astype(int)
            df['evening_rush'] = ((df['hour'] >= 17) & (df['hour'] <= 20)).astype(int)
            df['rush_hour'] = df['morning_rush'] + df['evening_rush']
            
            # Weekend-hour interaction
            if 'is_weekend' in df.columns:
                df['weekend_hour_interaction'] = df['is_weekend'] * df['hour']
        
        # Seasonal interactions
        if all(col in df.columns for col in ['month', 'T_forecast']):
            # Seasonal temperature anomaly
            monthly_temp_mean = df.groupby('month')['T_forecast'].transform('mean')
            df['temp_seasonal_anomaly'] = df['T_forecast'] - monthly_temp_mean
        
        logger.info("Created sophisticated interaction features")
        return df
    
    def create_lag_difference_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create lag and difference features for better temporal modeling
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with lag and difference features
        """
        df = df.copy()
        
        # Key variables for lag features
        key_vars = ['O3_forecast', 'NO2_forecast', 'T_forecast', 'q_forecast', 'wind_speed']
        
        for var in key_vars:
            if var in df.columns:
                # Multiple lag features
                for lag in [1, 2, 3, 6, 12, 24, 48]:
                    df[f'{var}_lag_{lag}'] = df[var].shift(lag)
                
                # Difference features (rate of change)
                for diff in [1, 3, 6, 12]:
                    df[f'{var}_diff_{diff}'] = df[var].diff(diff)
                    df[f'{var}_pct_change_{diff}'] = df[var].pct_change(diff)
                
                # Acceleration (second derivative)
                df[f'{var}_acceleration'] = df[var].diff().diff()
        
        # Cross-variable lag relationships
        if all(col in df.columns for col in ['O3_forecast', 'NO2_forecast']):
            # O3-NO2 lag relationships (important for photochemistry)
            for lag in [1, 3, 6]:
                df[f'O3_NO2_lag_ratio_{lag}'] = df['O3_forecast'] / (df['NO2_forecast'].shift(lag) + 1e-6)
                df[f'NO2_O3_lag_ratio_{lag}'] = df['NO2_forecast'] / (df['O3_forecast'].shift(lag) + 1e-6)
        
        logger.info("Created lag and difference features")
        return df
    
    def enhance_data_quality(
        self, 
        df: pd.DataFrame,
        handle_outliers: bool = True,
        smooth_data: bool = True,
        create_robust_stats: bool = True,
        create_interactions: bool = True,
        create_lags: bool = True,
        scaling_method: str = 'robust'
    ) -> pd.DataFrame:
        """
        Complete data quality enhancement pipeline
        
        Args:
            df: Input dataframe
            handle_outliers: Whether to handle outliers
            smooth_data: Whether to apply smoothing
            create_robust_stats: Whether to create robust statistical features
            create_interactions: Whether to create interaction features
            create_lags: Whether to create lag features
            scaling_method: Scaling method to use
            
        Returns:
            Enhanced dataframe
        """
        logger.info("Starting comprehensive data quality enhancement")
        
        # Store original shape
        original_shape = df.shape
        
        # 1. Handle outliers
        if handle_outliers:
            df = self.detect_and_handle_outliers(df, method='iqr', factor=2.0)
        
        # 2. Apply smoothing
        if smooth_data:
            df = self.smooth_time_series(df)
        
        # 3. Create robust statistical features
        if create_robust_stats:
            df = self.create_robust_features(df)
        
        # 4. Create interaction features
        if create_interactions:
            df = self.create_interaction_features(df)
        
        # 5. Create lag and difference features
        if create_lags:
            df = self.create_lag_difference_features(df)
        
        # 6. Advanced imputation for missing values
        df = self._advanced_imputation(df)
        
        # 7. Apply advanced scaling
        df = self.apply_advanced_scaling(df, method=scaling_method)
        
        # Store quality statistics
        self.quality_stats = {
            'original_shape': original_shape,
            'final_shape': df.shape,
            'features_added': df.shape[1] - original_shape[1],
            'missing_values_pct': (df.isnull().sum().sum() / df.size) * 100
        }
        
        logger.info(f"Data quality enhancement completed:")
        logger.info(f"  Original shape: {original_shape}")
        logger.info(f"  Final shape: {df.shape}")
        logger.info(f"  Features added: {df.shape[1] - original_shape[1]}")
        logger.info(f"  Missing values: {self.quality_stats['missing_values_pct']:.2f}%")
        
        return df
    
    def _advanced_imputation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply advanced imputation techniques
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with imputed values
        """
        df = df.copy()
        
        # Separate numeric and categorical columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # Check if there are missing values
        missing_counts = df[numeric_columns].isnull().sum()
        columns_with_missing = missing_counts[missing_counts > 0].index.tolist()
        
        if columns_with_missing:
            logger.info(f"Applying simple imputation to {len(columns_with_missing)} columns")
            
            # Use simple median imputation for now to avoid dimension issues
            for col in columns_with_missing:
                df[col] = df[col].fillna(df[col].median())
        
        return df
    
    def transform_new_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform new data using fitted transformers
        
        Args:
            df: New dataframe to transform
            
        Returns:
            Transformed dataframe
        """
        df = df.copy()
        
        # Apply same transformations as during fit
        df = self.detect_and_handle_outliers(df, method='iqr', factor=2.0)
        df = self.smooth_time_series(df)
        df = self.create_robust_features(df)
        df = self.create_interaction_features(df)
        df = self.create_lag_difference_features(df)
        
        # Apply fitted transformers
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        if 'imputer' in self.transformers:
            df[numeric_columns] = self.transformers['imputer'].transform(df[numeric_columns])
        
        if 'robust' in self.scalers:
            exclude_columns = ['year', 'month', 'day', 'hour', 'site_id']
            columns_to_scale = [col for col in numeric_columns if col not in exclude_columns]
            df[columns_to_scale] = self.scalers['robust'].transform(df[columns_to_scale])
        
        return df