import pytest

try:
    import numpy
    from pyutils_collection.bioinformatics_functions.translation_functions.transcribe_dna_to_rna import (
        transcribe_dna_to_rna,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    transcribe_dna_to_rna = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_transcribe_dna_to_rna_basic() -> None:
    """
    Test case 1: Basic DNA to RNA transcription.
    """
    seq = "ATGC"
    result = transcribe_dna_to_rna(seq)
    assert result == "AUGC"


def test_transcribe_dna_to_rna_no_thymine() -> None:
    """
    Test case 2: Sequence without thymine.
    """
    seq = "ACGACG"
    result = transcribe_dna_to_rna(seq)
    assert result == "ACGACG"


def test_transcribe_dna_to_rna_all_thymine() -> None:
    """
    Test case 3: Sequence with all thymines.
    """
    seq = "TTTT"
    result = transcribe_dna_to_rna(seq)
    assert result == "UUUU"


def test_transcribe_dna_to_rna_lowercase() -> None:
    """
    Test case 4: Lowercase input sequence.
    """
    seq = "atgc"
    result = transcribe_dna_to_rna(seq)
    assert result == "AUGC"


def test_transcribe_dna_to_rna_empty_sequence() -> None:
    """
    Test case 5: Empty sequence returns empty string.
    """
    result = transcribe_dna_to_rna("")
    assert result == ""


def test_transcribe_dna_to_rna_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        transcribe_dna_to_rna(12345)
    with pytest.raises(TypeError, match="seq must be str"):
        transcribe_dna_to_rna(None)


def test_transcribe_dna_to_rna_invalid_base_error() -> None:
    """
    Test case 7: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        transcribe_dna_to_rna("ATGCX")
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        transcribe_dna_to_rna("ATGCU")
