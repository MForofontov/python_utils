from typing import List

def sequence_gc_profile(seq: str, window: int) -> List[float]:
    """
    Calculate GC content profile in sliding windows across a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence.
    window : int
        Window size for GC calculation.

    Returns
    -------
    List[float]
        List of GC content percentages for each window.

    Raises
    ------
    TypeError
        If seq is not a string or window is not an integer.
    ValueError
        If window is not positive or longer than sequence.

    Examples
    --------
    >>> sequence_gc_profile('ATGCGCGT', 4)
    [50.0, 75.0, 75.0, 50.0, 50.0]
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    if not isinstance(window, int):
        raise TypeError(f"window must be int, got {type(window).__name__}")
    if window <= 0:
        raise ValueError("window must be positive")
    if window > len(seq):
        raise ValueError("window cannot be longer than sequence")
    seq = seq.upper()
    if not all(base in 'ATCG' for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")
    gc_profile = []
    for i in range(len(seq) - window + 1):
        window_seq = seq[i:i+window]
        gc = window_seq.count('G') + window_seq.count('C')
        gc_content = (gc / window) * 100 if window else 0.0
        gc_profile.append(gc_content)
    return gc_profile

__all__ = ["sequence_gc_profile"]
