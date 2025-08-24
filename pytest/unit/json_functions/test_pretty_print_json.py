import pytest
from json_functions.pretty_print_json import pretty_print_json
import json



def test_pretty_print_json_default():
    """
    Test case 1: Pretty print with default indent and sorted keys
    """
    # Test case 1: Default pretty print
    obj = {"b": 2, "a": 1}
    result = pretty_print_json(obj)
    assert isinstance(result, str)
    assert result.startswith('{')
    assert '\n' in result
    assert '    ' in result  # 4 spaces
    assert result.index('"a"') < result.index('"b"')

def test_pretty_print_json_indent():
    """
    Test case 2: Pretty print with custom indent
    """
    # Test case 2: Custom indent
    obj = {"a": 1}
    result = pretty_print_json(obj, indent=2)
    assert '\n  ' in result  # 2 spaces

def test_pretty_print_json_no_sort():
    """
    Test case 3: Pretty print with sort_keys=False
    """
    # Test case 3: No sort_keys
    obj = {"b": 2, "a": 1}
    result = pretty_print_json(obj, sort_keys=False)
    assert isinstance(result, str)
