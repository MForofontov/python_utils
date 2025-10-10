

def sequence_statistics(seq: str) -> dict[str, float]:
    """
    Calculate basic statistics for a nucleotide sequence: length, GC content, AT content.

    Parameters
    ----------
    seq : str
        Input sequence.

    Returns
    -------
    Dict[str, float]
        Dictionary with 'length', 'gc_content', 'at_content'.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters.

    Examples
    --------
    >>> sequence_statistics('ATGC')
    {'length': 4, 'gc_content': 50.0, 'at_content': 50.0}
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    seq = seq.upper()
    if not all(base in "ATCG" for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")
    length = len(seq)
    gc = seq.count("G") + seq.count("C")
    at = seq.count("A") + seq.count("T")
    gc_content = (gc / length) * 100 if length else 0.0
    at_content = (at / length) * 100 if length else 0.0
    return {"length": float(length), "gc_content": gc_content, "at_content": at_content}


__all__ = ["sequence_statistics"]
