"""Calculate percentage identity between two sequences."""


def pairwise_identity(seq1: str, seq2: str, aligned: bool = False) -> float:
    """
    Calculate the percentage identity between two sequences.

    Parameters
    ----------
    seq1 : str
        First sequence.
    seq2 : str
        Second sequence.
    aligned : bool, optional
        If True, treats sequences as pre-aligned (may contain gaps '-').
        If False, assumes unaligned sequences of equal length (by default False).

    Returns
    -------
    float
        Percentage identity (0.0 to 100.0).

    Raises
    ------
    TypeError
        If seq1 or seq2 is not a string.
        If aligned is not a boolean.
    ValueError
        If sequences have different lengths (when aligned=False).
        If either sequence is empty.

    Examples
    --------
    >>> pairwise_identity("ACGT", "ACGT")
    100.0
    >>> pairwise_identity("ACGT", "ACCT")
    75.0
    >>> pairwise_identity("ACGT", "TTTT")
    25.0
    >>> pairwise_identity("AC-GT", "ACGGT", aligned=True)
    80.0
    >>> pairwise_identity("A-CGT", "ATCGT", aligned=True)
    80.0

    Notes
    -----
    When aligned=True:
    - Gaps ('-') in either sequence are not counted in the comparison
    - Only positions where both sequences have non-gap characters are compared

    When aligned=False:
    - Sequences must be of equal length
    - Simple character-by-character comparison

    Complexity
    ----------
    Time: O(n), Space: O(1) where n is sequence length
    """
    # Input validation
    if not isinstance(seq1, str):
        raise TypeError(f"seq1 must be a string, got {type(seq1).__name__}")
    if not isinstance(seq2, str):
        raise TypeError(f"seq2 must be a string, got {type(seq2).__name__}")
    if not isinstance(aligned, bool):
        raise TypeError(f"aligned must be a boolean, got {type(aligned).__name__}")

    if len(seq1) == 0:
        raise ValueError("seq1 cannot be empty")
    if len(seq2) == 0:
        raise ValueError("seq2 cannot be empty")

    if not aligned and len(seq1) != len(seq2):
        raise ValueError(
            f"Sequences must have equal length when aligned=False, got {len(seq1)} and {len(seq2)}"
        )

    if aligned:
        # For aligned sequences, count only non-gap positions
        if len(seq1) != len(seq2):
            raise ValueError(
                f"Aligned sequences must have equal length, got {len(seq1)} and {len(seq2)}"
            )

        matches = 0
        compared_positions = 0

        for i in range(len(seq1)):
            # Skip positions where either sequence has a gap
            if seq1[i] != "-" and seq2[i] != "-":
                compared_positions += 1
                if seq1[i] == seq2[i]:
                    matches += 1

        if compared_positions == 0:
            return 0.0

        identity = (matches / compared_positions) * 100.0
    else:
        # For unaligned sequences, simple character comparison
        matches = sum(1 for i in range(len(seq1)) if seq1[i] == seq2[i])
        identity = (matches / len(seq1)) * 100.0

    return round(identity, 2)


__all__ = ["pairwise_identity"]
