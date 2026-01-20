import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.fasta_misc.fasta_filter import fasta_filter
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    fasta_filter = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_fasta_filter_basic() -> None:
    """
    Test case 1: Basic FASTA filtering by length.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTTAA"
    result = list(fasta_filter(fasta_str, lambda h, s: len(s) > 4))
    assert len(result) == 1
    assert result[0][0] == "seq2"


def test_fasta_filter_all_pass() -> None:
    """
    Test case 2: All sequences pass filter.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_filter(fasta_str, lambda h, s: len(s) >= 4))
    assert len(result) == 2


def test_fasta_filter_none_pass() -> None:
    """
    Test case 3: No sequences pass filter.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_filter(fasta_str, lambda h, s: len(s) > 10))
    assert result == []


def test_fasta_filter_by_header() -> None:
    """
    Test case 4: Filter by header pattern.
    """
    fasta_str = ">gene1\nATGC\n>protein1\nGGTT"
    result = list(fasta_filter(fasta_str, lambda h, s: h.startswith("gene")))
    assert len(result) == 1
    assert result[0][0] == "gene1"


def test_fasta_filter_empty() -> None:
    """
    Test case 5: Empty FASTA string.
    """
    result = list(fasta_filter("", lambda h, s: True))
    assert result == []


def test_fasta_filter_complex_predicate() -> None:
    """
    Test case 6: Complex predicate combining header and sequence.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTTAA"
    result = list(fasta_filter(fasta_str, lambda h, s: "seq2" in h and len(s) > 5))
    assert len(result) == 1
