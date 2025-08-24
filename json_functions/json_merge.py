from typing import Any
import copy

def json_merge(a: Any, b: Any, deep: bool = True) -> Any:
    """
    Merge two JSON-serializable objects (dicts/lists/primitives).
    If both are dicts, merge keys (b overrides a). If both are lists, concatenate.
    If deep is True, merge recursively for nested dicts/lists.
    Otherwise, return b if types differ or b is not None.
    """
    if isinstance(a, dict) and isinstance(b, dict):
        result = copy.deepcopy(a)
        for k, v in b.items():
            if k in result and deep:
                result[k] = json_merge(result[k], v, deep=deep)
            else:
                result[k] = copy.deepcopy(v)
        return result
    elif isinstance(a, list) and isinstance(b, list):
        return copy.deepcopy(a) + copy.deepcopy(b)
    else:
        return copy.deepcopy(b) if b is not None else copy.deepcopy(a)
