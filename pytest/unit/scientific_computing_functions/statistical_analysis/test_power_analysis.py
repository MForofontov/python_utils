"""Unit tests for power_analysis function."""

import pytest
from scientific_computing_functions.statistical_analysis.power_analysis import (
    power_analysis,
)


# Normal operation tests
def test_power_analysis_ttest_medium_effect() -> None:
    """Test case 1: Normal t-test power analysis with medium effect size."""
    # Arrange
    effect_size = 0.5  # Medium effect (Cohen's d)
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="t-test")

    # Assert
    assert result["required_sample_size"] > 0
    assert result["total_sample_size"] == result["required_sample_size"] * 2
    assert result["effect_size"] == effect_size
    assert result["alpha"] == alpha
    assert result["power"] == power
    # Allow for rounding variation (±2 samples)
    assert 62 <= result["required_sample_size"] <= 66


def test_power_analysis_ttest_small_effect() -> None:
    """Test case 2: Normal t-test with small effect size (requires larger sample)."""
    # Arrange
    effect_size = 0.2  # Small effect
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="t-test")

    # Assert
    assert result["required_sample_size"] > 300  # Small effects need large samples
    assert result["total_sample_size"] > 600


def test_power_analysis_ttest_large_effect() -> None:
    """Test case 3: Normal t-test with large effect size (requires smaller sample)."""
    # Arrange
    effect_size = 0.8  # Large effect
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="t-test")

    # Assert
    assert result["required_sample_size"] < 30  # Large effects need small samples
    # Allow for rounding variation (24-27 samples)
    assert 24 <= result["required_sample_size"] <= 27


def test_power_analysis_anova() -> None:
    """Test case 4: Normal ANOVA power analysis."""
    # Arrange
    effect_size = 0.25  # Cohen's f (medium effect for ANOVA)
    alpha = 0.05
    power = 0.8
    n_groups = 3

    # Act
    result = power_analysis(
        effect_size, alpha, power, test_type="anova", n_groups=n_groups
    )

    # Assert
    assert result["required_sample_size"] > 0
    assert result["total_sample_size"] == result["required_sample_size"] * n_groups


def test_power_analysis_proportion() -> None:
    """Test case 5: Normal proportion test power analysis."""
    # Arrange
    effect_size = 0.5  # Cohen's h (medium effect for proportions)
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="proportion")

    # Assert
    assert result["required_sample_size"] > 0
    assert result["total_sample_size"] == result["required_sample_size"] * 2


def test_power_analysis_correlation() -> None:
    """Test case 6: Normal correlation power analysis."""
    # Arrange
    effect_size = 0.3  # Correlation coefficient (medium effect)
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="correlation")

    # Assert
    assert result["required_sample_size"] > 60
    assert (
        result["total_sample_size"] == result["required_sample_size"]
    )  # Single sample


def test_power_analysis_one_sided_greater() -> None:
    """Test case 7: Normal operation with one-sided test (greater)."""
    # Arrange
    effect_size = 0.5
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(
        effect_size, alpha, power, test_type="t-test", alternative="greater"
    )

    # Assert
    assert result["required_sample_size"] > 0
    # One-sided tests require smaller samples than two-sided
    result_two_sided = power_analysis(
        effect_size, alpha, power, test_type="t-test", alternative="two-sided"
    )
    assert result["required_sample_size"] < result_two_sided["required_sample_size"]


def test_power_analysis_one_sided_less() -> None:
    """Test case 8: Normal operation with one-sided test (less)."""
    # Arrange
    effect_size = 0.5
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(
        effect_size, alpha, power, test_type="t-test", alternative="less"
    )

    # Assert
    assert result["required_sample_size"] > 0


# Edge case tests
def test_power_analysis_very_small_effect() -> None:
    """Test case 9: Edge case with very small effect size."""
    # Arrange
    effect_size = 0.01  # Very small effect
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="t-test")

    # Assert
    assert result["required_sample_size"] > 10000  # Very large sample needed


def test_power_analysis_high_power() -> None:
    """Test case 10: Edge case with high desired power (0.95)."""
    # Arrange
    effect_size = 0.5
    alpha = 0.05
    power = 0.95  # High power

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="t-test")

    # Assert
    # Higher power requires larger sample than 0.8
    result_80 = power_analysis(effect_size, alpha, 0.8, test_type="t-test")
    assert result["required_sample_size"] > result_80["required_sample_size"]


def test_power_analysis_strict_alpha() -> None:
    """Test case 11: Edge case with strict alpha (0.01)."""
    # Arrange
    effect_size = 0.5
    alpha = 0.01  # Stricter than typical 0.05
    power = 0.8

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="t-test")

    # Assert
    # Stricter alpha requires larger sample
    result_005 = power_analysis(effect_size, 0.05, power, test_type="t-test")
    assert result["required_sample_size"] > result_005["required_sample_size"]


def test_power_analysis_anova_many_groups() -> None:
    """Test case 12: Edge case with many groups in ANOVA."""
    # Arrange
    effect_size = 0.25
    alpha = 0.05
    power = 0.8
    n_groups = 10

    # Act
    result = power_analysis(
        effect_size, alpha, power, test_type="anova", n_groups=n_groups
    )

    # Assert
    assert result["total_sample_size"] == result["required_sample_size"] * 10


