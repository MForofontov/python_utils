import pytest
from bioinformatics_functions.fasta_misc.degenerate_primer_generator import (
    degenerate_primer_generator,
)


def test_degenerate_primer_generator_basic() -> None:
    """
    Test case 1: Basic degenerate primer generation.
    """
    seq = "ATGR"
    result = degenerate_primer_generator(seq)
    assert set(result) == {"ATGA", "ATGG"}


def test_degenerate_primer_generator_no_degeneracy() -> None:
    """
    Test case 2: No degenerate bases.
    """
    seq = "ATGC"
    result = degenerate_primer_generator(seq)
    assert result == ["ATGC"]


def test_degenerate_primer_generator_multiple_degenerate() -> None:
    """
    Test case 3: Multiple degenerate bases.
    """
    seq = "RY"
    result = degenerate_primer_generator(seq)
    assert len(result) == 4
    assert set(result) == {"AC", "AT", "GC", "GT"}


def test_degenerate_primer_generator_n_base() -> None:
    """
    Test case 4: N base (any base).
    """
    seq = "AN"
    result = degenerate_primer_generator(seq)
    assert len(result) == 4
    assert set(result) == {"AA", "AC", "AG", "AT"}


def test_degenerate_primer_generator_lowercase() -> None:
    """
    Test case 5: Lowercase input.
    """
    seq = "atgr"
    result = degenerate_primer_generator(seq)
    assert len(result) == 2


def test_degenerate_primer_generator_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        degenerate_primer_generator(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        degenerate_primer_generator(None)


def test_degenerate_primer_generator_invalid_base_error() -> None:
    """
    Test case 7: ValueError for invalid DNA/IUPAC bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA/IUPAC bases"):
        degenerate_primer_generator("ATGX")
    with pytest.raises(ValueError, match="Sequence contains invalid DNA/IUPAC bases"):
        degenerate_primer_generator("ATGU")
