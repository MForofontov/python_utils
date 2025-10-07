def find_motif_positions(seq: str, motif: str, allow_overlap: bool = True) -> list[int]:
    """
    Find all positions of a motif in a sequence.

    Parameters
    ----------
    seq : str
        Sequence to search in.
    motif : str
        Motif pattern to find.
    allow_overlap : bool, optional
        If True, finds overlapping occurrences (by default True).
        If False, skips positions after a match.

    Returns
    -------
    list[int]
        List of 0-based positions where motif starts.

    Raises
    ------
    TypeError
        If seq or motif is not a string.
        If allow_overlap is not a boolean.
    ValueError
        If motif is empty or longer than sequence.

    Examples
    --------
    >>> find_motif_positions("ATGATGATG", "ATG")
    [0, 3, 6]
    >>> find_motif_positions("AAAAAAA", "AAA", allow_overlap=True)
    [0, 1, 2, 3, 4]
    >>> find_motif_positions("AAAAAAA", "AAA", allow_overlap=False)
    [0, 3]
    >>> find_motif_positions("ATGCATGC", "GC")
    [2, 6]

    Notes
    -----
    Case-sensitive search - convert both sequence and motif to same case if needed.
    Returns empty list if motif not found.
    
    Complexity
    ----------
    Time: O(n*m), Space: O(k) where n is sequence length, m is motif length, k is matches
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")
    if not isinstance(motif, str):
        raise TypeError(f"motif must be a string, got {type(motif).__name__}")
    if not isinstance(allow_overlap, bool):
        raise TypeError(f"allow_overlap must be a boolean, got {type(allow_overlap).__name__}")
    
    if len(motif) == 0:
        raise ValueError("Motif cannot be empty")
    if len(motif) > len(seq):
        raise ValueError(f"Motif length ({len(motif)}) cannot be greater than sequence length ({len(seq)})")
    
    positions = []
    start = 0
    
    while start <= len(seq) - len(motif):
        pos = seq.find(motif, start)
        if pos == -1:
            break
        positions.append(pos)
        
        if allow_overlap:
            start = pos + 1
        else:
            start = pos + len(motif)
    
    return positions


__all__ = ['find_motif_positions']
