"""Generate reverse complement of DNA sequences."""


def reverse_complement(seq: str) -> str:
    """
    Return the reverse complement of a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence (A, T, C, G).

    Returns
    -------
    str
        Reverse complement sequence.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters.

    Examples
    --------
    >>> reverse_complement('ATGC')
    'GCAT'
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    if not all(base in "ATCG" for base in seq.upper()):
        raise ValueError("Sequence contains invalid DNA bases")
    complement = str.maketrans("ATCGatcg", "TAGCtagc")
    return seq.translate(complement)[::-1]


__all__ = ["reverse_complement"]
