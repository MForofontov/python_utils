from typing import Sequence

def sequence_complexity(sequence: str, window: int = 10) -> float:
    """
    Calculate linguistic complexity of a sequence (ratio of observed to possible substrings).

    Parameters
    ----------
    sequence : str
        Input sequence.
    window : int, optional
        Window size for substrings (default 10).

    Returns
    -------
    float
        Linguistic complexity score (0-1).

    Raises
    ------
    ValueError
        If window is not positive or sequence is empty.

    Examples
    --------
    >>> sequence_complexity("ATGCATGC", window=4)
    0.75

    Complexity
    ----------
    Time: O(n*w), Space: O(n)
    """
    if not sequence:
        raise ValueError("sequence cannot be empty")
    if window <= 0:
        raise ValueError("window must be positive")
    n = len(sequence)
    observed = set()
    possible = 0
    for w in range(1, window + 1):
        possible += max(n - w + 1, 0)
        for i in range(n - w + 1):
            observed.add(sequence[i:i + w])
    return len(observed) / possible if possible > 0 else 0.0

__all__ = ['sequence_complexity']
