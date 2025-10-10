import pytest
from bioinformatics_functions.sequence_statistics.calculate_isoelectric_point import (
    calculate_isoelectric_point,
)


def test_calculate_isoelectric_point_acidic_protein() -> None:
    """
    Test case 1: Acidic protein with excess negative charges.
    """
    # Arrange
    seq = "ACDEFGH"  # Has D and E (acidic)

    # Act
    result = calculate_isoelectric_point(seq)

    # Assert
    assert isinstance(result, float)
    assert result < 7.0  # Acidic proteins have pI < 7


def test_calculate_isoelectric_point_basic_protein() -> None:
    """
    Test case 2: Basic protein with excess positive charges.
    """
    # Arrange
    seq = "KKKKK"  # All lysine (basic)

    # Act
    result = calculate_isoelectric_point(seq)

    # Assert
    assert isinstance(result, float)
    assert result > 7.0  # Basic proteins have pI > 7


def test_calculate_isoelectric_point_neutral_protein() -> None:
    """
    Test case 3: Neutral protein.
    """
    # Arrange
    seq = "AAAAGGGG"  # No charged residues

    # Act
    result = calculate_isoelectric_point(seq)

    # Assert
    assert isinstance(result, float)
    assert result == 7.0  # Neutral proteins have pI ~7


def test_calculate_isoelectric_point_balanced_charges() -> None:
    """
    Test case 4: Balanced positive and negative charges.
    """
    # Arrange
    seq = "KDEKDEKD"  # Equal K (basic) and D (acidic)

    # Act
    result = calculate_isoelectric_point(seq)

    # Assert
    assert isinstance(result, float)
    assert result == 7.0  # Balanced charges


def test_calculate_isoelectric_point_lowercase_input() -> None:
    """
    Test case 5: Lowercase amino acid sequence.
    """
    # Arrange
    seq = "acdefgh"

    # Act
    result = calculate_isoelectric_point(seq)

    # Assert
    assert isinstance(result, float)


def test_calculate_isoelectric_point_mixed_case() -> None:
    """
    Test case 6: Mixed case amino acid sequence.
    """
    # Arrange
    seq = "AcDeFgH"

    # Act
    result = calculate_isoelectric_point(seq)

    # Assert
    assert isinstance(result, float)


def test_calculate_isoelectric_point_long_sequence() -> None:
    """
    Test case 7: Long protein sequence.
    """
    # Arrange
    seq = "ACDEFGHIKLMNPQRSTVWY" * 10

    # Act
    result = calculate_isoelectric_point(seq)

    # Assert
    assert isinstance(result, float)
    assert 0 < result < 14  # pH range


def test_calculate_isoelectric_point_all_charged_residues() -> None:
    """
    Test case 8: Only charged residues.
    """
    # Arrange
    seq = "DEKR"  # D,E (acidic), K,R (basic)

    # Act
    result = calculate_isoelectric_point(seq)

    # Assert
    assert isinstance(result, float)


def test_calculate_isoelectric_point_type_error_not_string() -> None:
    """
    Test case 9: TypeError when input is not a string.
    """
    # Arrange
    invalid_input = 12345  # type: ignore
    expected_message = "seq must be str, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        calculate_isoelectric_point(invalid_input)  # type: ignore


def test_calculate_isoelectric_point_type_error_list() -> None:
    """
    Test case 10: TypeError when input is a list.
    """
    # Arrange
    invalid_input = ["A", "C", "D"]  # type: ignore
    expected_message = "seq must be str, got list"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        calculate_isoelectric_point(invalid_input)  # type: ignore


def test_calculate_isoelectric_point_value_error_empty_sequence() -> None:
    """
    Test case 11: ValueError for empty sequence.
    """
    # Arrange
    invalid_seq = ""
    expected_message = "Sequence cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        calculate_isoelectric_point(invalid_seq)


def test_calculate_isoelectric_point_value_error_invalid_amino_acid() -> None:
    """
    Test case 12: ValueError for invalid amino acid codes.
    """
    # Arrange
    invalid_seq = "ACDEFGHXYZ"
    expected_message = "Sequence contains invalid amino acid codes"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        calculate_isoelectric_point(invalid_seq)


def test_calculate_isoelectric_point_value_error_numbers() -> None:
    """
    Test case 13: ValueError for numeric characters.
    """
    # Arrange
    invalid_seq = "ACD123"
    expected_message = "Sequence contains invalid amino acid codes"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        calculate_isoelectric_point(invalid_seq)


def test_calculate_isoelectric_point_value_error_special_chars() -> None:
    """
    Test case 14: ValueError for special characters.
    """
    # Arrange
    invalid_seq = "ACD-EF"
    expected_message = "Sequence contains invalid amino acid codes"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        calculate_isoelectric_point(invalid_seq)
