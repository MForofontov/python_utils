import pytest
from bioinformatics_functions.motif_functions.generate_consensus_sequence import generate_consensus_sequence


def test_generate_consensus_sequence_identical() -> None:
    """Test consensus of identical sequences."""
    result = generate_consensus_sequence(["ATGC", "ATGC", "ATGC"])
    assert result == "ATGC"


def test_generate_consensus_sequence_majority() -> None:
    """Test consensus with majority rule."""
    # Position 2: G appears 2/3 times (66% > 50% threshold)
    result = generate_consensus_sequence(["ATGC", "ATCC", "ATAC"])
    # Most common at each position: A, T, G/C (tie?), C
    assert len(result) == 4
    assert result[0] == "A"
    assert result[1] == "T"


def test_generate_consensus_sequence_below_threshold() -> None:
    """Test consensus with no clear majority."""
    # Position 0: A,T,C,G each appear once (25% < 50% threshold) -> N
    result = generate_consensus_sequence(["ATGC", "TTGC", "CTGC", "GTGC"])
    assert result == "NTGC"


def test_generate_consensus_sequence_with_gaps() -> None:
    """Test consensus with gap characters."""
    result = generate_consensus_sequence(["AT-C", "ATGC", "ATCC"], threshold=0.5)
    # Position 2: G,C,- -> G appears 1/3, C appears 1/3, - appears 1/3 -> no majority
    assert len(result) == 4


def test_generate_consensus_sequence_custom_threshold() -> None:
    """Test consensus with custom threshold."""
    # With 0.67 threshold, need 2/3 sequences
    result = generate_consensus_sequence(["ATGC", "ATGC", "TTGC"], threshold=0.67)
    assert result[0] == "A"  # A appears 2/3 times
    assert result[2] == "G"  # G appears 3/3 times


def test_generate_consensus_sequence_empty_list() -> None:
    """Test ValueError for empty sequences list."""
    with pytest.raises(ValueError, match="Sequences list cannot be empty"):
        generate_consensus_sequence([])


def test_generate_consensus_sequence_different_lengths() -> None:
    """Test ValueError for sequences with different lengths."""
    with pytest.raises(ValueError, match="All sequences must have same length"):
        generate_consensus_sequence(["ATGC", "ATG"])


def test_generate_consensus_sequence_invalid_threshold() -> None:
    """Test ValueError for invalid threshold."""
    with pytest.raises(ValueError, match="threshold must be between 0 and 1"):
        generate_consensus_sequence(["ATGC"], threshold=1.5)


def test_generate_consensus_sequence_type_error() -> None:
    """Test TypeError for non-list input."""
    with pytest.raises(TypeError, match="sequences must be a list"):
        generate_consensus_sequence("ATGC")
