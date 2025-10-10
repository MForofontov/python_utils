

def codon_usage_frequency(seq: str) -> dict[str, float]:
    """
    Calculate codon usage frequency from a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence (A, T, C, G).

    Returns
    -------
    Dict[str, float]
        Dictionary mapping each codon to its frequency (0-1).

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters or length is not a multiple of 3.

    Examples
    --------
    >>> codon_usage_frequency('ATGATGATG')
    {'ATG': 1.0}
    >>> codon_usage_frequency('ATGATGAAA')
    {'ATG': 0.6666666666666666, 'AAA': 0.3333333333333333}

    Notes
    -----
    Useful for analyzing codon bias in genes.

    Complexity
    ----------
    Time: O(n/3), Space: O(k) where k is number of unique codons
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")

    seq = seq.upper()
    if not all(base in "ATCG" for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")

    if len(seq) % 3 != 0:
        raise ValueError("Sequence length must be a multiple of 3")

    codon_counts: dict[str, int] = {}
    total_codons = len(seq) // 3

    for i in range(0, len(seq), 3):
        codon = seq[i : i + 3]
        codon_counts[codon] = codon_counts.get(codon, 0) + 1

    return {codon: count / total_codons for codon, count in codon_counts.items()}


__all__ = ["codon_usage_frequency"]
