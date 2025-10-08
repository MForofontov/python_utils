import pytest
from bioinformatics_functions.alignment_functions.smith_waterman import smith_waterman


def test_smith_waterman_identical() -> None:
    """Test local alignment of identical sequences."""
    score, aligned1, aligned2 = smith_waterman("ACGT", "ACGT")
    assert score == 8  # 4 matches * 2
    assert aligned1 == "ACGT"
    assert aligned2 == "ACGT"


def test_smith_waterman_partial_match() -> None:
    """Test local alignment with partial match."""
    score, aligned1, aligned2 = smith_waterman("ACGT", "ACT")
    assert score > 0
    assert len(aligned1) == len(aligned2)


def test_smith_waterman_finds_best_local() -> None:
    """Test that algorithm finds best local alignment."""
    score, aligned1, aligned2 = smith_waterman("GGTTGACTA", "TGTTACGG")
    assert score > 0
    assert aligned1 in "GGTTGACTA"
    assert aligned2 in "TGTTACGG"


def test_smith_waterman_custom_scores() -> None:
    """Test with custom scoring parameters."""
    score1, _, _ = smith_waterman("ACGT", "ACGT", match=3, mismatch=-1, gap=-1)
    score2, _, _ = smith_waterman("ACGT", "ACGT", match=2, mismatch=-1, gap=-1)
    assert score1 > score2


def test_smith_waterman_no_similarity() -> None:
    """Test sequences with no good local alignment."""
    score, aligned1, aligned2 = smith_waterman("AAAA", "TTTT")
    # Should find minimal or no alignment
    assert len(aligned1) == len(aligned2)


def test_smith_waterman_seq1_type_error() -> None:
    """Test TypeError for non-string seq1."""
    with pytest.raises(TypeError, match="seq1 must be a string"):
        smith_waterman(123, "ACGT")


def test_smith_waterman_seq2_type_error() -> None:
    """Test TypeError for non-string seq2."""
    with pytest.raises(TypeError, match="seq2 must be a string"):
        smith_waterman("ACGT", 123)


def test_smith_waterman_empty_seq1() -> None:
    """Test ValueError for empty seq1."""
    with pytest.raises(ValueError, match="seq1 cannot be empty"):
        smith_waterman("", "ACGT")


def test_smith_waterman_empty_seq2() -> None:
    """Test ValueError for empty seq2."""
    with pytest.raises(ValueError, match="seq2 cannot be empty"):
        smith_waterman("ACGT", "")
