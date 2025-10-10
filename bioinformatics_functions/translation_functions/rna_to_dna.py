def rna_to_dna(seq: str) -> str:
    """
    Convert RNA sequence to DNA sequence (U → T).

    Parameters
    ----------
    seq : str
        RNA sequence to convert.

    Returns
    -------
    str
        DNA sequence with all U bases converted to T.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid RNA bases (not A, U, G, C, case-insensitive).

    Examples
    --------
    >>> rna_to_dna("AUGC")
    'ATGC'
    >>> rna_to_dna("UUUUAAAA")
    'TTTTAAAA'
    >>> rna_to_dna("augc")
    'ATGC'

    Notes
    -----
    Case-insensitive input - returns uppercase output.
    Validates that input contains only valid RNA bases (A, U, G, C).

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is sequence length
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")

    # Convert to uppercase for consistency
    seq_upper = seq.upper()

    # Validate that all characters are valid RNA bases
    valid_bases = set("AUGC")
    seq_bases = set(seq_upper)
    invalid_bases = seq_bases - valid_bases
    if invalid_bases:
        raise ValueError(f"Invalid RNA bases found: {', '.join(sorted(invalid_bases))}")

    # Convert U to T
    dna_seq = seq_upper.replace("U", "T")

    return dna_seq


__all__ = ["rna_to_dna"]
