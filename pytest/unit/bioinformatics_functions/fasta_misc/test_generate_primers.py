import pytest

try:
    import numpy
    from python_utils.bioinformatics_functions.fasta_misc.generate_primers import generate_primers
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    numpy = None  # type: ignore
    generate_primers = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bioinformatics,
    pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed"),
]


def test_generate_primers_valid_sequence() -> None:
    """
    Test case 1: Generate primers from valid DNA sequence.
    """
    # Arrange
    seq = "ATGCATGCATGCATGCATGC"
    length = 10

    # Act
    result = generate_primers(seq, length=length, gc_min=0.4, gc_max=0.6)

    # Assert
    assert isinstance(result, list)
    assert all(len(primer) == length for primer in result)
    assert all(isinstance(primer, str) for primer in result)


def test_generate_primers_default_parameters() -> None:
    """
    Test case 2: Generate primers with default parameters.
    """
    # Arrange
    seq = "ATGCATGCATGCATGCATGCATGC" * 2  # 48 bases

    # Act
    result = generate_primers(seq)

    # Assert
    assert isinstance(result, list)
    assert all(len(primer) == 20 for primer in result)


def test_generate_primers_custom_length() -> None:
    """
    Test case 3: Generate primers with custom length.
    """
    # Arrange
    seq = "ATGCATGCATGCATGCATGC"
    length = 15

    # Act
    result = generate_primers(seq, length=length)

    # Assert
    if result:
        assert all(len(primer) == length for primer in result)


def test_generate_primers_strict_gc_range() -> None:
    """
    Test case 4: Generate primers with strict GC content range.
    """
    # Arrange
    seq = "GCGCGCGCGCGCGCGCGCGC"
    length = 10

    # Act
    result = generate_primers(seq, length=length, gc_min=0.9, gc_max=1.0)

    # Assert
    assert isinstance(result, list)
    # High GC sequence should have primers
    assert len(result) > 0


def test_generate_primers_no_valid_primers() -> None:
    """
    Test case 5: No primers meet GC content criteria.
    """
    # Arrange
    seq = "AAAAAAAAAAAAAAAAAAAAAA"  # All A, 0% GC
    length = 10

    # Act
    result = generate_primers(seq, length=length, gc_min=0.4, gc_max=0.6)

    # Assert
    assert result == []


def test_generate_primers_filters_ccc_endings() -> None:
    """
    Test case 6: Primers ending in CCC or GGG are filtered out.
    """
    # Arrange
    seq = "ATGCATGCGGGCCCATGC"
    length = 10

    # Act
    result = generate_primers(seq, length=length, gc_min=0.3, gc_max=0.7)

    # Assert
    assert isinstance(result, list)
    # Check no primers end with GGG or CCC
    for primer in result:
        assert not primer.endswith("GGG")
        assert not primer.endswith("CCC")


def test_generate_primers_lowercase_input() -> None:
    """
    Test case 7: Lowercase DNA sequence input.
    """
    # Arrange
    seq = "atgcatgcatgcatgcatgc"
    length = 10

    # Act
    result = generate_primers(seq, length=length)

    # Assert
    assert isinstance(result, list)
    assert all(primer.isupper() for primer in result)


def test_generate_primers_mixed_case() -> None:
    """
    Test case 8: Mixed case DNA sequence.
    """
    # Arrange
    seq = "AtGcAtGcAtGcAtGcAtGc"
    length = 10

    # Act
    result = generate_primers(seq, length=length)

    # Assert
    assert isinstance(result, list)
    assert all(primer.isupper() for primer in result)


def test_generate_primers_minimum_length() -> None:
    """
    Test case 9: Generate primers with minimum length.
    """
    # Arrange
    seq = "ATGCATGCATGCATGC"
    length = 5

    # Act
    result = generate_primers(seq, length=length, gc_min=0.3, gc_max=0.7)

    # Assert
    assert isinstance(result, list)
    if result:
        assert all(len(primer) == length for primer in result)


def test_generate_primers_type_error_seq_not_string() -> None:
    """
    Test case 10: TypeError when seq is not a string.
    """
    # Arrange
    invalid_seq = 12345  # type: ignore
    expected_message = "seq must be str, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        generate_primers(invalid_seq)  # type: ignore


