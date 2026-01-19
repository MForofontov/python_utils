import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.sequence_statistics.codon_adaptation_index import (
    codon_adaptation_index,
)


def test_codon_adaptation_index_uniform() -> None:
    """Test case 1: Test CAI with no reference weights (uniform)."""
    result = codon_adaptation_index("ATGATGATG")
    assert 0.0 <= result <= 1.0
    assert result == 1.0  # All same codon, weight 1.0


def test_codon_adaptation_index_with_weights() -> None:
    """Test case 2: Test CAI with custom reference weights."""
    weights = {"ATG": 1.0, "ATT": 0.5, "ATC": 0.8}
    result = codon_adaptation_index("ATGATT", reference_weights=weights)
    assert 0.0 <= result <= 1.0
    assert result < 1.0  # Mixed weights


def test_codon_adaptation_index_stop_codon() -> None:
    """Test case 3: Test CAI excludes stop codons."""
    # TAA is stop codon
    result = codon_adaptation_index("ATGATGTAA")
    assert result > 0.0  # Should calculate without stop codon


def test_codon_adaptation_index_lowercase() -> None:
    """Test case 4: Test CAI with lowercase sequence."""
    result = codon_adaptation_index("atgatgatg")
    assert result == 1.0


def test_codon_adaptation_index_not_multiple_of_3() -> None:
    """Test case 5: Test ValueError for sequence not multiple of 3."""
    with pytest.raises(ValueError, match="Sequence length must be multiple of 3"):
        codon_adaptation_index("ATGATG A")


def test_codon_adaptation_index_invalid_bases() -> None:
    """Test case 6: Test ValueError for invalid DNA bases."""
    with pytest.raises(ValueError, match="Invalid DNA bases found"):
        codon_adaptation_index("ATXATGATG")


def test_codon_adaptation_index_empty() -> None:
    """Test case 7: Test ValueError for empty sequence."""
    with pytest.raises(ValueError, match="Sequence cannot be empty"):
        codon_adaptation_index("")


def test_codon_adaptation_index_type_error() -> None:
    """Test case 8: Test TypeError for non-string input."""
    with pytest.raises(TypeError, match="seq must be a string"):
        codon_adaptation_index(123)


def test_codon_adaptation_index_weights_type_error() -> None:
    """Test case 9: Test TypeError for non-dict reference_weights."""
    with pytest.raises(TypeError, match="reference_weights must be a dict or None"):
        codon_adaptation_index("ATGATG", reference_weights="not_a_dict")
