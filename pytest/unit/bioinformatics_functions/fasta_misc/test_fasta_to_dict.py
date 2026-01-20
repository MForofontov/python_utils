import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.fasta_misc.fasta_to_dict import fasta_to_dict
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    fasta_to_dict = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_fasta_to_dict_basic() -> None:
    """
    Test case 1: Basic FASTA to dictionary conversion.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = fasta_to_dict(fasta_str)
    assert isinstance(result, dict)
    assert result == {"seq1": "ATGC", "seq2": "GGTT"}


def test_fasta_to_dict_single_sequence() -> None:
    """
    Test case 2: Single sequence conversion.
    """
    fasta_str = ">seq1\nATGCATGC"
    result = fasta_to_dict(fasta_str)
    assert result == {"seq1": "ATGCATGC"}


def test_fasta_to_dict_empty() -> None:
    """
    Test case 3: Empty FASTA string returns empty dict.
    """
    result = fasta_to_dict("")
    assert result == {}


def test_fasta_to_dict_multiline_sequence() -> None:
    """
    Test case 4: Multi-line sequences.
    """
    fasta_str = ">seq1\nATGC\nGCTA"
    result = fasta_to_dict(fasta_str)
    assert "seq1" in result


def test_fasta_to_dict_multiple_sequences() -> None:
    """
    Test case 5: Multiple sequences conversion.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT\n>seq3\nCCCC"
    result = fasta_to_dict(fasta_str)
    assert len(result) == 3


def test_fasta_to_dict_duplicate_header_error() -> None:
    """
    Test case 6: ValueError for duplicate headers.
    """
    fasta_str = ">seq1\nATGC\n>seq1\nGGTT"
    with pytest.raises(ValueError, match="Duplicate header found"):
        fasta_to_dict(fasta_str)
