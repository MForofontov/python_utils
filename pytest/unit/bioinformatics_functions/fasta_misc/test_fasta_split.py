import pytest
from bioinformatics_functions.fasta_misc.fasta_split import fasta_split


def test_fasta_split_basic() -> None:
    """
    Test case 1: Basic FASTA splitting.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_split(fasta_str))
    assert len(result) == 2
    assert ">seq1" in result[0]
    assert "ATGC" in result[0]


def test_fasta_split_single_sequence() -> None:
    """
    Test case 2: Single sequence splitting.
    """
    fasta_str = ">seq1\nATGCATGC"
    result = list(fasta_split(fasta_str))
    assert len(result) == 1
    assert result[0] == ">seq1\nATGCATGC"


def test_fasta_split_empty() -> None:
    """
    Test case 3: Empty FASTA string.
    """
    result = list(fasta_split(""))
    assert result == []


def test_fasta_split_multiple_sequences() -> None:
    """
    Test case 4: Multiple sequences splitting.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT\n>seq3\nCCCC"
    result = list(fasta_split(fasta_str))
    assert len(result) == 3


def test_fasta_split_multiline_sequence() -> None:
    """
    Test case 5: Multi-line sequences.
    """
    fasta_str = ">seq1\nATGC\nGCTA"
    result = list(fasta_split(fasta_str))
    assert len(result) == 1


def test_fasta_split_preserves_format() -> None:
    """
    Test case 6: Splitting preserves FASTA format.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_split(fasta_str))
    assert all(r.startswith(">") for r in result)
