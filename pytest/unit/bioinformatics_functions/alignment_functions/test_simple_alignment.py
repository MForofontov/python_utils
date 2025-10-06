import pytest
from bioinformatics_functions.alignment_functions.simple_alignment import simple_alignment


def test_simple_alignment_basic() -> None:
    """
    Test case 1: Basic alignment of two identical sequences.
    """
    seq1 = "ACTG"
    seq2 = "ACTG"
    aligned1, aligned2 = simple_alignment(seq1, seq2)
    assert isinstance(aligned1, str)
    assert isinstance(aligned2, str)
    assert aligned1 == seq1
    assert aligned2 == seq2


def test_simple_alignment_mismatch() -> None:
    """
    Test case 2: Alignment of sequences with mismatches.
    """
    seq1 = "ACTG"
    seq2 = "ACGG"
    aligned1, aligned2 = simple_alignment(seq1, seq2)
    assert aligned1 == seq1
    assert aligned2 == seq2


def test_simple_alignment_gap() -> None:
    """
    Test case 3: Alignment with shorter sequence (should pad with '-').
    """
    seq1 = "ACTG"
    seq2 = "ACG"
    aligned1, aligned2 = simple_alignment(seq1, seq2)
    assert aligned1 == seq1
    assert aligned2 == "ACG-"


def test_simple_alignment_empty() -> None:
    """
    Test case 4: Alignment with empty sequence.
    """
    seq1 = ""
    seq2 = "ACTG"
    aligned1, aligned2 = simple_alignment(seq1, seq2)
    assert aligned1 == "----"
    assert aligned2 == "ACTG"


def test_simple_alignment_type_error() -> None:
    """
    Test case 5: TypeError for non-string input.
    """
    with pytest.raises(TypeError):
        simple_alignment(123, "ACTG")


def test_simple_alignment_value_error() -> None:
    """
    Test case 6: ValueError for invalid sequence characters.
    """
    with pytest.raises(ValueError):
        simple_alignment("ACTG", "ACXG")
