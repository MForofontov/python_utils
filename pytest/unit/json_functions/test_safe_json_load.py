import pytest
from json_functions.safe_json_load import safe_json_load
import json

def test_safe_json_load_valid():
    data = '{"a": 1, "b": 2}'
    result = safe_json_load(data)
    assert result == {"a": 1, "b": 2}

def test_safe_json_load_invalid():
    data = '{a: 1, b: 2}'  # Invalid JSON
    result = safe_json_load(data, default={"error": True})
    assert result == {"error": True}

def test_safe_json_load_empty():
    result = safe_json_load('', default=None)
    assert result is None

def test_safe_json_load_object_hook():
    data = '{"a": 1, "b": 2}'
    def hook(d):
        d['sum'] = d['a'] + d['b']
        return d
    result = safe_json_load(data, object_hook=hook)
    assert result['sum'] == 3

def test_safe_json_load_custom_decoder():
    class MyDecoder(json.JSONDecoder):
        def decode(self, s):
            obj = super().decode(s)
            obj['custom'] = True
            return obj
    data = '{"a": 1}'
    result = safe_json_load(data, decoder=MyDecoder)
    assert result['custom'] is True
