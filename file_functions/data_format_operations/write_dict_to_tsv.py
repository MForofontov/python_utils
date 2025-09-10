from typing import Any
from itertools import zip_longest


def write_dict_to_tsv(file_path: str, data: dict[str, list[Any]]) -> None:
    """
    Write a dictionary to a TSV (Tab-Separated Values) file.

    Parameters
    ----------
    file_path : str
        The file path to save the TSV file.
    data : dict[str, list[Any]]
        The dictionary where keys are column names and values are lists of values for each column.

    Returns
    -------
    None
    """
    with open(file_path, "w") as f:
        f.write("\t".join(data.keys()) + "\n")
        for row in zip_longest(*data.values(), fillvalue=""):
            row_str: str = "\t".join(map(str, row))
            f.write(row_str + "\n")


__all__ = ['write_dict_to_tsv']
