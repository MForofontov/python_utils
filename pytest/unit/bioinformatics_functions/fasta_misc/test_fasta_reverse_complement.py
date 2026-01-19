import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.fasta_misc.fasta_reverse_complement import (
    fasta_reverse_complement,
)


def test_fasta_reverse_complement_basic() -> None:
    """
    Test case 1: Basic reverse complement of FASTA.
    """
    fasta_str = ">seq1\nATGC"
    result = list(fasta_reverse_complement(fasta_str))
    assert len(result) == 1
    assert result[0][0] == "seq1"
    assert result[0][1] == "GCAT"


def test_fasta_reverse_complement_multiple_sequences() -> None:
    """
    Test case 2: Multiple sequences reverse complement.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_reverse_complement(fasta_str))
    assert len(result) == 2
    assert result[0][1] == "GCAT"
    assert result[1][1] == "AACC"


def test_fasta_reverse_complement_lowercase() -> None:
    """
    Test case 3: Lowercase sequences.
    """
    fasta_str = ">seq1\natgc"
    result = list(fasta_reverse_complement(fasta_str))
    assert result[0][1] == "gcat"


def test_fasta_reverse_complement_empty() -> None:
    """
    Test case 4: Empty FASTA string.
    """
    result = list(fasta_reverse_complement(""))
    assert result == []


def test_fasta_reverse_complement_long_sequence() -> None:
    """
    Test case 5: Longer sequence reverse complement.
    """
    fasta_str = ">seq1\nATGCATGC"
    result = list(fasta_reverse_complement(fasta_str))
    assert result[0][1] == "GCATGCAT"


def test_fasta_reverse_complement_preserves_header() -> None:
    """
    Test case 6: Headers are preserved.
    """
    fasta_str = ">gene1\nATGC\n>protein1\nGGTT"
    result = list(fasta_reverse_complement(fasta_str))
    assert result[0][0] == "gene1"
    assert result[1][0] == "protein1"
