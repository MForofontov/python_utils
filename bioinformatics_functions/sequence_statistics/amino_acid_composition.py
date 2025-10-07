from typing import Dict

def amino_acid_composition(seq: str) -> Dict[str, float]:
    """
    Calculate amino acid composition (percentage of each amino acid).

    Parameters
    ----------
    seq : str
        Protein sequence (single-letter amino acid codes).

    Returns
    -------
    Dict[str, float]
        Dictionary mapping each amino acid to its percentage (0-100).

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid amino acid codes or is empty.

    Examples
    --------
    >>> amino_acid_composition('ACDEFGH')
    {'A': 14.29, 'C': 14.29, 'D': 14.29, 'E': 14.29, 'F': 14.29, 'G': 14.29, 'H': 14.29}

    Notes
    -----
    Useful for protein characterization and structure prediction.

    Complexity
    ----------
    Time: O(n), Space: O(k) where k is number of unique amino acids
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    
    seq = seq.upper()
    
    valid_amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    
    if not seq:
        raise ValueError("Sequence cannot be empty")
    
    if not all(aa in valid_amino_acids for aa in seq):
        raise ValueError("Sequence contains invalid amino acid codes")
    
    aa_counts: Dict[str, int] = {}
    total = len(seq)
    
    for aa in seq:
        aa_counts[aa] = aa_counts.get(aa, 0) + 1
    
    return {aa: round((count / total) * 100, 2) for aa, count in aa_counts.items()}

__all__ = ["amino_acid_composition"]
