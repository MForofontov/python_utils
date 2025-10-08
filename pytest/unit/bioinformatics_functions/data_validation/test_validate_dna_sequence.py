import pytest
from bioinformatics_functions.data_validation.validate_dna_sequence import validate_dna_sequence


def test_validate_dna_sequence_valid() -> None:
    """Test validation of a valid DNA sequence."""
    result = validate_dna_sequence("ATGC")
    assert result['is_valid'] is True
    assert result['length'] == 4
    assert result['invalid_chars'] == []
    assert result['has_lowercase'] is False
    assert result['gc_content'] == 50.0


def test_validate_dna_sequence_invalid_chars() -> None:
    """Test validation detects invalid characters."""
    result = validate_dna_sequence("ATGCX")
    assert result['is_valid'] is False
    assert result['length'] == 5
    assert result['invalid_chars'] == ['X']
    # GC content counts only valid ATGC: 2 GC out of 4 valid = 50%
    assert result['gc_content'] == 50.0


def test_validate_dna_sequence_lowercase() -> None:
    """Test validation detects lowercase letters."""
    result = validate_dna_sequence("atgc")
    assert result['is_valid'] is True
    assert result['length'] == 4
    assert result['invalid_chars'] == []
    assert result['has_lowercase'] is True
    assert result['gc_content'] == 50.0


def test_validate_dna_sequence_ambiguous_not_allowed() -> None:
    """Test ambiguous codes rejected when not allowed."""
    result = validate_dna_sequence("ATGCN")
    assert result['is_valid'] is False
    assert 'N' in result['invalid_chars']


def test_validate_dna_sequence_ambiguous_allowed() -> None:
    """Test ambiguous codes accepted when allowed."""
    result = validate_dna_sequence("ATGCN", allow_ambiguous=True)
    assert result['is_valid'] is True
    assert result['invalid_chars'] == []


def test_validate_dna_sequence_all_gc() -> None:
    """Test GC content calculation for all GC."""
    result = validate_dna_sequence("GGCC")
    assert result['gc_content'] == 100.0


def test_validate_dna_sequence_no_gc() -> None:
    """Test GC content calculation for no GC."""
    result = validate_dna_sequence("ATAT")
    assert result['gc_content'] == 0.0


def test_validate_dna_sequence_empty() -> None:
    """Test validation of empty sequence."""
    result = validate_dna_sequence("")
    assert result['is_valid'] is True
    assert result['length'] == 0
    assert result['gc_content'] == 0.0


def test_validate_dna_sequence_type_error() -> None:
    """Test TypeError for non-string input."""
    with pytest.raises(TypeError, match="seq must be a string"):
        validate_dna_sequence(123)


def test_validate_dna_sequence_allow_ambiguous_type_error() -> None:
    """Test TypeError for non-boolean allow_ambiguous."""
    with pytest.raises(TypeError, match="allow_ambiguous must be a boolean"):
        validate_dna_sequence("ATGC", allow_ambiguous="yes")
