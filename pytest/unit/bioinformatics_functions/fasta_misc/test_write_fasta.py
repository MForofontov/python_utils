import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.fasta_misc.write_fasta import write_fasta


def test_write_fasta_basic() -> None:
    """
    Test case 1: Basic FASTA writing.
    """
    records = [("seq1", "ATGC"), ("seq2", "GGTT")]
    result = write_fasta(records)
    assert isinstance(result, str)
    assert ">seq1" in result
    assert "ATGC" in result


def test_write_fasta_single_record() -> None:
    """
    Test case 2: Single record writing.
    """
    records = [("seq1", "ATGCATGC")]
    result = write_fasta(records)
    assert result == ">seq1\nATGCATGC\n"


def test_write_fasta_empty_list() -> None:
    """
    Test case 3: Empty list returns just newline.
    """
    result = write_fasta([])
    assert result == "\n"


def test_write_fasta_multiple_records() -> None:
    """
    Test case 4: Multiple records writing.
    """
    records = [("seq1", "ATGC"), ("seq2", "GGTT"), ("seq3", "CCCC")]
    result = write_fasta(records)
    lines = result.split("\n")
    assert len([line for line in lines if line.startswith(">")]) == 3


def test_write_fasta_long_sequence() -> None:
    """
    Test case 5: Long sequence writing.
    """
    records = [("seq1", "A" * 100)]
    result = write_fasta(records)
    assert "A" * 100 in result


def test_write_fasta_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid record format.
    """
    with pytest.raises(TypeError, match="Each record must be a \\(str, str\\) tuple"):
        write_fasta([("seq1",)])
    with pytest.raises(TypeError, match="Each record must be a \\(str, str\\) tuple"):
        write_fasta([(123, "ATGC")])
    with pytest.raises(TypeError, match="Each record must be a \\(str, str\\) tuple"):
        write_fasta(["seq1", "ATGC"])
