import pytest
from bioinformatics_functions.sequence_statistics.dinucleotide_frequency import (
    dinucleotide_frequency,
)


def test_dinucleotide_frequency_simple_sequence() -> None:
    """
    Test case 1: Dinucleotide frequency with simple sequence.
    """
    # Arrange
    seq = "ATGC"

    # Act
    result = dinucleotide_frequency(seq)

    # Assert
    assert result["AT"] == 1
    assert result["TG"] == 1
    assert result["GC"] == 1
    assert result["AA"] == 0


def test_dinucleotide_frequency_repeated_dinucleotide() -> None:
    """
    Test case 2: Sequence with repeated dinucleotide.
    """
    # Arrange
    seq = "AAAA"

    # Act
    result = dinucleotide_frequency(seq)

    # Assert
    assert result["AA"] == 3
    assert result["AT"] == 0


def test_dinucleotide_frequency_alternating_pattern() -> None:
    """
    Test case 3: Alternating pattern sequence.
    """
    # Arrange
    seq = "ATATATAT"

    # Act
    result = dinucleotide_frequency(seq)

    # Assert
    assert result["AT"] == 4
    assert result["TA"] == 3
    assert result["AA"] == 0


def test_dinucleotide_frequency_lowercase_input() -> None:
    """
    Test case 4: Lowercase DNA input.
    """
    # Arrange
    seq = "atgc"

    # Act
    result = dinucleotide_frequency(seq)

    # Assert
    assert result["AT"] == 1
    assert result["TG"] == 1
    assert result["GC"] == 1


def test_dinucleotide_frequency_mixed_case() -> None:
    """
    Test case 5: Mixed case DNA input.
    """
    # Arrange
    seq = "AtGc"

    # Act
    result = dinucleotide_frequency(seq)

    # Assert
    assert result["AT"] == 1
    assert result["TG"] == 1
    assert result["GC"] == 1


def test_dinucleotide_frequency_minimum_length() -> None:
    """
    Test case 6: Minimum valid sequence length (2 bases).
    """
    # Arrange
    seq = "AT"

    # Act
    result = dinucleotide_frequency(seq)

    # Assert
    assert result["AT"] == 1
    assert sum(result.values()) == 1


def test_dinucleotide_frequency_all_dinucleotides_present() -> None:
    """
    Test case 7: All 16 possible dinucleotides in result.
    """
    # Arrange
    seq = "ATGC"

    # Act
    result = dinucleotide_frequency(seq)

    # Assert
    assert len(result) == 16  # 4x4 possible dinucleotides
    bases = ["A", "T", "G", "C"]
    for b1 in bases:
        for b2 in bases:
            dinuc = f"{b1}{b2}"
            assert dinuc in result


def test_dinucleotide_frequency_long_sequence() -> None:
    """
    Test case 8: Long DNA sequence.
    """
    # Arrange
    seq = "ATGC" * 100  # 400 bases, 399 dinucleotides

    # Act
    result = dinucleotide_frequency(seq)

    # Assert
    assert result["AT"] == 100
    assert result["TG"] == 100
    assert result["GC"] == 100
    assert result["CA"] == 99  # Wraps around


def test_dinucleotide_frequency_type_error_not_string() -> None:
    """
    Test case 9: TypeError when input is not a string.
    """
    # Arrange
    invalid_input = 12345  # type: ignore
    expected_message = "seq must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        dinucleotide_frequency(invalid_input)  # type: ignore


def test_dinucleotide_frequency_type_error_list() -> None:
    """
    Test case 10: TypeError when input is a list.
    """
    # Arrange
    invalid_input = ["A", "T"]  # type: ignore
    expected_message = "seq must be a string, got list"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        dinucleotide_frequency(invalid_input)  # type: ignore


def test_dinucleotide_frequency_value_error_too_short() -> None:
    """
    Test case 11: ValueError when sequence is too short.
    """
    # Arrange
    invalid_seq = "A"
    expected_message = "Sequence must be at least 2 bases long, got 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        dinucleotide_frequency(invalid_seq)


def test_dinucleotide_frequency_value_error_empty_sequence() -> None:
    """
    Test case 12: ValueError for empty sequence.
    """
    # Arrange
    invalid_seq = ""
    expected_message = "Sequence must be at least 2 bases long, got 0"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        dinucleotide_frequency(invalid_seq)


def test_dinucleotide_frequency_value_error_invalid_base() -> None:
    """
    Test case 13: ValueError for invalid DNA base.
    """
    # Arrange
    invalid_seq = "ATGCX"
    expected_message = "Invalid DNA bases found: X"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        dinucleotide_frequency(invalid_seq)


def test_dinucleotide_frequency_value_error_rna_base() -> None:
    """
    Test case 14: ValueError for RNA base (U).
    """
    # Arrange
    invalid_seq = "AUGC"
    expected_message = "Invalid DNA bases found: U"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        dinucleotide_frequency(invalid_seq)


def test_dinucleotide_frequency_value_error_numbers() -> None:
    """
    Test case 15: ValueError for numeric characters.
    """
    # Arrange
    invalid_seq = "ATG123"
    expected_message = "Invalid DNA bases found:"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        dinucleotide_frequency(invalid_seq)


def test_dinucleotide_frequency_value_error_special_chars() -> None:
    """
    Test case 16: ValueError for special characters.
    """
    # Arrange
    invalid_seq = "ATG-C"
    expected_message = "Invalid DNA bases found:"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        dinucleotide_frequency(invalid_seq)
