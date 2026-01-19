import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.fasta_misc.fasta_rename_headers import (
    fasta_rename_headers,
)


def test_fasta_rename_headers_basic() -> None:
    """
    Test case 1: Basic header renaming.
    """
    fasta_str = ">seq1\nATGC"
    result = list(fasta_rename_headers(fasta_str, lambda h: h + "_renamed"))
    assert len(result) == 1
    assert result[0][0] == "seq1_renamed"
    assert result[0][1] == "ATGC"


def test_fasta_rename_headers_multiple_sequences() -> None:
    """
    Test case 2: Multiple sequences renaming.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_rename_headers(fasta_str, lambda h: f"new_{h}"))
    assert len(result) == 2
    assert result[0][0] == "new_seq1"
    assert result[1][0] == "new_seq2"


def test_fasta_rename_headers_uppercase() -> None:
    """
    Test case 3: Rename to uppercase.
    """
    fasta_str = ">seq1\nATGC"
    result = list(fasta_rename_headers(fasta_str, lambda h: h.upper()))
    assert result[0][0] == "SEQ1"


def test_fasta_rename_headers_empty() -> None:
    """
    Test case 4: Empty FASTA string.
    """
    result = list(fasta_rename_headers("", lambda h: h + "_renamed"))
    assert result == []


def test_fasta_rename_headers_complex_function() -> None:
    """
    Test case 5: Complex renaming function.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(
        fasta_rename_headers(fasta_str, lambda h: h.replace("seq", "sequence"))
    )
    assert result[0][0] == "sequence1"
    assert result[1][0] == "sequence2"


def test_fasta_rename_headers_preserves_sequence() -> None:
    """
    Test case 6: Sequences are preserved unchanged.
    """
    fasta_str = ">seq1\nATGCATGC"
    result = list(fasta_rename_headers(fasta_str, lambda h: "newname"))
    assert result[0][1] == "ATGCATGC"
