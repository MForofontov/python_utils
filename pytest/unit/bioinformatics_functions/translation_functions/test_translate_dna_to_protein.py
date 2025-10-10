import pytest
from bioinformatics_functions.translation_functions.translate_dna_to_protein import (
    translate_dna_to_protein,
)


def test_translate_dna_to_protein_basic() -> None:
    """
    Test case 1: Basic DNA to protein translation.
    """
    seq = "ATGGCC"
    result = translate_dna_to_protein(seq)
    assert result == "MA"


def test_translate_dna_to_protein_start_codon() -> None:
    """
    Test case 2: Start codon ATG translates to M.
    """
    seq = "ATG"
    result = translate_dna_to_protein(seq)
    assert result == "M"


def test_translate_dna_to_protein_stop_codon() -> None:
    """
    Test case 3: Stop codon translates to asterisk.
    """
    seq = "ATGTAA"
    result = translate_dna_to_protein(seq)
    assert result == "M*"


def test_translate_dna_to_protein_lowercase() -> None:
    """
    Test case 4: Lowercase input sequence.
    """
    seq = "atggcc"
    result = translate_dna_to_protein(seq)
    assert result == "MA"


def test_translate_dna_to_protein_longer_sequence() -> None:
    """
    Test case 5: Longer sequence translation.
    """
    seq = "ATGGCCAAATAG"
    result = translate_dna_to_protein(seq)
    assert len(result) == 4


def test_translate_dna_to_protein_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        translate_dna_to_protein(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        translate_dna_to_protein(None)


def test_translate_dna_to_protein_invalid_base_error() -> None:
    """
    Test case 7: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        translate_dna_to_protein("ATGCXX")


def test_translate_dna_to_protein_invalid_length_error() -> None:
    """
    Test case 8: ValueError for length not multiple of 3.
    """
    with pytest.raises(ValueError, match="Sequence length must be a multiple of 3"):
        translate_dna_to_protein("ATGC")
    with pytest.raises(ValueError, match="Sequence length must be a multiple of 3"):
        translate_dna_to_protein("ATGCC")
