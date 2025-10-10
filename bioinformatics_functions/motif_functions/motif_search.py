

def motif_search(seq: str, motif: str) -> list[int]:
    """
    Find all positions of a motif (pattern) in a sequence, supporting ambiguous bases.

    Parameters
    ----------
    seq : str
        Input sequence.
    motif : str
        Motif/pattern to search for (may contain IUPAC codes).

    Returns
    -------
    List[int]
        List of start positions (0-based) where motif matches.

    Raises
    ------
    TypeError
        If seq or motif is not a string.
    ValueError
        If motif is empty or contains invalid characters.

    Examples
    --------
    >>> motif_search('ATGCGTAG', 'N')
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> motif_search('ATGCGTAG', 'R')
    [0, 3, 6]
    """
    iupac = {
        "A": {"A"},
        "C": {"C"},
        "G": {"G"},
        "T": {"T"},
        "R": {"A", "G"},
        "Y": {"C", "T"},
        "S": {"G", "C"},
        "W": {"A", "T"},
        "K": {"G", "T"},
        "M": {"A", "C"},
        "B": {"C", "G", "T"},
        "D": {"A", "G", "T"},
        "H": {"A", "C", "T"},
        "V": {"A", "C", "G"},
        "N": {"A", "C", "G", "T"},
    }
    if not isinstance(seq, str) or not isinstance(motif, str):
        raise TypeError("seq and motif must be strings")
    seq = seq.upper()
    motif = motif.upper()
    if not motif:
        raise ValueError("motif must not be empty")
    if not all(base in iupac for base in motif):
        raise ValueError("motif contains invalid IUPAC codes")
    positions = []
    for i in range(len(seq) - len(motif) + 1):
        if all(seq[i + j] in iupac[motif[j]] for j in range(len(motif))):
            positions.append(i)
    return positions


__all__ = ["motif_search"]
