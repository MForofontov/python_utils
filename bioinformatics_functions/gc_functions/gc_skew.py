def gc_skew(seq: str) -> float:
    """
    Calculate the GC skew of a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence.

    Returns
    -------
    float
        GC skew: (G - C) / (G + C)

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters or has no G/C bases.

    Examples
    --------
    >>> gc_skew('GGCC')
    0.0
    >>> gc_skew('GGGCCC')
    0.0
    >>> gc_skew('GGGCC')
    0.2
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    seq = seq.upper()
    if not all(base in 'ATCG' for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")
    g = seq.count('G')
    c = seq.count('C')
    if g + c == 0:
        raise ValueError("No G or C bases in sequence")
    return (g - c) / (g + c)

__all__ = ["gc_skew"]
