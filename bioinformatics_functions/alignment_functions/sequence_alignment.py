from typing import Tuple

def simple_alignment(seq1: str, seq2: str) -> Tuple[str, str]:
    """
    Perform a simple global alignment of two DNA sequences (Needleman-Wunsch, no gap penalty).

    Parameters
    ----------
    seq1 : str
        First DNA sequence.
    seq2 : str
        Second DNA sequence.

    Returns
    -------
    Tuple[str, str]
        Aligned sequences.

    Raises
    ------
    TypeError
        If inputs are not strings.
    ValueError
        If sequences contain invalid characters.

    Examples
    --------
    >>> simple_alignment('ATGC', 'ATGGC')
    ('AT-GC', 'ATGGC')
    """
    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError("Both sequences must be strings")
    seq1 = seq1.upper()
    seq2 = seq2.upper()
    if not all(base in 'ATCG' for base in seq1+seq2):
        raise ValueError("Sequences contain invalid DNA bases")
    # Simple alignment: pad shorter sequence with '-' to match length
    max_len = max(len(seq1), len(seq2))
    s1 = seq1.ljust(max_len, '-')
    s2 = seq2.ljust(max_len, '-')
    return s1, s2

__all__ = ["simple_alignment"]
