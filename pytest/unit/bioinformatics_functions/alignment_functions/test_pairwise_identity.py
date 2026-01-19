import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.alignment_functions.pairwise_identity import (
    pairwise_identity,
)


def test_pairwise_identity_identical() -> None:
    """Test case 1: Test identity of identical sequences."""
    assert pairwise_identity("ACGT", "ACGT") == 100.0


def test_pairwise_identity_75_percent() -> None:
    """Test case 2: Test 75% identity (3 out of 4 match)."""
    assert pairwise_identity("ACGT", "ACCT") == 75.0


def test_pairwise_identity_50_percent() -> None:
    """Test case 3: Test 50% identity (2 out of 4 match)."""
    assert pairwise_identity("ACGT", "AGTT") == 50.0


def test_pairwise_identity_zero() -> None:
    """Test case 4: Test 0% identity (no matches)."""
    assert pairwise_identity("AAAA", "TTTT") == 0.0


def test_pairwise_identity_aligned_with_gaps() -> None:
    """Test case 5: Test identity with aligned sequences containing gaps."""
    # "AC-GT" vs "ACGGT": positions 0,1,3,4 compared (skip gap at pos 2), 4 matches out of 4 = 100%
    result = pairwise_identity("AC-GT", "ACGGT", aligned=True)
    assert result == 100.0  # Only non-gap positions compared, all match


def test_pairwise_identity_aligned_different_gaps() -> None:
    """Test case 6: Test identity with gaps at different positions."""
    # "A-CGT" vs "ATCGT": compare positions 0,2,3,4 (skip gap at pos 1), all 4 match = 100%
    result = pairwise_identity("A-CGT", "ATCGT", aligned=True)
    assert result == 100.0


def test_pairwise_identity_unequal_length_unaligned() -> None:
    """Test case 7: Test ValueError for unequal length when aligned=False."""
    with pytest.raises(
        ValueError, match="Sequences must have equal length when aligned=False"
    ):
        pairwise_identity("ACGT", "ACT", aligned=False)


def test_pairwise_identity_unequal_length_aligned() -> None:
    """Test case 8: Test ValueError for unequal length when aligned=True."""
    with pytest.raises(ValueError, match="Aligned sequences must have equal length"):
        pairwise_identity("ACGT", "ACT", aligned=True)


def test_pairwise_identity_empty_seq1() -> None:
    """Test case 9: Test ValueError for empty seq1."""
    with pytest.raises(ValueError, match="seq1 cannot be empty"):
        pairwise_identity("", "ACGT")


def test_pairwise_identity_empty_seq2() -> None:
    """Test case 10: Test ValueError for empty seq2."""
    with pytest.raises(ValueError, match="seq2 cannot be empty"):
        pairwise_identity("ACGT", "")


def test_pairwise_identity_seq1_type_error() -> None:
    """Test case 11: Test TypeError for non-string seq1."""
    with pytest.raises(TypeError, match="seq1 must be a string"):
        pairwise_identity(123, "ACGT")


def test_pairwise_identity_seq2_type_error() -> None:
    """Test case 12: Test TypeError for non-string seq2."""
    with pytest.raises(TypeError, match="seq2 must be a string"):
        pairwise_identity("ACGT", 123)


def test_pairwise_identity_aligned_type_error() -> None:
    """Test case 13: Test TypeError for non-boolean aligned parameter."""
    with pytest.raises(TypeError, match="aligned must be a boolean"):
        pairwise_identity("ACGT", "ACGT", aligned="yes")  # type: ignore


def test_pairwise_identity_all_gaps() -> None:
    """Test case 14: Test 0% identity when all positions are gaps."""
    # Both sequences have only gaps, no positions to compare
    result = pairwise_identity("---", "---", aligned=True)
    assert result == 0.0
