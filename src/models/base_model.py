"""
Base model class for air quality forecasting
"""
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple
import joblib
from pathlib import Path

from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseModel(ABC):
    """Abstract base class for all forecasting models"""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.model = None
        self.is_fitted = False
        self.feature_names = []
        self.target_names = []
        self.model_params = kwargs
        
    @abstractmethod
    def build_model(self, input_shape: Tuple, output_shape: Tuple) -> Any:
        """Build the model architecture"""
        pass
    
    @abstractmethod
    def fit(self, X_train: np.ndarray, y_train: np.ndarray, 
            X_val: Optional[np.ndarray] = None, y_val: Optional[np.ndarray] = None,
            **kwargs) -> Dict[str, Any]:
        """Train the model"""
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        pass
    
    def save_model(self, model_path: Path) -> None:
        """
        Save the trained model
        
        Args:
            model_path: Path to save the model
        """
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Save model-specific components
        self._save_model_specific(model_path)
        
        # Save metadata
        metadata = {
            'model_name': self.model_name,
            'is_fitted': self.is_fitted,
            'feature_names': self.feature_names,
            'target_names': self.target_names,
            'model_params': self.model_params
        }
        
        joblib.dump(metadata, model_path / 'metadata.pkl')
        logger.info(f"Model saved to {model_path}")
    
    def load_model(self, model_path: Path) -> None:
        """
        Load a trained model
        
        Args:
            model_path: Path to load the model from
        """
        # Load metadata
        metadata = joblib.load(model_path / 'metadata.pkl')
        self.model_name = metadata['model_name']
        self.is_fitted = metadata['is_fitted']
        self.feature_names = metadata['feature_names']
        self.target_names = metadata['target_names']
        self.model_params = metadata['model_params']
        
        # Load model-specific components
        self._load_model_specific(model_path)
        
        logger.info(f"Model loaded from {model_path}")
    
    @abstractmethod
    def _save_model_specific(self, model_path: Path) -> None:
        """Save model-specific components"""
        pass
    
    @abstractmethod
    def _load_model_specific(self, model_path: Path) -> None:
        """Load model-specific components"""
        pass
    
    def get_feature_importance(self) -> Optional[Dict[str, float]]:
        """
        Get feature importance if available
        
        Returns:
            Dictionary of feature names and their importance scores
        """
        return None
    
    def validate_input(self, X: np.ndarray) -> None:
        """
        Validate input data
        
        Args:
            X: Input data
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        if X.ndim < 2:
            raise ValueError("Input must be at least 2-dimensional")
    
    def __str__(self) -> str:
        return f"{self.model_name}(fitted={self.is_fitted})"
    
    def __repr__(self) -> str:
        return self.__str__()