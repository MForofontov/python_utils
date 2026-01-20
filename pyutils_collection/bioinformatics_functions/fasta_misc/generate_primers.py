"""Generate PCR primers from DNA sequences."""


def generate_primers(
    seq: str, length: int = 20, gc_min: float = 0.4, gc_max: float = 0.6
) -> list[str]:
    """
    Generate potential PCR primers from a DNA sequence based on GC content.

    Parameters
    ----------
    seq : str
        DNA sequence (A, T, C, G).
    length : int, optional
        Primer length (default: 20).
    gc_min : float, optional
        Minimum GC content (default: 0.4).
    gc_max : float, optional
        Maximum GC content (default: 0.6).

    Returns
    -------
    List[str]
        List of potential primer sequences.

    Raises
    ------
    TypeError
        If seq is not a string or parameters have wrong types.
    ValueError
        If seq contains invalid characters or parameters are invalid.

    Examples
    --------
    >>> generate_primers('ATGCATGCATGCATGCATGC', length=10, gc_min=0.4, gc_max=0.6)
    ['ATGCATGCAT', 'TGCATGCATG', ...]

    Notes
    -----
    Filters primers based on GC content to ensure good PCR performance.

    Complexity
    ----------
    Time: O(n*m), Space: O(k) where k is number of valid primers
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    if not isinstance(length, int):
        raise TypeError(f"length must be int, got {type(length).__name__}")
    if not isinstance(gc_min, (int, float)):
        raise TypeError(f"gc_min must be a number, got {type(gc_min).__name__}")
    if not isinstance(gc_max, (int, float)):
        raise TypeError(f"gc_max must be a number, got {type(gc_max).__name__}")

    seq = seq.upper()
    if not all(base in "ATCG" for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")

    if length <= 0 or length > len(seq):
        raise ValueError("length must be positive and <= sequence length")
    if not 0 <= gc_min <= 1:
        raise ValueError("gc_min must be between 0 and 1")
    if not 0 <= gc_max <= 1:
        raise ValueError("gc_max must be between 0 and 1")
    if gc_min > gc_max:
        raise ValueError("gc_min cannot be greater than gc_max")

    primers: list[str] = []

    for i in range(len(seq) - length + 1):
        primer = seq[i : i + length]

        # Calculate GC content
        gc_count = primer.count("G") + primer.count("C")
        gc_content = gc_count / length

        # Check GC content range
        if gc_min <= gc_content <= gc_max:
            # Additional check: avoid primers ending in G or C runs
            if not (primer.endswith("GGG") or primer.endswith("CCC")):
                primers.append(primer)

    return primers


__all__ = ["generate_primers"]
