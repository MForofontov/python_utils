import pytest
from bioinformatics_functions.fasta_misc.fasta_parser import parse_fasta


def test_parse_fasta_single_sequence() -> None:
    """
    Test case 1: Parse single FASTA sequence.
    """
    # Arrange
    fasta_str = ">seq1\nATGCATGC"
    expected = [("seq1", "ATGCATGC")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_multiple_sequences() -> None:
    """
    Test case 2: Parse multiple FASTA sequences.
    """
    # Arrange
    fasta_str = ">seq1\nATGC\n>seq2\nGCTA\n>seq3\nTACG"
    expected = [("seq1", "ATGC"), ("seq2", "GCTA"), ("seq3", "TACG")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_multiline_sequence() -> None:
    """
    Test case 3: Parse sequence split across multiple lines.
    """
    # Arrange
    fasta_str = ">seq1\nATGC\nATGC\nATGC"
    expected = [("seq1", "ATGCATGCATGC")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_empty_lines() -> None:
    """
    Test case 4: Parse FASTA with empty lines.
    """
    # Arrange
    fasta_str = ">seq1\nATGC\n\n>seq2\nGCTA"
    expected = [("seq1", "ATGC"), ("seq2", "GCTA")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_whitespace() -> None:
    """
    Test case 5: Parse FASTA with whitespace.
    """
    # Arrange
    fasta_str = ">seq1  \n  ATGC  \n>seq2\nGCTA  "
    expected = [("seq1", "ATGC"), ("seq2", "GCTA")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_header_with_description() -> None:
    """
    Test case 6: Parse header with description.
    """
    # Arrange
    fasta_str = ">seq1 description here\nATGC"
    expected = [("seq1 description here", "ATGC")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_lowercase_sequence() -> None:
    """
    Test case 7: Parse lowercase DNA sequence (preserves case).
    """
    # Arrange
    fasta_str = ">seq1\natgcatgc"
    expected = [("seq1", "atgcatgc")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_mixed_case() -> None:
    """
    Test case 8: Parse mixed case DNA sequence (preserves case).
    """
    # Arrange
    fasta_str = ">seq1\nAtGcAtGc"
    expected = [("seq1", "AtGcAtGc")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_long_sequence() -> None:
    """
    Test case 9: Parse long sequence split across many lines.
    """
    # Arrange
    seq_lines = ["ATGC"] * 10
    fasta_str = ">seq1\n" + "\n".join(seq_lines)
    expected = [("seq1", "ATGC" * 10)]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_generator_behavior() -> None:
    """
    Test case 10: Verify function returns generator.
    """
    # Arrange
    fasta_str = ">seq1\nATGC"

    # Act
    result = parse_fasta(fasta_str)

    # Assert
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


def test_parse_fasta_empty_sequence() -> None:
    """
    Test case 11: Parse FASTA with empty sequence.
    """
    # Arrange
    fasta_str = ">seq1\n>seq2\nATGC"
    expected = [("seq1", ""), ("seq2", "ATGC")]

    # Act
    result = list(parse_fasta(fasta_str))

    # Assert
    assert result == expected


def test_parse_fasta_type_error_not_string() -> None:
    """
    Test case 12: TypeError when input is not a string.
    """
    # Arrange
    invalid_input = 12345
    expected_message = "fasta_str must be str, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        list(parse_fasta(invalid_input))  # type: ignore


def test_parse_fasta_type_error_none() -> None:
    """
    Test case 13: TypeError when input is None.
    """
    # Arrange
    invalid_input = None
    expected_message = "fasta_str must be str, got NoneType"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        list(parse_fasta(invalid_input))  # type: ignore


def test_parse_fasta_value_error_no_header() -> None:
    """
    Test case 14: ValueError when sequence appears before header.
    """
    # Arrange
    invalid_fasta = "ATGCATGC\n>seq1"
    expected_message = "FASTA format error: sequence before header"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        list(parse_fasta(invalid_fasta))


def test_parse_fasta_value_error_sequence_first() -> None:
    """
    Test case 15: ValueError when file starts with sequence.
    """
    # Arrange
    invalid_fasta = "ATGC"
    expected_message = "FASTA format error: sequence before header"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        list(parse_fasta(invalid_fasta))
