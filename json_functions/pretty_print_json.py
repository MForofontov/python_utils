import json
from typing import Any

def pretty_print_json(obj: Any, indent: int = 4, sort_keys: bool = True) -> str:
    """
    Return a pretty-printed JSON string from a Python object.
    
    Args:
        obj: The object to serialize.
        indent: Number of spaces for indentation (default: 4).
        sort_keys: Whether to sort keys alphabetically (default: True).
    Returns:
        A pretty-printed JSON string.
    """
    return json.dumps(obj, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
