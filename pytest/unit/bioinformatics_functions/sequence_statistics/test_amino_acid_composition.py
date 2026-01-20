import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.sequence_statistics.amino_acid_composition import (
        amino_acid_composition,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    amino_acid_composition = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_amino_acid_composition_balanced_composition() -> None:
    """
    Test case 1: Balanced amino acid composition.
    """
    # Arrange
    seq = "ACDEFGH"

    # Act
    result = amino_acid_composition(seq)

    # Assert
    assert len(result) == 7
    for _aa, percentage in result.items():
        assert abs(percentage - 14.29) < 0.01  # Each is ~14.29%


def test_amino_acid_composition_single_amino_acid() -> None:
    """
    Test case 2: Single amino acid type.
    """
    # Arrange
    seq = "AAAA"
    expected = {"A": 100.0}

    # Act
    result = amino_acid_composition(seq)

    # Assert
    assert result == expected


def test_amino_acid_composition_multiple_same() -> None:
    """
    Test case 3: Multiple occurrences of same amino acids.
    """
    # Arrange
    seq = "AAAACCCC"  # 50% A, 50% C

    # Act
    result = amino_acid_composition(seq)

    # Assert
    assert result["A"] == 50.0
    assert result["C"] == 50.0
    assert len(result) == 2


def test_amino_acid_composition_lowercase_input() -> None:
    """
    Test case 4: Lowercase amino acid sequence.
    """
    # Arrange
    seq = "acdefgh"

    # Act
    result = amino_acid_composition(seq)

    # Assert
    assert len(result) == 7
    assert all(isinstance(v, float) for v in result.values())


def test_amino_acid_composition_mixed_case() -> None:
    """
    Test case 5: Mixed case amino acid sequence.
    """
    # Arrange
    seq = "AaCcDdEe"

    # Act
    result = amino_acid_composition(seq)

    # Assert
    assert result["A"] == 25.0
    assert result["C"] == 25.0
    assert result["D"] == 25.0
    assert result["E"] == 25.0


def test_amino_acid_composition_all_amino_acids() -> None:
    """
    Test case 6: Sequence with all 20 amino acids.
    """
    # Arrange
    seq = "ACDEFGHIKLMNPQRSTVWY"

    # Act
    result = amino_acid_composition(seq)

    # Assert
    assert len(result) == 20
    for percentage in result.values():
        assert abs(percentage - 5.0) < 0.01  # Each is 5%


def test_amino_acid_composition_long_sequence() -> None:
    """
    Test case 7: Long protein sequence.
    """
    # Arrange
    seq = "ACDEFGHIKLMNPQRSTVWY" * 10  # 200 amino acids

    # Act
    result = amino_acid_composition(seq)

    # Assert
    assert len(result) == 20
    for percentage in result.values():
        assert abs(percentage - 5.0) < 0.01


def test_amino_acid_composition_type_error_not_string() -> None:
    """
    Test case 8: TypeError when input is not a string.
    """
    # Arrange
    invalid_input = 12345  # type: ignore
    expected_message = "seq must be str, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        amino_acid_composition(invalid_input)  # type: ignore


def test_amino_acid_composition_type_error_list() -> None:
    """
    Test case 9: TypeError when input is a list.
    """
    # Arrange
    invalid_input = ["A", "C", "D"]  # type: ignore
    expected_message = "seq must be str, got list"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        amino_acid_composition(invalid_input)  # type: ignore


def test_amino_acid_composition_value_error_empty_sequence() -> None:
    """
    Test case 10: ValueError for empty sequence.
    """
    # Arrange
    invalid_seq = ""
    expected_message = "Sequence cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        amino_acid_composition(invalid_seq)


def test_amino_acid_composition_value_error_invalid_amino_acid() -> None:
    """
    Test case 11: ValueError for invalid amino acid codes.
    """
    # Arrange
    invalid_seq = "ACDEFGHXYZ"
    expected_message = "Sequence contains invalid amino acid codes"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        amino_acid_composition(invalid_seq)


def test_amino_acid_composition_value_error_numbers() -> None:
    """
    Test case 12: ValueError for numeric characters.
    """
    # Arrange
    invalid_seq = "ACD123"
    expected_message = "Sequence contains invalid amino acid codes"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        amino_acid_composition(invalid_seq)


def test_amino_acid_composition_value_error_special_chars() -> None:
    """
    Test case 13: ValueError for special characters.
    """
    # Arrange
    invalid_seq = "ACD-EF"
    expected_message = "Sequence contains invalid amino acid codes"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        amino_acid_composition(invalid_seq)
