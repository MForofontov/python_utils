from typing import List

def degenerate_primer_generator(seq: str) -> List[str]:
    """
    Generate all possible degenerate primers for a DNA sequence containing ambiguous bases.

    Parameters
    ----------
    seq : str
        DNA sequence (may contain IUPAC ambiguity codes).

    Returns
    -------
    List[str]
        All possible primer sequences (no ambiguity codes).

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters.

    Examples
    --------
    >>> degenerate_primer_generator('ATGR')
    ['ATGA', 'ATGG']
    """
    iupac = {
        'A': ['A'], 'C': ['C'], 'G': ['G'], 'T': ['T'],
        'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'],
        'K': ['G', 'T'], 'M': ['A', 'C'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'],
        'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'], 'N': ['A', 'C', 'G', 'T']
    }
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    seq = seq.upper()
    if not all(base in iupac for base in seq):
        raise ValueError("Sequence contains invalid DNA/IUPAC bases")
    primers = ['']
    for base in seq:
        primers = [p + b for p in primers for b in iupac[base]]
    return primers

__all__ = ["degenerate_primer_generator"]
