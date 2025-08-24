import pytest
from json_functions.pretty_print_json import pretty_print_json
import json

def test_pretty_print_json_default():
    obj = {"b": 2, "a": 1}
    result = pretty_print_json(obj)
    assert isinstance(result, str)
    # Should be indented and sorted
    assert result.startswith('{')
    assert '\n' in result
    assert '    ' in result  # 4 spaces
    assert result.index('"a"') < result.index('"b"')

def test_pretty_print_json_indent():
    obj = {"a": 1}
    result = pretty_print_json(obj, indent=2)
    assert '\n  ' in result  # 2 spaces

def test_pretty_print_json_no_sort():
    obj = {"b": 2, "a": 1}
    result = pretty_print_json(obj, sort_keys=False)
    assert isinstance(result, str)
