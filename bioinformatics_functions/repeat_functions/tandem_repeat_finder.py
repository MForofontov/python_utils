

def tandem_repeat_finder(
    sequence: str, min_repeat: int = 2, min_length: int = 2
) -> list[tuple[int, int, str]]:
    """
    Identify tandem repeats in a sequence.

    Parameters
    ----------
    sequence : str
        Input sequence.
    min_repeat : int, optional
        Minimum number of repeats (default 2).
    min_length : int, optional
        Minimum length of repeat unit (default 2).

    Returns
    -------
    list[tuple[int, int, str]]
        List of (start, end, repeat_unit) for each tandem repeat.

    Raises
    ------
    ValueError
        If min_repeat or min_length is not positive.

    Examples
    --------
    >>> tandem_repeat_finder("ATATATGC", min_repeat=2, min_length=2)
    [(0, 6, 'AT')]

    Complexity
    ----------
    Time: O(n^2), Space: O(n)
    """
    if min_repeat <= 1:
        raise ValueError("min_repeat must be > 1")
    if min_length <= 0:
        raise ValueError("min_length must be > 0")
    n = len(sequence)
    results = []
    for l in range(min_length, n // min_repeat + 1):
        for i in range(n - l * min_repeat + 1):
            unit = sequence[i : i + l]
            count = 1
            while sequence[i + count * l : i + (count + 1) * l] == unit:
                count += 1
            if count >= min_repeat:
                results.append((i, i + count * l, unit))
    return results


__all__ = ["tandem_repeat_finder"]
