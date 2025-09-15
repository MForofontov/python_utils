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


def test_json_merge_empty_dicts() -> None:
    """
    Test case 6: Merging empty dictionaries.
    """
    a = {}
    b = {}
    result = json_merge(a, b)
    assert result == {}


def test_json_merge_empty_lists() -> None:
    """
    Test case 7: Merging empty lists.
    """
    a = []
    b = []
    result = json_merge(a, b)
    assert result == []


def test_json_merge_primitives() -> None:
    """
    Test case 8: Merging primitive values.
    """
    result = json_merge(1, 2)
    assert result == 2

    result = json_merge("hello", "world")
    assert result == "world"

    result = json_merge(True, False)
    assert result == False


def test_json_merge_complex_nested() -> None:
    """
    Test case 9: Complex nested structure merge.
    """
    a = {"users": [{"id": 1, "name": "Alice"}], "config": {"theme": "dark"}}
    b = {"users": [{"id": 2, "name": "Bob"}], "config": {"timeout": 30}}
    result = json_merge(a, b, deep=True)
    expected = {
        "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
        "config": {"theme": "dark", "timeout": 30},
    }
    assert result == expected


def test_json_merge_invalid_deep_parameter() -> None:
    """
    Test case 10: Test json_merge with invalid deep parameter type.
    """
    with pytest.raises(TypeError):
        json_merge({"a": 1}, {"b": 2}, deep="invalid")
