import pytest
from bioinformatics_functions.alignment_functions.needleman_wunsch import needleman_wunsch


def test_needleman_wunsch_identical() -> None:
    """Test case 1: Test alignment of identical sequences."""
    score, aligned1, aligned2 = needleman_wunsch("ACGT", "ACGT")
    assert score == 4  # 4 matches
    assert aligned1 == "ACGT"
    assert aligned2 == "ACGT"


def test_needleman_wunsch_one_gap() -> None:
    """Test case 2: Test alignment with one gap."""
    score, aligned1, aligned2 = needleman_wunsch("ACGT", "ACT")
    assert score == 2
    assert '-' in aligned1 or '-' in aligned2
    assert len(aligned1) == len(aligned2)


def test_needleman_wunsch_insertion() -> None:
    """Test case 3: Test alignment with insertion."""
    score, aligned1, aligned2 = needleman_wunsch("GAT", "GAAT")
    assert len(aligned1) == len(aligned2)
    assert '-' in aligned1


def test_needleman_wunsch_custom_scores() -> None:
    """Test case 4: Test with custom scoring parameters."""
    score1, _, _ = needleman_wunsch("ACGT", "ACGT", match=2, mismatch=-2, gap=-1)
    score2, _, _ = needleman_wunsch("ACGT", "ACGT", match=1, mismatch=-1, gap=-1)
    assert score1 > score2  # Higher match score gives higher total


def test_needleman_wunsch_completely_different() -> None:
    """Test case 5: Test alignment of completely different sequences."""
    score, aligned1, aligned2 = needleman_wunsch("AAAA", "TTTT")
    assert score < 0  # All mismatches
    assert len(aligned1) == len(aligned2)


def test_needleman_wunsch_seq1_type_error() -> None:
    """Test case 6: Test TypeError for non-string seq1."""
    with pytest.raises(TypeError, match="seq1 must be a string"):
        needleman_wunsch(123, "ACGT")


def test_needleman_wunsch_seq2_type_error() -> None:
    """Test case 7: Test TypeError for non-string seq2."""
    with pytest.raises(TypeError, match="seq2 must be a string"):
        needleman_wunsch("ACGT", 123)


def test_needleman_wunsch_empty_seq1() -> None:
    """Test case 8: Test ValueError for empty seq1."""
    with pytest.raises(ValueError, match="seq1 cannot be empty"):
        needleman_wunsch("", "ACGT")


def test_needleman_wunsch_empty_seq2() -> None:
    """Test case 9: Test ValueError for empty seq2."""
    with pytest.raises(ValueError, match="seq2 cannot be empty"):
        needleman_wunsch("ACGT", "")
