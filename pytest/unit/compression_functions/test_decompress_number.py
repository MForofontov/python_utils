"""Unit tests for decompress_number function."""
import pytest

from compression_functions.decompress_number import decompress_number


def test_decompress_number_basic_value() -> None:
    """
    Test case 1: Decompress basic encoded value.
    """
    # Arrange
    text = "?"
    index = 0

    # Act
    new_index, result = decompress_number(text, index)

    # Assert
    assert new_index == 1
    assert result == 0


def test_decompress_number_positive_value() -> None:
    """
    Test case 2: Decompress positive value.
    """
    # Arrange
    text = "A"
    index = 0

    # Act
    new_index, result = decompress_number(text, index)

    # Assert
    assert new_index == 1
    assert result == 1


def test_decompress_number_negative_value() -> None:
    """
    Test case 3: Decompress negative value.
    """
    # Arrange
    text = "@"
    index = 0

    # Act
    new_index, result = decompress_number(text, index)

    # Assert
    assert new_index == 1
    assert result == -1


def test_decompress_number_multi_character() -> None:
    """
    Test case 4: Decompress multi-character encoded value.
    """
    # Arrange
    text = "_p~iF"
    index = 0

    # Act
    new_index, result = decompress_number(text, index)

    # Assert
    assert new_index > 1
    assert isinstance(result, int)


def test_decompress_number_type_error_non_string_text() -> None:
    """
    Test case 5: TypeError when text is not a string.
    """
    # Arrange
    invalid_text = 123
    index = 0

    # Act & Assert
    with pytest.raises(TypeError, match="text must be a string"):
        decompress_number(invalid_text, index)  # type: ignore


def test_decompress_number_type_error_non_integer_index() -> None:
    """
    Test case 6: TypeError when index is not an integer.
    """
    # Arrange
    text = "?"
    invalid_index = "0"

    # Act & Assert
    with pytest.raises(TypeError, match="index must be an integer"):
        decompress_number(text, invalid_index)  # type: ignore


def test_decompress_number_start_at_different_index() -> None:
    """
    Test case 7: Start decompressing from a different index.
    """
    # Arrange
    text = "??A"
    index = 2

    # Act
    new_index, result = decompress_number(text, index)

    # Assert
    assert new_index == 3
    assert result == 1


def test_decompress_number_complex_encoding() -> None:
    """
    Test case 8: Decompress complex encoded number.
    """
    # Arrange
    text = "_ibE"
    index = 0

    # Act
    new_index, result = decompress_number(text, index)

    # Assert
    assert new_index <= len(text)
    assert isinstance(result, int)
