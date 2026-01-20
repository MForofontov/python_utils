import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.motif_functions.find_motif_positions import (
        find_motif_positions,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    find_motif_positions = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_find_motif_positions_basic() -> None:
    """Test case 1: Test finding basic motif positions."""
    result = find_motif_positions("ATGATGATG", "ATG")
    assert result == [0, 3, 6]


def test_find_motif_positions_overlapping() -> None:
    """Test case 2: Test finding overlapping motifs."""
    result = find_motif_positions("AAAAAAA", "AAA", allow_overlap=True)
    assert result == [0, 1, 2, 3, 4]


def test_find_motif_positions_non_overlapping() -> None:
    """Test case 3: Test finding non-overlapping motifs."""
    result = find_motif_positions("AAAAAAA", "AAA", allow_overlap=False)
    # AAAAAAA is 7 chars, AAA is 3 chars: positions 0-2, 3-5, 6-8 (incomplete)
    assert result == [0, 3]  # Only complete matches


def test_find_motif_positions_not_found() -> None:
    """Test case 4: Test when motif is not found."""
    result = find_motif_positions("ATGCATGC", "TTT")
    assert result == []


def test_find_motif_positions_single_match() -> None:
    """Test case 5: Test single motif match."""
    result = find_motif_positions("ATGCATGC", "GCA")
    assert result == [2]


def test_find_motif_positions_empty_motif() -> None:
    """Test case 6: Test ValueError for empty motif."""
    with pytest.raises(ValueError, match="Motif cannot be empty"):
        find_motif_positions("ATGC", "")


def test_find_motif_positions_motif_longer_than_seq() -> None:
    """Test case 7: Test ValueError for motif longer than sequence."""
    with pytest.raises(
        ValueError, match="Motif length .* cannot be greater than sequence length"
    ):
        find_motif_positions("ATG", "ATGCATGC")


def test_find_motif_positions_seq_type_error() -> None:
    """Test case 8: Test TypeError for non-string seq."""
    with pytest.raises(TypeError, match="seq must be a string"):
        find_motif_positions(123, "ATG")


def test_find_motif_positions_motif_type_error() -> None:
    """Test case 9: Test TypeError for non-string motif."""
    with pytest.raises(TypeError, match="motif must be a string"):
        find_motif_positions("ATGC", 123)


def test_find_motif_positions_allow_overlap_type_error() -> None:
    """Test case 10: Test TypeError for non-boolean allow_overlap."""
    with pytest.raises(TypeError, match="allow_overlap must be a boolean"):
        find_motif_positions("ATGC", "ATG", allow_overlap="yes")  # type: ignore
