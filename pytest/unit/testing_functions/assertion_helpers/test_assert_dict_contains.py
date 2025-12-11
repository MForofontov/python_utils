import pytest
from testing_functions.assertion_helpers.assert_dict_contains import (
    assert_dict_contains,
)


def test_assert_dict_contains_case_1_exact_match() -> None:
    """
    Test case 1: Assert dict contains exact match.
    """
    # Act & Assert
    assert_dict_contains({'a': 1, 'b': 2}, {'a': 1, 'b': 2})


def test_assert_dict_contains_case_2_subset() -> None:
    """
    Test case 2: Assert dict contains subset.
    """
    # Act & Assert
    assert_dict_contains({'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 2})


def test_assert_dict_contains_case_3_single_key() -> None:
    """
    Test case 3: Assert dict contains single key.
    """
    # Act & Assert
    assert_dict_contains({'x': 'y', 'z': 'w'}, {'x': 'y'})


def test_assert_dict_contains_case_4_empty_subset() -> None:
    """
    Test case 4: Assert dict contains empty subset.
    """
    # Act & Assert
    assert_dict_contains({'a': 1}, {})


def test_assert_dict_contains_case_5_nested_values() -> None:
    """
    Test case 5: Assert dict contains with nested values.
    """
    # Act & Assert
    assert_dict_contains({'a': [1, 2], 'b': {'x': 1}}, {'a': [1, 2]})


def test_assert_dict_contains_case_6_type_error_actual_dict() -> None:
    """
    Test case 6: TypeError for invalid actual_dict type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="actual_dict must be a dict"):
        assert_dict_contains("not a dict", {'a': 1})


def test_assert_dict_contains_case_7_type_error_expected_subset() -> None:
    """
    Test case 7: TypeError for invalid expected_subset type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="expected_subset must be a dict"):
        assert_dict_contains({'a': 1}, "not a dict")


def test_assert_dict_contains_case_8_assertion_error_missing_key() -> None:
    """
    Test case 8: AssertionError for missing key.
    """
    # Act & Assert
    with pytest.raises(AssertionError, match="Key .* not found in actual dictionary"):
        assert_dict_contains({'a': 1}, {'b': 2})


def test_assert_dict_contains_case_9_assertion_error_value_mismatch() -> None:
    """
    Test case 9: AssertionError for value mismatch.
    """
    # Act & Assert
    with pytest.raises(AssertionError, match="Value mismatch for key"):
        assert_dict_contains({'a': 1, 'b': 2}, {'a': 1, 'b': 3})
