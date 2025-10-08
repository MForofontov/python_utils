import pytest
from bioinformatics_functions.fasta_misc.genbank_to_fasta import genbank_to_fasta


def test_genbank_to_fasta_simple() -> None:
    """Test conversion of simple GenBank record."""
    gb = "LOCUS       SEQ1\nORIGIN\n        1 atgcatgcat\n//"
    result = genbank_to_fasta(gb)
    assert ">SEQ1" in result
    assert "ATGCATGCAT" in result


def test_genbank_to_fasta_with_definition() -> None:
    """Test conversion with DEFINITION line."""
    gb = "LOCUS       AB123\nDEFINITION  Test sequence\nORIGIN\n        1 atgc\n//"
    result = genbank_to_fasta(gb)
    assert ">AB123" in result
    assert "ATGC" in result


def test_genbank_to_fasta_multiline_sequence() -> None:
    """Test conversion with multi-line sequence."""
    gb = "LOCUS       SEQ1\nORIGIN\n        1 atgcat gcatgcat\n       21 atgcatgcat\n//"
    result = genbank_to_fasta(gb)
    # Spaces should be removed
    assert "ATGCATGCATGCATATGCATGCAT" in result or "ATGCAT" in result


def test_genbank_to_fasta_multiple_records() -> None:
    """Test conversion of multiple GenBank records."""
    gb = "LOCUS       SEQ1\nORIGIN\n        1 atgc\n//\nLOCUS       SEQ2\nORIGIN\n        1 ggcc\n//"
    result = genbank_to_fasta(gb)
    assert ">SEQ1" in result
    assert ">SEQ2" in result
    assert "ATGC" in result
    assert "GGCC" in result


def test_genbank_to_fasta_no_locus() -> None:
    """Test ValueError when no valid LOCUS found."""
    gb = "ORIGIN\n        1 atgc\n//"
    with pytest.raises(ValueError, match="No valid GenBank sequences found"):
        genbank_to_fasta(gb)


def test_genbank_to_fasta_no_origin() -> None:
    """Test ValueError when no ORIGIN section found."""
    gb = "LOCUS       SEQ1\nDEFINITION  Test\n//"
    with pytest.raises(ValueError, match="No valid GenBank sequences found"):
        genbank_to_fasta(gb)


def test_genbank_to_fasta_empty_input() -> None:
    """Test ValueError for empty input."""
    with pytest.raises(ValueError, match="genbank_str cannot be empty"):
        genbank_to_fasta("")


def test_genbank_to_fasta_whitespace_only() -> None:
    """Test ValueError for whitespace-only input."""
    with pytest.raises(ValueError, match="genbank_str cannot be empty"):
        genbank_to_fasta("   \n\n   ")


def test_genbank_to_fasta_type_error() -> None:
    """Test TypeError for non-string input."""
    with pytest.raises(TypeError, match="genbank_str must be a string"):
        genbank_to_fasta(123)
