import pytest
from bioinformatics_functions.motif_functions.find_motif_positions import find_motif_positions


def test_find_motif_positions_basic() -> None:
    """Test finding basic motif positions."""
    result = find_motif_positions("ATGATGATG", "ATG")
    assert result == [0, 3, 6]


def test_find_motif_positions_overlapping() -> None:
    """Test finding overlapping motifs."""
    result = find_motif_positions("AAAAAAA", "AAA", allow_overlap=True)
    assert result == [0, 1, 2, 3, 4]


def test_find_motif_positions_non_overlapping() -> None:
    """Test finding non-overlapping motifs."""
    result = find_motif_positions("AAAAAAA", "AAA", allow_overlap=False)
    assert result == [0, 3, 6]


def test_find_motif_positions_not_found() -> None:
    """Test when motif is not found."""
    result = find_motif_positions("ATGCATGC", "TTT")
    assert result == []


def test_find_motif_positions_single_match() -> None:
    """Test single motif match."""
    result = find_motif_positions("ATGCATGC", "GCA")
    assert result == [2]


def test_find_motif_positions_empty_motif() -> None:
    """Test ValueError for empty motif."""
    with pytest.raises(ValueError, match="Motif cannot be empty"):
        find_motif_positions("ATGC", "")


def test_find_motif_positions_motif_longer_than_seq() -> None:
    """Test ValueError for motif longer than sequence."""
    with pytest.raises(ValueError, match="Motif length .* cannot be greater than sequence length"):
        find_motif_positions("ATG", "ATGCATGC")


def test_find_motif_positions_seq_type_error() -> None:
    """Test TypeError for non-string seq."""
    with pytest.raises(TypeError, match="seq must be a string"):
        find_motif_positions(123, "ATG")


def test_find_motif_positions_motif_type_error() -> None:
    """Test TypeError for non-string motif."""
    with pytest.raises(TypeError, match="motif must be a string"):
        find_motif_positions("ATGC", 123)
