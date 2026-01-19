"""
Unit tests for perform_t_test function.

Tests cover normal operation, edge cases, and error conditions.
"""

try:
    import numpy as np
    import scipy
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None  # type: ignore
    scipy = None  # type: ignore

import pytest
from python_utils.scientific_computing_functions.statistical_analysis.perform_t_test import (
    perform_t_test,
)

pytestmark = pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy/scipy not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.scientific_computing]

# Normal operation tests


def test_perform_t_test_equal_variances() -> None:
    """Test case 1: Normal operation with equal variances."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [3, 4, 5, 6, 7]

    # Act
    result = perform_t_test(group1, group2, equal_var=True)

    # Assert
    assert "statistic" in result
    assert "pvalue" in result
    assert "significant" in result
    assert "cohens_d" in result
    assert "effect_size_interpretation" in result
    assert result["statistic"] < 0  # group1 mean < group2 mean


def test_perform_t_test_unequal_variances() -> None:
    """Test case 2: Normal operation with unequal variances (Welch's t-test)."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [10, 20, 30, 40, 50]

    # Act
    result = perform_t_test(group1, group2, equal_var=False)

    # Assert
    assert result["statistic"] < 0  # group1 mean < group2 mean
    assert result["pvalue"] < 0.05  # Significant difference
    assert result["significant"]


def test_perform_t_test_two_sided() -> None:
    """Test case 3: Normal operation with two-sided alternative."""
    # Arrange
    group1 = [10, 12, 14, 16, 18]
    group2 = [11, 13, 15, 17, 19]

    # Act
    result = perform_t_test(group1, group2, alternative="two-sided")

    # Assert
    assert result["pvalue"] > 0  # Valid p-value
    assert "cohens_d" in result


def test_perform_t_test_greater_alternative() -> None:
    """Test case 4: Normal operation with greater alternative."""
    # Arrange
    group1 = [10, 11, 12, 13, 14]
    group2 = [5, 6, 7, 8, 9]

    # Act
    result = perform_t_test(group1, group2, alternative="greater")

    # Assert
    assert result["statistic"] > 0  # group1 mean > group2 mean
    assert result["pvalue"] < 0.05  # Significant


def test_perform_t_test_less_alternative() -> None:
    """Test case 5: Normal operation with less alternative."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [6, 7, 8, 9, 10]

    # Act
    result = perform_t_test(group1, group2, alternative="less")

    # Assert
    assert result["statistic"] < 0  # group1 mean < group2 mean
    assert result["pvalue"] < 0.05  # Significant


def test_perform_t_test_numpy_arrays() -> None:
    """Test case 6: Normal operation with numpy arrays."""
    # Arrange
    group1 = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    group2 = np.array([3.0, 4.0, 5.0, 6.0, 7.0])

    # Act
    result = perform_t_test(group1, group2)

    # Assert
    assert isinstance(result["statistic"], (float, np.floating))
    assert isinstance(result["pvalue"], (float, np.floating))


# Edge case tests


def test_perform_t_test_identical_groups() -> None:
    """Test case 7: Edge case with identical groups."""
    # Arrange
    group1 = [5, 5, 5, 5, 5]
    group2 = [5, 5, 5, 5, 5]

    # Act
    result = perform_t_test(group1, group2)

    # Assert
    assert np.isnan(result["statistic"])  # Undefined for identical groups
    assert np.isnan(result["pvalue"])  # p-value also undefined
    assert not result["significant"]


def test_perform_t_test_small_sample() -> None:
    """Test case 8: Edge case with minimum sample size."""
    # Arrange
    group1 = [1.0, 2.0]
    group2 = [3.0, 4.0]

    # Act
    result = perform_t_test(group1, group2)

    # Assert
    assert "statistic" in result
    assert "pvalue" in result


def test_perform_t_test_large_effect_size() -> None:
    """Test case 9: Edge case with large effect size."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [100, 200, 300, 400, 500]

    # Act
    result = perform_t_test(group1, group2)

    # Assert
    assert abs(result["cohens_d"]) > 0.8  # Large effect size
    assert result["effect_size_interpretation"] in ["medium", "large"]


def test_perform_t_test_high_variance_group() -> None:
    """Test case 10: Edge case with high variance in one group."""
    # Arrange
    group1 = [5, 5, 5, 5, 5]  # No variance
    group2 = [1, 10, 1, 10, 5]  # High variance

    # Act
    result = perform_t_test(group1, group2, equal_var=False)

    # Assert
    assert result is not None
    assert "statistic" in result


def test_perform_t_test_different_sizes() -> None:
    """Test case 11: Edge case with different group sizes."""
    # Arrange
    group1 = [1, 2, 3]
    group2 = [4, 5, 6, 7, 8]

    # Act
    result = perform_t_test(group1, group2)

    # Assert
    assert result["statistic"] < 0
    assert "cohens_d" in result


def test_perform_t_test_negative_values() -> None:
    """Test case 12: Edge case with negative values."""
    # Arrange
    group1 = [-5, -4, -3, -2, -1]
    group2 = [-2, -1, 0, 1, 2]

    # Act
    result = perform_t_test(group1, group2)

    # Assert
    assert result["statistic"] < 0
    assert result["pvalue"] < 0.05


def test_perform_t_test_alpha_01() -> None:
    """Test case 13: Edge case with stricter alpha level."""
    # Arrange
    group1 = [10, 11, 12, 13, 14]
    group2 = [10.5, 11.5, 12.5, 13.5, 14.5]

    # Act
    result = perform_t_test(group1, group2, alpha=0.01)

    # Assert
    assert "significant" in result
    assert result["pvalue"] > 0.01  # Likely not significant at 0.01


# Error case tests


def test_perform_t_test_invalid_group1_type() -> None:
    """Test case 14: TypeError for invalid group1 type."""
    # Arrange
    invalid_group1 = "not_a_list"
    group2 = [1, 2, 3, 4, 5]
    expected_message = "group1 must be a list or numpy array"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        perform_t_test(invalid_group1, group2)


def test_perform_t_test_invalid_group2_type() -> None:
    """Test case 15: TypeError for invalid group2 type."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    invalid_group2 = 123
    expected_message = "group2 must be a list or numpy array"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        perform_t_test(group1, invalid_group2)


def test_perform_t_test_empty_group1() -> None:
    """Test case 16: ValueError for empty group1."""
    # Arrange
    empty_group1 = []
    group2 = [1, 2, 3, 4, 5]
    expected_message = "group1 cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        perform_t_test(empty_group1, group2)


def test_perform_t_test_empty_group2() -> None:
    """Test case 17: ValueError for empty group2."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    empty_group2 = []
    expected_message = "group2 cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        perform_t_test(group1, empty_group2)


def test_perform_t_test_invalid_alternative_type() -> None:
    """Test case 18: TypeError for invalid alternative type."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [3, 4, 5, 6, 7]
    invalid_alternative = 123
    expected_message = "alternative must be a string"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        perform_t_test(group1, group2, alternative=invalid_alternative)


def test_perform_t_test_invalid_alternative_value() -> None:
    """Test case 19: ValueError for invalid alternative value."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [3, 4, 5, 6, 7]
    invalid_alternative = "invalid"
    expected_message = "alternative must be"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        perform_t_test(group1, group2, alternative=invalid_alternative)


def test_perform_t_test_invalid_equal_var_type() -> None:
    """Test case 20: TypeError for invalid equal_var type."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [3, 4, 5, 6, 7]
    invalid_equal_var = "true"
    expected_message = "equal_var must be a boolean"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        perform_t_test(group1, group2, equal_var=invalid_equal_var)


def test_perform_t_test_invalid_alpha_type() -> None:
    """Test case 21: TypeError for invalid alpha type."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [3, 4, 5, 6, 7]
    invalid_alpha = "0.05"
    expected_message = "alpha must be a number"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        perform_t_test(group1, group2, alpha=invalid_alpha)


def test_perform_t_test_alpha_out_of_range_low() -> None:
    """Test case 22: ValueError for alpha below valid range."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [3, 4, 5, 6, 7]
    invalid_alpha = 0.0
    expected_message = "alpha must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        perform_t_test(group1, group2, alpha=invalid_alpha)


def test_perform_t_test_alpha_out_of_range_high() -> None:
    """Test case 23: ValueError for alpha above valid range."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    group2 = [3, 4, 5, 6, 7]
    invalid_alpha = 1.0
    expected_message = "alpha must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        perform_t_test(group1, group2, alpha=invalid_alpha)


def test_perform_t_test_non_numeric_group1() -> None:
    """Test case 24: ValueError for non-numeric values in group1."""
    # Arrange
    invalid_group1 = [1, 2, "three", 4, 5]
    group2 = [3, 4, 5, 6, 7]
    expected_message = "groups contain non-numeric values"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        perform_t_test(invalid_group1, group2)


def test_perform_t_test_non_numeric_group2() -> None:
    """Test case 25: ValueError for non-numeric values in group2."""
    # Arrange
    group1 = [1, 2, 3, 4, 5]
    invalid_group2 = [3, 4, "five", 6, 7]
    expected_message = "groups contain non-numeric values"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        perform_t_test(group1, invalid_group2)
