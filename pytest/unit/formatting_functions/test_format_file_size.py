"""Unit tests for format_file_size function."""

import pytest
from formatting_functions.format_file_size import format_file_size


def test_format_file_size_binary_units() -> None:
    """
    Test case 1: Format with binary units (1024-based).
    """
    # Arrange & Act & Assert
    assert format_file_size(1024) == "1.00 KiB"
    assert format_file_size(1536) == "1.50 KiB"
    assert format_file_size(1048576) == "1.00 MiB"
    assert format_file_size(1073741824) == "1.00 GiB"
    assert format_file_size(1099511627776) == "1.00 TiB"


def test_format_file_size_decimal_units() -> None:
    """
    Test case 2: Format with decimal units (1000-based).
    """
    # Arrange & Act & Assert
    assert format_file_size(1000, binary=False) == "1.00 KB"
    assert format_file_size(1500, binary=False) == "1.50 KB"
    assert format_file_size(1000000, binary=False) == "1.00 MB"
    assert format_file_size(1000000000, binary=False) == "1.00 GB"


def test_format_file_size_precision() -> None:
    """
    Test case 3: Test different precision values.
    """
    # Arrange
    size = 1536
    
    # Act & Assert
    assert format_file_size(size, precision=0) == "2 KiB"
    assert format_file_size(size, precision=1) == "1.5 KiB"
    assert format_file_size(size, precision=2) == "1.50 KiB"
    assert format_file_size(size, precision=3) == "1.500 KiB"


def test_format_file_size_bytes() -> None:
    """
    Test case 4: Format bytes without unit conversion.
    """
    # Arrange & Act & Assert
    assert format_file_size(0) == "0 B"
    assert format_file_size(512) == "512 B"
    assert format_file_size(1023) == "1023 B"


def test_format_file_size_large_sizes() -> None:
    """
    Test case 5: Format very large file sizes.
    """
    # Arrange & Act & Assert
    assert format_file_size(1_125_899_906_842_624) == "1.00 PiB"
    assert format_file_size(1_152_921_504_606_846_976) == "1.00 EiB"


def test_format_file_size_float_input() -> None:
    """
    Test case 6: Handle float input values.
    """
    # Arrange & Act & Assert
    assert format_file_size(1536.7) == "1.50 KiB"
    assert format_file_size(1048576.9) == "1.00 MiB"


def test_format_file_size_boundary_values() -> None:
    """
    Test case 7: Test boundary values between units.
    """
    # Arrange & Act & Assert
    # Just below and at 1 KiB
    assert format_file_size(1023) == "1023 B"
    assert format_file_size(1024) == "1.00 KiB"
    
    # Just below and at 1 MiB
    assert format_file_size(1048575) == "1024.00 KiB"
    assert format_file_size(1048576) == "1.00 MiB"


def test_format_file_size_invalid_type_size_bytes() -> None:
    """
    Test case 8: TypeError for invalid size_bytes type.
    """
    # Arrange
    invalid_input = "1024"
    expected_message = "size_bytes must be a number, got str"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_file_size(invalid_input)


def test_format_file_size_invalid_type_binary() -> None:
    """
    Test case 9: TypeError for invalid binary type.
    """
    # Arrange
    expected_message = "binary must be a boolean, got str"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_file_size(1024, binary="true")


def test_format_file_size_invalid_type_precision() -> None:
    """
    Test case 10: TypeError for invalid precision type.
    """
    # Arrange
    expected_message = "precision must be an integer, got float"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_file_size(1024, precision=2.5)


def test_format_file_size_negative_size() -> None:
    """
    Test case 11: ValueError for negative size.
    """
    # Arrange
    expected_message = "size_bytes must be non-negative"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        format_file_size(-1024)


def test_format_file_size_negative_precision() -> None:
    """
    Test case 12: ValueError for negative precision.
    """
    # Arrange
    expected_message = "precision must be non-negative"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        format_file_size(1024, precision=-1)
