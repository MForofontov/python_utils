import pytest
from typing import Any
from iterable_functions.dictionary_operations.dict_difference import dict_difference


def test_dict_difference_normal_case() -> None:
    """
    Test case 1: Normal operation with differences.
    """
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = {'b': 2, 'c': 4, 'd': 5}
    only_in_1, only_in_2, different = dict_difference(dict1, dict2)

    assert only_in_1 == {'a'}
    assert only_in_2 == {'d'}
    assert different == {'c': (3, 4)}


def test_dict_difference_identical_dicts() -> None:
    """
    Test case 2: Identical dictionaries.
    """
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'a': 1, 'b': 2}
    only_in_1, only_in_2, different = dict_difference(dict1, dict2)

    assert only_in_1 == set()
    assert only_in_2 == set()
    assert different == {}


def test_dict_difference_empty_dicts() -> None:
    """
    Test case 3: Both dictionaries empty.
    """
    dict1 = {}
    dict2 = {}
    only_in_1, only_in_2, different = dict_difference(dict1, dict2)

    assert only_in_1 == set()
    assert only_in_2 == set()
    assert different == {}


def test_dict_difference_one_empty() -> None:
    """
    Test case 4: One dictionary empty.
    """
    dict1 = {'a': 1, 'b': 2}
    dict2 = {}
    only_in_1, only_in_2, different = dict_difference(dict1, dict2)

    assert only_in_1 == {'a', 'b'}
    assert only_in_2 == set()
    assert different == {}


def test_dict_difference_type_error_dict1() -> None:
    """
    Test case 5: TypeError for non-dict dict1.
    """
    with pytest.raises(TypeError, match="dict1 must be a dict"):
        dict_difference("not a dict", {'a': 1})


def test_dict_difference_type_error_dict2() -> None:
    """
    Test case 6: TypeError for non-dict dict2.
    """
    with pytest.raises(TypeError, match="dict2 must be a dict"):
        dict_difference({'a': 1}, "not a dict")


def test_dict_difference_boundary_single_key() -> None:
    """
    Test case 7: Single key in each dict, different values.
    """
    dict1 = {'key': 'old'}
    dict2 = {'key': 'new'}
    only_in_1, only_in_2, different = dict_difference(dict1, dict2)

    assert only_in_1 == set()
    assert only_in_2 == set()
    assert different == {'key': ('old', 'new')}


def test_dict_difference_large_dicts() -> None:
    """
    Test case 8: Performance test with large dictionaries.
    """
    dict1 = {f'key{i}': i for i in range(1000)}
    dict2 = {f'key{i}': i for i in range(500, 1500)}

    only_in_1, only_in_2, different = dict_difference(dict1, dict2)

    assert len(only_in_1) == 500  # keys 0-499
    assert len(only_in_2) == 500  # keys 1000-1499
    assert len(different) == 0  # overlapping keys have same values
