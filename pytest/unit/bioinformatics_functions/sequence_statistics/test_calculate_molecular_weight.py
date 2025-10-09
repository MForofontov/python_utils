import pytest
from bioinformatics_functions.sequence_statistics.calculate_molecular_weight import calculate_molecular_weight


def test_calculate_molecular_weight_dna_sequence() -> None:
    """
    Test case 1: Calculate molecular weight of DNA sequence.
    """
    # Arrange
    dna_seq = "ATGC"
    
    # Act
    result = calculate_molecular_weight(dna_seq, 'dna')
    
    # Assert
    assert isinstance(result, float)
    assert result > 0


def test_calculate_molecular_weight_rna_sequence() -> None:
    """
    Test case 2: Calculate molecular weight of RNA sequence.
    """
    # Arrange
    rna_seq = "AUGC"
    
    # Act
    result = calculate_molecular_weight(rna_seq, 'rna')
    
    # Assert
    assert isinstance(result, float)
    assert result > 0


def test_calculate_molecular_weight_protein_sequence() -> None:
    """
    Test case 3: Calculate molecular weight of protein sequence.
    """
    # Arrange
    protein_seq = "ACDEFGH"
    
    # Act
    result = calculate_molecular_weight(protein_seq, 'protein')
    
    # Assert
    assert isinstance(result, float)
    assert result > 0


def test_calculate_molecular_weight_default_type() -> None:
    """
    Test case 4: Default sequence type is DNA.
    """
    # Arrange
    dna_seq = "ATGC"
    
    # Act
    result = calculate_molecular_weight(dna_seq)
    
    # Assert
    assert isinstance(result, float)
    assert result > 0


def test_calculate_molecular_weight_lowercase_input() -> None:
    """
    Test case 5: Lowercase sequence input.
    """
    # Arrange
    dna_seq = "atgc"
    
    # Act
    result = calculate_molecular_weight(dna_seq, 'dna')
    
    # Assert
    assert isinstance(result, float)
    assert result > 0


def test_calculate_molecular_weight_mixed_case() -> None:
    """
    Test case 6: Mixed case sequence input.
    """
    # Arrange
    dna_seq = "AtGc"
    
    # Act
    result = calculate_molecular_weight(dna_seq, 'dna')
    
    # Assert
    assert isinstance(result, float)
    assert result > 0


def test_calculate_molecular_weight_long_sequence() -> None:
    """
    Test case 7: Long sequence.
    """
    # Arrange
    dna_seq = "ATGC" * 100
    
    # Act
    result = calculate_molecular_weight(dna_seq, 'dna')
    
    # Assert
    assert isinstance(result, float)
    assert result > 0


def test_calculate_molecular_weight_empty_sequence() -> None:
    """
    Test case 8: Empty sequence returns zero.
    """
    # Arrange
    empty_seq = ""
    
    # Act
    result = calculate_molecular_weight(empty_seq, 'dna')
    
    # Assert
    assert result == 0.0


def test_calculate_molecular_weight_type_error_seq_not_string() -> None:
    """
    Test case 9: TypeError when seq is not a string.
    """
    # Arrange
    invalid_seq = 12345  # type: ignore
    expected_message = "seq must be str, got int"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        calculate_molecular_weight(invalid_seq, 'dna')  # type: ignore


def test_calculate_molecular_weight_type_error_seq_type_not_string() -> None:
    """
    Test case 10: TypeError when seq_type is not a string.
    """
    # Arrange
    seq = "ATGC"
    invalid_type = 123  # type: ignore
    expected_message = "seq_type must be str, got int"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        calculate_molecular_weight(seq, invalid_type)  # type: ignore


def test_calculate_molecular_weight_value_error_invalid_seq_type() -> None:
    """
    Test case 11: ValueError for invalid seq_type.
    """
    # Arrange
    seq = "ATGC"
    invalid_type = "invalid"
    expected_message = "seq_type must be 'dna', 'rna', or 'protein'"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        calculate_molecular_weight(seq, invalid_type)


def test_calculate_molecular_weight_value_error_invalid_dna_characters() -> None:
    """
    Test case 12: ValueError for invalid DNA characters.
    """
    # Arrange
    invalid_seq = "ATGCXYZ"
    expected_message = "Sequence contains invalid dna characters"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        calculate_molecular_weight(invalid_seq, 'dna')


def test_calculate_molecular_weight_value_error_invalid_rna_characters() -> None:
    """
    Test case 13: ValueError for invalid RNA characters.
    """
    # Arrange
    invalid_seq = "AUGCXYZ"
    expected_message = "Sequence contains invalid rna characters"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        calculate_molecular_weight(invalid_seq, 'rna')


def test_calculate_molecular_weight_value_error_invalid_protein_characters() -> None:
    """
    Test case 14: ValueError for invalid protein characters.
    """
    # Arrange
    invalid_seq = "ACDEFXYZ"
    expected_message = "Sequence contains invalid protein characters"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        calculate_molecular_weight(invalid_seq, 'protein')
