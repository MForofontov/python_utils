import pytest
from bioinformatics_functions.fasta_misc.fasta_stats import fasta_stats


def test_fasta_stats_basic() -> None:
    """
    Test case 1: Basic FASTA statistics.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    num, avg_len, avg_gc = fasta_stats(fasta_str)
    assert num == 2
    assert avg_len == 4.0
    assert avg_gc == 0.5


def test_fasta_stats_single_sequence() -> None:
    """
    Test case 2: Single sequence statistics.
    """
    fasta_str = ">seq1\nATGC"
    num, avg_len, avg_gc = fasta_stats(fasta_str)
    assert num == 1
    assert avg_len == 4.0


def test_fasta_stats_empty() -> None:
    """
    Test case 3: Empty FASTA string.
    """
    num, avg_len, avg_gc = fasta_stats("")
    assert num == 0
    assert avg_len == 0.0
    assert avg_gc == 0.0


def test_fasta_stats_high_gc() -> None:
    """
    Test case 4: High GC content sequences.
    """
    fasta_str = ">seq1\nGGCC"
    num, avg_len, avg_gc = fasta_stats(fasta_str)
    assert avg_gc == 1.0


def test_fasta_stats_low_gc() -> None:
    """
    Test case 5: Low GC content sequences.
    """
    fasta_str = ">seq1\nATAT"
    num, avg_len, avg_gc = fasta_stats(fasta_str)
    assert avg_gc == 0.0


def test_fasta_stats_multiple_sequences() -> None:
    """
    Test case 6: Multiple sequences with different lengths.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nATGCATGC"
    num, avg_len, avg_gc = fasta_stats(fasta_str)
    assert num == 2
    assert avg_len == 6.0
