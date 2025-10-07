def levenshtein_distance(seq1: str, seq2: str) -> int:
    """
    Calculate the Levenshtein distance (edit distance) between two sequences.

    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions, or substitutions) required to change one sequence
    into the other.

    Parameters
    ----------
    seq1 : str
        First sequence.
    seq2 : str
        Second sequence.

    Returns
    -------
    int
        The Levenshtein distance between the two sequences.

    Raises
    ------
    TypeError
        If seq1 or seq2 is not a string.

    Examples
    --------
    >>> levenshtein_distance("ACGT", "ACGT")
    0
    >>> levenshtein_distance("ACGT", "ACT")
    1
    >>> levenshtein_distance("kitten", "sitting")
    3
    >>> levenshtein_distance("", "ABC")
    3
    >>> levenshtein_distance("ABC", "")
    3

    Notes
    -----
    The algorithm uses dynamic programming with O(n*m) time complexity.
    Space complexity can be optimized to O(min(n,m)) but this implementation
    uses O(n*m) for clarity.
    
    Complexity
    ----------
    Time: O(n*m), Space: O(n*m) where n, m are sequence lengths
    """
    # Input validation
    if not isinstance(seq1, str):
        raise TypeError(f"seq1 must be a string, got {type(seq1).__name__}")
    if not isinstance(seq2, str):
        raise TypeError(f"seq2 must be a string, got {type(seq2).__name__}")
    
    # Handle empty strings
    if len(seq1) == 0:
        return len(seq2)
    if len(seq2) == 0:
        return len(seq1)
    
    # Initialize distance matrix
    n, m = len(seq1), len(seq2)
    distance = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    
    # Initialize first row and column
    for i in range(n + 1):
        distance[i][0] = i
    for j in range(m + 1):
        distance[0][j] = j
    
    # Fill the distance matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                cost = 0
            else:
                cost = 1
            
            distance[i][j] = min(
                distance[i - 1][j] + 1,      # deletion
                distance[i][j - 1] + 1,      # insertion
                distance[i - 1][j - 1] + cost  # substitution
            )
    
    return distance[n][m]


__all__ = ['levenshtein_distance']
