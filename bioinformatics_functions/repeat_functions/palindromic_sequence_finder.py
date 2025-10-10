

def palindromic_sequence_finder(
    sequence: str, min_length: int = 4
) -> list[tuple[int, int, str]]:
    """
    Find palindromic regions in a sequence.

    Parameters
    ----------
    sequence : str
        Input sequence.
    min_length : int, optional
        Minimum length of palindrome (default 4).

    Returns
    -------
    list[tuple[int, int, str]]
        List of (start, end, palindrome) for each palindromic region.

    Raises
    ------
    ValueError
        If min_length is not positive.

    Examples
    --------
    >>> palindromic_sequence_finder("ATGCAT", min_length=4)
    [(0, 4, 'ATGC'), (2, 6, 'GCAT')]

    Complexity
    ----------
    Time: O(n^2), Space: O(n)
    """
    if min_length <= 0:
        raise ValueError("min_length must be > 0")
    n = len(sequence)
    results = []
    for l in range(min_length, n + 1):
        for i in range(n - l + 1):
            substr = sequence[i : i + l]
            if substr == substr[::-1]:
                results.append((i, i + l, substr))
    return results


__all__ = ["palindromic_sequence_finder"]
