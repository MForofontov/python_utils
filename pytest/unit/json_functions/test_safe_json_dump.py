from json_functions.safe_json_dump import safe_json_dump
import json



def test_safe_json_dump_valid():
    """
    Test case 1: Valid object is serialized to JSON string.
    """
    obj = {"a": 1, "b": 2}
    result = safe_json_dump(obj)
    assert result == '{"a": 1, "b": 2}' or result == '{"b": 2, "a": 1}'

def test_safe_json_dump_invalid():
    """
    Test case 2: Unserializable object returns default value.
    """
    class NotSerializable:
        pass
    obj = NotSerializable()
    result = safe_json_dump(obj, default=None)
    assert result is None


def test_safe_json_dump_non_string_default():
    """
    Test case 3: Unserializable object returns a non-string default value.
    """
    class NotSerializable:
        pass

    obj = NotSerializable()
    default = {"error": "failed"}
    result = safe_json_dump(obj, default=default)
    assert result is default

def test_safe_json_dump_custom_encoder():
    """
    Test case 4: Custom encoder is used for special types.
    """
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return super().default(obj)
    obj = {"a": {1, 2, 3}}
    result = safe_json_dump(obj, encoder=MyEncoder)
    assert '1' in result and '2' in result and '3' in result