def test_power_analysis_low_power() -> None:
    """Test case 13: Edge case with low desired power (0.5)."""
    # Arrange
    effect_size = 0.5
    alpha = 0.05
    power = 0.5  # Low power

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="t-test")

    # Assert
    assert result["required_sample_size"] > 0
    # Lower power requires smaller sample
    result_80 = power_analysis(effect_size, alpha, 0.8, test_type="t-test")
    assert result["required_sample_size"] < result_80["required_sample_size"]


def test_power_analysis_large_correlation() -> None:
    """Test case 14: Edge case with large correlation coefficient."""
    # Arrange
    effect_size = 0.8  # Strong correlation
    alpha = 0.05
    power = 0.8

    # Act
    result = power_analysis(effect_size, alpha, power, test_type="correlation")

    # Assert
    assert result["required_sample_size"] < 20  # Small sample for large effect


# Error case tests
def test_power_analysis_invalid_effect_size_type() -> None:
    """Test case 15: TypeError for invalid effect size type."""
    # Arrange
    invalid_effect_size = "0.5"
    expected_message = "effect_size must be a number"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        power_analysis(invalid_effect_size)


def test_power_analysis_negative_effect_size() -> None:
    """Test case 16: ValueError for negative effect size."""
    # Arrange
    invalid_effect_size = -0.5
    expected_message = "effect_size must be positive"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        power_analysis(invalid_effect_size)


def test_power_analysis_zero_effect_size() -> None:
    """Test case 17: ValueError for zero effect size."""
    # Arrange
    invalid_effect_size = 0.0
    expected_message = "effect_size must be positive"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        power_analysis(invalid_effect_size)


def test_power_analysis_invalid_alpha_type() -> None:
    """Test case 18: TypeError for invalid alpha type."""
    # Arrange
    effect_size = 0.5
    invalid_alpha = "0.05"
    expected_message = "alpha must be a number"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        power_analysis(effect_size, alpha=invalid_alpha)


def test_power_analysis_alpha_out_of_range_zero() -> None:
    """Test case 19: ValueError for alpha = 0."""
    # Arrange
    effect_size = 0.5
    invalid_alpha = 0.0
    expected_message = "alpha must be in \\(0, 1\\)"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        power_analysis(effect_size, alpha=invalid_alpha)


def test_power_analysis_alpha_out_of_range_one() -> None:
    """Test case 20: ValueError for alpha = 1."""
    # Arrange
    effect_size = 0.5
    invalid_alpha = 1.0
    expected_message = "alpha must be in \\(0, 1\\)"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        power_analysis(effect_size, alpha=invalid_alpha)


def test_power_analysis_invalid_power_type() -> None:
    """Test case 21: TypeError for invalid power type."""
    # Arrange
    effect_size = 0.5
    invalid_power = "0.8"
    expected_message = "power must be a number"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        power_analysis(effect_size, power=invalid_power)


def test_power_analysis_power_out_of_range() -> None:
    """Test case 22: ValueError for power > 1."""
    # Arrange
    effect_size = 0.5
    invalid_power = 1.5
    expected_message = "power must be in \\(0, 1\\)"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        power_analysis(effect_size, power=invalid_power)


def test_power_analysis_invalid_test_type() -> None:
    """Test case 23: ValueError for invalid test type."""
    # Arrange
    effect_size = 0.5
    invalid_test_type = "invalid-test"
    expected_message = "Invalid test_type"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        power_analysis(effect_size, test_type=invalid_test_type)


def test_power_analysis_invalid_alternative() -> None:
    """Test case 24: ValueError for invalid alternative hypothesis."""
    # Arrange
    effect_size = 0.5
    invalid_alternative = "invalid"
    expected_message = "Invalid alternative"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        power_analysis(effect_size, alternative=invalid_alternative)


def test_power_analysis_invalid_n_groups_type() -> None:
    """Test case 25: TypeError for invalid n_groups type."""
    # Arrange
    effect_size = 0.5
    invalid_n_groups = 2.5
    expected_message = "n_groups must be an integer"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        power_analysis(effect_size, test_type="anova", n_groups=invalid_n_groups)


def test_power_analysis_n_groups_less_than_two() -> None:
    """Test case 26: ValueError for n_groups < 2."""
    # Arrange
    effect_size = 0.5
    invalid_n_groups = 1
    expected_message = "n_groups must be >= 2"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        power_analysis(effect_size, test_type="anova", n_groups=invalid_n_groups)


def test_power_analysis_invalid_test_type_type() -> None:
    """Test case 27: TypeError for invalid test_type type."""
    # Arrange
    effect_size = 0.5
    invalid_test_type = 123
    expected_message = "test_type must be a string"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        power_analysis(effect_size, test_type=invalid_test_type)


def test_power_analysis_invalid_alternative_type() -> None:
    """Test case 28: TypeError for invalid alternative type."""
    # Arrange
    effect_size = 0.5
    invalid_alternative = 123
    expected_message = "alternative must be a string"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        power_analysis(effect_size, alternative=invalid_alternative)
