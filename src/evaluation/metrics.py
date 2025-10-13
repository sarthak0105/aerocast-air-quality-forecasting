"""
Evaluation metrics for air quality forecasting models
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy import stats

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ModelEvaluator:
    """Comprehensive model evaluation for air quality forecasting"""
    
    def __init__(self):
        self.target_names = ['O3_forecast', 'NO2_forecast']
    
    def calculate_metrics(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray,
        target_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive evaluation metrics
        
        Args:
            y_true: True values
            y_pred: Predicted values
            target_names: Names of target variables
            
        Returns:
            Dictionary of metrics
        """
        target_names = target_names or self.target_names
        
        # Ensure arrays are 2D
        if y_true.ndim == 1:
            y_true = y_true.reshape(-1, 1)
        if y_pred.ndim == 1:
            y_pred = y_pred.reshape(-1, 1)
        
        # Handle multi-step forecasts
        if y_true.ndim == 3:
            y_true = y_true.reshape(-1, y_true.shape[-1])
            y_pred = y_pred.reshape(-1, y_pred.shape[-1])
        
        metrics = {}
        
        # Overall metrics
        metrics['rmse'] = np.sqrt(mean_squared_error(y_true, y_pred))
        metrics['mae'] = mean_absolute_error(y_true, y_pred)
        metrics['mape'] = self._mean_absolute_percentage_error(y_true, y_pred)
        metrics['r2'] = r2_score(y_true, y_pred)
        metrics['bias'] = np.mean(y_pred - y_true)
        metrics['normalized_rmse'] = metrics['rmse'] / (np.max(y_true) - np.min(y_true))
        
        # Per-target metrics
        n_targets = y_true.shape[1] if y_true.ndim > 1 else 1
        
        for i in range(n_targets):
            target_name = target_names[i] if i < len(target_names) else f'target_{i}'
            
            if n_targets > 1:
                y_true_i = y_true[:, i]
                y_pred_i = y_pred[:, i]
            else:
                y_true_i = y_true.flatten()
                y_pred_i = y_pred.flatten()
            
            metrics[f'{target_name}_rmse'] = np.sqrt(mean_squared_error(y_true_i, y_pred_i))
            metrics[f'{target_name}_mae'] = mean_absolute_error(y_true_i, y_pred_i)
            metrics[f'{target_name}_mape'] = self._mean_absolute_percentage_error(y_true_i, y_pred_i)
            metrics[f'{target_name}_r2'] = r2_score(y_true_i, y_pred_i)
            metrics[f'{target_name}_bias'] = np.mean(y_pred_i - y_true_i)
            
            # Correlation
            correlation, p_value = stats.pearsonr(y_true_i, y_pred_i)
            metrics[f'{target_name}_correlation'] = correlation
            metrics[f'{target_name}_correlation_pvalue'] = p_value
            
            # Per-target accuracy metrics
            metrics[f'{target_name}_accuracy_within_10_percent'] = self._accuracy_within_threshold(y_true_i, y_pred_i, 0.10)
            metrics[f'{target_name}_accuracy_within_20_percent'] = self._accuracy_within_threshold(y_true_i, y_pred_i, 0.20)
            metrics[f'{target_name}_accuracy_within_10_units'] = self._accuracy_within_absolute_threshold(y_true_i, y_pred_i, 10.0)
            metrics[f'{target_name}_overall_accuracy'] = self._overall_accuracy_score(y_true_i, y_pred_i)
        
        # Additional statistical metrics
        metrics['index_of_agreement'] = self._index_of_agreement(y_true, y_pred)
        metrics['nash_sutcliffe'] = self._nash_sutcliffe_efficiency(y_true, y_pred)
        
        # Accuracy metrics for regression
        metrics['accuracy_within_10_percent'] = self._accuracy_within_threshold(y_true, y_pred, 0.10)
        metrics['accuracy_within_20_percent'] = self._accuracy_within_threshold(y_true, y_pred, 0.20)
        metrics['accuracy_within_30_percent'] = self._accuracy_within_threshold(y_true, y_pred, 0.30)
        
        # Absolute accuracy (within fixed thresholds)
        metrics['accuracy_within_5_units'] = self._accuracy_within_absolute_threshold(y_true, y_pred, 5.0)
        metrics['accuracy_within_10_units'] = self._accuracy_within_absolute_threshold(y_true, y_pred, 10.0)
        metrics['accuracy_within_15_units'] = self._accuracy_within_absolute_threshold(y_true, y_pred, 15.0)
        
        # Overall accuracy score (custom metric)
        metrics['overall_accuracy_score'] = self._overall_accuracy_score(y_true, y_pred)
        
        logger.info(f"Calculated metrics: RMSE={metrics['rmse']:.3f}, MAE={metrics['mae']:.3f}, R²={metrics['r2']:.3f}")
        
        return metrics
    
    def _mean_absolute_percentage_error(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Absolute Percentage Error"""
        # Avoid division by zero
        mask = y_true != 0
        if not np.any(mask):
            return np.inf
        
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    
    def _index_of_agreement(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Willmott's Index of Agreement"""
        y_true_mean = np.mean(y_true)
        numerator = np.sum((y_true - y_pred) ** 2)
        denominator = np.sum((np.abs(y_pred - y_true_mean) + np.abs(y_true - y_true_mean)) ** 2)
        
        if denominator == 0:
            return 1.0
        
        return 1 - (numerator / denominator)
    
    def _nash_sutcliffe_efficiency(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Nash-Sutcliffe Efficiency"""
        y_true_mean = np.mean(y_true)
        numerator = np.sum((y_true - y_pred) ** 2)
        denominator = np.sum((y_true - y_true_mean) ** 2)
        
        if denominator == 0:
            return 1.0
        
        return 1 - (numerator / denominator)
    
    def _accuracy_within_threshold(self, y_true: np.ndarray, y_pred: np.ndarray, threshold: float) -> float:
        """
        Calculate accuracy as percentage of predictions within a relative threshold
        
        Args:
            y_true: True values
            y_pred: Predicted values
            threshold: Relative threshold (e.g., 0.10 for 10%)
            
        Returns:
            Accuracy as percentage (0-100)
        """
        # Avoid division by zero
        mask = y_true != 0
        if not np.any(mask):
            return 0.0
        
        y_true_masked = y_true[mask]
        y_pred_masked = y_pred[mask]
        
        relative_error = np.abs((y_true_masked - y_pred_masked) / y_true_masked)
        within_threshold = relative_error <= threshold
        
        return np.mean(within_threshold) * 100
    
    def _accuracy_within_absolute_threshold(self, y_true: np.ndarray, y_pred: np.ndarray, threshold: float) -> float:
        """
        Calculate accuracy as percentage of predictions within an absolute threshold
        
        Args:
            y_true: True values
            y_pred: Predicted values
            threshold: Absolute threshold (e.g., 5.0 for ±5 μg/m³)
            
        Returns:
            Accuracy as percentage (0-100)
        """
        absolute_error = np.abs(y_true - y_pred)
        within_threshold = absolute_error <= threshold
        
        return np.mean(within_threshold) * 100
    
    def _overall_accuracy_score(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate overall accuracy score combining multiple factors
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Overall accuracy score (0-100)
        """
        # Combine different accuracy measures with weights
        acc_10_pct = self._accuracy_within_threshold(y_true, y_pred, 0.10)
        acc_20_pct = self._accuracy_within_threshold(y_true, y_pred, 0.20)
        acc_10_units = self._accuracy_within_absolute_threshold(y_true, y_pred, 10.0)
        
        # R² contribution (normalized to 0-100)
        r2 = r2_score(y_true, y_pred)
        r2_contribution = max(0, min(100, r2 * 100))
        
        # Weighted combination
        overall_score = (
            0.3 * acc_10_pct +      # 30% weight for ±10% accuracy
            0.2 * acc_20_pct +      # 20% weight for ±20% accuracy
            0.3 * acc_10_units +    # 30% weight for ±10 units accuracy
            0.2 * r2_contribution   # 20% weight for R² score
        )
        
        return overall_score
    
    def create_evaluation_plots(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        target_names: Optional[List[str]] = None,
        title: str = "Model Evaluation",
        save_path: Optional[str] = None
    ) -> Dict[str, plt.Figure]:
        """
        Create comprehensive evaluation plots
        
        Args:
            y_true: True values
            y_pred: Predicted values
            target_names: Names of target variables
            title: Plot title
            save_path: Path to save plots
            
        Returns:
            Dictionary of matplotlib figures
        """
        target_names = target_names or self.target_names
        plots = {}
        
        # Ensure arrays are 2D
        if y_true.ndim == 1:
            y_true = y_true.reshape(-1, 1)
        if y_pred.ndim == 1:
            y_pred = y_pred.reshape(-1, 1)
        
        # Handle multi-step forecasts
        if y_true.ndim == 3:
            y_true = y_true.reshape(-1, y_true.shape[-1])
            y_pred = y_pred.reshape(-1, y_pred.shape[-1])
        
        n_targets = y_true.shape[1]
        
        # 1. Scatter plot (Predicted vs Actual)
        fig, axes = plt.subplots(1, n_targets, figsize=(6*n_targets, 5))
        if n_targets == 1:
            axes = [axes]
        
        for i, ax in enumerate(axes):
            target_name = target_names[i] if i < len(target_names) else f'Target {i+1}'
            
            y_true_i = y_true[:, i]
            y_pred_i = y_pred[:, i]
            
            ax.scatter(y_true_i, y_pred_i, alpha=0.6, s=20)
            
            # Perfect prediction line
            min_val = min(np.min(y_true_i), np.min(y_pred_i))
            max_val = max(np.max(y_true_i), np.max(y_pred_i))
            ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
            
            # Regression line
            z = np.polyfit(y_true_i, y_pred_i, 1)
            p = np.poly1d(z)
            ax.plot(y_true_i, p(y_true_i), 'b-', alpha=0.8, label=f'Fit: y={z[0]:.2f}x+{z[1]:.2f}')
            
            ax.set_xlabel(f'Actual {target_name}')
            ax.set_ylabel(f'Predicted {target_name}')
            ax.set_title(f'{target_name} - Predicted vs Actual')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.suptitle(f'{title} - Scatter Plot')
        plt.tight_layout()
        plots['scatter'] = fig
        
        # 2. Time series plot
        fig, axes = plt.subplots(n_targets, 1, figsize=(12, 4*n_targets))
        if n_targets == 1:
            axes = [axes]
        
        for i, ax in enumerate(axes):
            target_name = target_names[i] if i < len(target_names) else f'Target {i+1}'
            
            y_true_i = y_true[:, i]
            y_pred_i = y_pred[:, i]
            
            # Plot subset of data for clarity
            n_points = min(500, len(y_true_i))
            indices = np.linspace(0, len(y_true_i)-1, n_points, dtype=int)
            
            ax.plot(indices, y_true_i[indices], label='Actual', alpha=0.8)
            ax.plot(indices, y_pred_i[indices], label='Predicted', alpha=0.8)
            
            ax.set_xlabel('Time Index')
            ax.set_ylabel(f'{target_name} Concentration')
            ax.set_title(f'{target_name} - Time Series Comparison')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.suptitle(f'{title} - Time Series')
        plt.tight_layout()
        plots['timeseries'] = fig
        
        # 3. Residual plots
        fig, axes = plt.subplots(2, n_targets, figsize=(6*n_targets, 8))
        if n_targets == 1:
            axes = axes.reshape(-1, 1)
        
        for i in range(n_targets):
            target_name = target_names[i] if i < len(target_names) else f'Target {i+1}'
            
            y_true_i = y_true[:, i]
            y_pred_i = y_pred[:, i]
            residuals = y_true_i - y_pred_i
            
            # Residuals vs Predicted
            axes[0, i].scatter(y_pred_i, residuals, alpha=0.6, s=20)
            axes[0, i].axhline(y=0, color='r', linestyle='--')
            axes[0, i].set_xlabel(f'Predicted {target_name}')
            axes[0, i].set_ylabel('Residuals')
            axes[0, i].set_title(f'{target_name} - Residuals vs Predicted')
            axes[0, i].grid(True, alpha=0.3)
            
            # Residual histogram
            axes[1, i].hist(residuals, bins=30, alpha=0.7, edgecolor='black')
            axes[1, i].axvline(x=0, color='r', linestyle='--')
            axes[1, i].set_xlabel('Residuals')
            axes[1, i].set_ylabel('Frequency')
            axes[1, i].set_title(f'{target_name} - Residual Distribution')
            axes[1, i].grid(True, alpha=0.3)
        
        plt.suptitle(f'{title} - Residual Analysis')
        plt.tight_layout()
        plots['residuals'] = fig
        
        # 4. Error distribution by pollution level
        fig, axes = plt.subplots(1, n_targets, figsize=(6*n_targets, 5))
        if n_targets == 1:
            axes = [axes]
        
        for i, ax in enumerate(axes):
            target_name = target_names[i] if i < len(target_names) else f'Target {i+1}'
            
            y_true_i = y_true[:, i]
            y_pred_i = y_pred[:, i]
            
            # Create pollution level bins
            percentiles = [0, 25, 50, 75, 90, 100]
            bins = np.percentile(y_true_i, percentiles)
            bin_labels = ['Low', 'Moderate', 'High', 'Very High', 'Extreme']
            
            # Calculate errors for each bin
            errors_by_bin = []
            for j in range(len(bins)-1):
                mask = (y_true_i >= bins[j]) & (y_true_i < bins[j+1])
                if j == len(bins)-2:  # Last bin includes the maximum
                    mask = (y_true_i >= bins[j]) & (y_true_i <= bins[j+1])
                
                if np.any(mask):
                    errors = np.abs(y_true_i[mask] - y_pred_i[mask])
                    errors_by_bin.append(errors)
                else:
                    errors_by_bin.append([])
            
            # Box plot
            ax.boxplot(errors_by_bin, labels=bin_labels)
            ax.set_xlabel('Pollution Level')
            ax.set_ylabel('Absolute Error')
            ax.set_title(f'{target_name} - Error by Pollution Level')
            ax.grid(True, alpha=0.3)
        
        plt.suptitle(f'{title} - Error Analysis by Pollution Level')
        plt.tight_layout()
        plots['error_by_level'] = fig
        
        # Save plots if path provided
        if save_path:
            for plot_name, fig in plots.items():
                fig.savefig(f"{save_path}_{plot_name}.png", dpi=300, bbox_inches='tight')
        
        return plots
    
    def create_metrics_summary(
        self,
        metrics: Dict[str, Any],
        target_names: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Create a summary table of metrics
        
        Args:
            metrics: Dictionary of calculated metrics
            target_names: Names of target variables
            
        Returns:
            DataFrame with metrics summary
        """
        target_names = target_names or self.target_names
        
        # Overall metrics
        overall_metrics = {
            'RMSE': metrics.get('rmse', np.nan),
            'MAE': metrics.get('mae', np.nan),
            'MAPE (%)': metrics.get('mape', np.nan),
            'R²': metrics.get('r2', np.nan),
            'Bias': metrics.get('bias', np.nan),
            'Index of Agreement': metrics.get('index_of_agreement', np.nan),
            'Nash-Sutcliffe': metrics.get('nash_sutcliffe', np.nan)
        }
        
        summary_data = {'Overall': overall_metrics}
        
        # Per-target metrics
        for target_name in target_names:
            target_metrics = {
                'RMSE': metrics.get(f'{target_name}_rmse', np.nan),
                'MAE': metrics.get(f'{target_name}_mae', np.nan),
                'MAPE (%)': metrics.get(f'{target_name}_mape', np.nan),
                'R²': metrics.get(f'{target_name}_r2', np.nan),
                'Bias': metrics.get(f'{target_name}_bias', np.nan),
                'Correlation': metrics.get(f'{target_name}_correlation', np.nan)
            }
            summary_data[target_name] = target_metrics
        
        summary_df = pd.DataFrame(summary_data).round(4)
        
        return summary_df
    
    def compare_models(
        self,
        model_results: Dict[str, Dict[str, Any]],
        metric: str = 'rmse'
    ) -> pd.DataFrame:
        """
        Compare multiple models based on a specific metric
        
        Args:
            model_results: Dictionary of model results
            metric: Metric to compare models on
            
        Returns:
            DataFrame with model comparison
        """
        comparison_data = []
        
        for model_name, results in model_results.items():
            metrics = results.get('metrics', {})
            
            row = {
                'Model': model_name,
                'RMSE': metrics.get('rmse', np.nan),
                'MAE': metrics.get('mae', np.nan),
                'MAPE (%)': metrics.get('mape', np.nan),
                'R²': metrics.get('r2', np.nan),
                'Bias': metrics.get('bias', np.nan)
            }
            
            # Add per-target metrics
            for target_name in self.target_names:
                row[f'{target_name}_RMSE'] = metrics.get(f'{target_name}_rmse', np.nan)
                row[f'{target_name}_R²'] = metrics.get(f'{target_name}_r2', np.nan)
            
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Sort by the specified metric (ascending for error metrics, descending for R²)
        ascending = metric.lower() not in ['r2', 'correlation', 'index_of_agreement', 'nash_sutcliffe']
        comparison_df = comparison_df.sort_values(metric.upper(), ascending=ascending)
        
        return comparison_df.round(4)
    
    def create_accuracy_summary(self, metrics: Dict[str, Any]) -> None:
        """
        Print a comprehensive accuracy summary
        
        Args:
            metrics: Dictionary of calculated metrics
        """
        print("\n" + "="*60)
        print("ACCURACY SUMMARY")
        print("="*60)
        
        # Overall accuracy
        overall_acc = metrics.get('overall_accuracy_score', 0)
        print(f"Overall Model Accuracy: {overall_acc:.1f}%")
        
        # Accuracy categories
        if overall_acc >= 80:
            accuracy_grade = "Excellent (A)"
        elif overall_acc >= 70:
            accuracy_grade = "Good (B)"
        elif overall_acc >= 60:
            accuracy_grade = "Fair (C)"
        elif overall_acc >= 50:
            accuracy_grade = "Poor (D)"
        else:
            accuracy_grade = "Very Poor (F)"
        
        print(f"Accuracy Grade: {accuracy_grade}")
        
        print("\nAccuracy Breakdown:")
        print(f"  Within ±10%: {metrics.get('accuracy_within_10_percent', 0):.1f}%")
        print(f"  Within ±20%: {metrics.get('accuracy_within_20_percent', 0):.1f}%")
        print(f"  Within ±30%: {metrics.get('accuracy_within_30_percent', 0):.1f}%")
        
        print(f"\nAbsolute Accuracy:")
        print(f"  Within ±5 μg/m³: {metrics.get('accuracy_within_5_units', 0):.1f}%")
        print(f"  Within ±10 μg/m³: {metrics.get('accuracy_within_10_units', 0):.1f}%")
        print(f"  Within ±15 μg/m³: {metrics.get('accuracy_within_15_units', 0):.1f}%")
        
        # Per-pollutant accuracy
        print(f"\nPer-Pollutant Accuracy:")
        for target in ['O3_forecast', 'NO2_forecast']:
            pollutant = target.replace('_forecast', '')
            acc_key = f'{target}_overall_accuracy'
            if acc_key in metrics:
                print(f"  {pollutant}: {metrics[acc_key]:.1f}%")
        
        # Statistical measures
        print(f"\nStatistical Measures:")
        print(f"  R² Score: {metrics.get('r2', 0):.3f}")
        print(f"  RMSE: {metrics.get('rmse', 0):.2f} μg/m³")
        print(f"  MAE: {metrics.get('mae', 0):.2f} μg/m³")
        
        print("="*60)