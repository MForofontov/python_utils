from typing import Sequence

def phylogenetic_distance(seq1: str, seq2: str) -> float:
    """
    Compute simple evolutionary distance (proportion of differences) between two sequences.

    Parameters
    ----------
    seq1 : str
        First sequence.
    seq2 : str
        Second sequence.

    Returns
    -------
    float
        Proportion of differing positions.

    Raises
    ------
    ValueError
        If sequences are not the same length.

    Examples
    --------
    >>> phylogenetic_distance("ATGC", "ATGT")
    0.25

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be the same length")
    if len(seq1) == 0:
        raise ValueError("Sequences must not be empty")
    differences = sum(a != b for a, b in zip(seq1, seq2))
    return differences / len(seq1)

__all__ = ['phylogenetic_distance']
