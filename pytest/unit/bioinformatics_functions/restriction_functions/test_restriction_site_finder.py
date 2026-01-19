import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.restriction_functions.restriction_site_finder import (
    restriction_site_finder,
)


def test_restriction_site_finder_single_site() -> None:
    """
    Test case 1: Find single restriction site occurrence.
    """
    # Arrange
    seq = "ATGCGAATTCATGC"
    sites = ["GAATTC"]  # EcoRI recognition site
    expected = {"GAATTC": [4]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_multiple_occurrences() -> None:
    """
    Test case 2: Find multiple occurrences of same site.
    """
    # Arrange
    seq = "GAATTCATGAATTC"
    sites = ["GAATTC"]
    expected = {"GAATTC": [0, 8]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_multiple_sites() -> None:
    """
    Test case 3: Find multiple different restriction sites.
    """
    # Arrange
    seq = "GAATTCATGCGGATCCATGC"
    sites = ["GAATTC", "GGATCC"]  # EcoRI and BamHI
    expected = {"GAATTC": [0], "GGATCC": [10]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_no_matches() -> None:
    """
    Test case 4: No restriction sites found.
    """
    # Arrange
    seq = "ATGCATGCATGC"
    sites = ["GAATTC"]
    expected: dict[str, list[int]] = {"GAATTC": []}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_overlapping_sites() -> None:
    """
    Test case 5: Overlapping restriction sites.
    """
    # Arrange
    seq = "GAATTC"
    sites = ["GAATTC", "AATTC"]
    expected = {"GAATTC": [0], "AATTC": [1]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_site_at_start() -> None:
    """
    Test case 6: Restriction site at start of sequence.
    """
    # Arrange
    seq = "GAATTCATGC"
    sites = ["GAATTC"]
    expected = {"GAATTC": [0]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_site_at_end() -> None:
    """
    Test case 7: Restriction site at end of sequence.
    """
    # Arrange
    seq = "ATGCGAATTC"
    sites = ["GAATTC"]
    expected = {"GAATTC": [4]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_lowercase_input() -> None:
    """
    Test case 8: Lowercase DNA sequence input.
    """
    # Arrange
    seq = "atgcgaattcatgc"
    sites = ["gaattc"]
    expected = {"GAATTC": [4]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_mixed_case() -> None:
    """
    Test case 9: Mixed case input.
    """
    # Arrange
    seq = "AtGcGaAtTcAtGc"
    sites = ["GaAtTc"]
    expected = {"GAATTC": [4]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_short_sites() -> None:
    """
    Test case 10: Short restriction sites (4bp).
    """
    # Arrange
    seq = "ATGCATGCATGC"
    sites = ["ATGC"]
    expected = {"ATGC": [0, 4, 8]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_long_site() -> None:
    """
    Test case 11: Long recognition site (8bp).
    """
    # Arrange
    seq = "ATGCGCGGCCGCATGC"
    sites = ["GCGGCCGC"]  # NotI
    expected = {"GCGGCCGC": [4]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_site_longer_than_sequence() -> None:
    """
    Test case 12: Site longer than sequence returns no matches.
    """
    # Arrange
    seq = "ATGC"
    sites = ["GAATTCATGC"]
    expected: dict[str, list[int]] = {"GAATTCATGC": []}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_many_sites() -> None:
    """
    Test case 13: Search for many different sites.
    """
    # Arrange
    seq = "GAATTCGGATCCAAGCTT"
    sites = ["GAATTC", "GGATCC", "AAGCTT"]  # EcoRI, BamHI, HindIII
    expected = {"GAATTC": [0], "GGATCC": [6], "AAGCTT": [12]}

    # Act
    result = restriction_site_finder(seq, sites)

    # Assert
    assert result == expected


def test_restriction_site_finder_value_error_empty_sites() -> None:
    """
    Test case 14: ValueError for empty sites list.
    """
    # Arrange
    seq = "ATGCATGC"
    empty_sites: list[str] = []
    expected_message = "sites cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        restriction_site_finder(seq, empty_sites)
