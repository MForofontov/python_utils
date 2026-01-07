"""
Evaluate model performance with comprehensive metrics.
"""

import logging
from typing import Any, Literal
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score
)

logger = logging.getLogger(__name__)


def evaluate_model_performance(
    model: Any,
    X: np.ndarray,
    y_true: np.ndarray,
    task: Literal['classification', 'regression'] = 'classification',
) -> dict[str, float]:
    """
    Evaluate model performance with comprehensive metrics.

    Parameters
    ----------
    model : Any
        Trained sklearn model with predict method.
    X : np.ndarray
        Feature matrix for evaluation.
    y_true : np.ndarray
        True target values.
    task : Literal['classification', 'regression'], optional
        Type of task (by default 'classification').

    Returns
    -------
    dict[str, float]
        Dictionary of performance metrics.
        Classification: accuracy, precision, recall, f1, roc_auc (if binary)
        Regression: mse, rmse, mae, r2

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.linear_model import LogisticRegression
    >>> X = np.random.randn(100, 5)
    >>> y = np.random.randint(0, 2, 100)
    >>> model = LogisticRegression().fit(X, y)
    >>> metrics = evaluate_model_performance(model, X, y, task='classification')
    >>> 'accuracy' in metrics
    True

    >>> # Regression
    >>> from sklearn.linear_model import LinearRegression
    >>> y_reg = np.random.randn(100)
    >>> model_reg = LinearRegression().fit(X, y_reg)
    >>> metrics_reg = evaluate_model_performance(model_reg, X, y_reg, task='regression')
    >>> 'mse' in metrics_reg
    True

    Notes
    -----
    Computes all standard metrics for the task type in one call.
    
    Use battle-tested libraries: Built on sklearn metrics.
    Adds value through: comprehensive metric calculation and convenient interface.

    Complexity
    ----------
    Time: O(n) for prediction and metric calculation, Space: O(n)
    """

    # Type validation
    if not isinstance(X, np.ndarray):
        raise TypeError(f"X must be a numpy array, got {type(X).__name__}")
    if not isinstance(y_true, np.ndarray):
        raise TypeError(f"y_true must be a numpy array, got {type(y_true).__name__}")
    if task not in ('classification', 'regression'):
        raise ValueError(f"task must be 'classification' or 'regression', got {task}")

    # Value validation
    if not hasattr(model, 'predict'):
        raise ValueError("model must have predict method")
    if X.shape[0] != y_true.shape[0]:
        raise ValueError(f"X and y_true must have same number of samples: {X.shape[0]} != {y_true.shape[0]}")
    if X.shape[0] == 0:
        raise ValueError("X cannot be empty")

    # Make predictions
    y_pred = model.predict(X)

    metrics = {}

    if task == 'classification':
        metrics['accuracy'] = float(accuracy_score(y_true, y_pred))
        
        # Handle multiclass vs binary
        n_classes = len(np.unique(y_true))
        average = 'binary' if n_classes == 2 else 'macro'
        
        metrics['precision'] = float(precision_score(y_true, y_pred, average=average, zero_division=0))
        metrics['recall'] = float(recall_score(y_true, y_pred, average=average, zero_division=0))
        metrics['f1'] = float(f1_score(y_true, y_pred, average=average, zero_division=0))

        # ROC AUC for binary classification with predict_proba
        if n_classes == 2 and hasattr(model, 'predict_proba'):
            try:
                y_proba = model.predict_proba(X)[:, 1]
                metrics['roc_auc'] = float(roc_auc_score(y_true, y_proba))
            except Exception:
                logger.debug("Could not calculate ROC AUC")

    else:  # regression
        metrics['mse'] = float(mean_squared_error(y_true, y_pred))
        metrics['rmse'] = float(np.sqrt(metrics['mse']))
        metrics['mae'] = float(mean_absolute_error(y_true, y_pred))
        metrics['r2'] = float(r2_score(y_true, y_pred))

    logger.debug(f"Evaluated {task} model: {len(metrics)} metrics calculated")

    return metrics


__all__ = ['evaluate_model_performance']
