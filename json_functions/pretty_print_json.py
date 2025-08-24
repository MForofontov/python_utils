import json
from typing import Any

def pretty_print_json(obj: Any, indent: int = 4, sort_keys: bool = True) -> str:
    """
    Return a pretty-printed JSON string from a Python object.
    
    Parameters
    ----------
    obj : Any
        The object to serialize.
    indent : int, optional
        Number of spaces for indentation (default: 4).
    sort_keys : bool, optional
        Whether to sort keys alphabetically (default: True).
        
    Returns
    -------
    str
        A pretty-printed JSON string.
        
    Examples
    --------
    >>> pretty_print_json({'b': 2, 'a': 1})
    '{\\n    "a": 1,\\n    "b": 2\\n}'
    """
    return json.dumps(obj, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
