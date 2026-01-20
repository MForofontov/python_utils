import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.translation_functions.rna_to_dna import rna_to_dna
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    rna_to_dna = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_rna_to_dna_normal_conversion() -> None:
    """
    Test case 1: Normal RNA to DNA conversion.
    """
    # Arrange
    rna_seq = "AUGC"
    expected = "ATGC"

    # Act
    result = rna_to_dna(rna_seq)

    # Assert
    assert result == expected


def test_rna_to_dna_all_uracil() -> None:
    """
    Test case 2: RNA sequence with all uracil bases.
    """
    # Arrange
    rna_seq = "UUUUAAAA"
    expected = "TTTTAAAA"

    # Act
    result = rna_to_dna(rna_seq)

    # Assert
    assert result == expected


def test_rna_to_dna_lowercase_input() -> None:
    """
    Test case 3: Lowercase RNA input converts to uppercase DNA.
    """
    # Arrange
    rna_seq = "augc"
    expected = "ATGC"

    # Act
    result = rna_to_dna(rna_seq)

    # Assert
    assert result == expected


def test_rna_to_dna_mixed_case_input() -> None:
    """
    Test case 4: Mixed case RNA input.
    """
    # Arrange
    rna_seq = "AuGcUaGc"
    expected = "ATGCTAGC"

    # Act
    result = rna_to_dna(rna_seq)

    # Assert
    assert result == expected


def test_rna_to_dna_empty_sequence() -> None:
    """
    Test case 5: Empty RNA sequence.
    """
    # Arrange
    rna_seq = ""
    expected = ""

    # Act
    result = rna_to_dna(rna_seq)

    # Assert
    assert result == expected


def test_rna_to_dna_long_sequence() -> None:
    """
    Test case 6: Long RNA sequence conversion.
    """
    # Arrange
    rna_seq = "AUGCAUGCUUUUAAAAGGGCCCUUU" * 100
    expected = "ATGCATGCTTTTAAAAGGGCCCTTT" * 100

    # Act
    result = rna_to_dna(rna_seq)

    # Assert
    assert result == expected
    assert len(result) == len(rna_seq)


def test_rna_to_dna_type_error_not_string() -> None:
    """
    Test case 7: TypeError when input is not a string.
    """
    # Arrange
    invalid_input = 12345  # type: ignore
    expected_message = "seq must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        rna_to_dna(invalid_input)  # type: ignore


def test_rna_to_dna_type_error_list() -> None:
    """
    Test case 8: TypeError when input is a list.
    """
    # Arrange
    invalid_input = ["A", "U", "G", "C"]  # type: ignore
    expected_message = "seq must be a string, got list"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        rna_to_dna(invalid_input)  # type: ignore


def test_rna_to_dna_value_error_invalid_bases() -> None:
    """
    Test case 9: ValueError for invalid RNA bases.
    """
    # Arrange
    invalid_seq = "ATGC"  # Contains T which is DNA, not RNA
    expected_message = "Invalid RNA bases found: T"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        rna_to_dna(invalid_seq)


def test_rna_to_dna_value_error_multiple_invalid_bases() -> None:
    """
    Test case 10: ValueError for multiple invalid bases.
    """
    # Arrange
    invalid_seq = "AUGCXYZ"
    expected_message = "Invalid RNA bases found:"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        rna_to_dna(invalid_seq)


def test_rna_to_dna_value_error_numbers() -> None:
    """
    Test case 11: ValueError for numeric characters in sequence.
    """
    # Arrange
    invalid_seq = "AUG123"
    expected_message = "Invalid RNA bases found:"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        rna_to_dna(invalid_seq)


def test_rna_to_dna_value_error_special_chars() -> None:
    """
    Test case 12: ValueError for special characters in sequence.
    """
    # Arrange
    invalid_seq = "AUG-C"
    expected_message = "Invalid RNA bases found:"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        rna_to_dna(invalid_seq)
