def dinucleotide_frequency(seq: str) -> dict[str, int]:
    """
    Calculate the frequency of each dinucleotide in a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence to analyze.

    Returns
    -------
    dict[str, int]
        Dictionary with dinucleotides as keys and their counts as values.
        All possible dinucleotides (AA, AT, AG, AC, TA, TT, TG, TC, etc.)
        are included with count 0 if not present.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid DNA bases (not A, T, G, C, case-insensitive).
        If seq is too short (less than 2 bases).

    Examples
    --------
    >>> dinucleotide_frequency("ATGC")
    {'AT': 1, 'TG': 1, 'GC': 1, 'AA': 0, 'AC': 0, ...}
    >>> dinucleotide_frequency("AAAA")['AA']
    3
    >>> dinucleotide_frequency("ATATATAT")['AT']
    4

    Notes
    -----
    Case-insensitive - converts all input to uppercase before counting.
    Uses sliding window of size 2 to count overlapping dinucleotides.

    Complexity
    ----------
    Time: O(n), Space: O(1) where n is sequence length
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")

    if len(seq) < 2:
        raise ValueError(f"Sequence must be at least 2 bases long, got {len(seq)}")

    # Convert to uppercase for consistency
    seq_upper = seq.upper()

    # Validate that all characters are valid DNA bases
    valid_bases = set("ATGC")
    seq_bases = set(seq_upper)
    invalid_bases = seq_bases - valid_bases
    if invalid_bases:
        raise ValueError(f"Invalid DNA bases found: {', '.join(sorted(invalid_bases))}")

    # Initialize frequency dictionary with all possible dinucleotides
    bases = ["A", "T", "G", "C"]
    frequency = {f"{b1}{b2}": 0 for b1 in bases for b2 in bases}

    # Count dinucleotides using sliding window
    for i in range(len(seq_upper) - 1):
        dinuc = seq_upper[i : i + 2]
        frequency[dinuc] += 1

    return frequency


__all__ = ["dinucleotide_frequency"]
