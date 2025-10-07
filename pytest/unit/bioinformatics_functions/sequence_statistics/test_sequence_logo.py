import pytest
import numpy as np
from bioinformatics_functions.sequence_statistics.sequence_logo import sequence_logo_matrix


def test_sequence_logo_matrix_basic() -> None:
    """
    Test case 1: Basic position frequency matrix.
    """
    sequences = ["ATGC", "ATGT", "ATGA"]
    result = sequence_logo_matrix(sequences)
    assert isinstance(result, np.ndarray)
    assert result.shape[0] == 4  # 4 positions


def test_sequence_logo_matrix_all_same() -> None:
    """
    Test case 2: All sequences identical.
    """
    sequences = ["ATGC", "ATGC", "ATGC"]
    result = sequence_logo_matrix(sequences)
    assert result[0, :].sum() == 3  # 3 sequences


def test_sequence_logo_matrix_two_bases() -> None:
    """
    Test case 3: Only two different bases.
    """
    sequences = ["AAA", "TTT"]
    result = sequence_logo_matrix(sequences)
    assert result.shape[0] == 3  # 3 positions


def test_sequence_logo_matrix_single_sequence() -> None:
    """
    Test case 4: Single sequence.
    """
    sequences = ["ATGC"]
    result = sequence_logo_matrix(sequences)
    assert result.shape[0] == 4
    assert result.sum() == 4


def test_sequence_logo_matrix_longer_sequences() -> None:
    """
    Test case 5: Longer sequences.
    """
    sequences = ["ATGCATGC", "ATGCATGC"]
    result = sequence_logo_matrix(sequences)
    assert result.shape[0] == 8


def test_sequence_logo_matrix_empty_error() -> None:
    """
    Test case 6: ValueError for empty sequences.
    """
    with pytest.raises(ValueError, match="sequences cannot be empty"):
        sequence_logo_matrix([])


def test_sequence_logo_matrix_different_length_error() -> None:
    """
    Test case 7: ValueError for different length sequences.
    """
    with pytest.raises(ValueError, match="All sequences must be the same length"):
        sequence_logo_matrix(["ATGC", "ATG"])
