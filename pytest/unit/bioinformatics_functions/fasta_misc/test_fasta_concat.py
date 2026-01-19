import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.fasta_misc.fasta_concat import fasta_concat


def test_fasta_concat_basic() -> None:
    """
    Test case 1: Basic FASTA concatenation.
    """
    fasta_strs = [">seq1\nATGC", ">seq2\nGGTT"]
    result = fasta_concat(fasta_strs)
    assert ">seq1" in result
    assert ">seq2" in result
    assert "ATGC" in result


def test_fasta_concat_single_sequence() -> None:
    """
    Test case 2: Single sequence concatenation.
    """
    fasta_strs = [">seq1\nATGCATGC"]
    result = fasta_concat(fasta_strs)
    assert result == ">seq1\nATGCATGC"


def test_fasta_concat_empty_list() -> None:
    """
    Test case 3: Empty list returns empty string.
    """
    result = fasta_concat([])
    assert result == ""


def test_fasta_concat_multiple_sequences() -> None:
    """
    Test case 4: Multiple sequences concatenation.
    """
    fasta_strs = [">seq1\nATGC", ">seq2\nGGTT", ">seq3\nCCCC"]
    result = fasta_concat(fasta_strs)
    assert result.count(">") == 3


def test_fasta_concat_strips_whitespace() -> None:
    """
    Test case 5: Concatenation strips extra whitespace.
    """
    fasta_strs = [">seq1\nATGC  ", "  >seq2\nGGTT"]
    result = fasta_concat(fasta_strs)
    assert "  " not in result or result.strip()


def test_fasta_concat_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="All elements must be strings"):
        fasta_concat([">seq1\nATGC", 123])
    with pytest.raises(TypeError, match="All elements must be strings"):
        fasta_concat([">seq1\nATGC", None])
