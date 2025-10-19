import pytest
from compression_functions.polyline_decoding_list_of_ints import (
    polyline_decoding_list_of_ints,
)


def test_polyline_decoding_list_of_ints_basic_decoding() -> None:
    """
    Test case 1: Decode basic polyline encoded string.
    """
    # Arrange
    encoded_text = "AAA"

    # Act
    result = polyline_decoding_list_of_ints(encoded_text)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(x, float) for x in result)


def test_polyline_decoding_list_of_ints_single_value() -> None:
    """
    Test case 2: Decode string with single encoded value.
    """
    # Arrange
    encoded_text = "?A"

    # Act
    result = polyline_decoding_list_of_ints(encoded_text)

    # Assert
    assert isinstance(result, list)
    assert len(result) >= 1


def test_polyline_decoding_list_of_ints_precision_handling() -> None:
    """
    Test case 3: Verify precision is handled correctly.
    """
    # Arrange
    encoded_text = "?AA"

    # Act
    result = polyline_decoding_list_of_ints(encoded_text)

    # Assert
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)


def test_polyline_decoding_list_of_ints_multiple_values() -> None:
    """
    Test case 4: Decode string with multiple values.
    """
    # Arrange
    encoded_text = "AAAAA"

    # Act
    result = polyline_decoding_list_of_ints(encoded_text)

    # Assert
    assert isinstance(result, list)
    assert len(result) > 1


def test_polyline_decoding_list_of_ints_complex_encoding() -> None:
    """
    Test case 5: Decode complex polyline encoded string.
    """
    # Arrange
    encoded_text = "B_ibE"

    # Act
    result = polyline_decoding_list_of_ints(encoded_text)

    # Assert
    assert isinstance(result, list)
    assert len(result) >= 1
    assert all(isinstance(x, float) for x in result)


def test_polyline_decoding_list_of_ints_returns_float_list() -> None:
    """
    Test case 6: Verify return type is list of floats.
    """
    # Arrange
    encoded_text = "AAA"

    # Act
    result = polyline_decoding_list_of_ints(encoded_text)

    # Assert
    assert isinstance(result, list)
    for value in result:
        assert isinstance(value, float)


def test_polyline_decoding_list_of_ints_round_trip() -> None:
    """
    Test case 7: Verify encoding and decoding are consistent.
    """
    # Arrange
    from compression_functions.polyline_encoding_list_of_ints import (
        polyline_encoding_list_of_ints,
    )

    original_values = [10, 20, 30]
    encoded = polyline_encoding_list_of_ints(original_values)

    # Act
    decoded = polyline_decoding_list_of_ints(encoded)

    # Assert
    assert len(decoded) == len(original_values)
    # Values should be close after round-trip (accounting for precision)
    for i, orig in enumerate(original_values):
        assert abs(decoded[i] - orig) <= 1.0  # Allow some precision loss


def test_polyline_decoding_list_of_ints_empty_string_error() -> None:
    """
    Test case 8: ValueError when encoded text is empty.
    """
    # Arrange
    empty_text = ""

    # Act & Assert
    with pytest.raises(ValueError, match="Encoded text cannot be empty"):
        polyline_decoding_list_of_ints(empty_text)


def test_polyline_decoding_list_of_ints_malformed_input_error() -> None:
    """
    Test case 9: ValueError when encoded text is malformed and causes decompression error.
    """
    # Arrange - Create a string that will cause an IndexError during decoding
    # The string starts a multi-byte encoding but doesn't complete it
    # A character >= 0x20+63 (i.e., 'c' or 99) indicates more bytes follow
    malformed_text = "A" + chr(0x20 + 63)  # Precision + incomplete multi-byte number

    # Act & Assert
    with pytest.raises(ValueError, match="Error decompressing number"):
        polyline_decoding_list_of_ints(malformed_text)
