import json
from typing import Any


def json_to_dict(file_path: str) -> dict[str, Any]:
    """
    Read a JSON file and return its contents as a dictionary.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Returns
    -------
    Dict[str, Any]
        Dictionary representation of the JSON contents.
    """
    with open(file_path) as f:
        data: dict[str, Any] = json.load(f)

    return data


__all__ = ["json_to_dict"]
