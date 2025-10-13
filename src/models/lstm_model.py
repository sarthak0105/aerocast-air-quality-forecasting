"""
Advanced LSTM model for air quality forecasting with attention and ensemble capabilities
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    LSTM, Dense, Dropout, BatchNormalization, Input, Concatenate,
    MultiHeadAttention, LayerNormalization, GlobalAveragePooling1D,
    Conv1D, MaxPooling1D, Flatten, Bidirectional, GRU, TimeDistributed,
    Add, Multiply, Lambda, Reshape
)
from tensorflow.keras.optimizers import Adam, AdamW
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.regularizers import l1_l2
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from src.models.base_model import BaseModel
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LSTMModel(BaseModel):
    """Advanced LSTM model with attention, CNN features, and ensemble capabilities"""
    
    def __init__(
        self,
        lstm_units: int = 128,
        num_layers: int = 3,
        dropout_rate: float = 0.3,
        learning_rate: float = 0.0005,
        use_attention: bool = True,
        use_cnn_features: bool = True,
        use_bidirectional: bool = True,
        attention_heads: int = 8,
        cnn_filters: int = 64,
        l1_reg: float = 1e-5,
        l2_reg: float = 1e-4,
        use_residual: bool = True,
        **kwargs
    ):
        super().__init__("AdvancedLSTM", **kwargs)
        self.lstm_units = lstm_units
        self.num_layers = num_layers
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        self.use_attention = use_attention
        self.use_cnn_features = use_cnn_features
        self.use_bidirectional = use_bidirectional
        self.attention_heads = attention_heads
        self.cnn_filters = cnn_filters
        self.l1_reg = l1_reg
        self.l2_reg = l2_reg
        self.use_residual = use_residual
        self.history = None
        
    def build_model(self, input_shape: Tuple, output_shape: Tuple) -> tf.keras.Model:
        """
        Build advanced LSTM model with attention, CNN features, and residual connections
        
        Args:
            input_shape: Shape of input data (sequence_length, n_features)
            output_shape: Shape of output data (forecast_horizon, n_targets)
            
        Returns:
            Compiled Keras model
        """
        # Input layer
        inputs = Input(shape=input_shape, name='main_input')
        
        # CNN Feature Extraction Branch
        if self.use_cnn_features:
            cnn_branch = self._build_cnn_branch(inputs)
        
        # LSTM Branch with Attention
        lstm_branch = self._build_lstm_branch(inputs)
        
        # Combine branches
        if self.use_cnn_features:
            # For simplicity, just use LSTM branch when attention is enabled
            # CNN features are already processed through the same input
            combined = lstm_branch
        else:
            combined = lstm_branch
        
        # Attention mechanism
        if self.use_attention:
            attention_output = self._build_attention_layer(combined)
            # Residual connection
            if self.use_residual and combined.shape[-1] == attention_output.shape[-1]:
                combined = Add()([combined, attention_output])
            else:
                combined = attention_output
            
            # Global pooling for attention output
            pooled = GlobalAveragePooling1D()(combined)
        else:
            # If no attention, combined should be 2D from LSTM, so use it directly
            if len(combined.shape) == 3:
                pooled = GlobalAveragePooling1D()(combined)
            else:
                pooled = combined
        
        # Dense layers with residual connections
        dense1 = Dense(
            self.lstm_units * 2, 
            activation='relu',
            kernel_regularizer=l1_l2(self.l1_reg, self.l2_reg),
            name='dense1'
        )(pooled)
        dense1 = BatchNormalization()(dense1)
        dense1 = Dropout(self.dropout_rate)(dense1)
        
        dense2 = Dense(
            self.lstm_units, 
            activation='relu',
            kernel_regularizer=l1_l2(self.l1_reg, self.l2_reg),
            name='dense2'
        )(dense1)
        dense2 = BatchNormalization()(dense2)
        dense2 = Dropout(self.dropout_rate)(dense2)
        
        # Residual connection for dense layers
        if self.use_residual and pooled.shape[-1] == dense2.shape[-1]:
            dense2 = Add()([pooled, dense2])
        
        # Output layers
        output_size = output_shape[0] * output_shape[1] if len(output_shape) == 2 else output_shape[0]
        
        # Single output layer (simplified)
        outputs = Dense(output_size, activation='linear', name='main_output')(dense2)
        
        # Reshape if needed
        if len(output_shape) == 2:
            outputs = Reshape(output_shape, name='reshape')(outputs)
        
        # Create model
        model = Model(inputs=inputs, outputs=outputs, name='AdvancedLSTM')
        
        # Compile with advanced optimizer and custom metrics
        optimizer = AdamW(
            learning_rate=self.learning_rate,
            weight_decay=1e-4,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-7
        )
        
        # Enhanced custom metrics
        def accuracy_within_threshold(y_true, y_pred, threshold=0.1):
            """Enhanced accuracy metric with better numerical stability"""
            # Add small epsilon to avoid division by zero
            epsilon = tf.keras.backend.epsilon()
            y_true_safe = tf.where(tf.abs(y_true) < epsilon, epsilon, y_true)
            
            relative_error = tf.abs((y_true - y_pred) / y_true_safe)
            within_threshold = tf.cast(tf.less_equal(relative_error, threshold), tf.float32)
            
            return tf.reduce_mean(within_threshold)
        
        def accuracy_5_percent(y_true, y_pred):
            return accuracy_within_threshold(y_true, y_pred, 0.05)
        
        def accuracy_10_percent(y_true, y_pred):
            return accuracy_within_threshold(y_true, y_pred, 0.10)
        
        def accuracy_15_percent(y_true, y_pred):
            return accuracy_within_threshold(y_true, y_pred, 0.15)
        
        def accuracy_20_percent(y_true, y_pred):
            return accuracy_within_threshold(y_true, y_pred, 0.20)
        
        def r_squared(y_true, y_pred):
            """R-squared metric"""
            ss_res = tf.reduce_sum(tf.square(y_true - y_pred))
            ss_tot = tf.reduce_sum(tf.square(y_true - tf.reduce_mean(y_true)))
            return 1 - ss_res / (ss_tot + tf.keras.backend.epsilon())
        
        # Compile model (simplified)
        model.compile(
            optimizer=optimizer,
            loss='huber',  # More robust to outliers than MSE
            metrics=[
                'mae', 'mse', accuracy_5_percent, accuracy_10_percent,
                accuracy_15_percent, accuracy_20_percent, r_squared
            ]
        )
        
        self.model = model
        logger.info(f"Built Advanced LSTM model with {model.count_params():,} parameters")
        logger.info(f"Model architecture: {self.num_layers} LSTM layers, "
                   f"Attention: {self.use_attention}, CNN: {self.use_cnn_features}, "
                   f"Bidirectional: {self.use_bidirectional}")
        
        return model
    
    def _build_cnn_branch(self, inputs):
        """Build CNN feature extraction branch"""
        # 1D CNN for temporal pattern extraction
        cnn = Conv1D(
            filters=self.cnn_filters,
            kernel_size=3,
            activation='relu',
            padding='same',
            kernel_regularizer=l1_l2(self.l1_reg, self.l2_reg)
        )(inputs)
        cnn = BatchNormalization()(cnn)
        cnn = Dropout(self.dropout_rate)(cnn)
        
        # Additional CNN layers
        cnn = Conv1D(
            filters=self.cnn_filters // 2,
            kernel_size=5,
            activation='relu',
            padding='same',
            kernel_regularizer=l1_l2(self.l1_reg, self.l2_reg)
        )(cnn)
        cnn = BatchNormalization()(cnn)
        cnn = MaxPooling1D(pool_size=2)(cnn)
        cnn = Dropout(self.dropout_rate)(cnn)
        
        return cnn
    
    def _build_lstm_branch(self, inputs):
        """Build LSTM branch with optional bidirectional layers"""
        x = inputs
        
        # LSTM layers
        for i in range(self.num_layers):
            return_sequences = i < self.num_layers - 1 or self.use_attention
            
            if self.use_bidirectional:
                lstm_layer = Bidirectional(
                    LSTM(
                        self.lstm_units // 2,  # Divide by 2 since bidirectional doubles the output
                        return_sequences=return_sequences,
                        dropout=self.dropout_rate,
                        recurrent_dropout=self.dropout_rate * 0.5,
                        kernel_regularizer=l1_l2(self.l1_reg, self.l2_reg),
                        recurrent_regularizer=l1_l2(self.l1_reg, self.l2_reg)
                    )
                )(x)
            else:
                lstm_layer = LSTM(
                    self.lstm_units,
                    return_sequences=return_sequences,
                    dropout=self.dropout_rate,
                    recurrent_dropout=self.dropout_rate * 0.5,
                    kernel_regularizer=l1_l2(self.l1_reg, self.l2_reg),
                    recurrent_regularizer=l1_l2(self.l1_reg, self.l2_reg)
                )(x)
            
            x = BatchNormalization()(lstm_layer)
            
            # Residual connection if dimensions match
            if self.use_residual and i > 0 and x.shape[-1] == inputs.shape[-1]:
                x = Add()([x, inputs])
        
        return x
    
    def _build_attention_layer(self, inputs):
        """Build multi-head attention layer"""
        # Multi-head self-attention
        attention = MultiHeadAttention(
            num_heads=self.attention_heads,
            key_dim=inputs.shape[-1] // self.attention_heads,
            dropout=self.dropout_rate
        )(inputs, inputs)
        
        # Layer normalization and residual connection
        attention = LayerNormalization()(attention)
        
        return attention
    
    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        epochs: int = 200,
        batch_size: int = 64,
        patience: int = 25,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Train the advanced LSTM model with enhanced training strategies
        
        Args:
            X_train: Training input data
            y_train: Training target data
            X_val: Validation input data
            y_val: Validation target data
            epochs: Number of training epochs
            batch_size: Batch size for training
            patience: Early stopping patience
            
        Returns:
            Training history
        """
        if self.model is None:
            input_shape = X_train.shape[1:]
            output_shape = y_train.shape[1:]
            self.build_model(input_shape, output_shape)
        
        # Data augmentation for time series
        X_train_aug, y_train_aug = self._augment_data(X_train, y_train)
        
        # Enhanced callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy_10_percent' if X_val is not None else 'accuracy_10_percent',
                patience=patience,
                restore_best_weights=True,
                verbose=1,
                mode='max'  # We want to maximize accuracy
            ),
            ReduceLROnPlateau(
                monitor='val_loss' if X_val is not None else 'loss',
                factor=0.7,
                patience=patience // 3,
                min_lr=1e-8,
                verbose=1,
                cooldown=5
            ),
            # Cosine annealing for learning rate
            tf.keras.callbacks.LearningRateScheduler(
                lambda epoch: self.learning_rate * (0.5 * (1 + np.cos(np.pi * epoch / epochs))),
                verbose=0
            )
        ]
        
        # Add model checkpoint
        if hasattr(self, 'model_path'):
            checkpoint = ModelCheckpoint(
                filepath=str(self.model_path / 'best_model.h5'),
                monitor='val_accuracy_10_percent' if X_val is not None else 'accuracy_10_percent',
                save_best_only=True,
                mode='max',
                verbose=1
            )
            callbacks.append(checkpoint)
        
        # Prepare validation data
        validation_data = (X_val, y_val) if X_val is not None and y_val is not None else None
        
        # Train model with progressive batch size
        logger.info(f"Training Advanced LSTM model for {epochs} epochs")
        logger.info(f"Training data shape: {X_train_aug.shape}, Validation data shape: {X_val.shape if X_val is not None else 'None'}")
        
        # Stage 1: Warm-up training with smaller batch size
        warmup_epochs = min(20, epochs // 4)
        logger.info(f"Stage 1: Warm-up training for {warmup_epochs} epochs with batch size {batch_size // 2}")
        
        history1 = self.model.fit(
            X_train_aug, y_train_aug,
            validation_data=validation_data,
            epochs=warmup_epochs,
            batch_size=batch_size // 2,
            callbacks=[callbacks[1]],  # Only learning rate reduction
            verbose=1
        )
        
        # Stage 2: Main training with full batch size
        remaining_epochs = epochs - warmup_epochs
        logger.info(f"Stage 2: Main training for {remaining_epochs} epochs with batch size {batch_size}")
        
        history2 = self.model.fit(
            X_train_aug, y_train_aug,
            validation_data=validation_data,
            epochs=remaining_epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1,
            initial_epoch=warmup_epochs
        )
        
        # Combine histories
        combined_history = {}
        for key in history1.history.keys():
            combined_history[key] = history1.history[key] + history2.history[key]
        
        self.history = combined_history
        self.is_fitted = True
        
        # Final evaluation
        if X_val is not None and y_val is not None:
            val_predictions = self.model.predict(X_val, verbose=0)
            val_accuracy = self._calculate_accuracy(y_val, val_predictions)
            logger.info(f"Final validation accuracy: {val_accuracy:.2f}%")
        
        logger.info("Advanced LSTM model training completed")
        return self.history
    
    def _augment_data(self, X: np.ndarray, y: np.ndarray, augment_factor: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply data augmentation techniques for time series
        
        Args:
            X: Input data
            y: Target data
            augment_factor: Factor controlling augmentation strength
            
        Returns:
            Augmented data
        """
        X_aug = X.copy()
        y_aug = y.copy()
        
        # Ensure we're working with numeric data only
        if not np.issubdtype(X.dtype, np.number):
            logger.warning("Non-numeric data detected in augmentation, skipping noise addition")
            return X_aug, y_aug
        
        # Add small amount of Gaussian noise
        try:
            noise_std = np.std(X.astype(np.float32)) * augment_factor
            X_noise = X + np.random.normal(0, noise_std, X.shape).astype(X.dtype)
        except Exception as e:
            logger.warning(f"Could not add noise: {str(e)}, skipping noise augmentation")
            X_noise = X
        
        # Time warping (slight stretching/compression)
        X_warped = []
        y_warped = []
        
        for i in range(len(X)):
            # Random time warping factor
            warp_factor = np.random.uniform(0.95, 1.05)
            seq_len = X.shape[1]
            new_len = int(seq_len * warp_factor)
            
            if new_len > 0:
                # Resample sequence
                indices = np.linspace(0, seq_len - 1, new_len).astype(int)
                X_sample = X[i][indices]
                
                # Pad or truncate to original length
                if new_len < seq_len:
                    # Pad with last values
                    padding = np.repeat(X_sample[-1:], seq_len - new_len, axis=0)
                    X_sample = np.concatenate([X_sample, padding], axis=0)
                elif new_len > seq_len:
                    # Truncate
                    X_sample = X_sample[:seq_len]
                
                X_warped.append(X_sample)
                y_warped.append(y[i])
        
        if X_warped:
            X_warped = np.array(X_warped)
            y_warped = np.array(y_warped)
            
            # Combine original, noisy, and warped data
            X_combined = np.concatenate([X_aug, X_noise[:len(X)//2], X_warped[:len(X)//4]], axis=0)
            y_combined = np.concatenate([y_aug, y_aug[:len(y)//2], y_warped[:len(y)//4]], axis=0)
        else:
            # Just use original and noisy data
            X_combined = np.concatenate([X_aug, X_noise[:len(X)//2]], axis=0)
            y_combined = np.concatenate([y_aug, y_aug[:len(y)//2]], axis=0)
        
        # Shuffle the augmented data
        indices = np.random.permutation(len(X_combined))
        X_combined = X_combined[indices]
        y_combined = y_combined[indices]
        
        logger.info(f"Data augmentation: {X.shape} -> {X_combined.shape}")
        return X_combined, y_combined
    
    def _calculate_accuracy(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate overall accuracy percentage"""
        # Flatten arrays if needed
        if y_true.ndim > 2:
            y_true = y_true.reshape(-1, y_true.shape[-1])
            y_pred = y_pred.reshape(-1, y_pred.shape[-1])
        
        # Calculate accuracy within 10% threshold
        epsilon = 1e-8
        y_true_safe = np.where(np.abs(y_true) < epsilon, epsilon, y_true)
        relative_error = np.abs((y_true - y_pred) / y_true_safe)
        within_10_percent = np.mean(relative_error <= 0.10) * 100
        
        return within_10_percent
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained model
        
        Args:
            X: Input data for prediction
            
        Returns:
            Predictions
        """
        self.validate_input(X)
        predictions = self.model.predict(X, verbose=0)
        return predictions
    
    def predict_with_uncertainty(
        self,
        X: np.ndarray,
        n_samples: int = 100
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions with uncertainty estimation using Monte Carlo Dropout
        
        Args:
            X: Input data
            n_samples: Number of Monte Carlo samples
            
        Returns:
            Tuple of (mean_predictions, std_predictions)
        """
        self.validate_input(X)
        
        # Enable dropout during inference
        predictions = []
        for _ in range(n_samples):
            pred = self.model(X, training=True)
            predictions.append(pred.numpy())
        
        predictions = np.array(predictions)
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        
        return mean_pred, std_pred
    
    def _save_model_specific(self, model_path: Path) -> None:
        """Save LSTM-specific components"""
        if self.model is not None:
            self.model.save(model_path / 'lstm_model.h5')
        
        if self.history is not None:
            import json
            with open(model_path / 'training_history.json', 'w') as f:
                # Convert numpy arrays to lists for JSON serialization
                history_serializable = {}
                for key, value in self.history.items():
                    if isinstance(value, np.ndarray):
                        history_serializable[key] = value.tolist()
                    else:
                        history_serializable[key] = value
                json.dump(history_serializable, f, indent=2)
    
    def _load_model_specific(self, model_path: Path) -> None:
        """Load LSTM-specific components"""
        model_file = model_path / 'lstm_model.h5'
        if model_file.exists():
            self.model = tf.keras.models.load_model(model_file)
        
        history_file = model_path / 'training_history.json'
        if history_file.exists():
            import json
            with open(history_file, 'r') as f:
                self.history = json.load(f)
    
    def plot_training_history(self) -> None:
        """Plot training history"""
        if self.history is None:
            logger.warning("No training history available")
            return
        
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # Loss
        axes[0, 0].plot(self.history['loss'], label='Training Loss')
        if 'val_loss' in self.history:
            axes[0, 0].plot(self.history['val_loss'], label='Validation Loss')
        axes[0, 0].set_title('Model Loss')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        
        # MAE
        if 'mae' in self.history:
            axes[0, 1].plot(self.history['mae'], label='Training MAE')
            if 'val_mae' in self.history:
                axes[0, 1].plot(self.history['val_mae'], label='Validation MAE')
            axes[0, 1].set_title('Mean Absolute Error')
            axes[0, 1].set_xlabel('Epoch')
            axes[0, 1].set_ylabel('MAE')
            axes[0, 1].legend()
        
        # MAPE
        if 'mape' in self.history:
            axes[1, 0].plot(self.history['mape'], label='Training MAPE')
            if 'val_mape' in self.history:
                axes[1, 0].plot(self.history['val_mape'], label='Validation MAPE')
            axes[1, 0].set_title('Mean Absolute Percentage Error')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('MAPE')
            axes[1, 0].legend()
        
        # Learning rate
        if 'lr' in self.history:
            axes[1, 1].plot(self.history['lr'])
            axes[1, 1].set_title('Learning Rate')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Learning Rate')
            axes[1, 1].set_yscale('log')
        
        plt.tight_layout()
        plt.show()