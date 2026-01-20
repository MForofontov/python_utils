import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.fasta_misc.fastq_to_fasta import fastq_to_fasta
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    fastq_to_fasta = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_fastq_to_fasta_single_sequence() -> None:
    """Test case 1: Test conversion of single FASTQ sequence."""
    fastq = "@SEQ1\nATGC\n+\nIIII\n"
    result = fastq_to_fasta(fastq)
    assert result == ">SEQ1\nATGC\n"


def test_fastq_to_fasta_multiple_sequences() -> None:
    """Test case 2: Test conversion of multiple FASTQ sequences."""
    fastq = "@SEQ1\nATGC\n+\nIIII\n@SEQ2\nGGCC\n+\nJJJJ\n"
    result = fastq_to_fasta(fastq)
    assert ">SEQ1\nATGC\n>SEQ2\nGGCC" in result


def test_fastq_to_fasta_quality_filter() -> None:
    """Test case 3: Test quality filtering during conversion."""
    # First seq has low quality (! = Phred score 0), second has high quality (I = Phred score 40)
    fastq = "@SEQ1\nATGC\n+\n!!!!\n@SEQ2\nGGCC\n+\nIIII\n"
    result = fastq_to_fasta(fastq, min_quality=20)
    assert ">SEQ2" in result
    assert ">SEQ1" not in result


def test_fastq_to_fasta_no_quality_filter() -> None:
    """Test case 4: Test conversion without quality filtering."""
    fastq = "@SEQ1\nATGC\n+\n!!!!\n"
    result = fastq_to_fasta(fastq)
    assert ">SEQ1\nATGC" in result


def test_fastq_to_fasta_all_filtered() -> None:
    """Test case 5: Test when all sequences are filtered out."""
    fastq = "@SEQ1\nATGC\n+\n!!!!\n"
    result = fastq_to_fasta(fastq, min_quality=30)
    assert result == ""


def test_fastq_to_fasta_empty_input() -> None:
    """Test case 6: Test ValueError for empty input."""
    with pytest.raises(ValueError, match="fastq_str cannot be empty"):
        fastq_to_fasta("")


def test_fastq_to_fasta_malformed_lines() -> None:
    """Test case 7: Test ValueError for wrong number of lines."""
    with pytest.raises(ValueError, match="FASTQ format requires 4 lines per sequence"):
        fastq_to_fasta("@SEQ1\nATGC\n+\n")  # Missing quality line


def test_fastq_to_fasta_malformed_header() -> None:
    """Test case 8: Test ValueError for invalid header."""
    with pytest.raises(ValueError, match="FASTQ header must start with '@'"):
        fastq_to_fasta("SEQ1\nATGC\n+\nIIII\n")


def test_fastq_to_fasta_length_mismatch() -> None:
    """Test case 9: Test ValueError for sequence/quality length mismatch."""
    with pytest.raises(ValueError, match="Sequence and quality lengths must match"):
        fastq_to_fasta("@SEQ1\nATGC\n+\nII\n")


def test_fastq_to_fasta_type_error() -> None:
    """Test case 10: Test TypeError for non-string input."""
    with pytest.raises(TypeError, match="fastq_str must be a string"):
        fastq_to_fasta(123)


def test_fastq_to_fasta_quality_type_error() -> None:
    """Test case 11: Test TypeError for non-integer min_quality."""
    with pytest.raises(TypeError, match="min_quality must be an integer or None"):
        fastq_to_fasta("@SEQ1\nATGC\n+\nIIII\n", min_quality="20")


def test_fastq_to_fasta_malformed_plus_line() -> None:
    """Test case 12: Test ValueError for invalid plus line separator."""
    with pytest.raises(ValueError, match="FASTQ separator must start with '\\+'"):
        fastq_to_fasta("@SEQ1\nATGC\n-\nIIII\n")


def test_fastq_to_fasta_sequence_quality_length_mismatch() -> None:
    """Test case 13: Test ValueError when sequence and quality have different lengths."""
    # This creates a proper 4-line format but with mismatched lengths
    with pytest.raises(ValueError, match="Sequence and quality lengths must match"):
        fastq_to_fasta("@SEQ1\nATGCTT\n+\nIII\n")


def test_fastq_to_fasta_negative_min_quality() -> None:
    """Test case 14: Test ValueError for negative min_quality."""
    with pytest.raises(ValueError, match="min_quality must be non-negative"):
        fastq_to_fasta("@SEQ1\nATGC\n+\nIIII\n", min_quality=-5)
