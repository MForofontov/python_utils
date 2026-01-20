import pytest

try:
    import snappy
    from pyutils_collection.compression_functions.polyline_encoding_list_of_ints import (
        polyline_encoding_list_of_ints,
    )
    SNAPPY_AVAILABLE = True
except ImportError:
    SNAPPY_AVAILABLE = False
    snappy = None  # type: ignore
    polyline_encoding_list_of_ints = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.compression,
    pytest.mark.skipif(not SNAPPY_AVAILABLE, reason="python-snappy not installed"),
]


def test_polyline_encoding_list_of_ints_simple_values() -> None:
    """
    Test case 1: Encode simple list of integers.
    """
    # Arrange
    list_of_ints = [1, 2]

    # Act
    result = polyline_encoding_list_of_ints(list_of_ints)

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_polyline_encoding_list_of_ints_single_value() -> None:
    """
    Test case 2: Encode list with single value.
    """
    # Arrange
    list_of_ints = [5]

    # Act
    result = polyline_encoding_list_of_ints(list_of_ints)

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_polyline_encoding_list_of_ints_negative_values() -> None:
    """
    Test case 3: Encode list with negative values.
    """
    # Arrange
    list_of_ints = [-1, -2, -3]

    # Act
    result = polyline_encoding_list_of_ints(list_of_ints)

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_polyline_encoding_list_of_ints_mixed_values() -> None:
    """
    Test case 4: Encode list with mixed positive and negative values.
    """
    # Arrange
    list_of_ints = [1, -1, 2, -2, 0]

    # Act
    result = polyline_encoding_list_of_ints(list_of_ints)

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_polyline_encoding_list_of_ints_large_values() -> None:
    """
    Test case 5: Encode list with large values.
    """
    # Arrange
    list_of_ints = [1000, 2000, 3000]

    # Act
    result = polyline_encoding_list_of_ints(list_of_ints)

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_polyline_encoding_list_of_ints_sequential_values() -> None:
    """
    Test case 6: Encode sequential values.
    """
    # Arrange
    list_of_ints = list(range(0, 10))

    # Act
    result = polyline_encoding_list_of_ints(list_of_ints)

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_polyline_encoding_list_of_ints_zero_values() -> None:
    """
    Test case 7: Encode list with zeros.
    """
    # Arrange
    list_of_ints = [0, 0, 0]

    # Act
    result = polyline_encoding_list_of_ints(list_of_ints)

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_polyline_encoding_list_of_ints_empty_list_error() -> None:
    """
    Test case 8: ValueError when input list is empty.
    """
    # Arrange
    empty_list: list[int] = []

    # Act & Assert
    with pytest.raises(ValueError, match="Input list cannot be empty"):
        polyline_encoding_list_of_ints(empty_list)


def test_polyline_encoding_list_of_ints_negative_precision_error() -> None:
    """
    Test case 9: ValueError when precision is negative.
    """
    # Arrange
    list_of_ints = [1, 2, 3]

    # Act & Assert
    with pytest.raises(ValueError, match="Precision must be non-negative"):
        polyline_encoding_list_of_ints(list_of_ints, precision=-1)
