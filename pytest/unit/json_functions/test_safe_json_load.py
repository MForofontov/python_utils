import pytest
from json_functions.safe_json_load import safe_json_load
import json



def test_safe_json_load_valid():
    """
    Test case 1: Valid JSON string should load as dict
    """
    # Test case 1: Valid JSON string
    data = '{"a": 1, "b": 2}'
    result = safe_json_load(data)
    assert result == {"a": 1, "b": 2}

def test_safe_json_load_invalid():
    """
    Test case 2: Invalid JSON string returns default value
    """
    # Test case 2: Invalid JSON string returns default
    data = '{a: 1, b: 2}'
    result = safe_json_load(data, default={"error": True})
    assert result == {"error": True}

def test_safe_json_load_empty():
    """
    Test case 3: Empty string returns None (default)
    """
    # Test case 3: Empty string returns None
    result = safe_json_load('', default=None)
    assert result is None

def test_safe_json_load_object_hook():
    """
    Test case 4: Custom object_hook is used for decoding
    """
    # Test case 4: Use object_hook for custom decoding
    data = '{"a": 1, "b": 2}'
    def hook(d):
        d['sum'] = d['a'] + d['b']
        return d
    result = safe_json_load(data, object_hook=hook)
    assert result['sum'] == 3

def test_safe_json_load_custom_decoder():
    """
    Test case 5: Custom decoder class is used
    """
    # Test case 5: Use custom decoder class
    class MyDecoder(json.JSONDecoder):
        def decode(self, s):
            obj = super().decode(s)
            obj['custom'] = True
            return obj
    data = '{"a": 1}'
    result = safe_json_load(data, decoder=MyDecoder)
    assert result['custom'] is True
