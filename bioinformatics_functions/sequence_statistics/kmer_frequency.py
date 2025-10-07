from typing import Dict

def kmer_frequency(seq: str, k: int) -> Dict[str, int]:
    """
    Calculate k-mer frequency distribution in a sequence.

    Parameters
    ----------
    seq : str
        Input sequence.
    k : int
        Length of k-mer.

    Returns
    -------
    Dict[str, int]
        Dictionary mapping each k-mer to its count.

    Raises
    ------
    TypeError
        If seq is not a string or k is not an integer.
    ValueError
        If k is not positive or longer than sequence.

    Examples
    --------
    >>> kmer_frequency('ATGCATGC', 3)
    {'ATG': 2, 'TGC': 2, 'GCA': 1, 'CAT': 1}
    >>> kmer_frequency('AAAA', 2)
    {'AA': 3}

    Notes
    -----
    Useful for sequence composition analysis and motif discovery.

    Complexity
    ----------
    Time: O(n*k), Space: O(m) where m is number of unique k-mers
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    if not isinstance(k, int):
        raise TypeError(f"k must be int, got {type(k).__name__}")
    if k <= 0:
        raise ValueError("k must be positive")
    if k > len(seq):
        raise ValueError("k cannot be longer than sequence")
    
    kmer_counts: Dict[str, int] = {}
    
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1
    
    return kmer_counts

__all__ = ["kmer_frequency"]
