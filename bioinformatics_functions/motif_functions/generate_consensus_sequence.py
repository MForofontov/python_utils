from collections import Counter


def generate_consensus_sequence(sequences: list[str], threshold: float = 0.5) -> str:
    """
    Generate a consensus sequence from multiple aligned sequences.

    Parameters
    ----------
    sequences : list[str]
        List of aligned sequences (must all be same length).
    threshold : float, optional
        Minimum fraction of sequences that must have a base for it to be
        included in consensus (by default 0.5). Otherwise 'N' is used.

    Returns
    -------
    str
        Consensus sequence.

    Raises
    ------
    TypeError
        If sequences is not a list.
        If threshold is not a float or int.
    ValueError
        If sequences list is empty.
        If sequences have different lengths.
        If threshold is not between 0 and 1.

    Examples
    --------
    >>> generate_consensus_sequence(["ATGC", "ATGC", "ATGC"])
    'ATGC'
    >>> generate_consensus_sequence(["ATGC", "ATCC", "ATAC"])
    'ATGC'
    >>> generate_consensus_sequence(["ATGC", "TTGC", "CTGC", "GTGC"])
    'NTGC'
    >>> generate_consensus_sequence(["AT-C", "ATGC", "ATCC"], threshold=0.5)
    'ATGC'

    Notes
    -----
    For each position, the most common base is chosen.
    If no base reaches the threshold, 'N' is used.
    Gaps ('-') are treated as regular characters.
    Case-sensitive - returns uppercase consensus.

    Complexity
    ----------
    Time: O(n*m), Space: O(m) where n is number of sequences, m is sequence length
    """
    # Input validation
    if not isinstance(sequences, list):
        raise TypeError(f"sequences must be a list, got {type(sequences).__name__}")
    if not isinstance(threshold, (int, float)):
        raise TypeError(f"threshold must be a number, got {type(threshold).__name__}")

    if len(sequences) == 0:
        raise ValueError("Sequences list cannot be empty")

    if not (0.0 <= threshold <= 1.0):
        raise ValueError(f"threshold must be between 0 and 1, got {threshold}")

    # Check all sequences have same length
    seq_length = len(sequences[0])
    for i, seq in enumerate(sequences):
        if not isinstance(seq, str):
            raise TypeError(
                f"All sequences must be strings, got {type(seq).__name__} at index {i}"
            )
        if len(seq) != seq_length:
            raise ValueError(
                f"All sequences must have same length. Expected {seq_length}, got {len(seq)} at index {i}"
            )

    # Convert all to uppercase
    sequences_upper = [seq.upper() for seq in sequences]

    # Build consensus
    consensus = []
    num_sequences = len(sequences_upper)

    for pos in range(seq_length):
        # Count bases at this position
        bases_at_pos = [seq[pos] for seq in sequences_upper]
        base_counts = Counter(bases_at_pos)

        # Find most common base
        most_common_base, count = base_counts.most_common(1)[0]

        # Check if it meets threshold
        if count / num_sequences >= threshold:
            consensus.append(most_common_base)
        else:
            consensus.append("N")

    return "".join(consensus)


__all__ = ["generate_consensus_sequence"]
