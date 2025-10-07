def nucleotide_frequency(seq: str) -> dict[str, int]:
    """
    Calculate the frequency of each nucleotide in a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence to analyze.

    Returns
    -------
    dict[str, int]
        Dictionary with nucleotide bases as keys and their counts as values.
        Keys are 'A', 'T', 'G', 'C' in uppercase.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid DNA bases (not A, T, G, C, case-insensitive).

    Examples
    --------
    >>> nucleotide_frequency("ATGC")
    {'A': 1, 'T': 1, 'G': 1, 'C': 1}
    >>> nucleotide_frequency("AAATTTGGGCCC")
    {'A': 3, 'T': 3, 'G': 3, 'C': 3}
    >>> nucleotide_frequency("atgc")
    {'A': 1, 'T': 1, 'G': 1, 'C': 1}

    Notes
    -----
    Case-insensitive - converts all input to uppercase before counting.
    Returns counts for all four bases (A, T, G, C) even if count is 0.

    Complexity
    ----------
    Time: O(n), Space: O(1) where n is sequence length
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")
    
    # Convert to uppercase for consistency
    seq_upper = seq.upper()
    
    # Validate that all characters are valid DNA bases
    valid_bases = set('ATGC')
    seq_bases = set(seq_upper)
    invalid_bases = seq_bases - valid_bases
    if invalid_bases:
        raise ValueError(f"Invalid DNA bases found: {', '.join(sorted(invalid_bases))}")
    
    # Initialize frequency dictionary with all bases
    frequency = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    
    # Count each nucleotide
    for base in seq_upper:
        frequency[base] += 1
    
    return frequency


__all__ = ['nucleotide_frequency']
