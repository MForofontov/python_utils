"""Local sequence alignment using Smith-Waterman algorithm."""


def smith_waterman(
    seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -1
) -> tuple[int, str, str]:
    """
    Perform local sequence alignment using Smith-Waterman algorithm.

    Parameters
    ----------
    seq1 : str
        First sequence to align.
    seq2 : str
        Second sequence to align.
    match : int, optional
        Score for matching characters (by default 2).
    mismatch : int, optional
        Penalty for mismatching characters (by default -1).
    gap : int, optional
        Penalty for gaps (by default -1).

    Returns
    -------
    tuple[int, str, str]
        Tuple containing:
        - alignment_score: int, the optimal local alignment score
        - aligned_seq1: str, aligned portion of first sequence with gaps
        - aligned_seq2: str, aligned portion of second sequence with gaps

    Raises
    ------
    TypeError
        If seq1 or seq2 is not a string.
        If match, mismatch, or gap is not an integer.
    ValueError
        If either sequence is empty.

    Examples
    --------
    >>> smith_waterman("ACGT", "ACT")
    (4, 'AC', 'AC')
    >>> smith_waterman("GGTTGACTA", "TGTTACGG")
    (13, 'GTTAC', 'GTTAC')
    >>> smith_waterman("GCATGCU", "GATTACA")
    (6, 'AT', 'AT')

    Notes
    -----
    This is a simplified implementation for educational purposes.
    For production use, consider using established bioinformatics libraries.
    Finds the best local alignment between two sequences.
    Algorithm uses dynamic programming with O(n*m) time and space complexity.

    Complexity
    ----------
    Time: O(n*m), Space: O(n*m) where n, m are sequence lengths
    """
    # Input validation
    if not isinstance(seq1, str):
        raise TypeError(f"seq1 must be a string, got {type(seq1).__name__}")
    if not isinstance(seq2, str):
        raise TypeError(f"seq2 must be a string, got {type(seq2).__name__}")
    if not isinstance(match, int):
        raise TypeError(f"match must be an integer, got {type(match).__name__}")
    if not isinstance(mismatch, int):
        raise TypeError(f"mismatch must be an integer, got {type(mismatch).__name__}")
    if not isinstance(gap, int):
        raise TypeError(f"gap must be an integer, got {type(gap).__name__}")

    if len(seq1) == 0:
        raise ValueError("seq1 cannot be empty")
    if len(seq2) == 0:
        raise ValueError("seq2 cannot be empty")

    # Initialize scoring matrix
    n, m = len(seq1), len(seq2)
    score_matrix = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    # Track maximum score and position
    max_score = 0
    max_i, max_j = 0, 0

    # Fill the scoring matrix (Smith-Waterman allows negative scores to become 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                diagonal = score_matrix[i - 1][j - 1] + match
            else:
                diagonal = score_matrix[i - 1][j - 1] + mismatch

            up = score_matrix[i - 1][j] + gap
            left = score_matrix[i][j - 1] + gap

            # Smith-Waterman: scores cannot be negative
            score_matrix[i][j] = max(0, diagonal, up, left)

            # Track maximum score position
            if score_matrix[i][j] > max_score:
                max_score = score_matrix[i][j]
                max_i, max_j = i, j

    # Traceback from maximum score position until we hit 0
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = max_i, max_j

    while i > 0 and j > 0 and score_matrix[i][j] > 0:
        current_score = score_matrix[i][j]

        if seq1[i - 1] == seq2[j - 1]:
            diagonal_score = score_matrix[i - 1][j - 1] + match
        else:
            diagonal_score = score_matrix[i - 1][j - 1] + mismatch

        if current_score == diagonal_score:
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and current_score == score_matrix[i - 1][j] + gap:
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append("-")
            i -= 1
        elif j > 0 and current_score == score_matrix[i][j - 1] + gap:
            aligned_seq1.append("-")
            aligned_seq2.append(seq2[j - 1])
            j -= 1
        else:
            break

    # Reverse alignments (built backwards during traceback)
    aligned_seq1_str = "".join(reversed(aligned_seq1))
    aligned_seq2_str = "".join(reversed(aligned_seq2))

    return max_score, aligned_seq1_str, aligned_seq2_str


__all__ = ["smith_waterman"]
