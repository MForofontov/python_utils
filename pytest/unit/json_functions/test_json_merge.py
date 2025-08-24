import pytest
from json_functions.json_merge import json_merge


def test_json_merge_dicts_shallow() -> None:
    """
    Test case 1: Shallow merge of two dicts (no recursion).
    """
    a = {"a": 1, "b": 2}
    b = {"b": 3, "c": 4}
    result = json_merge(a, b, deep=False)
    assert result == {"a": 1, "b": 3, "c": 4}


def test_json_merge_dicts_deep() -> None:
    """
    Test case 2: Deep merge of two dicts (recursive merge of nested dicts).
    """
    a = {"a": {"x": 1}, "b": 2}
    b = {"a": {"y": 2}, "b": 3}
    result = json_merge(a, b, deep=True)
    assert result == {"a": {"x": 1, "y": 2}, "b": 3}


def test_json_merge_lists() -> None:
    """
    Test case 3: Merging two lists (concatenation).
    """
    a = [1, 2]
    b = [3, 4]
    result = json_merge(a, b)
    assert result == [1, 2, 3, 4]


def test_json_merge_dict_and_list() -> None:
    """
    Test case 4: Merging dict and list (should return the list).
    """
    a = {"a": 1}
    b = [1, 2]
    result = json_merge(a, b)
    assert result == [1, 2]


def test_json_merge_none() -> None:
    """
    Test case 5: Merging with None (should return the non-None value).
    """
    a = None
    b = {"a": 1}
    result = json_merge(a, b)
    assert result == {"a": 1}
    result2 = json_merge(b, None)
    assert result2 == {"a": 1}
