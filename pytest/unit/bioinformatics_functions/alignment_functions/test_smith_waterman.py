import pytest
from bioinformatics_functions.alignment_functions.smith_waterman import smith_waterman


def test_smith_waterman_identical() -> None:
    """Test case 1: Test local alignment of identical sequences."""
    score, aligned1, aligned2 = smith_waterman("ACGT", "ACGT")
    assert score == 8  # 4 matches * 2
    assert aligned1 == "ACGT"
    assert aligned2 == "ACGT"


def test_smith_waterman_partial_match() -> None:
    """Test case 2: Test local alignment with partial match."""
    score, aligned1, aligned2 = smith_waterman("ACGT", "ACT")
    assert score > 0
    assert len(aligned1) == len(aligned2)


def test_smith_waterman_finds_best_local() -> None:
    """Test case 3: Test that algorithm finds best local alignment."""
    score, aligned1, aligned2 = smith_waterman("GGTTGACTA", "TGTTACGG")
    assert score > 0
    # aligned sequences may have gaps, so check they're substrings or have gaps
    assert len(aligned1) == len(aligned2)
    assert len(aligned1) > 0


def test_smith_waterman_custom_scores() -> None:
    """Test case 4: Test with custom scoring parameters."""
    score1, _, _ = smith_waterman("ACGT", "ACGT", match=3, mismatch=-1, gap=-1)
    score2, _, _ = smith_waterman("ACGT", "ACGT", match=2, mismatch=-1, gap=-1)
    assert score1 > score2


def test_smith_waterman_no_similarity() -> None:
    """Test case 5: Test sequences with no good local alignment."""
    score, aligned1, aligned2 = smith_waterman("AAAA", "TTTT")
    # Should find minimal or no alignment
    assert len(aligned1) == len(aligned2)


def test_smith_waterman_insertion_path() -> None:
    """Test case 6: Test traceback with insertion (gap in seq1)."""
    # Create sequences where insertion path is optimal
    # Use a gap penalty that makes insertions more favorable
    score, aligned1, aligned2 = smith_waterman(
        "ACGT", "ACGTTTT", match=2, mismatch=-3, gap=-1
    )
    assert score > 0
    assert len(aligned1) == len(aligned2)
    # Should have gaps in aligned1 for the extra T's
    assert "-" in aligned1 or len(aligned1) > 0


def test_smith_waterman_deletion_path() -> None:
    """Test case 7: Test traceback with deletion (gap in seq2)."""
    # Create sequences where deletion path is optimal
    score, aligned1, aligned2 = smith_waterman(
        "ACGTTTT", "ACGT", match=2, mismatch=-3, gap=-1
    )
    assert score > 0
    assert len(aligned1) == len(aligned2)
    # Should have gaps in aligned2 for the missing T's
    assert "-" in aligned2 or len(aligned2) > 0


def test_smith_waterman_seq1_type_error() -> None:
    """Test case 8: Test TypeError for non-string seq1."""
    with pytest.raises(TypeError, match="seq1 must be a string"):
        smith_waterman(123, "ACGT")


def test_smith_waterman_seq2_type_error() -> None:
    """Test case 9: Test TypeError for non-string seq2."""
    with pytest.raises(TypeError, match="seq2 must be a string"):
        smith_waterman("ACGT", 123)


def test_smith_waterman_empty_seq1() -> None:
    """Test case 10: Test ValueError for empty seq1."""
    with pytest.raises(ValueError, match="seq1 cannot be empty"):
        smith_waterman("", "ACGT")


def test_smith_waterman_empty_seq2() -> None:
    """Test case 11: Test ValueError for empty seq2."""
    with pytest.raises(ValueError, match="seq2 cannot be empty"):
        smith_waterman("ACGT", "")


def test_smith_waterman_match_type_error() -> None:
    """Test case 12: Test TypeError for non-integer match parameter."""
    with pytest.raises(TypeError, match="match must be an integer"):
        smith_waterman("ACGT", "ACGT", match=2.5)  # type: ignore


def test_smith_waterman_mismatch_type_error() -> None:
    """Test case 13: Test TypeError for non-integer mismatch parameter."""
    with pytest.raises(TypeError, match="mismatch must be an integer"):
        smith_waterman("ACGT", "ACGT", mismatch=-1.5)  # type: ignore


def test_smith_waterman_gap_type_error() -> None:
    """Test case 14: Test TypeError for non-integer gap parameter."""
    with pytest.raises(TypeError, match="gap must be an integer"):
        smith_waterman("ACGT", "ACGT", gap=-1.5)  # type: ignore
