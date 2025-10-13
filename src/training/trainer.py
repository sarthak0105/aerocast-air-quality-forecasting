"""
Model training orchestrator for air quality forecasting
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path
import mlflow
import mlflow.tensorflow
from datetime import datetime

from config.settings import settings
from src.models.base_model import BaseModel
from src.models.lstm_model import LSTMModel
from src.preprocessing.feature_engineering import FeatureEngineer
from src.evaluation.metrics import ModelEvaluator
from src.utils.logger import get_logger
from src.utils.helpers import split_time_series

logger = get_logger(__name__)


class ModelTrainer:
    """Orchestrates the training process for air quality forecasting models"""
    
    def __init__(self, experiment_name: str = None):
        self.experiment_name = experiment_name or settings.MLFLOW_EXPERIMENT_NAME
        self.feature_engineer = FeatureEngineer()
        self.evaluator = ModelEvaluator()
        self.models = {}
        
        # Set up MLflow (with error handling)
        try:
            mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
            mlflow.set_experiment(self.experiment_name)
            self.mlflow_available = True
            logger.info("MLflow tracking enabled")
        except Exception as e:
            logger.warning(f"MLflow not available: {str(e)}. Training will continue without tracking.")
            self.mlflow_available = False
        
    def prepare_data(
        self,
        df: pd.DataFrame,
        sequence_length: int = 24,
        forecast_horizon: int = 1,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        use_simple_features: bool = False
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare data for training
        
        Args:
            df: Input dataframe
            sequence_length: Length of input sequences
            forecast_horizon: Number of steps to forecast
            train_ratio: Proportion for training set
            val_ratio: Proportion for validation set
            test_ratio: Proportion for test set
            
        Returns:
            Tuple of (X_train, y_train, X_val, y_val, X_test, y_test)
        """
        logger.info("Preparing data for training")
        
        # Split data chronologically
        train_df, val_df, test_df = split_time_series(
            df, 'datetime', train_ratio, val_ratio, test_ratio
        )
        
        # Feature engineering
        if use_simple_features:
            # Simple feature engineering - just basic numeric columns
            numeric_cols = train_df.select_dtypes(include=[np.number]).columns.tolist()
            if 'datetime' in numeric_cols:
                numeric_cols.remove('datetime')
            
            train_processed = train_df[numeric_cols].copy()
            val_processed = val_df[numeric_cols].copy()
            test_processed = test_df[numeric_cols].copy()
            
            # Simple normalization
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            train_processed = pd.DataFrame(
                scaler.fit_transform(train_processed), 
                columns=numeric_cols, 
                index=train_processed.index
            )
            val_processed = pd.DataFrame(
                scaler.transform(val_processed), 
                columns=numeric_cols, 
                index=val_processed.index
            )
            test_processed = pd.DataFrame(
                scaler.transform(test_processed), 
                columns=numeric_cols, 
                index=test_processed.index
            )
        else:
            # Full feature engineering
            train_processed = self.feature_engineer.fit_transform(train_df)
            val_processed = self.feature_engineer.transform(val_df)
            test_processed = self.feature_engineer.transform(test_df)
        
        # Create sequences
        if use_simple_features:
            # Simple sequence creation
            X_train, y_train = self._create_simple_sequences(
                train_processed, sequence_length, forecast_horizon
            )
            X_val, y_val = self._create_simple_sequences(
                val_processed, sequence_length, forecast_horizon
            )
            X_test, y_test = self._create_simple_sequences(
                test_processed, sequence_length, forecast_horizon
            )
        else:
            # Full feature engineering sequences
            X_train, y_train = self.feature_engineer.create_sequences(
                train_processed, sequence_length, forecast_horizon
            )
            X_val, y_val = self.feature_engineer.create_sequences(
                val_processed, sequence_length, forecast_horizon
            )
            X_test, y_test = self.feature_engineer.create_sequences(
            test_processed, sequence_length, forecast_horizon
        )
        
        logger.info(f"Data prepared - Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
        
        return X_train, y_train, X_val, y_val, X_test, y_test
    
    def _create_simple_sequences(self, data: pd.DataFrame, sequence_length: int, 
                                forecast_horizon: int) -> Tuple[np.ndarray, np.ndarray]:
        """Create simple sequences without complex feature engineering"""
        # Assume O3_forecast and NO2_forecast are the targets
        target_cols = ['O3_forecast', 'NO2_forecast']
        
        # Use all numeric columns as features
        feature_cols = [col for col in data.columns if col not in target_cols]
        
        X, y = [], []
        
        for i in range(len(data) - sequence_length - forecast_horizon + 1):
            # Features: sequence of all columns
            X_seq = data.iloc[i:i+sequence_length][feature_cols + target_cols].values
            
            # Targets: next values of O3 and NO2
            y_seq = data.iloc[i+sequence_length:i+sequence_length+forecast_horizon][target_cols].values
            
            X.append(X_seq)
            y.append(y_seq)
        
        return np.array(X), np.array(y)
    
    def train_model(
        self,
        model: BaseModel,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        model_params: Dict[str, Any] = None,
        save_model: bool = True
    ) -> Dict[str, Any]:
        """
        Train a single model
        
        Args:
            model: Model instance to train
            X_train: Training input data
            y_train: Training target data
            X_val: Validation input data
            y_val: Validation target data
            model_params: Additional model parameters
            save_model: Whether to save the trained model
            
        Returns:
            Training results
        """
        model_params = model_params or {}
        
        # Train model with optional MLflow tracking
        if self.mlflow_available:
            with mlflow.start_run(run_name=f"{model.model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
                return self._train_model_core(model, X_train, y_train, X_val, y_val, model_params, save_model)
        else:
            return self._train_model_core(model, X_train, y_train, X_val, y_val, model_params, save_model)
    
    def _train_model_core(
        self,
        model: BaseModel,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        model_params: Dict[str, Any] = None,
        save_model: bool = True
    ) -> Dict[str, Any]:
        """Core training logic without MLflow dependency"""
        model_params = model_params or {}
        
        # Log parameters to MLflow if available
        if self.mlflow_available:
            mlflow.log_params(model.model_params)
            mlflow.log_params(model_params)
        
        # Train model
        logger.info(f"Training {model.model_name} model")
        training_history = model.fit(
            X_train, y_train, X_val, y_val, **model_params
        )
        
        # Make predictions on validation set
        y_val_pred = model.predict(X_val)
        
        # Evaluate model
        val_metrics = self.evaluator.calculate_metrics(y_val, y_val_pred)
        
        # Log metrics to MLflow if available
        if self.mlflow_available:
            for metric_name, metric_value in val_metrics.items():
                if isinstance(metric_value, (int, float)):
                    mlflow.log_metric(f"val_{metric_name}", metric_value)
            
            # Log training history if available
            if hasattr(model, 'history') and model.history:
                for metric, values in model.history.items():
                    if isinstance(values, list) and len(values) > 0:
                        mlflow.log_metric(f"final_{metric}", values[-1])
        
        # Save model
        model_path = None
        if save_model:
            model_path = settings.MODEL_PATH / f"{model.model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            model.save_model(model_path)
            
            # Log model to MLflow if available
            if self.mlflow_available and isinstance(model, LSTMModel):
                try:
                    mlflow.tensorflow.log_model(
                        model.model,
                        artifact_path="model",
                        registered_model_name=f"air_quality_{model.model_name.lower()}"
                    )
                except Exception as e:
                    logger.warning(f"Failed to log model to MLflow: {str(e)}")
        
        # Store model
        self.models[model.model_name] = model
        
        results = {
            'model': model,
            'training_history': training_history,
            'validation_metrics': val_metrics,
            'model_path': model_path
        }
        
        logger.info(f"Training completed for {model.model_name}")
        return results
    
    def train_multiple_models(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        model_configs: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Train multiple models with different configurations
        
        Args:
            X_train: Training input data
            y_train: Training target data
            X_val: Validation input data
            y_val: Validation target data
            model_configs: List of model configurations
            
        Returns:
            Dictionary of training results for each model
        """
        results = {}
        
        for config in model_configs:
            model_type = config.pop('model_type')
            model_params = config.pop('model_params', {})
            training_params = config.pop('training_params', {})
            
            # Create model instance
            if model_type == 'LSTM':
                model = LSTMModel(**model_params)
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            # Train model
            try:
                result = self.train_model(
                    model, X_train, y_train, X_val, y_val, training_params
                )
                results[f"{model_type}_{len(results)}"] = result
            except Exception as e:
                logger.error(f"Failed to train {model_type}: {str(e)}")
                continue
        
        return results
    
    def hyperparameter_search(
        self,
        model_type: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        param_grid: Dict[str, List[Any]],
        n_trials: int = 10
    ) -> Dict[str, Any]:
        """
        Perform hyperparameter search
        
        Args:
            model_type: Type of model to search
            X_train: Training input data
            y_train: Training target data
            X_val: Validation input data
            y_val: Validation target data
            param_grid: Parameter grid for search
            n_trials: Number of trials to run
            
        Returns:
            Best model and parameters
        """
        import optuna
        
        def objective(trial):
            # Sample parameters
            params = {}
            for param_name, param_values in param_grid.items():
                if isinstance(param_values[0], int):
                    params[param_name] = trial.suggest_int(
                        param_name, min(param_values), max(param_values)
                    )
                elif isinstance(param_values[0], float):
                    params[param_name] = trial.suggest_float(
                        param_name, min(param_values), max(param_values)
                    )
                else:
                    params[param_name] = trial.suggest_categorical(
                        param_name, param_values
                    )
            
            # Create and train model
            if model_type == 'LSTM':
                model = LSTMModel(**params)
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            try:
                model.fit(X_train, y_train, X_val, y_val, epochs=50, verbose=0)
                y_val_pred = model.predict(X_val)
                val_metrics = self.evaluator.calculate_metrics(y_val, y_val_pred)
                
                # Return validation RMSE as objective (to minimize)
                return val_metrics.get('rmse', float('inf'))
            except Exception as e:
                logger.error(f"Trial failed: {str(e)}")
                return float('inf')
        
        # Run optimization
        study = optuna.create_study(direction='minimize')
        study.optimize(objective, n_trials=n_trials)
        
        # Train best model
        best_params = study.best_params
        if model_type == 'LSTM':
            best_model = LSTMModel(**best_params)
        
        best_result = self.train_model(
            best_model, X_train, y_train, X_val, y_val
        )
        
        return {
            'best_params': best_params,
            'best_value': study.best_value,
            'best_model': best_model,
            'study': study,
            'training_result': best_result
        }
    
    def evaluate_models(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, Dict[str, Any]]:
        """
        Evaluate all trained models on test set
        
        Args:
            X_test: Test input data
            y_test: Test target data
            
        Returns:
            Evaluation results for each model
        """
        results = {}
        
        for model_name, model in self.models.items():
            logger.info(f"Evaluating {model_name} on test set")
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            test_metrics = self.evaluator.calculate_metrics(y_test, y_pred)
            
            # Generate evaluation plots
            plots = self.evaluator.create_evaluation_plots(
                y_test, y_pred, title=f"{model_name} Test Results"
            )
            
            results[model_name] = {
                'metrics': test_metrics,
                'predictions': y_pred,
                'plots': plots
            }
            
            # Log test metrics to MLflow if available
            if self.mlflow_available:
                try:
                    with mlflow.start_run(run_name=f"{model_name}_test_evaluation"):
                        for metric_name, metric_value in test_metrics.items():
                            if isinstance(metric_value, (int, float)):
                                mlflow.log_metric(f"test_{metric_name}", metric_value)
                except Exception as e:
                    logger.warning(f"Failed to log test metrics to MLflow: {str(e)}")
        
        return results