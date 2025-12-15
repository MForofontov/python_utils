"""
Register custom CSV dialect.
"""

import csv
from typing import Any


def register_csv_dialect(
    name: str,
    delimiter: str = ",",
    quotechar: str = '"',
    doublequote: bool = True,
    skipinitialspace: bool = False,
    lineterminator: str = "\r\n",
    quoting: int = csv.QUOTE_MINIMAL,
) -> None:
    """
    Register a custom CSV dialect for reuse.

    Parameters
    ----------
    name : str
        Name for the dialect.
    delimiter : str, optional
        Field delimiter (by default ",").
    quotechar : str, optional
        Quote character (by default '"').
    doublequote : bool, optional
        Whether to double quote chars (by default True).
    skipinitialspace : bool, optional
        Skip whitespace after delimiter (by default False).
    lineterminator : str, optional
        Line terminator (by default "\\r\\n").
    quoting : int, optional
        Quoting style (by default csv.QUOTE_MINIMAL).

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If delimiter or quotechar is not single character.

    Examples
    --------
    >>> register_csv_dialect('pipe', delimiter='|')
    >>> # Now use 'pipe' dialect in csv.reader/writer

    >>> register_csv_dialect('tab', delimiter='\\t', quoting=csv.QUOTE_NONE)

    Notes
    -----
    Once registered, dialect can be used by name in csv operations.
    See csv.QUOTE_* constants for quoting options.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a string, got {type(name).__name__}")
    
    if not isinstance(delimiter, str):
        raise TypeError(f"delimiter must be a string, got {type(delimiter).__name__}")
    
    if not isinstance(quotechar, str):
        raise TypeError(f"quotechar must be a string, got {type(quotechar).__name__}")
    
    if not isinstance(doublequote, bool):
        raise TypeError(f"doublequote must be a boolean, got {type(doublequote).__name__}")
    
    if not isinstance(skipinitialspace, bool):
        raise TypeError(f"skipinitialspace must be a boolean, got {type(skipinitialspace).__name__}")
    
    if not isinstance(lineterminator, str):
        raise TypeError(f"lineterminator must be a string, got {type(lineterminator).__name__}")
    
    if not isinstance(quoting, int):
        raise TypeError(f"quoting must be an integer, got {type(quoting).__name__}")
    
    if len(delimiter) != 1:
        raise ValueError(f"delimiter must be a single character, got '{delimiter}'")
    
    if len(quotechar) != 1:
        raise ValueError(f"quotechar must be a single character, got '{quotechar}'")
    
    csv.register_dialect(
        name,
        delimiter=delimiter,
        quotechar=quotechar,
        doublequote=doublequote,
        skipinitialspace=skipinitialspace,
        lineterminator=lineterminator,
        quoting=quoting,
    )


__all__ = ['register_csv_dialect']
