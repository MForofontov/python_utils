import json
from typing import Any


def write_dict_to_json(
    file_path: str, data: dict[str, Any], indent: int | None = None
) -> None:
    """
    Write a dictionary to a JSON file.

    Parameters
    ----------
    file_path : str
        Path to the JSON file to write.
    data : Dict[str, Any]
        Dictionary to serialize and write to the file.
    indent : Optional[int]
        Number of spaces to use for indentation in the output file (default is None).

    Returns
    -------
    None
    """
    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent)


__all__ = ["write_dict_to_json"]
