import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.sequence_operations.sequence_to_kmers import (
    sequence_to_kmers,
)


def test_sequence_to_kmers_basic() -> None:
    """
    Test case 1: Basic k-mer splitting.
    """
    seq = "ATGCGA"
    result = sequence_to_kmers(seq, 3)
    assert result == ["ATG", "TGC", "GCG", "CGA"]


def test_sequence_to_kmers_k_equals_length() -> None:
    """
    Test case 2: k equals sequence length.
    """
    seq = "ATGC"
    result = sequence_to_kmers(seq, 4)
    assert result == ["ATGC"]


def test_sequence_to_kmers_k_one() -> None:
    """
    Test case 3: k=1 returns individual characters.
    """
    seq = "ATGC"
    result = sequence_to_kmers(seq, 1)
    assert result == ["A", "T", "G", "C"]


def test_sequence_to_kmers_k_two() -> None:
    """
    Test case 4: k=2 returns dinucleotides.
    """
    seq = "ATGC"
    result = sequence_to_kmers(seq, 2)
    assert result == ["AT", "TG", "GC"]


def test_sequence_to_kmers_longer_sequence() -> None:
    """
    Test case 5: Longer sequence with k=3.
    """
    seq = "ATGCATGC"
    result = sequence_to_kmers(seq, 3)
    assert len(result) == 6


def test_sequence_to_kmers_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        sequence_to_kmers(12345, 3)
    with pytest.raises(TypeError, match="k must be int"):
        sequence_to_kmers("ATGC", 3.5)


def test_sequence_to_kmers_invalid_value_error() -> None:
    """
    Test case 7: ValueError for invalid k values.
    """
    with pytest.raises(ValueError, match="k must be positive"):
        sequence_to_kmers("ATGC", 0)
    with pytest.raises(ValueError, match="k must be positive"):
        sequence_to_kmers("ATGC", -1)
    with pytest.raises(ValueError, match="k cannot be longer than sequence"):
        sequence_to_kmers("ATGC", 5)
