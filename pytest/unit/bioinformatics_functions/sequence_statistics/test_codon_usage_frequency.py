import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.sequence_statistics.codon_usage_frequency import (
    codon_usage_frequency,
)


def test_codon_usage_frequency_basic() -> None:
    """
    Test case 1: Basic codon usage frequency calculation.
    """
    seq = "ATGATGAAA"
    result = codon_usage_frequency(seq)
    assert isinstance(result, dict)
    assert "ATG" in result
    # ATG appears 2 out of 3 codons = 0.6667
    assert abs(result["ATG"] - 0.6667) < 0.001
    assert abs(result["AAA"] - 0.3333) < 0.001


def test_codon_usage_frequency_single_codon() -> None:
    """
    Test case 2: Single codon returns frequency of 1.0.
    """
    seq = "ATG"
    result = codon_usage_frequency(seq)
    assert result == {"ATG": 1.0}


def test_codon_usage_frequency_multiple_codons() -> None:
    """
    Test case 3: Multiple different codons.
    """
    seq = "ATGAAAGGG"
    result = codon_usage_frequency(seq)
    assert len(result) == 3
    # Each codon appears once out of 3 = 0.3333
    assert abs(result["ATG"] - 0.3333) < 0.001
    assert abs(result["AAA"] - 0.3333) < 0.001
    assert abs(result["GGG"] - 0.3333) < 0.001


def test_codon_usage_frequency_repeated_codons() -> None:
    """
    Test case 4: Repeated codons have frequency of 1.0.
    """
    seq = "ATGATGATG"
    result = codon_usage_frequency(seq)
    # All 3 codons are ATG = 100% = 1.0
    assert result["ATG"] == 1.0


def test_codon_usage_frequency_lowercase() -> None:
    """
    Test case 5: Lowercase input sequence.
    """
    seq = "atgaaaggg"
    result = codon_usage_frequency(seq)
    assert abs(result["ATG"] - 0.3333) < 0.001
    assert abs(result["AAA"] - 0.3333) < 0.001


def test_codon_usage_frequency_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        codon_usage_frequency(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        codon_usage_frequency(None)


def test_codon_usage_frequency_invalid_length_error() -> None:
    """
    Test case 7: ValueError for length not multiple of 3.
    """
    with pytest.raises(ValueError, match="Sequence length must be a multiple of 3"):
        codon_usage_frequency("ATGC")
    with pytest.raises(ValueError, match="Sequence length must be a multiple of 3"):
        codon_usage_frequency("ATGCC")


def test_codon_usage_frequency_invalid_base_error() -> None:
    """
    Test case 8: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        codon_usage_frequency("ATGXXX")
