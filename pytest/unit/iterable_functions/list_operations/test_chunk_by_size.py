import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from python_utils.iterable_functions.list_operations.chunk_by_size import chunk_by_size


def test_chunk_by_size_normal_chunking() -> None:
    """
    Test case 1: Normal chunking with remainder.
    """
    # Arrange
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunk_size = 3

    # Act
    result = chunk_by_size(items, chunk_size)

    # Assert
    assert result == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]


def test_chunk_by_size_exact_division() -> None:
    """
    Test case 2: Items divide evenly into chunks.
    """
    # Arrange
    items = [1, 2, 3, 4, 5, 6]
    chunk_size = 2

    # Act
    result = chunk_by_size(items, chunk_size)

    # Assert
    assert result == [[1, 2], [3, 4], [5, 6]]


def test_chunk_by_size_single_chunk() -> None:
    """
    Test case 3: All items fit in one chunk.
    """
    # Arrange
    items = [1, 2, 3]
    chunk_size = 5

    # Act
    result = chunk_by_size(items, chunk_size)

    # Assert
    assert result == [[1, 2, 3]]


def test_chunk_by_size_chunk_size_one() -> None:
    """
    Test case 4: Chunk size of 1 creates individual items.
    """
    # Arrange
    items = [1, 2, 3, 4]
    chunk_size = 1

    # Act
    result = chunk_by_size(items, chunk_size)

    # Assert
    assert result == [[1], [2], [3], [4]]


def test_chunk_by_size_empty_list() -> None:
    """
    Test case 5: Empty list returns empty result.
    """
    # Arrange
    items: list[int] = []
    chunk_size = 3

    # Act
    result = chunk_by_size(items, chunk_size)

    # Assert
    assert result == []


def test_chunk_by_size_string_list() -> None:
    """
    Test case 6: Chunk list of strings.
    """
    # Arrange
    items = ["a", "b", "c", "d"]
    chunk_size = 2

    # Act
    result = chunk_by_size(items, chunk_size)

    # Assert
    assert result == [["a", "b"], ["c", "d"]]


def test_chunk_by_size_large_chunk_size() -> None:
    """
    Test case 7: Chunk size larger than list length.
    """
    # Arrange
    items = [1, 2, 3]
    chunk_size = 100

    # Act
    result = chunk_by_size(items, chunk_size)

    # Assert
    assert result == [[1, 2, 3]]


def test_chunk_by_size_mixed_types() -> None:
    """
    Test case 8: Chunk list with mixed types.
    """
    # Arrange
    items = [1, "two", 3.0, True, None]
    chunk_size = 2

    # Act
    result = chunk_by_size(items, chunk_size)

    # Assert
    assert result == [[1, "two"], [3.0, True], [None]]


def test_chunk_by_size_type_error_non_list() -> None:
    """
    Test case 9: TypeError when items is not a list.
    """
    # Arrange
    invalid_items = "not a list"
    chunk_size = 2

    # Act & Assert
    with pytest.raises(TypeError, match="items must be a list"):
        chunk_by_size(invalid_items, chunk_size)  # type: ignore


def test_chunk_by_size_type_error_non_integer_chunk_size() -> None:
    """
    Test case 10: TypeError when chunk_size is not an integer.
    """
    # Arrange
    items = [1, 2, 3]
    invalid_chunk_size = "2"

    # Act & Assert
    with pytest.raises(TypeError, match="chunk_size must be an integer"):
        chunk_by_size(items, invalid_chunk_size)  # type: ignore


def test_chunk_by_size_value_error_zero_chunk_size() -> None:
    """
    Test case 11: ValueError when chunk_size is 0.
    """
    # Arrange
    items = [1, 2, 3]
    chunk_size = 0

    # Act & Assert
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        chunk_by_size(items, chunk_size)


def test_chunk_by_size_value_error_negative_chunk_size() -> None:
    """
    Test case 12: ValueError when chunk_size is negative.
    """
    # Arrange
    items = [1, 2, 3]
    chunk_size = -5

    # Act & Assert
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        chunk_by_size(items, chunk_size)
