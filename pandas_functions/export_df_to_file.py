from os import PathLike, fspath
from typing import Any

import pandas as pd


def export_df_to_file(
    df: pd.DataFrame,
    file_path: str | PathLike[str],
    sep: str = ",",
    index: bool = False,
    **kwargs: Any,
) -> None:
    """Export a pandas DataFrame to a delimited text file.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to export.
    file_path : str | PathLike[str]
        Destination file path.
    sep : str, optional
        Field delimiter to use, by default ",".
    index : bool, optional
        Write row names (index), by default ``False``.
    **kwargs : Any
        Additional keyword arguments passed to :func:`pandas.DataFrame.to_csv`.

    Raises
    ------
    OSError
        If the file cannot be written.
    """
    try:
        df.to_csv(file_path, sep=sep, index=index, **kwargs)
    except OSError as exc:
        raise OSError(
            f"Could not write DataFrame to file: {fspath(file_path)}"
        ) from exc


__all__ = ["export_df_to_file"]
