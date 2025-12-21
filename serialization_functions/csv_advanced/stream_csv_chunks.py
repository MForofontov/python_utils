"""
Stream CSV file in chunks.
"""

import csv
from collections.abc import Iterator
from typing import Any


def stream_csv_chunks(
    input_path: str,
    chunk_size: int = 1000,
    encoding: str = "utf-8",
    use_dict: bool = True,
    **kwargs: Any,
) -> Iterator[list[dict[str, str]] | list[list[str]]]:
    """
    Stream CSV file in chunks to handle large files efficiently.

    Parameters
    ----------
    input_path : str
        Path to CSV file.
    chunk_size : int, optional
        Number of rows per chunk (by default 1000).
    encoding : str, optional
        File encoding (by default "utf-8").
    use_dict : bool, optional
        Return dicts if True, lists if False (by default True).
    **kwargs : Any
        Additional arguments for csv.DictReader or csv.reader.

    Yields
    ------
    list[dict[str, str]] | list[list[str]]
        Chunk of CSV rows as dicts or lists.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If chunk_size is non-positive.
    FileNotFoundError
        If input file doesn't exist.

    Examples
    --------
    >>> for chunk in stream_csv_chunks('large_file.csv', chunk_size=500):
    ...     process_chunk(chunk)

    >>> for chunk in stream_csv_chunks('data.csv', use_dict=False):
    ...     # chunk is list of lists
    ...     print(len(chunk))

    Notes
    -----
    Memory efficient for processing large CSV files.
    First row is treated as headers when use_dict=True.

    Complexity
    ----------
    Time: O(n), Space: O(chunk_size), where n is total rows
    """
    if not isinstance(input_path, str):
        raise TypeError(f"input_path must be a string, got {type(input_path).__name__}")
    
    if not isinstance(chunk_size, int):
        raise TypeError(f"chunk_size must be an integer, got {type(chunk_size).__name__}")
    
    if not isinstance(encoding, str):
        raise TypeError(f"encoding must be a string, got {type(encoding).__name__}")
    
    if not isinstance(use_dict, bool):
        raise TypeError(f"use_dict must be a boolean, got {type(use_dict).__name__}")
    
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")
    
    with open(input_path, 'r', encoding=encoding, newline='') as csvfile:
        reader: Any
        if use_dict:
            reader = csv.DictReader(csvfile, **kwargs)
        else:
            reader = csv.reader(csvfile, **kwargs)
        
        chunk: list[Any] = []
        for row in reader:
            chunk.append(row)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        
        # Yield remaining rows
        if chunk:
            yield chunk


__all__ = ['stream_csv_chunks']
