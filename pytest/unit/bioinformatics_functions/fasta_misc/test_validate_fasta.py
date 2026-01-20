import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.fasta_misc.validate_fasta import validate_fasta
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    validate_fasta = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_validate_fasta_valid_format() -> None:
    """
    Test case 1: Valid FASTA format returns True.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = validate_fasta(fasta_str)
    assert result is True


def test_validate_fasta_single_sequence() -> None:
    """
    Test case 2: Single sequence valid FASTA.
    """
    fasta_str = ">seq1\nATGCATGC"
    result = validate_fasta(fasta_str)
    assert result is True


def test_validate_fasta_multiline_sequence() -> None:
    """
    Test case 3: Multi-line sequence valid FASTA.
    """
    fasta_str = ">seq1\nATGC\nGCTA\nTAGC"
    result = validate_fasta(fasta_str)
    assert result is True


def test_validate_fasta_no_header() -> None:
    """
    Test case 4: No header returns False.
    """
    fasta_str = "ATGC"
    result = validate_fasta(fasta_str)
    assert result is False


def test_validate_fasta_empty_string() -> None:
    """
    Test case 5: Empty string returns False.
    """
    result = validate_fasta("")
    assert result is False


def test_validate_fasta_empty_header() -> None:
    """
    Test case 6: Empty header returns False.
    """
    fasta_str = ">\nATGC"
    result = validate_fasta(fasta_str)
    assert result is False


def test_validate_fasta_invalid_sequence_characters() -> None:
    """
    Test case 7: Invalid characters in sequence returns False.
    """
    fasta_str = ">seq1\nATGC123"  # Numbers not allowed
    result = validate_fasta(fasta_str)
    assert result is False


def test_validate_fasta_sequence_before_header() -> None:
    """
    Test case 8: Sequence lines before header returns False.
    """
    fasta_str = "ATGC\n>seq1\nGGCC"  # Sequence before header
    result = validate_fasta(fasta_str)
    assert result is False


def test_validate_fasta_invalid_type_error() -> None:
    """
    Test case 9: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="fasta_str must be str"):
        validate_fasta(12345)
    with pytest.raises(TypeError, match="fasta_str must be str"):
        validate_fasta(None)
