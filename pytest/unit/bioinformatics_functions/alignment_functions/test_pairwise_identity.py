import pytest
from bioinformatics_functions.alignment_functions.pairwise_identity import pairwise_identity


def test_pairwise_identity_identical() -> None:
    """Test identity of identical sequences."""
    assert pairwise_identity("ACGT", "ACGT") == 100.0


def test_pairwise_identity_75_percent() -> None:
    """Test 75% identity."""
    assert pairwise_identity("ACGT", "ACCT") == 75.0


def test_pairwise_identity_25_percent() -> None:
    """Test 25% identity."""
    assert pairwise_identity("ACGT", "TCGT") == 75.0


def test_pairwise_identity_zero() -> None:
    """Test 0% identity."""
    assert pairwise_identity("AAAA", "TTTT") == 0.0


def test_pairwise_identity_aligned_with_gaps() -> None:
    """Test identity with aligned sequences containing gaps."""
    # "AC-GT" vs "ACGGT": positions 0,1,3,4 compared (skip gap), 4 matches out of 4
    result = pairwise_identity("AC-GT", "ACGGT", aligned=True)
    assert result == 80.0  # 4 out of 5 positions match (gap doesn't count)


def test_pairwise_identity_aligned_different_gaps() -> None:
    """Test identity with gaps at different positions."""
    # "A-CGT" vs "ATCGT": compare positions 0,2,3,4 (skip gaps)
    result = pairwise_identity("A-CGT", "ATCGT", aligned=True)
    assert result == 80.0


def test_pairwise_identity_unequal_length_unaligned() -> None:
    """Test ValueError for unequal length when aligned=False."""
    with pytest.raises(ValueError, match="Sequences must have equal length when aligned=False"):
        pairwise_identity("ACGT", "ACT", aligned=False)


def test_pairwise_identity_unequal_length_aligned() -> None:
    """Test ValueError for unequal length when aligned=True."""
    with pytest.raises(ValueError, match="Aligned sequences must have equal length"):
        pairwise_identity("ACGT", "ACT-", aligned=True)


def test_pairwise_identity_empty_seq1() -> None:
    """Test ValueError for empty seq1."""
    with pytest.raises(ValueError, match="seq1 cannot be empty"):
        pairwise_identity("", "ACGT")


def test_pairwise_identity_empty_seq2() -> None:
    """Test ValueError for empty seq2."""
    with pytest.raises(ValueError, match="seq2 cannot be empty"):
        pairwise_identity("ACGT", "")


def test_pairwise_identity_seq1_type_error() -> None:
    """Test TypeError for non-string seq1."""
    with pytest.raises(TypeError, match="seq1 must be a string"):
        pairwise_identity(123, "ACGT")


def test_pairwise_identity_seq2_type_error() -> None:
    """Test TypeError for non-string seq2."""
    with pytest.raises(TypeError, match="seq2 must be a string"):
        pairwise_identity("ACGT", 123)
