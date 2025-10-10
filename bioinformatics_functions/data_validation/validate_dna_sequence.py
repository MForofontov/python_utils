from typing import Any


def validate_dna_sequence(seq: str, allow_ambiguous: bool = False) -> dict[str, Any]:
    """
    Validate a DNA sequence and return detailed validation report.

    Parameters
    ----------
    seq : str
        DNA sequence to validate.
    allow_ambiguous : bool, optional
        If True, allows IUPAC ambiguous nucleotide codes (by default False).

    Returns
    -------
    dict[str, Any]
        Validation report containing:
        - 'is_valid': bool, whether sequence is valid
        - 'length': int, sequence length
        - 'invalid_chars': list[str], list of invalid characters found
        - 'has_lowercase': bool, whether sequence contains lowercase
        - 'gc_content': float, GC content percentage

    Raises
    ------
    TypeError
        If seq is not a string.
        If allow_ambiguous is not a boolean.

    Examples
    --------
    >>> validate_dna_sequence("ATGC")
    {'is_valid': True, 'length': 4, 'invalid_chars': [], 'has_lowercase': False, 'gc_content': 50.0}
    >>> validate_dna_sequence("ATGCX")
    {'is_valid': False, 'length': 5, 'invalid_chars': ['X'], 'has_lowercase': False, 'gc_content': 40.0}
    >>> validate_dna_sequence("atgc")
    {'is_valid': True, 'length': 4, 'invalid_chars': [], 'has_lowercase': True, 'gc_content': 50.0}
    >>> validate_dna_sequence("ATGCN", allow_ambiguous=True)
    {'is_valid': True, 'length': 5, 'invalid_chars': [], 'has_lowercase': False, 'gc_content': 40.0}

    Notes
    -----
    Standard DNA bases: A, T, G, C
    IUPAC ambiguous codes: R, Y, S, W, K, M, B, D, H, V, N

    Complexity
    ----------
    Time: O(n), Space: O(k) where n is sequence length, k is unique invalid chars
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")
    if not isinstance(allow_ambiguous, bool):
        raise TypeError(
            f"allow_ambiguous must be a boolean, got {type(allow_ambiguous).__name__}"
        )

    # Define valid bases
    valid_bases = set("ATGC")
    if allow_ambiguous:
        # IUPAC ambiguous nucleotide codes
        valid_bases.update("RYSWKMBDHVN")

    # Check for lowercase
    has_lowercase = seq != seq.upper()

    # Convert to uppercase for validation
    seq_upper = seq.upper()

    # Find invalid characters
    seq_bases = set(seq_upper)
    invalid_chars = sorted(seq_bases - valid_bases)

    # Determine if valid
    is_valid = len(invalid_chars) == 0

    # Calculate GC content (only count standard bases)
    gc_count = sum(1 for base in seq_upper if base in "GC")
    total_standard = sum(1 for base in seq_upper if base in "ATGC")
    gc_content = (gc_count / total_standard * 100.0) if total_standard > 0 else 0.0

    # Build report
    report: dict[str, Any] = {
        "is_valid": is_valid,
        "length": len(seq),
        "invalid_chars": invalid_chars,
        "has_lowercase": has_lowercase,
        "gc_content": round(gc_content, 2),
    }

    return report


__all__ = ["validate_dna_sequence"]
