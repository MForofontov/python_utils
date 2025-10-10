from collections.abc import Sequence

import numpy as np


def sequence_logo_matrix(sequences: Sequence[str]) -> np.ndarray:
    """
    Generate a position frequency matrix for sequence logo visualization.

    Parameters
    ----------
    sequences : Sequence[str]
        List of aligned sequences (equal length).

    Returns
    -------
    np.ndarray
        Matrix of shape (positions, alphabet_size) with counts.

    Raises
    ------
    ValueError
        If input sequences are not all the same length or empty.

    Examples
    --------
    >>> sequence_logo_matrix(["ATGC", "ATGT", "ATGA"])
    array([[0, 3, 0, 0],
           [0, 0, 3, 0],
           [0, 0, 0, 3],
           [1, 1, 1, 0]])

    Complexity
    ----------
    Time: O(n*m), Space: O(m*a)
    """
    if not sequences:
        raise ValueError("sequences cannot be empty")
    length = len(sequences[0])
    if any(len(seq) != length for seq in sequences):
        raise ValueError("All sequences must be the same length")
    alphabet = sorted(set("".join(sequences)))
    matrix = np.zeros((length, len(alphabet)), dtype=int)
    char_to_idx = {c: i for i, c in enumerate(alphabet)}
    for seq in sequences:
        for i, char in enumerate(seq):
            matrix[i, char_to_idx[char]] += 1
    return matrix


__all__ = ["sequence_logo_matrix"]
