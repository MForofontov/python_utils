import pytest
from testing_functions.assertion_helpers.assert_type_match import assert_type_match


def test_assert_type_match_int_type() -> None:
    """
    Test case 1: Assert integer type match.
    """
    # Act & Assert
    assert_type_match(5, int)


def test_assert_type_match_str_type() -> None:
    """
    Test case 2: Assert string type match.
    """
    # Act & Assert
    assert_type_match("hello", str)


def test_assert_type_match_list_type() -> None:
    """
    Test case 3: Assert list type match.
    """
    # Act & Assert
    assert_type_match([1, 2, 3], list)


def test_assert_type_match_dict_type() -> None:
    """
    Test case 4: Assert dict type match.
    """
    # Act & Assert
    assert_type_match({"a": 1}, dict)


def test_assert_type_match_float_type() -> None:
    """
    Test case 5: Assert float type match.
    """
    # Act & Assert
    assert_type_match(3.14, float)


def test_assert_type_match_type_error_expected_type() -> None:
    """
    Test case 6: TypeError for invalid expected_type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="expected_type must be a type"):
        assert_type_match(5, "int")


def test_assert_type_match_assertion_error_type_mismatch() -> None:
    """
    Test case 7: AssertionError for type mismatch.
    """
    # Act & Assert
    with pytest.raises(AssertionError, match="Type mismatch"):
        assert_type_match("5", int)


def test_assert_type_match_assertion_error_int_float_mismatch() -> None:
    """
    Test case 8: AssertionError for int/float mismatch.
    """
    # Act & Assert
    with pytest.raises(AssertionError, match="Type mismatch"):
        assert_type_match(5, float)
