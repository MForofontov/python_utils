"""Comprehensive prediction analysis for model diagnostics."""

import logging
from typing import Any, Literal

import numpy as np

logger = logging.getLogger(__name__)


def analyze_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    task: Literal["classification", "regression"] = "regression",
    class_labels: list[str] | None = None,
) -> dict[str, Any]:
    """
    Analyze predictions with comprehensive diagnostics and error patterns.

    Provides detailed analysis beyond basic metrics: error distribution,
    prediction confidence, bias detection, and per-class analysis.

    Parameters
    ----------
    y_true : np.ndarray
        True target values.
    y_pred : np.ndarray
        Predicted values.
    task : Literal['classification', 'regression'], optional
        Type of task (by default 'regression').
    class_labels : list[str] | None, optional
        Class names for classification (by default None uses indices).

    Returns
    -------
    dict[str, Any]
        Comprehensive analysis results:
        - Regression: residuals stats, outliers, bias, heteroscedasticity
        - Classification: per-class errors, confusion patterns, confidence

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> import numpy as np
    >>> y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    >>> y_pred = np.array([1.1, 2.2, 2.8, 4.1, 4.9])
    >>> analysis = analyze_predictions(y_true, y_pred, task='regression')
    >>> 'residuals' in analysis
    True
    >>> 'mean_error' in analysis
    True

    >>> # Classification
    >>> y_true_clf = np.array([0, 1, 1, 0, 1])
    >>> y_pred_clf = np.array([0, 1, 0, 0, 1])
    >>> analysis_clf = analyze_predictions(y_true_clf, y_pred_clf, task='classification')
    >>> 'per_class_accuracy' in analysis_clf
    True

    Notes
    -----
    Provides insights for model debugging and improvement.

    Use battle-tested libraries: Built on numpy statistical functions.
    Adds value through: comprehensive diagnostics, error pattern detection,
    actionable insights beyond basic metrics.

    Complexity
    ----------
    Time: O(n) for analysis, Space: O(n) for residuals/errors
    """
    # Input validation
    if not isinstance(y_true, np.ndarray):
        raise TypeError(f"y_true must be numpy array, got {type(y_true).__name__}")
    if not isinstance(y_pred, np.ndarray):
        raise TypeError(f"y_pred must be numpy array, got {type(y_pred).__name__}")
    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"y_true and y_pred shapes must match: {y_true.shape} vs {y_pred.shape}"
        )
    if not isinstance(task, str):
        raise TypeError(f"task must be str, got {type(task).__name__}")
    if task not in ["classification", "regression"]:
        raise ValueError(f"task must be 'classification' or 'regression', got {task}")
    if len(y_true) == 0:
        raise ValueError("y_true and y_pred cannot be empty")

    result: dict[str, Any] = {}

    if task == "regression":
        # Calculate residuals
        residuals = y_true - y_pred
        result["residuals"] = residuals

        # Basic statistics
        result["mean_error"] = float(np.mean(residuals))
        result["median_error"] = float(np.median(residuals))
        result["std_error"] = float(np.std(residuals))
        result["min_error"] = float(np.min(residuals))
        result["max_error"] = float(np.max(residuals))

        # Outlier detection (>2 std from mean)
        outlier_threshold = 2 * result["std_error"]
        outliers = np.abs(residuals) > outlier_threshold
        result["n_outliers"] = int(np.sum(outliers))
        result["outlier_percentage"] = float(100 * np.sum(outliers) / len(residuals))

        # Bias detection
        result["positive_bias"] = bool(result["mean_error"] > 0)  # Overpredicting
        result["bias_magnitude"] = float(np.abs(result["mean_error"]))

        # Heteroscedasticity check (variance changes with prediction value)
        # Split into quartiles and compare variance
        sorted_indices = np.argsort(y_pred)
        q1_end = len(y_pred) // 4
        q4_start = 3 * len(y_pred) // 4

        q1_residuals = residuals[sorted_indices[:q1_end]]
        q4_residuals = residuals[sorted_indices[q4_start:]]

        if len(q1_residuals) > 1 and len(q4_residuals) > 1:
            var_ratio = np.var(q4_residuals) / (np.var(q1_residuals) + 1e-10)
            result["heteroscedasticity_ratio"] = float(var_ratio)
            result["heteroscedastic"] = bool(var_ratio > 2.0 or var_ratio < 0.5)

        # Percentile errors
        result["error_percentiles"] = {
            "25": float(np.percentile(np.abs(residuals), 25)),
            "50": float(np.percentile(np.abs(residuals), 50)),
            "75": float(np.percentile(np.abs(residuals), 75)),
            "90": float(np.percentile(np.abs(residuals), 90)),
        }

    else:  # classification
        # Ensure integer labels
        y_true = y_true.astype(int)
        y_pred = y_pred.astype(int)

        # Get unique classes
        classes = np.unique(np.concatenate([y_true, y_pred]))
        n_classes = len(classes)

        if class_labels is None:
            class_labels = [f"class_{i}" for i in classes]

        # Per-class analysis
        per_class_correct = {}
        per_class_total = {}
        per_class_accuracy = {}

        for cls, label in zip(classes, class_labels, strict=True):
            mask = y_true == cls
            if np.sum(mask) > 0:
                per_class_total[label] = int(np.sum(mask))
                per_class_correct[label] = int(np.sum(y_pred[mask] == cls))
                per_class_accuracy[label] = float(
                    per_class_correct[label] / per_class_total[label]
                )

        result["per_class_accuracy"] = per_class_accuracy
        result["per_class_total"] = per_class_total
        result["per_class_correct"] = per_class_correct

        # Confusion patterns (most common misclassifications)
        errors = y_true != y_pred
        error_indices = np.where(errors)[0]

        if len(error_indices) > 0:
            confusion_pairs: dict[str, int] = {}
            for idx in error_indices:
                true_cls = int(y_true[idx])
                pred_cls = int(y_pred[idx])
                key = f"{true_cls}->{pred_cls}"
                confusion_pairs[key] = confusion_pairs.get(key, 0) + 1

            # Get top 5 confusion patterns
            sorted_pairs = sorted(
                confusion_pairs.items(), key=lambda x: x[1], reverse=True
            )
            result["top_confusion_patterns"] = dict(sorted_pairs[:5])
        else:
            result["top_confusion_patterns"] = {}

        # Overall statistics
        result["n_errors"] = int(np.sum(errors))
        result["error_rate"] = float(np.sum(errors) / len(y_true))
        result["n_classes"] = n_classes

        # Class balance in errors
        error_class_dist = {}
        for cls, label in zip(classes, class_labels, strict=True):
            error_mask = errors & (y_true == cls)
            error_class_dist[label] = int(np.sum(error_mask))
        result["errors_by_true_class"] = error_class_dist

    return result


__all__ = ["analyze_predictions"]
