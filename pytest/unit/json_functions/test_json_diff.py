from json_functions.json_diff import json_diff


def test_json_diff_dicts() -> None:
    """Test case 1: Test json_diff with dictionary differences."""
    a = {"a": 1, "b": 2}
    b = {"a": 1, "b": 3, "c": 4}
    result = json_diff(a, b)
    assert ("b", 2, 3) in result or ("b", 2, 3) in [
        (p.split(".")[-1], av, bv) for p, av, bv in result
    ]
    assert ("c", None, 4) in result or ("c", None, 4) in [
        (p.split(".")[-1], av, bv) for p, av, bv in result
    ]


def test_json_diff_lists() -> None:
    """Test case 2: Test json_diff with list differences."""
    a = [1, 2, 3]
    b = [1, 4]
    result = json_diff(a, b)
    assert ("[1]", 2, 4) in result
    assert ("[2]", 3, None) in result


def test_json_diff_nested() -> None:
    """Test case 3: Test json_diff with nested structure differences."""
    a = {"a": {"x": 1, "y": 2}, "b": [1, 2]}
    b = {"a": {"x": 1, "y": 3}, "b": [1, 2, 3]}
    result = json_diff(a, b)
    assert any("a.y" in p and av == 2 and bv == 3 for p, av, bv in result)
    assert any("b[2]" in p and av is None and bv == 3 for p, av, bv in result)


def test_json_diff_type_change() -> None:
    """Test case 4: Test json_diff with type changes."""
    a = {"a": 1}
    b = [1]
    result = json_diff(a, b)
    assert ("", {"a": 1}, [1]) in result
