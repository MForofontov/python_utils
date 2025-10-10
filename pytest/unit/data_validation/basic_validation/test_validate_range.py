from datetime import date, datetime
from decimal import Decimal

import pytest
from data_validation import validate_range


def test_validate_range_numeric_ranges() -> None:
    """
    Test case 1: Numeric range validation with integers and floats.
    """
    # Test integer ranges
    validate_range(5, min_value=0, max_value=10)
    validate_range(0, min_value=0, max_value=10)  # Minimum boundary
    validate_range(10, min_value=0, max_value=10)  # Maximum boundary

    # Test float ranges
    validate_range(5.5, min_value=0.0, max_value=10.0)
    validate_range(3.14159, min_value=3.0, max_value=4.0)

    # Test negative ranges
    validate_range(-5, min_value=-10, max_value=0)
    validate_range(-2.5, min_value=-10.0, max_value=10.0)


def test_validate_range_exclusive_bounds() -> None:
    """
    Test case 2: Exclusive boundary validation.
    """
    # Test exclusive minimum
    validate_range(5, min_value=0, min_inclusive=False)  # 5 > 0
    validate_range(1, min_value=0, min_inclusive=False)  # 1 > 0

    # Test exclusive maximum
    validate_range(5, max_value=10, max_inclusive=False)  # 5 < 10
    validate_range(9, max_value=10, max_inclusive=False)  # 9 < 10

    # Test both exclusive
    validate_range(
        5, min_value=0, max_value=10, min_inclusive=False, max_inclusive=False
    )


def test_validate_range_single_bounds() -> None:
    """
    Test case 3: Single boundary validation (only min or max).
    """
    # Test only minimum
    validate_range(100, min_value=0)
    validate_range(0, min_value=0)

    # Test only maximum
    validate_range(-100, max_value=0)
    validate_range(0, max_value=0)

    # Test no bounds (should always pass)
    validate_range(999999)
    validate_range(-999999)


def test_validate_range_string_ranges() -> None:
    """
    Test case 4: String lexicographic range validation.
    """
    # Test alphabetical ranges
    validate_range("hello", min_value="a", max_value="z")
    validate_range("apple", min_value="a", max_value="z")
    validate_range("zulu", min_value="a", max_value="zulu")

    # Test specific string ranges
    validate_range("dog", min_value="cat", max_value="elephant")
    validate_range("cat", min_value="cat", max_value="elephant")
    validate_range("elephant", min_value="cat", max_value="elephant")


def test_validate_range_date_ranges() -> None:
    """
    Test case 5: Date and datetime range validation.
    """
    # Test date ranges
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    test_date = date(2023, 6, 15)

    validate_range(test_date, min_value=start_date, max_value=end_date)
    validate_range(start_date, min_value=start_date, max_value=end_date)
    validate_range(end_date, min_value=start_date, max_value=end_date)

    # Test datetime ranges
    start_datetime = datetime(2023, 1, 1, 0, 0, 0)
    end_datetime = datetime(2023, 12, 31, 23, 59, 59)
    test_datetime = datetime(2023, 6, 15, 12, 30, 45)

    validate_range(test_datetime, min_value=start_datetime, max_value=end_datetime)


def test_validate_range_decimal_ranges() -> None:
    """
    Test case 6: Decimal number range validation.
    """
    # Test Decimal ranges
    validate_range(Decimal("5.5"), min_value=Decimal("0.0"), max_value=Decimal("10.0"))
    validate_range(Decimal("0.0"), min_value=Decimal("0.0"), max_value=Decimal("10.0"))
    validate_range(Decimal("10.0"), min_value=Decimal("0.0"), max_value=Decimal("10.0"))

    # Test high precision decimals
    validate_range(
        Decimal("3.141592653589793"), min_value=Decimal("3.0"), max_value=Decimal("4.0")
    )


