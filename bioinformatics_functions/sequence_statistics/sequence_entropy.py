import math


def sequence_entropy(seq: str) -> float:
    """
    Calculate the Shannon entropy of a nucleotide or protein sequence.

    Parameters
    ----------
    seq : str
        Input sequence.

    Returns
    -------
    float
        Shannon entropy value.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq is empty.

    Examples
    --------
    >>> sequence_entropy('AAAA')
    0.0
    >>> sequence_entropy('ATGC')
    2.0
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    if not seq:
        raise ValueError("Sequence must not be empty")
    freq = {}
    for base in seq:
        freq[base] = freq.get(base, 0) + 1
    entropy = 0.0
    for count in freq.values():
        p = count / len(seq)
        entropy -= p * math.log2(p)
    return entropy


__all__ = ["sequence_entropy"]
