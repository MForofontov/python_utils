"""Reverse nucleotide or protein sequences."""


def reverse_sequence(seq: str) -> str:
    """
    Return the reverse of a nucleotide or protein sequence.

    Parameters
    ----------
    seq : str
        Input sequence.

    Returns
    -------
    str
        Reversed sequence.

    Raises
    ------
    TypeError
        If seq is not a string.

    Examples
    --------
    >>> reverse_sequence('ATGC')
    'CGTA'
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    return seq[::-1]


__all__ = ["reverse_sequence"]