def test_validate_range_case_11_boundary_conditions() -> None:
    """
    Test case 7: Edge cases and boundary conditions.
    """
    # Test zero boundaries
    validate_range(0, min_value=0, max_value=0)

    # Test very small ranges
    validate_range(1, min_value=1, max_value=1)

    # Test large numbers
    large_num = 10**15
    validate_range(large_num, min_value=0, max_value=10**16)

    # Test very small floats
    validate_range(1e-10, min_value=0.0, max_value=1e-9)


def test_validate_range_case_12_performance_large_numbers() -> None:
    """
    Test case 8: Performance with large numbers and many validations.
    """
    # Test with very large numbers
    large_value = 10**100
    validate_range(large_value, min_value=0, max_value=10**101)

    # Performance test
    import time

    start_time = time.time()
    for i in range(10000):
        validate_range(i, min_value=0, max_value=20000)
    elapsed_time = time.time() - start_time

    assert elapsed_time < 1.0  # Should complete within 1 second


def test_validate_range_value_error_below_minimum() -> None:
    """
    Test case 9: ValueError for values below minimum.
    """
    # Test inclusive minimum
    with pytest.raises(ValueError, match="value must be >= 0, got -1"):
        validate_range(-1, min_value=0)

    with pytest.raises(ValueError, match="value must be >= 5.0, got 4.9"):
        validate_range(4.9, min_value=5.0)

    # Test exclusive minimum
    with pytest.raises(ValueError, match="value must be > 0, got 0"):
        validate_range(0, min_value=0, min_inclusive=False)

    # Test with custom param name
    with pytest.raises(ValueError, match="age must be >= 0, got -5"):
        validate_range(-5, min_value=0, param_name="age")


def test_validate_range_value_error_above_maximum() -> None:
    """
    Test case 10: ValueError for values above maximum.
    """
    # Test inclusive maximum
    with pytest.raises(ValueError, match="value must be <= 10, got 11"):
        validate_range(11, max_value=10)

    with pytest.raises(ValueError, match="value must be <= 5.5, got 6.0"):
        validate_range(6.0, max_value=5.5)

    # Test exclusive maximum
    with pytest.raises(ValueError, match="value must be < 10, got 10"):
        validate_range(10, max_value=10, max_inclusive=False)

    # Test with custom param name
    with pytest.raises(ValueError, match="score must be <= 100, got 105"):
        validate_range(105, max_value=100, param_name="score")


def test_validate_range_invalid_range_bounds() -> None:
    """
    Test case 11: ValueError for invalid range bounds.
    """
    # Test min > max
    with pytest.raises(
        ValueError, match="min_value \\(10\\) cannot be greater than max_value \\(5\\)"
    ):
        validate_range(7, min_value=10, max_value=5)

    # Test equal bounds with exclusive
    with pytest.raises(
        ValueError,
        match="min_value and max_value are equal \\(5\\), but at least one bound is exclusive",
    ):
        validate_range(5, min_value=5, max_value=5, min_inclusive=False)

    with pytest.raises(
        ValueError,
        match="min_value and max_value are equal \\(5\\), but at least one bound is exclusive",
    ):
        validate_range(5, min_value=5, max_value=5, max_inclusive=False)


def test_validate_range_case_10_type_errors() -> None:
    """
    Test case 12: TypeError for invalid parameter types and incompatible comparisons.
    """
    # Test invalid parameter types
    with pytest.raises(TypeError, match="min_inclusive must be bool, got str"):
        validate_range(5, min_value=0, min_inclusive="true")

    with pytest.raises(TypeError, match="max_inclusive must be bool, got int"):
        validate_range(5, max_value=10, max_inclusive=1)

    with pytest.raises(TypeError, match="param_name must be str, got int"):
        validate_range(5, param_name=123)

    # Test incompatible type comparisons
    with pytest.raises(
        TypeError, match="Cannot compare value of type int with min_value of type str"
    ):
        validate_range(5, min_value="hello")

    with pytest.raises(
        TypeError, match="Cannot compare value of type str with max_value of type int"
    ):
        validate_range("hello", max_value=10)
