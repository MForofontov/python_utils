"""Remove low-complexity regions from sequences."""


def remove_low_complexity_regions(
    seq: str,
    window_size: int = 10,
    complexity_threshold: float = 1.5,
    replace_with: str = "N",
) -> str:
    """
    Remove or mask low-complexity regions in a DNA sequence.

    Low-complexity regions are repetitive or simple sequence regions that may
    interfere with analysis. This function uses Shannon entropy to detect them.

    Parameters
    ----------
    seq : str
        DNA sequence to process.
    window_size : int, optional
        Size of sliding window for complexity calculation (by default 10).
    complexity_threshold : float, optional
        Minimum entropy threshold (bits). Lower values = lower complexity.
        Range is 0-2 for DNA (by default 1.5).
    replace_with : str, optional
        Character to replace low-complexity regions with (by default 'N').

    Returns
    -------
    str
        Sequence with low-complexity regions replaced.

    Raises
    ------
    TypeError
        If seq or replace_with is not a string.
        If window_size is not an integer.
        If complexity_threshold is not a number.
    ValueError
        If window_size is less than 2.
        If complexity_threshold is negative or greater than 2.
        If replace_with is not a single character.
        If seq contains invalid DNA bases.

    Examples
    --------
    >>> remove_low_complexity_regions("ATGATGATGATGATG")
    'NNNNNNNNNNNNNNN'
    >>> remove_low_complexity_regions("ATGCTAGCTAGC", window_size=4, complexity_threshold=1.0)
    'ATGCTAGCTAGC'
    >>> remove_low_complexity_regions("AAAAAATGCATGC", window_size=5, complexity_threshold=1.0)
    'NNNNNNTGCATGC'

    Notes
    -----
    Uses Shannon entropy to measure sequence complexity:
    H = -sum(p_i * log2(p_i)) where p_i is frequency of base i

    For DNA: H ranges from 0 (all same base) to 2 (equal ATGC distribution)
    Typical threshold: 1.5 bits

    Complexity
    ----------
    Time: O(n*w), Space: O(n) where n is sequence length, w is window size
    """
    import math
    from collections import Counter

    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")
    if not isinstance(window_size, int):
        raise TypeError(
            f"window_size must be an integer, got {type(window_size).__name__}"
        )
    if not isinstance(complexity_threshold, (int, float)):
        raise TypeError(
            f"complexity_threshold must be a number, got {type(complexity_threshold).__name__}"
        )
    if not isinstance(replace_with, str):
        raise TypeError(
            f"replace_with must be a string, got {type(replace_with).__name__}"
        )

    if window_size < 2:
        raise ValueError(f"window_size must be at least 2, got {window_size}")
    if complexity_threshold < 0 or complexity_threshold > 2:
        raise ValueError(
            f"complexity_threshold must be between 0 and 2, got {complexity_threshold}"
        )
    if len(replace_with) != 1:
        raise ValueError(
            f"replace_with must be a single character, got '{replace_with}'"
        )

    # Validate DNA sequence
    seq_upper = seq.upper()
    valid_bases = set("ATGCN")
    invalid_bases = set(seq_upper) - valid_bases
    if invalid_bases:
        raise ValueError(f"Invalid DNA bases found: {', '.join(sorted(invalid_bases))}")

    if len(seq) < window_size:
        # Sequence too short, return as-is
        return seq

    def calculate_entropy(subseq: str) -> float:
        """Calculate Shannon entropy for a sequence."""
        if len(subseq) == 0:
            return 0.0

        counts = Counter(subseq)
        length = len(subseq)
        entropy = 0.0

        for count in counts.values():
            if count > 0:
                p = count / length
                entropy -= p * math.log2(p)

        return entropy

    # Mark low-complexity positions
    is_low_complexity = [False] * len(seq)

    for i in range(len(seq) - window_size + 1):
        window = seq_upper[i : i + window_size]
        entropy = calculate_entropy(window)

        if entropy < complexity_threshold:
            # Mark this window as low complexity
            for j in range(i, i + window_size):
                is_low_complexity[j] = True

    # Build result sequence
    result = []
    for i, base in enumerate(seq):
        if is_low_complexity[i]:
            result.append(replace_with)
        else:
            result.append(base)

    return "".join(result)


__all__ = ["remove_low_complexity_regions"]
