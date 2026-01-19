import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.sequence_statistics.sequence_conservation import (
    sequence_conservation,
)


def test_sequence_conservation_basic() -> None:
    """
    Test case 1: Basic conservation score calculation.
    """
    sequences = ["ATGC", "ATGT", "ATGA"]
    result = sequence_conservation(sequences)
    assert isinstance(result, list)
    assert len(result) == 4
    assert all(isinstance(x, float) for x in result)


def test_sequence_conservation_fully_conserved() -> None:
    """
    Test case 2: Fully conserved positions.
    """
    sequences = ["ATGC", "ATGC", "ATGC"]
    result = sequence_conservation(sequences)
    assert all(score == 1.0 for score in result)


def test_sequence_conservation_no_conservation() -> None:
    """
    Test case 3: No conservation at position.
    """
    sequences = ["AAAA", "TTTT", "GGGG", "CCCC"]
    result = sequence_conservation(sequences)
    assert all(score == 0.25 for score in result)


def test_sequence_conservation_partial() -> None:
    """
    Test case 4: Partial conservation.
    """
    sequences = ["ATGC", "ATGT", "ATGA"]
    result = sequence_conservation(sequences)
    assert result[0] == 1.0  # All A
    assert result[1] == 1.0  # All T
    assert result[2] == 1.0  # All G
    assert abs(result[3] - 0.333333) < 0.01  # C, T, A


def test_sequence_conservation_two_sequences() -> None:
    """
    Test case 5: Two sequences conservation.
    """
    sequences = ["ATGC", "ATGC"]
    result = sequence_conservation(sequences)
    assert all(score == 1.0 for score in result)


def test_sequence_conservation_empty_error() -> None:
    """
    Test case 6: ValueError for empty sequences.
    """
    with pytest.raises(ValueError, match="sequences cannot be empty"):
        sequence_conservation([])


def test_sequence_conservation_different_length_error() -> None:
    """
    Test case 7: ValueError for different length sequences.
    """
    with pytest.raises(ValueError, match="All sequences must be the same length"):
        sequence_conservation(["ATGC", "ATG"])
