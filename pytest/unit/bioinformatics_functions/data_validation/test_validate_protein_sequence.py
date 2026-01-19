import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.data_validation.validate_protein_sequence import (
    validate_protein_sequence,
)


def test_validate_protein_sequence_valid() -> None:
    """Test case 1: Test validation of a valid protein sequence."""
    result = validate_protein_sequence("ACDEFG")
    assert result["is_valid"] is True
    assert result["length"] == 6
    assert result["invalid_chars"] == []
    assert result["has_lowercase"] is False
    assert result["has_stop_codon"] is False
    assert result["molecular_weight"] > 0


def test_validate_protein_sequence_all_standard() -> None:
    """Test case 2: Test all 20 standard amino acids."""
    result = validate_protein_sequence("ACDEFGHIKLMNPQRSTVWY")
    assert result["is_valid"] is True
    assert result["length"] == 20
    assert result["invalid_chars"] == []


def test_validate_protein_sequence_invalid_chars() -> None:
    """Test case 3: Test validation detects invalid characters."""
    result = validate_protein_sequence("ACDEFJ")
    assert result["is_valid"] is False
    assert result["invalid_chars"] == ["J"]


def test_validate_protein_sequence_lowercase() -> None:
    """Test case 4: Test validation detects lowercase letters."""
    result = validate_protein_sequence("acdef")
    assert result["is_valid"] is True
    assert result["has_lowercase"] is True
    assert result["invalid_chars"] == []


def test_validate_protein_sequence_stop_codon() -> None:
    """Test case 5: Test detection of stop codon."""
    result = validate_protein_sequence("ACDEF*")
    assert result["is_valid"] is True
    assert result["has_stop_codon"] is True


def test_validate_protein_sequence_ambiguous() -> None:
    """Test case 6: Test ambiguous amino acid codes (B, Z, X)."""
    result = validate_protein_sequence("ABZX")
    assert result["is_valid"] is True
    assert result["invalid_chars"] == []


def test_validate_protein_sequence_molecular_weight() -> None:
    """Test case 7: Test molecular weight calculation."""
    # Alanine (A) has MW of 89.1 Da
    result = validate_protein_sequence("AAA")
    expected_weight = 89.1 * 3
    assert abs(result["molecular_weight"] - expected_weight) < 0.1


def test_validate_protein_sequence_empty() -> None:
    """Test case 8: Test validation of empty sequence."""
    result = validate_protein_sequence("")
    assert result["is_valid"] is True
    assert result["length"] == 0
    assert result["molecular_weight"] == 0.0


def test_validate_protein_sequence_type_error() -> None:
    """Test case 9: Test TypeError for non-string input."""
    with pytest.raises(TypeError, match="seq must be a string"):
        validate_protein_sequence(123)
