"""Unit tests for format_number_compact function."""

import pytest
from formatting_functions.format_number_compact import format_number_compact


def test_format_number_compact_zero() -> None:
    """
    Test case 1: Format zero.
    """
    # Arrange & Act & Assert
    assert format_number_compact(0) == "0"


def test_format_number_compact_below_threshold() -> None:
    """
    Test case 2: Format numbers below threshold.
    """
    # Arrange & Act & Assert
    assert format_number_compact(500) == "500"
    assert format_number_compact(999) == "999"
    assert format_number_compact(500, threshold=1000) == "500"


def test_format_number_compact_thousands() -> None:
    """
    Test case 3: Format numbers in thousands.
    """
    # Arrange & Act & Assert
    assert format_number_compact(1000) == "1K"
    assert format_number_compact(1500) == "1.5K"
    assert format_number_compact(15000) == "15K"
    assert format_number_compact(999999) == "1000K"


def test_format_number_compact_millions() -> None:
    """
    Test case 4: Format numbers in millions.
    """
    # Arrange & Act & Assert
    assert format_number_compact(1000000) == "1M"
    assert format_number_compact(1500000) == "1.5M"
    assert format_number_compact(2300000) == "2.3M"
    assert format_number_compact(999999999) == "1000M"


def test_format_number_compact_billions() -> None:
    """
    Test case 5: Format numbers in billions.
    """
    # Arrange & Act & Assert
    assert format_number_compact(1000000000) == "1B"
    assert format_number_compact(2300000000) == "2.3B"
    assert format_number_compact(5678000000) == "5.7B"


def test_format_number_compact_trillions() -> None:
    """
    Test case 6: Format numbers in trillions.
    """
    # Arrange & Act & Assert
    assert format_number_compact(1000000000000) == "1T"
    assert format_number_compact(3450000000000) == "3.5T"


def test_format_number_compact_quadrillions() -> None:
    """
    Test case 7: Format numbers in quadrillions.
    """
    # Arrange & Act & Assert
    assert format_number_compact(1000000000000000) == "1Q"
    assert format_number_compact(2500000000000000) == "2.5Q"


def test_format_number_compact_precision() -> None:
    """
    Test case 8: Test different precision values.
    """
    # Arrange
    number = 1567000
    
    # Act & Assert
    assert format_number_compact(number, precision=0) == "2M"
    assert format_number_compact(number, precision=1) == "1.6M"
    assert format_number_compact(number, precision=2) == "1.57M"
    assert format_number_compact(number, precision=3) == "1.567M"


def test_format_number_compact_removes_trailing_zeros() -> None:
    """
    Test case 9: Verify trailing zeros are removed.
    """
    # Arrange & Act & Assert
    assert format_number_compact(1000000, precision=2) == "1M"  # Not "1.00M"
    assert format_number_compact(1500000, precision=2) == "1.5M"  # Not "1.50M"


def test_format_number_compact_custom_threshold() -> None:
    """
    Test case 10: Test custom threshold values.
    """
    # Arrange & Act & Assert
    assert format_number_compact(100, threshold=100) == "0.1K"
    assert format_number_compact(500, threshold=100) == "0.5K"
    assert format_number_compact(99, threshold=100) == "99"


def test_format_number_compact_negative_numbers() -> None:
    """
    Test case 11: Format negative numbers.
    """
    # Arrange & Act & Assert
    assert format_number_compact(-1500) == "-1.5K"
    assert format_number_compact(-1500000) == "-1.5M"
    assert format_number_compact(-500) == "-500"


def test_format_number_compact_float_input() -> None:
    """
    Test case 12: Handle float input.
    """
    # Arrange & Act & Assert
    assert format_number_compact(1500.7) == "1.5K"
    assert format_number_compact(1500000.9) == "1.5M"
    assert format_number_compact(500.5, threshold=1000) == "500.5"


def test_format_number_compact_invalid_type_number() -> None:
    """
    Test case 13: TypeError for invalid number type.
    """
    # Arrange
    expected_message = "number must be a number, got str"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_number_compact("1500")


def test_format_number_compact_invalid_type_precision() -> None:
    """
    Test case 14: TypeError for invalid precision type.
    """
    # Arrange
    expected_message = "precision must be an integer, got str"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_number_compact(1500, precision="2")


def test_format_number_compact_invalid_type_threshold() -> None:
    """
    Test case 15: TypeError for invalid threshold type.
    """
    # Arrange
    expected_message = "threshold must be an integer, got float"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_number_compact(1500, threshold=1000.5)


def test_format_number_compact_negative_precision() -> None:
    """
    Test case 16: ValueError for negative precision.
    """
    # Arrange
    expected_message = "precision must be non-negative"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        format_number_compact(1500, precision=-1)


def test_format_number_compact_negative_threshold() -> None:
    """
    Test case 17: ValueError for negative threshold.
    """
    # Arrange
    expected_message = "threshold must be non-negative"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        format_number_compact(1500, threshold=-100)


def test_format_number_compact_boundary_values() -> None:
    """
    Test case 18: Test boundary values between units.
    """
    # Arrange & Act & Assert
    # Thousand boundary
    assert format_number_compact(999) == "999"
    assert format_number_compact(1000) == "1K"
    
    # Million boundary
    assert format_number_compact(999999) == "1000K"
    assert format_number_compact(1000000) == "1M"
    
    # Billion boundary
    assert format_number_compact(999999999) == "1000M"
    assert format_number_compact(1000000000) == "1B"
