"""Calculate Hamming distance between sequences."""


def hamming_distance(seq1: str, seq2: str) -> int:
    """
    Calculate Hamming distance between two sequences (number of differing positions).

    Parameters
    ----------
    seq1 : str
        First sequence.
    seq2 : str
        Second sequence.

    Returns
    -------
    int
        Number of positions at which sequences differ.

    Raises
    ------
    TypeError
        If seq1 or seq2 is not a string.
    ValueError
        If sequences are not the same length.

    Examples
    --------
    >>> hamming_distance('ATGC', 'ATGC')
    0
    >>> hamming_distance('ATGC', 'ATGT')
    1
    >>> hamming_distance('ATGC', 'GCTA')
    4

    Notes
    -----
    Used for measuring sequence similarity and mutation analysis.

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(seq1, str):
        raise TypeError(f"seq1 must be str, got {type(seq1).__name__}")
    if not isinstance(seq2, str):
        raise TypeError(f"seq2 must be str, got {type(seq2).__name__}")

    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be the same length")

    return sum(a != b for a, b in zip(seq1, seq2, strict=False))


__all__ = ["hamming_distance"]
