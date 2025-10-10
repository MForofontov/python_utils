import pytest
from bioinformatics_functions.motif_functions.motif_search import motif_search


def test_motif_search_exact_match() -> None:
    """
    Test case 1: Exact motif match in sequence.
    """
    # Arrange
    seq = "ATGCGTAG"
    motif = "GCG"
    expected = [2]

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_multiple_matches() -> None:
    """
    Test case 2: Multiple occurrences of motif.
    """
    # Arrange
    seq = "ATGATGATG"
    motif = "ATG"
    expected = [0, 3, 6]

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_no_matches() -> None:
    """
    Test case 3: No matches found.
    """
    # Arrange
    seq = "AAAAAAA"
    motif = "GGG"
    expected = []

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_ambiguous_n() -> None:
    """
    Test case 4: Ambiguous base N matches any base.
    """
    # Arrange
    seq = "ATGCGTAG"
    motif = "N"
    expected = [0, 1, 2, 3, 4, 5, 6, 7]

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_ambiguous_r() -> None:
    """
    Test case 5: Ambiguous base R matches A or G.
    """
    # Arrange
    seq = "ATGCGTAG"
    motif = "R"
    expected = [0, 2, 4, 6]  # Positions with A or G

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_ambiguous_pattern() -> None:
    """
    Test case 6: Motif with multiple ambiguous bases.
    """
    # Arrange
    seq = "ATGCATGC"
    motif = "NTG"
    expected = [0, 4]

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_lowercase_input() -> None:
    """
    Test case 7: Lowercase input is converted to uppercase.
    """
    # Arrange
    seq = "atgcgtag"
    motif = "gcg"
    expected = [2]

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_mixed_case() -> None:
    """
    Test case 8: Mixed case input.
    """
    # Arrange
    seq = "AtGcGtAg"
    motif = "GcG"
    expected = [2]

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_single_character_motif() -> None:
    """
    Test case 9: Single character motif.
    """
    # Arrange
    seq = "ATGCGTAG"
    motif = "G"
    expected = [2, 4, 6]

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_motif_longer_than_seq() -> None:
    """
    Test case 10: Motif longer than sequence returns empty list.
    """
    # Arrange
    seq = "ATG"
    motif = "ATGCGTAG"
    expected = []

    # Act
    result = motif_search(seq, motif)

    # Assert
    assert result == expected


def test_motif_search_type_error_seq_not_string() -> None:
    """
    Test case 11: TypeError when seq is not a string.
    """
    # Arrange
    invalid_seq = 12345  # type: ignore
    motif = "ATG"
    expected_message = "seq and motif must be strings"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        motif_search(invalid_seq, motif)  # type: ignore


def test_motif_search_type_error_motif_not_string() -> None:
    """
    Test case 12: TypeError when motif is not a string.
    """
    # Arrange
    seq = "ATGCGTAG"
    invalid_motif = 123  # type: ignore
    expected_message = "seq and motif must be strings"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        motif_search(seq, invalid_motif)  # type: ignore


def test_motif_search_value_error_empty_motif() -> None:
    """
    Test case 13: ValueError for empty motif.
    """
    # Arrange
    seq = "ATGCGTAG"
    empty_motif = ""
    expected_message = "motif must not be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        motif_search(seq, empty_motif)


def test_motif_search_value_error_invalid_iupac() -> None:
    """
    Test case 14: ValueError for invalid IUPAC codes.
    """
    # Arrange
    seq = "ATGCGTAG"
    invalid_motif = "ATX"
    expected_message = "motif contains invalid IUPAC codes"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        motif_search(seq, invalid_motif)
