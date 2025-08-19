from os import PathLike, fspath
from typing import Any

import pandas as pd


def import_df_from_file(
    file_path: str | PathLike[str], sep: str = ",", **kwargs: Any
) -> pd.DataFrame:
    """Using pandas, import a file path as a dataframe.

    Parameters
    ----------
    file_path : str | PathLike[str]
        Path to the file.
    sep : str, optional
        String to separate entries in the file, by default ",".
    **kwargs : Any
        Additional keyword arguments passed to :func:`pandas.read_csv`.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe that contains the file values separated by ``sep``.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be parsed.
    """
    try:
        return pd.read_csv(file_path, sep=sep, **kwargs)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {fspath(file_path)}") from exc
    except (pd.errors.ParserError, pd.errors.EmptyDataError, ValueError) as exc:
        raise ValueError(f"Could not parse file: {fspath(file_path)}") from exc

__all__ = ['import_df_from_file']
