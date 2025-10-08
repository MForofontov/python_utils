import pytest
from bioinformatics_functions.sequence_statistics.effective_number_of_codons import effective_number_of_codons


def test_effective_number_of_codons_extreme_bias() -> None:
    """Test case 1: Test ENC with extreme bias (one codon repeated)."""
    # ATG repeated should give low ENC (close to 20)
    result = effective_number_of_codons("ATGATGATG")
    assert 20.0 <= result <= 61.0
    assert result == 20.0  # Extreme bias


def test_effective_number_of_codons_multiple_codons() -> None:
    """Test case 2: Test ENC with multiple different codons."""
    result = effective_number_of_codons("ATGATCATTATAACG")
    assert 20.0 <= result <= 61.0


def test_effective_number_of_codons_mixed() -> None:
    """Test case 3: Test ENC with varied codon usage."""
    # More diverse codon usage should give higher ENC
    seq = "ATG" + "ATC" + "AAA" + "GGG" + "CCC" + "TTT"
    result = effective_number_of_codons(seq)
    assert 20.0 <= result <= 61.0


def test_effective_number_of_codons_lowercase() -> None:
    """Test case 4: Test ENC with lowercase sequence."""
    result = effective_number_of_codons("atgatgatg")
    assert result == 20.0


def test_effective_number_of_codons_not_multiple_of_3() -> None:
    """Test case 5: Test ValueError for sequence not multiple of 3."""
    with pytest.raises(ValueError, match="Sequence length must be multiple of 3"):
        effective_number_of_codons("ATGATGA")


def test_effective_number_of_codons_too_short() -> None:
    """Test case 6: Test ValueError for sequence too short."""
    with pytest.raises(ValueError, match="Sequence must be at least 3 bases long"):
        effective_number_of_codons("AT")


def test_effective_number_of_codons_invalid_bases() -> None:
    """Test case 7: Test ValueError for invalid DNA bases."""
    with pytest.raises(ValueError, match="Invalid DNA bases found"):
        effective_number_of_codons("ATXATGATG")


def test_effective_number_of_codons_type_error() -> None:
    """Test case 8: Test TypeError for non-string input."""
    with pytest.raises(TypeError, match="seq must be a string"):
        effective_number_of_codons(123)
