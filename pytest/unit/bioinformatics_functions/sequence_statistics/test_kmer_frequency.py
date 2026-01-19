import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.sequence_statistics.kmer_frequency import kmer_frequency


def test_kmer_frequency_basic() -> None:
    """
    Test case 1: Basic k-mer frequency calculation.
    """
    seq = "ATGCATGC"
    result = kmer_frequency(seq, 3)
    assert isinstance(result, dict)
    assert "ATG" in result
    assert result["ATG"] == 2


def test_kmer_frequency_k_two() -> None:
    """
    Test case 2: K-mer frequency with k=2.
    """
    seq = "ATGCAT"
    result = kmer_frequency(seq, 2)
    assert result["AT"] == 2
    assert result["TG"] == 1
    assert result["GC"] == 1
    assert result["CA"] == 1


def test_kmer_frequency_k_one() -> None:
    """
    Test case 3: K-mer frequency with k=1 (base count).
    """
    seq = "AATT"
    result = kmer_frequency(seq, 1)
    assert result["A"] == 2
    assert result["T"] == 2


def test_kmer_frequency_no_repeats() -> None:
    """
    Test case 4: All unique k-mers.
    """
    seq = "ATGC"
    result = kmer_frequency(seq, 2)
    assert all(count == 1 for count in result.values())


def test_kmer_frequency_lowercase() -> None:
    """
    Test case 5: Lowercase input sequence.
    """
    seq = "atgcatgc"
    result = kmer_frequency(seq, 3)
    # Check if uppercase version exists or handle lowercase
    assert "ATG" in result or "atg" in result
    if "ATG" in result:
        assert result["ATG"] == 2
    else:
        assert result["atg"] == 2


def test_kmer_frequency_k_equals_length() -> None:
    """
    Test case 6: K equals sequence length.
    """
    seq = "ATGC"
    result = kmer_frequency(seq, 4)
    assert result == {"ATGC": 1}


def test_kmer_frequency_invalid_type_error() -> None:
    """
    Test case 7: TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        kmer_frequency(12345, 3)
    with pytest.raises(TypeError, match="k must be int"):
        kmer_frequency("ATGC", 3.5)


def test_kmer_frequency_invalid_value_error() -> None:
    """
    Test case 8: ValueError for invalid k values.
    """
    with pytest.raises(ValueError, match="k must be positive"):
        kmer_frequency("ATGC", 0)
    with pytest.raises(ValueError, match="k cannot be longer than sequence"):
        kmer_frequency("ATGC", 5)
