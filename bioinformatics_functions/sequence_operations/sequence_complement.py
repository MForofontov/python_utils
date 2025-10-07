def sequence_complement(seq: str) -> str:
    """
    Return the DNA complement of a sequence (without reversing).

    Converts each base to its complement: A↔T, G↔C.
    This is different from reverse_complement which also reverses the sequence.

    Parameters
    ----------
    seq : str
        DNA sequence to complement.

    Returns
    -------
    str
        Complemented DNA sequence (same direction as input).

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid DNA bases (not A, T, G, C, case-insensitive).

    Examples
    --------
    >>> sequence_complement("ATGC")
    'TACG'
    >>> sequence_complement("AAAA")
    'TTTT'
    >>> sequence_complement("atgc")
    'TACG'

    Notes
    -----
    Case-insensitive input - returns uppercase output.
    For reverse complement, use the reverse_complement function.
    
    Complexity
    ----------
    Time: O(n), Space: O(n) where n is sequence length
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
    
    # Complement mapping
    complement_map = {
        'A': 'T',
        'T': 'A',
        'G': 'C',
        'C': 'G'
    }
    
    # Build complement sequence
    complement = ''.join(complement_map[base] for base in seq_upper)
    
    return complement


__all__ = ['sequence_complement']
