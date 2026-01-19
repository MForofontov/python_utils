import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.sequence_operations.find_orfs import find_orfs


def test_find_orfs_basic() -> None:
    """
    Test case 1: Basic ORF finding.
    """
    seq = "ATGAAATAGATGTAA"
    result = list(find_orfs(seq))
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) for item in result)
    assert all(len(item) == 3 for item in result)


def test_find_orfs_no_orfs() -> None:
    """
    Test case 2: No ORFs found.
    """
    seq = "ATCATCATC"
    result = list(find_orfs(seq))
    assert result == []


def test_find_orfs_multiple_orfs() -> None:
    """
    Test case 3: Multiple ORFs in sequence.
    """
    seq = "ATGAAATAGATGTAA"
    result = list(find_orfs(seq))
    assert len(result) >= 1


def test_find_orfs_empty_sequence() -> None:
    """
    Test case 4: Empty sequence returns no ORFs.
    """
    result = list(find_orfs(""))
    assert result == []


def test_find_orfs_lowercase() -> None:
    """
    Test case 5: Lowercase input sequence.
    """
    seq = "atgaaatag"
    result = list(find_orfs(seq))
    assert len(result) >= 1


def test_find_orfs_invalid_type_error() -> None:
    """
    Test case 6: TypeError for invalid input type.
    """
    with pytest.raises(TypeError, match="seq must be str"):
        list(find_orfs(12345))
    with pytest.raises(TypeError, match="seq must be str"):
        list(find_orfs(None))


def test_find_orfs_invalid_base_error() -> None:
    """
    Test case 7: ValueError for invalid DNA bases.
    """
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        list(find_orfs("ATGCX"))
    with pytest.raises(ValueError, match="Sequence contains invalid DNA bases"):
        list(find_orfs("ATGCU"))


def test_find_orfs_no_stop_codon() -> None:
    """
    Test case 8: ORF starting but no stop codon (incomplete ORF).
    """
    # ATG followed by codons but no stop codon
    seq = "ATGAAACCCTTT"
    result = list(find_orfs(seq))
    # Should return empty since no complete ORF (no stop codon)
    assert result == []
