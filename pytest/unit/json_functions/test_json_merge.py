import pytest
from json_functions.json_merge import json_merge

def test_json_merge_dicts_shallow() -> None:
    a = {"a": 1, "b": 2}
    b = {"b": 3, "c": 4}
    result = json_merge(a, b, deep=False)
    assert result == {"a": 1, "b": 3, "c": 4}

def test_json_merge_dicts_deep() -> None:
    a = {"a": {"x": 1}, "b": 2}
    b = {"a": {"y": 2}, "b": 3}
    result = json_merge(a, b, deep=True)
    assert result == {"a": {"x": 1, "y": 2}, "b": 3}

def test_json_merge_lists() -> None:
    a = [1, 2]
    b = [3, 4]
    result = json_merge(a, b)
    assert result == [1, 2, 3, 4]

def test_json_merge_dict_and_list() -> None:
    a = {"a": 1}
    b = [1, 2]
    result = json_merge(a, b)
    assert result == [1, 2]

def test_json_merge_none() -> None:
    a = None
    b = {"a": 1}
    result = json_merge(a, b)
    assert result == {"a": 1}
    result2 = json_merge(b, None)
    assert result2 == {"a": 1}
