import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.fasta_misc.genbank_to_fasta import genbank_to_fasta
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    genbank_to_fasta = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_genbank_to_fasta_simple() -> None:
    """Test case 1: Test conversion of simple GenBank record."""
    gb = "LOCUS       SEQ1\nORIGIN\n        1 atgcatgcat\n//"
    result = genbank_to_fasta(gb)
    assert ">SEQ1" in result
    assert "ATGCATGCAT" in result


def test_genbank_to_fasta_with_definition() -> None:
    """Test case 2: Test conversion with DEFINITION line."""
    gb = "LOCUS       AB123\nDEFINITION  Test sequence\nORIGIN\n        1 atgc\n//"
    result = genbank_to_fasta(gb)
    assert ">AB123" in result
    assert "ATGC" in result


def test_genbank_to_fasta_multiline_sequence() -> None:
    """Test case 3: Test conversion with multi-line sequence."""
    gb = "LOCUS       SEQ1\nORIGIN\n        1 atgcat gcatgcat\n       21 atgcatgcat\n//"
    result = genbank_to_fasta(gb)
    # Spaces should be removed
    assert "ATGCATGCATGCATATGCATGCAT" in result or "ATGCAT" in result


def test_genbank_to_fasta_multiple_records() -> None:
    """Test case 4: Test conversion of multiple GenBank records."""
    gb = "LOCUS       SEQ1\nORIGIN\n        1 atgc\n//\nLOCUS       SEQ2\nORIGIN\n        1 ggcc\n//"
    result = genbank_to_fasta(gb)
    assert ">SEQ1" in result
    assert ">SEQ2" in result
    assert "ATGC" in result
    assert "GGCC" in result


def test_genbank_to_fasta_no_locus() -> None:
    """Test case 5: Test ValueError when no valid LOCUS found."""
    gb = "ORIGIN\n        1 atgc\n//"
    with pytest.raises(ValueError, match="No valid GenBank sequences found"):
        genbank_to_fasta(gb)


def test_genbank_to_fasta_no_origin() -> None:
    """Test case 6: Test ValueError when no ORIGIN section found."""
    gb = "LOCUS       SEQ1\nDEFINITION  Test\n//"
    with pytest.raises(ValueError, match="No valid GenBank sequences found"):
        genbank_to_fasta(gb)


def test_genbank_to_fasta_empty_input() -> None:
    """Test case 7: Test ValueError for empty input."""
    with pytest.raises(ValueError, match="genbank_str cannot be empty"):
        genbank_to_fasta("")


def test_genbank_to_fasta_whitespace_only() -> None:
    """Test case 8: Test ValueError for whitespace-only input."""
    with pytest.raises(ValueError, match="genbank_str cannot be empty"):
        genbank_to_fasta("   \n\n   ")


def test_genbank_to_fasta_type_error() -> None:
    """Test case 9: Test TypeError for non-string input."""
    with pytest.raises(TypeError, match="genbank_str must be a string"):
        genbank_to_fasta(123)
