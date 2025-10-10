from collections.abc import Sequence


def restriction_site_finder(
    sequence: str, sites: Sequence[str]
) -> list[tuple[int, str]]:
    """
    Locate restriction enzyme recognition sites in a sequence.

    Parameters
    ----------
    sequence : str
        Input sequence.
    sites : Sequence[str]
        List of recognition site sequences.

    Returns
    -------
    list[tuple[int, str]]
        List of (position, site) for each match.

    Raises
    ------
    ValueError
        If sites is empty.

    Examples
    --------
    >>> restriction_site_finder("ATGCGAATTC", ["GAATTC"])
    [(4, 'GAATTC')]

    Complexity
    ----------
    Time: O(n*m), Space: O(k)
    """
    if not sites:
        raise ValueError("sites cannot be empty")
    results = []
    for site in sites:
        start = 0
        while True:
            idx = sequence.find(site, start)
            if idx == -1:
                break
            results.append((idx, site))
            start = idx + 1
    return results


__all__ = ["restriction_site_finder"]
