from typing import Any, Dict, List, Tuple

def json_diff(a: Any, b: Any, path: str = "") -> List[Tuple[str, Any, Any]]:
    """
    Compute the difference between two JSON-serializable objects.
    Returns a list of (path, a_value, b_value) for changed/added/removed fields.
    """
    diffs = []
    if type(a) != type(b):
        diffs.append((path, a, b))
        return diffs
    if isinstance(a, dict):
        a_keys = set(a.keys())
        b_keys = set(b.keys())
        for k in a_keys | b_keys:
            new_path = f"{path}.{k}" if path else k
            if k in a and k in b:
                diffs.extend(json_diff(a[k], b[k], new_path))
            elif k in a:
                diffs.append((new_path, a[k], None))
            else:
                diffs.append((new_path, None, b[k]))
    elif isinstance(a, list):
        for i, (ai, bi) in enumerate(zip(a, b)):
            new_path = f"{path}[{i}]"
            diffs.extend(json_diff(ai, bi, new_path))
        if len(a) > len(b):
            for i in range(len(b), len(a)):
                diffs.append((f"{path}[{i}]", a[i], None))
        elif len(b) > len(a):
            for i in range(len(a), len(b)):
                diffs.append((f"{path}[{i}]", None, b[i]))
    else:
        if a != b:
            diffs.append((path, a, b))
    return diffs
