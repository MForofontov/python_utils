import json
from typing import Any, Optional, Type, TypeVar

T = TypeVar('T')

def safe_json_load(json_string: str, object_hook: Optional[Any] = None, default: Optional[Any] = None, decoder: Optional[Type[json.JSONDecoder]] = None) -> Any:
    """
    Safely load a JSON string, returning a default value on error.
    
    Parameters
    ----------
    json_string : str
        The JSON string to parse.
    object_hook : callable, optional
        Function for custom object decoding.
    default : Any, optional
        Value to return if parsing fails (default: None).
    decoder : type, optional
        Custom JSONDecoder class.
        
    Returns
    -------
    Any
        The parsed object, or default if parsing fails.
        
    Examples
    --------
    >>> safe_json_load('{"a": 1}')
    {'a': 1}
    >>> safe_json_load('invalid', default={'error': True})
    {'error': True}
    """
    try:
        return json.loads(json_string, object_hook=object_hook, cls=decoder) if decoder else json.loads(json_string, object_hook=object_hook)
    except (json.JSONDecodeError, TypeError, ValueError):
        return default
