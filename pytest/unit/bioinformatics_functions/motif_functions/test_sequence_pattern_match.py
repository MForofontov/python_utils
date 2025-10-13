import pytest
from bioinformatics_functions.motif_functions.sequence_pattern_match import (
    sequence_pattern_match,
)


def test_sequence_pattern_match_literal() -> None:
    """Test case 1: Test literal pattern matching."""
    result = sequence_pattern_match("ATGCATGC", "ATG", use_iupac=False)
    assert result == [0, 4]


def test_sequence_pattern_match_iupac_r() -> None:
    """Test case 2: Test IUPAC code R (A or G)."""
    # R matches A or G, so ARG matches AAG or AGG
    # ATGCATGC has ATG which has T in middle, not matching
    result = sequence_pattern_match("AAGCAGG", "ARG", use_iupac=True)
    assert result == [0, 4]  # AAG at 0, AGG at 4


def test_sequence_pattern_match_iupac_n() -> None:
    """Test case 3: Test IUPAC code N (any base)."""
    result = sequence_pattern_match("ATGC", "N", use_iupac=True)
    assert result == [0, 1, 2, 3]  # N matches any single base


def test_sequence_pattern_match_iupac_y() -> None:
    """Test case 4: Test IUPAC code Y (C or T)."""
    # AYG matches ACG or ATG
    result = sequence_pattern_match("ATGCACG", "AYG", use_iupac=True)
    assert result == [0, 4]  # ATG and ACG


def test_sequence_pattern_match_iupac_w() -> None:
    """Test case 5: Test IUPAC code W (A or T)."""
    # WW matches AA, AT, TA, or TT
    # Note: regex finditer returns non-overlapping matches
    result = sequence_pattern_match("AATTGGCC", "WW", use_iupac=True)
    assert 0 in result  # AA at position 0-1
    assert 2 in result  # TT at position 2-3 (pos 1 skipped, used by match at 0)


def test_sequence_pattern_match_not_found() -> None:
    """Test case 6: Test when pattern is not found."""
    result = sequence_pattern_match("ATGC", "GGG", use_iupac=False)
    assert result == []


def test_sequence_pattern_match_empty_pattern() -> None:
    """Test case 7: Test ValueError for empty pattern."""
    with pytest.raises(ValueError, match="Pattern cannot be empty"):
        sequence_pattern_match("ATGC", "")


def test_sequence_pattern_match_pattern_longer() -> None:
    """Test case 8: Test ValueError for pattern longer than sequence."""
    with pytest.raises(
        ValueError, match="Pattern length .* cannot be greater than sequence length"
    ):
        sequence_pattern_match("ATG", "ATGCATGC")


def test_sequence_pattern_match_invalid_iupac() -> None:
    """Test case 9: Test ValueError for invalid IUPAC code."""
    with pytest.raises(ValueError, match="Invalid IUPAC codes in pattern"):
        sequence_pattern_match("ATGC", "ATX", use_iupac=True)


def test_sequence_pattern_match_invalid_sequence_type() -> None:
    """Test case 10: TypeError for non-string seq."""
    with pytest.raises(TypeError, match="seq must be a string"):
        sequence_pattern_match(123, "ATG")


def test_sequence_pattern_match_invalid_use_iupac_type() -> None:
    """Test case 11: TypeError for non-boolean use_iupac."""
    with pytest.raises(TypeError, match="use_iupac must be a boolean"):
        sequence_pattern_match("ATGC", "ATG", use_iupac="yes")  # type: ignore
