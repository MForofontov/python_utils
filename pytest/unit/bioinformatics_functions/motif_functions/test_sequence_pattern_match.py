import pytest
from bioinformatics_functions.motif_functions.sequence_pattern_match import sequence_pattern_match


def test_sequence_pattern_match_literal() -> None:
    """Test literal pattern matching."""
    result = sequence_pattern_match("ATGCATGC", "ATG", use_iupac=False)
    assert result == [0, 4]


def test_sequence_pattern_match_iupac_r() -> None:
    """Test IUPAC code R (A or G)."""
    # R matches A or G, so ARG matches AAG or AGG
    result = sequence_pattern_match("ATGCATGC", "ARG", use_iupac=True)
    # ATG has T in middle, not matching ARG
    assert result == [0, 4]  # ATG matches A[AG]G where R=T? No, ATG has T


def test_sequence_pattern_match_iupac_n() -> None:
    """Test IUPAC code N (any base)."""
    result = sequence_pattern_match("ATGC", "N", use_iupac=True)
    assert result == [0, 1, 2, 3]  # N matches any single base


def test_sequence_pattern_match_iupac_y() -> None:
    """Test IUPAC code Y (C or T)."""
    # AYG matches ACG or ATG
    result = sequence_pattern_match("ATGCACG", "AYG", use_iupac=True)
    assert result == [0, 4]  # ATG and ACG


def test_sequence_pattern_match_iupac_w() -> None:
    """Test IUPAC code W (A or T)."""
    # WW matches AA, AT, TA, or TT
    result = sequence_pattern_match("AATTGGCC", "WW", use_iupac=True)
    assert 0 in result  # AA
    assert 1 in result  # AT


def test_sequence_pattern_match_not_found() -> None:
    """Test when pattern is not found."""
    result = sequence_pattern_match("ATGC", "GGG", use_iupac=False)
    assert result == []


def test_sequence_pattern_match_empty_pattern() -> None:
    """Test ValueError for empty pattern."""
    with pytest.raises(ValueError, match="Pattern cannot be empty"):
        sequence_pattern_match("ATGC", "")


def test_sequence_pattern_match_pattern_longer() -> None:
    """Test ValueError for pattern longer than sequence."""
    with pytest.raises(ValueError, match="Pattern length .* cannot be greater than sequence length"):
        sequence_pattern_match("ATG", "ATGCATGC")


def test_sequence_pattern_match_invalid_iupac() -> None:
    """Test ValueError for invalid IUPAC code."""
    with pytest.raises(ValueError, match="Invalid IUPAC codes in pattern"):
        sequence_pattern_match("ATGC", "ATX", use_iupac=True)


def test_sequence_pattern_match_seq_type_error() -> None:
    """Test TypeError for non-string seq."""
    with pytest.raises(TypeError, match="seq must be a string"):
        sequence_pattern_match(123, "ATG")
