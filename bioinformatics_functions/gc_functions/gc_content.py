def gc_content(seq: str) -> float:
    """
    Calculate GC content percentage of a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence.

    Returns
    -------
    float
        GC content as a percentage (0-100).

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters.

    Examples
    --------
    >>> gc_content('ATGC')
    50.0
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    seq = seq.upper()
    if not all(base in "ATCG" for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")
    gc = seq.count("G") + seq.count("C")
    return (gc / len(seq)) * 100 if seq else 0.0


__all__ = ["gc_content"]
