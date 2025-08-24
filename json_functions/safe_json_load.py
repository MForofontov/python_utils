import json
from typing import Any, Optional, Type, TypeVar

T = TypeVar('T')

def safe_json_load(json_string: str, object_hook: Optional[Any] = None, default: Optional[Any] = None, decoder: Optional[Type[json.JSONDecoder]] = None) -> Any:
    """
    Safely load a JSON string, returning a default value on error.
    
    Args:
        json_string: The JSON string to parse.
        object_hook: Optional function for custom object decoding.
        default: Value to return if parsing fails (default: None).
        decoder: Optional custom JSONDecoder class.
    Returns:
        The parsed object, or default if parsing fails.
    """
    try:
        return json.loads(json_string, object_hook=object_hook, cls=decoder) if decoder else json.loads(json_string, object_hook=object_hook)
    except (json.JSONDecodeError, TypeError, ValueError):
        return default
