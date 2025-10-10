from collections.abc import Sequence


def sequence_conservation(sequences: Sequence[str]) -> list[float]:
    """
    Calculate conservation score for each position in a multiple sequence alignment.

    Parameters
    ----------
    sequences : Sequence[str]
        List of aligned sequences (equal length).

    Returns
    -------
    list[float]
        Conservation score (fraction of most common residue) per position.

    Raises
    ------
    ValueError
        If input sequences are not all the same length or empty.

    Examples
    --------
    >>> sequence_conservation(["ATGC", "ATGT", "ATGA"])
    [1.0, 1.0, 1.0, 0.6666666666666666]

    Complexity
    ----------
    Time: O(n*m), Space: O(m)
    """
    if not sequences:
        raise ValueError("sequences cannot be empty")
    length = len(sequences[0])
    if any(len(seq) != length for seq in sequences):
        raise ValueError("All sequences must be the same length")
    scores = []
    for i in range(length):
        column = [seq[i] for seq in sequences]
        most_common = max(set(column), key=column.count)
        score = column.count(most_common) / len(column)
        scores.append(score)
    return scores


__all__ = ["sequence_conservation"]
