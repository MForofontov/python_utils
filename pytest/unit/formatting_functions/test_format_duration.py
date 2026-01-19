"""Unit tests for format_duration function."""

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.formatting]
from formatting_functions.format_duration import format_duration


# Normal test cases
def test_format_duration_seconds_only() -> None:
    """
    Test case 1: Format durations less than a minute.
    """
    # Arrange & Act & Assert
    assert format_duration(30) == "30s"
    assert format_duration(30, long_format=True) == "30 seconds"
    assert format_duration(1, long_format=True) == "1 second"


def test_format_duration_minutes() -> None:
    """
    Test case 2: Format durations with minutes.
    """
    # Arrange & Act & Assert
    assert format_duration(90) == "1m 30s"
    assert format_duration(90, long_format=True) == "1 minute 30 seconds"
    assert format_duration(120) == "2m"
    assert format_duration(120, long_format=True) == "2 minutes"


def test_format_duration_hours() -> None:
    """
    Test case 3: Format durations with hours.
    """
    # Arrange & Act & Assert
    assert format_duration(3600) == "1h"
    assert format_duration(3665) == "1h 1m"
    assert format_duration(3665, precision=3) == "1h 1m 5s"
    assert format_duration(3665, long_format=True) == "1 hour 1 minute"


def test_format_duration_days() -> None:
    """
    Test case 4: Format durations with days.
    """
    # Arrange & Act & Assert
    assert format_duration(86400) == "1d"
    assert format_duration(90000) == "1d 1h"
    assert format_duration(90000, precision=3) == "1d 1h"
    assert format_duration(90061, precision=3) == "1d 1h 1m"


def test_format_duration_weeks() -> None:
    """
    Test case 5: Format durations with weeks.
    """
    # Arrange & Act & Assert
    assert format_duration(604800) == "1w"
    assert format_duration(691200) == "1w 1d"
    assert format_duration(691200, long_format=True) == "1 week 1 day"


def test_format_duration_years() -> None:
    """
    Test case 6: Format durations with years.
    """
    # Arrange & Act & Assert
    assert format_duration(31536000) == "1y"  # 365 days
    assert format_duration(32140800) == "1y 1w"
    assert format_duration(32140800, long_format=True) == "1 year 1 week"


def test_format_duration_precision_variations() -> None:
    """
    Test case 7: Test different precision values.
    """
    # Arrange & Act & Assert
    # Precision = 1 (single unit)
    assert format_duration(3665, precision=1) == "1h"
    assert format_duration(90061, precision=1) == "1d"
    assert format_duration(691261, precision=1) == "1w"

    # Precision = 3 (three units)
    assert format_duration(90061, precision=3) == "1d 1h 1m"
    assert (
        format_duration(90061, precision=3, long_format=True) == "1 day 1 hour 1 minute"
    )


def test_format_duration_long_format_pluralization() -> None:
    """
    Test case 8: Verify correct pluralization in long format.
    """
    # Arrange & Act & Assert
    assert format_duration(1, long_format=True) == "1 second"
    assert format_duration(2, long_format=True) == "2 seconds"
    assert format_duration(60, long_format=True) == "1 minute"
    assert format_duration(120, long_format=True) == "2 minutes"
    assert format_duration(3600, long_format=True) == "1 hour"
    assert format_duration(7200, long_format=True) == "2 hours"


# Edge case tests
def test_format_duration_zero() -> None:
    """
    Test case 9: Format zero seconds.
    """
    # Arrange & Act & Assert
    assert format_duration(0) == "0s"
    assert format_duration(0, long_format=True) == "0 seconds"


def test_format_duration_float_input() -> None:
    """
    Test case 10: Handle float seconds.
    """
    # Arrange & Act & Assert
    assert format_duration(90.5) == "1m 30s"
    assert format_duration(90.9) == "1m 30s"
    assert format_duration(3665.7) == "1h 1m"


def test_format_duration_boundary_conditions() -> None:
    """
    Test case 11: Test boundary conditions for time units.
    """
    # Arrange & Act & Assert
    assert format_duration(59) == "59s"
    assert format_duration(60) == "1m"
    assert format_duration(61) == "1m 1s"
    assert format_duration(3600) == "1h"


def test_format_duration_large_values() -> None:
    """
    Test case 12: Format very large durations.
    """
    # Arrange & Act & Assert
    # 10 years
    assert format_duration(315360000) == "10y"

    # Multiple years with all units
    large_duration = (
        (2 * 365 * 24 * 60 * 60) + (3 * 7 * 24 * 60 * 60) + (4 * 24 * 60 * 60)
    )
    result = format_duration(large_duration, precision=3)
    assert result == "2y 3w 4d"


# Error case tests
def test_format_duration_invalid_type_seconds() -> None:
    """
    Test case 13: TypeError for non-numeric seconds.
    """
    # Arrange
    expected_message = "seconds must be a number, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_duration("90")


def test_format_duration_invalid_type_precision() -> None:
    """
    Test case 14: TypeError for invalid precision type.
    """
    # Arrange
    expected_message = "precision must be an integer, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_duration(90, precision="2")


def test_format_duration_invalid_type_long_format() -> None:
    """
    Test case 15: TypeError for invalid long_format type.
    """
    # Arrange
    expected_message = "long_format must be a boolean, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_duration(90, long_format="true")


def test_format_duration_negative_seconds() -> None:
    """
    Test case 16: ValueError for negative seconds.
    """
    # Arrange
    expected_message = "seconds must be non-negative"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        format_duration(-90)


def test_format_duration_invalid_precision() -> None:
    """
    Test case 17: ValueError for invalid precision value.
    """
    # Arrange
    expected_message = "precision must be at least 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        format_duration(90, precision=0)

    with pytest.raises(ValueError, match=expected_message):
        format_duration(90, precision=-1)
