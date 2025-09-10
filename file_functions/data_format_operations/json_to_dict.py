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
    dict[str, Any]
        Dictionary representation of the JSON contents.

    Raises
    ------
    FileNotFoundError
        If ``file_path`` does not exist.
    json.JSONDecodeError
        If the file does not contain valid JSON.

    Examples
    --------
    >>> json_to_dict('example.json')  # doctest: +SKIP
    {'key': 'value'}
    """
    with open(file_path) as f:
        data: dict[str, Any] = json.load(f)

    return data


__all__ = ["json_to_dict"]
