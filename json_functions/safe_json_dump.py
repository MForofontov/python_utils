import json
from typing import Any, Optional, Type

def safe_json_dump(obj: Any, default: Optional[Any] = None, encoder: Optional[Type[json.JSONEncoder]] = None, **kwargs) -> str:
    """
    Safely dump an object to a JSON string, returning a default value on error.
    
    Parameters
    ----------
    obj : Any
        The object to serialize.
    default : Any, optional
        Value to return if serialization fails (default: None).
    encoder : type, optional
        Custom JSONEncoder class.
    **kwargs
        Additional arguments for json.dumps.
        
    Returns
    -------
    str
        The JSON string, or default if serialization fails.
        
    Examples
    --------
    >>> safe_json_dump({'a': 1})
    '{"a": 1}'
    >>> safe_json_dump(set([1, 2]), default='error')
    'error'
    """
    try:
        return json.dumps(obj, cls=encoder, **kwargs) if encoder else json.dumps(obj, **kwargs)
    except (TypeError, ValueError):
        return default
