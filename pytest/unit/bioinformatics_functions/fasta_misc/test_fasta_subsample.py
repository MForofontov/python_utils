import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.fasta_misc.fasta_subsample import fasta_subsample


def test_fasta_subsample_basic() -> None:
    """
    Test case 1: Basic subsampling.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT\n>seq3\nCCCC"
    result = list(fasta_subsample(fasta_str, 2))
    assert len(result) == 2
    assert all(isinstance(r, tuple) for r in result)


def test_fasta_subsample_all_sequences() -> None:
    """
    Test case 2: Sample all sequences.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_subsample(fasta_str, 2))
    assert len(result) == 2


def test_fasta_subsample_zero() -> None:
    """
    Test case 3: Sample zero sequences.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_subsample(fasta_str, 0))
    assert result == []


def test_fasta_subsample_single() -> None:
    """
    Test case 4: Sample single sequence.
    """
    fasta_str = ">seq1\nATGC\n>seq2\nGGTT"
    result = list(fasta_subsample(fasta_str, 1))
    assert len(result) == 1


def test_fasta_subsample_empty() -> None:
    """
    Test case 5: Empty FASTA with n=0.
    """
    result = list(fasta_subsample("", 0))
    assert result == []


def test_fasta_subsample_negative_error() -> None:
    """
    Test case 6: ValueError for negative n.
    """
    fasta_str = ">seq1\nATGC"
    with pytest.raises(ValueError, match="n must be between 0 and number of sequences"):
        list(fasta_subsample(fasta_str, -1))


def test_fasta_subsample_exceeds_count_error() -> None:
    """
    Test case 7: ValueError for n exceeding sequence count.
    """
    fasta_str = ">seq1\nATGC"
    with pytest.raises(ValueError, match="n must be between 0 and number of sequences"):
        list(fasta_subsample(fasta_str, 5))
