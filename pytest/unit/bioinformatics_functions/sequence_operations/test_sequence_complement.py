import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.sequence_operations.sequence_complement import (
    sequence_complement,
)


def test_sequence_complement_normal_sequence() -> None:
    """
    Test case 1: Normal DNA complement conversion.
    """
    # Arrange
    seq = "ATGC"
    expected = "TACG"

    # Act
    result = sequence_complement(seq)

    # Assert
    assert result == expected


def test_sequence_complement_all_adenine() -> None:
    """
    Test case 2: Sequence with all adenine bases.
    """
    # Arrange
    seq = "AAAA"
    expected = "TTTT"

    # Act
    result = sequence_complement(seq)

    # Assert
    assert result == expected


def test_sequence_complement_all_thymine() -> None:
    """
    Test case 3: Sequence with all thymine bases.
    """
    # Arrange
    seq = "TTTT"
    expected = "AAAA"

    # Act
    result = sequence_complement(seq)

    # Assert
    assert result == expected


def test_sequence_complement_lowercase_input() -> None:
    """
    Test case 4: Lowercase DNA input converts to uppercase complement.
    """
    # Arrange
    seq = "atgc"
    expected = "TACG"

    # Act
    result = sequence_complement(seq)

    # Assert
    assert result == expected


def test_sequence_complement_mixed_case() -> None:
    """
    Test case 5: Mixed case DNA input.
    """
    # Arrange
    seq = "AtGc"
    expected = "TACG"

    # Act
    result = sequence_complement(seq)

    # Assert
    assert result == expected


def test_sequence_complement_empty_sequence() -> None:
    """
    Test case 6: Empty DNA sequence.
    """
    # Arrange
    seq = ""
    expected = ""

    # Act
    result = sequence_complement(seq)

    # Assert
    assert result == expected


def test_sequence_complement_long_sequence() -> None:
    """
    Test case 7: Long DNA sequence complement.
    """
    # Arrange
    seq = "ATGCATGC" * 100
    expected = "TACGTACG" * 100

    # Act
    result = sequence_complement(seq)

    # Assert
    assert result == expected
    assert len(result) == len(seq)


def test_sequence_complement_palindrome() -> None:
    """
    Test case 8: Palindromic sequence (complement equals reverse).
    """
    # Arrange
    seq = "GAATTC"  # EcoRI recognition site
    complement = "CTTAAG"

    # Act
    result = sequence_complement(seq)

    # Assert
    assert result == complement
    assert result[::-1] == seq  # Palindromic property


def test_sequence_complement_type_error_not_string() -> None:
    """
    Test case 9: TypeError when input is not a string.
    """
    # Arrange
    invalid_input = 12345  # type: ignore
    expected_message = "seq must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        sequence_complement(invalid_input)  # type: ignore


def test_sequence_complement_type_error_list() -> None:
    """
    Test case 10: TypeError when input is a list.
    """
    # Arrange
    invalid_input = ["A", "T", "G", "C"]  # type: ignore
    expected_message = "seq must be a string, got list"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        sequence_complement(invalid_input)  # type: ignore


def test_sequence_complement_value_error_invalid_base() -> None:
    """
    Test case 11: ValueError for invalid DNA base.
    """
    # Arrange
    invalid_seq = "ATGCX"
    expected_message = "Invalid DNA bases found: X"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        sequence_complement(invalid_seq)


def test_sequence_complement_value_error_rna_base() -> None:
    """
    Test case 12: ValueError for RNA base (U).
    """
    # Arrange
    invalid_seq = "AUGC"
    expected_message = "Invalid DNA bases found: U"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        sequence_complement(invalid_seq)


def test_sequence_complement_value_error_numbers() -> None:
    """
    Test case 13: ValueError for numeric characters.
    """
    # Arrange
    invalid_seq = "ATG123"
    expected_message = "Invalid DNA bases found:"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        sequence_complement(invalid_seq)


def test_sequence_complement_value_error_special_chars() -> None:
    """
    Test case 14: ValueError for special characters.
    """
    # Arrange
    invalid_seq = "ATG-C"
    expected_message = "Invalid DNA bases found:"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        sequence_complement(invalid_seq)
