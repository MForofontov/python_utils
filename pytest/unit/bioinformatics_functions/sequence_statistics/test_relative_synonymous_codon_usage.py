import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.sequence_statistics.relative_synonymous_codon_usage import (
        relative_synonymous_codon_usage,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    relative_synonymous_codon_usage = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_relative_synonymous_codon_usage_single_codon() -> None:
    """Test case 1: Test RSCU with single codon repeated."""
    result = relative_synonymous_codon_usage("ATGATGATG")
    # ATG (Met) has only one codon, so RSCU = 1.0
    assert result["ATG"] == 1.0


def test_relative_synonymous_codon_usage_synonymous() -> None:
    """Test case 2: Test RSCU with synonymous codons."""
    # TTT and TTC both code for Phe (2-fold degenerate)
    # 3 TTT, 1 TTC out of 4 total
    result = relative_synonymous_codon_usage("TTTTTTTTCTTT")
    # TTT: observed = 3/4 = 0.75, expected = 1/2 = 0.5, RSCU = 0.75 / 0.5 = 1.5
    # TTC: observed = 1/4 = 0.25, expected = 1/2 = 0.5, RSCU = 0.25 / 0.5 = 0.5
    assert abs(result["TTT"] - 1.5) < 0.01
    assert abs(result["TTC"] - 0.5) < 0.01


def test_relative_synonymous_codon_usage_equal_usage() -> None:
    """Test case 3: Test RSCU with equal usage of synonymous codons."""
    # TTT and TTC used equally
    result = relative_synonymous_codon_usage("TTTTTTTTCTTC")
    # Each used 2 times, RSCU should be 1.0 for both
    assert abs(result["TTT"] - 1.0) < 0.01
    assert abs(result["TTC"] - 1.0) < 0.01


def test_relative_synonymous_codon_usage_multiple_aa() -> None:
    """Test case 4: Test RSCU with multiple amino acids."""
    # Mix of codons for different amino acids
    seq = "ATGATGATG" + "TTTTTT" + "GCAGCA"  # Met + Phe + Ala
    result = relative_synonymous_codon_usage(seq)
    assert "ATG" in result
    assert "TTT" in result
    assert "GCA" in result


def test_relative_synonymous_codon_usage_lowercase() -> None:
    """Test case 5: Test RSCU with lowercase sequence."""
    result = relative_synonymous_codon_usage("atgatgatg")
    assert result["ATG"] == 1.0


def test_relative_synonymous_codon_usage_not_multiple_of_3() -> None:
    """Test case 6: Test ValueError for sequence not multiple of 3."""
    with pytest.raises(ValueError, match="Sequence length must be multiple of 3"):
        relative_synonymous_codon_usage("ATGATGA")


def test_relative_synonymous_codon_usage_too_short() -> None:
    """Test case 7: Test ValueError for sequence too short."""
    with pytest.raises(ValueError, match="Sequence must be at least 3 bases long"):
        relative_synonymous_codon_usage("AT")


def test_relative_synonymous_codon_usage_invalid_bases() -> None:
    """Test case 8: Test ValueError for invalid DNA bases."""
    with pytest.raises(ValueError, match="Invalid DNA bases found"):
        relative_synonymous_codon_usage("ATXATGATG")


def test_relative_synonymous_codon_usage_type_error() -> None:
    """Test case 9: Test TypeError for non-string input."""
    with pytest.raises(TypeError, match="seq must be a string"):
        relative_synonymous_codon_usage(123)
