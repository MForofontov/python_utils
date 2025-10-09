import pytest
from bioinformatics_functions.sequence_statistics.nucleotide_frequency import nucleotide_frequency


def test_nucleotide_frequency_balanced_sequence() -> None:
    """
    Test case 1: Nucleotide frequency with balanced sequence.
    """
    # Arrange
    seq = "ATGC"
    expected = {'A': 1, 'T': 1, 'G': 1, 'C': 1}
    
    # Act
    result = nucleotide_frequency(seq)
    
    # Assert
    assert result == expected


def test_nucleotide_frequency_unbalanced_sequence() -> None:
    """
    Test case 2: Nucleotide frequency with unbalanced sequence.
    """
    # Arrange
    seq = "AAATTTGGGCCC"
    expected = {'A': 3, 'T': 3, 'G': 3, 'C': 3}
    
    # Act
    result = nucleotide_frequency(seq)
    
    # Assert
    assert result == expected


def test_nucleotide_frequency_single_base_type() -> None:
    """
    Test case 3: Nucleotide frequency with single base type.
    """
    # Arrange
    seq = "AAAA"
    expected = {'A': 4, 'T': 0, 'G': 0, 'C': 0}
    
    # Act
    result = nucleotide_frequency(seq)
    
    # Assert
    assert result == expected


def test_nucleotide_frequency_lowercase_input() -> None:
    """
    Test case 4: Lowercase DNA input.
    """
    # Arrange
    seq = "atgc"
    expected = {'A': 1, 'T': 1, 'G': 1, 'C': 1}
    
    # Act
    result = nucleotide_frequency(seq)
    
    # Assert
    assert result == expected


def test_nucleotide_frequency_mixed_case() -> None:
    """
    Test case 5: Mixed case DNA input.
    """
    # Arrange
    seq = "AaTtGgCc"
    expected = {'A': 2, 'T': 2, 'G': 2, 'C': 2}
    
    # Act
    result = nucleotide_frequency(seq)
    
    # Assert
    assert result == expected


def test_nucleotide_frequency_empty_sequence() -> None:
    """
    Test case 6: Empty DNA sequence returns zero counts.
    """
    # Arrange
    seq = ""
    expected = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    
    # Act
    result = nucleotide_frequency(seq)
    
    # Assert
    assert result == expected


def test_nucleotide_frequency_long_sequence() -> None:
    """
    Test case 7: Long DNA sequence.
    """
    # Arrange
    seq = "ATGC" * 250  # 1000 bases
    expected = {'A': 250, 'T': 250, 'G': 250, 'C': 250}
    
    # Act
    result = nucleotide_frequency(seq)
    
    # Assert
    assert result == expected


def test_nucleotide_frequency_all_keys_present() -> None:
    """
    Test case 8: All four bases in result even if not in sequence.
    """
    # Arrange
    seq = "AAA"
    
    # Act
    result = nucleotide_frequency(seq)
    
    # Assert
    assert 'A' in result
    assert 'T' in result
    assert 'G' in result
    assert 'C' in result
    assert result['A'] == 3
    assert result['T'] == 0


def test_nucleotide_frequency_type_error_not_string() -> None:
    """
    Test case 9: TypeError when input is not a string.
    """
    # Arrange
    invalid_input = 12345  # type: ignore
    expected_message = "seq must be a string, got int"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        nucleotide_frequency(invalid_input)  # type: ignore


def test_nucleotide_frequency_type_error_list() -> None:
    """
    Test case 10: TypeError when input is a list.
    """
    # Arrange
    invalid_input = ["A", "T", "G", "C"]  # type: ignore
    expected_message = "seq must be a string, got list"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        nucleotide_frequency(invalid_input)  # type: ignore


def test_nucleotide_frequency_value_error_invalid_base() -> None:
    """
    Test case 11: ValueError for invalid DNA base.
    """
    # Arrange
    invalid_seq = "ATGCX"
    expected_message = "Invalid DNA bases found: X"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        nucleotide_frequency(invalid_seq)


def test_nucleotide_frequency_value_error_rna_base() -> None:
    """
    Test case 12: ValueError for RNA base (U).
    """
    # Arrange
    invalid_seq = "AUGC"
    expected_message = "Invalid DNA bases found: U"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        nucleotide_frequency(invalid_seq)


def test_nucleotide_frequency_value_error_numbers() -> None:
    """
    Test case 13: ValueError for numeric characters.
    """
    # Arrange
    invalid_seq = "ATG123"
    expected_message = "Invalid DNA bases found:"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        nucleotide_frequency(invalid_seq)


def test_nucleotide_frequency_value_error_special_chars() -> None:
    """
    Test case 14: ValueError for special characters.
    """
    # Arrange
    invalid_seq = "ATG-C"
    expected_message = "Invalid DNA bases found:"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        nucleotide_frequency(invalid_seq)
