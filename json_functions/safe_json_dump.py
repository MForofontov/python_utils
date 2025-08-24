import json
from typing import Any, Optional, Type

def safe_json_dump(obj: Any, default: Optional[Any] = None, encoder: Optional[Type[json.JSONEncoder]] = None, **kwargs) -> str:
    """
    Safely dump an object to a JSON string, returning a default value on error.
    
    Args:
        obj: The object to serialize.
        default: Value to return if serialization fails (default: None).
        encoder: Optional custom JSONEncoder class.
        **kwargs: Additional arguments for json.dumps.
    Returns:
        The JSON string, or default if serialization fails.
    """
    try:
        return json.dumps(obj, cls=encoder, **kwargs) if encoder else json.dumps(obj, **kwargs)
    except (TypeError, ValueError):
        return default