def test_generate_primers_type_error_length_not_int() -> None:
    """
    Test case 11: TypeError when length is not an integer.
    """
    # Arrange
    seq = "ATGCATGC"
    invalid_length = "20"  # type: ignore
    expected_message = "length must be int, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        generate_primers(seq, length=invalid_length)  # type: ignore


def test_generate_primers_type_error_gc_min_not_number() -> None:
    """
    Test case 12: TypeError when gc_min is not a number.
    """
    # Arrange
    seq = "ATGCATGC"
    invalid_gc = "0.4"  # type: ignore
    expected_message = "gc_min must be a number, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        generate_primers(seq, gc_min=invalid_gc)  # type: ignore


def test_generate_primers_type_error_gc_max_not_number() -> None:
    """
    Test case 13: TypeError when gc_max is not a number.
    """
    # Arrange
    seq = "ATGCATGC"
    invalid_gc = "0.6"  # type: ignore
    expected_message = "gc_max must be a number, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        generate_primers(seq, gc_max=invalid_gc)  # type: ignore


def test_generate_primers_value_error_invalid_bases() -> None:
    """
    Test case 14: ValueError for invalid DNA bases.
    """
    # Arrange
    invalid_seq = "ATGCXYZ"
    expected_message = "Sequence contains invalid DNA bases"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(invalid_seq)


def test_generate_primers_value_error_length_zero() -> None:
    """
    Test case 15: ValueError when length is zero.
    """
    # Arrange
    seq = "ATGCATGC"
    invalid_length = 0
    expected_message = "length must be positive"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(seq, length=invalid_length)


def test_generate_primers_value_error_length_negative() -> None:
    """
    Test case 16: ValueError when length is negative.
    """
    # Arrange
    seq = "ATGCATGC"
    invalid_length = -5
    expected_message = "length must be positive"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(seq, length=invalid_length)


def test_generate_primers_value_error_length_too_large() -> None:
    """
    Test case 17: ValueError when length exceeds sequence length.
    """
    # Arrange
    seq = "ATGC"
    invalid_length = 100
    expected_message = "length must be positive and <= sequence length"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(seq, length=invalid_length)


def test_generate_primers_value_error_gc_min_negative() -> None:
    """
    Test case 18: ValueError when gc_min is negative.
    """
    # Arrange
    seq = "ATGCATGCATGCATGCATGC"  # 20 chars to match default length
    invalid_gc = -0.5
    expected_message = "gc_min must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(seq, gc_min=invalid_gc)


def test_generate_primers_value_error_gc_min_greater_than_one() -> None:
    """
    Test case 19: ValueError when gc_min is greater than 1.
    """
    # Arrange
    seq = "ATGCATGCATGCATGCATGC"  # 20 chars to match default length
    invalid_gc = 1.5
    expected_message = "gc_min must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(seq, gc_min=invalid_gc)


def test_generate_primers_value_error_gc_max_negative() -> None:
    """
    Test case 20: ValueError when gc_max is negative.
    """
    # Arrange
    seq = "ATGCATGCATGCATGCATGC"  # 20 chars to match default length
    invalid_gc = -0.5
    expected_message = "gc_max must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(seq, gc_max=invalid_gc)


def test_generate_primers_value_error_gc_max_greater_than_one() -> None:
    """
    Test case 21: ValueError when gc_max is greater than 1.
    """
    # Arrange
    seq = "ATGCATGCATGCATGCATGC"  # 20 chars to match default length
    invalid_gc = 1.5
    expected_message = "gc_max must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(seq, gc_max=invalid_gc)


def test_generate_primers_value_error_gc_min_greater_than_gc_max() -> None:
    """
    Test case 22: ValueError when gc_min is greater than gc_max.
    """
    # Arrange
    seq = "ATGCATGCATGCATGCATGC"  # 20 chars to match default length
    invalid_min = 0.8
    invalid_max = 0.4
    expected_message = "gc_min cannot be greater than gc_max"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_primers(seq, gc_min=invalid_min, gc_max=invalid_max)
