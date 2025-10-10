from collections.abc import Sequence


def restriction_site_finder(
    sequence: str, sites: Sequence[str]
) -> dict[str, list[int]]:
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
    dict[str, list[int]]
        Dictionary mapping each site to list of positions where it was found.

    Raises
    ------
    ValueError
        If sites is empty.

    Examples
    --------
    >>> restriction_site_finder("ATGCGAATTC", ["GAATTC"])
    {'GAATTC': [4]}

    Complexity
    ----------
    Time: O(n*m), Space: O(k)
    """
    if not sites:
        raise ValueError("sites cannot be empty")
    
    # Convert sequence and sites to uppercase for case-insensitive matching
    sequence_upper = sequence.upper()
    
    results: dict[str, list[int]] = {}
    for site in sites:
        site_upper = site.upper()
        positions: list[int] = []
        start = 0
        while True:
            idx = sequence_upper.find(site_upper, start)
            if idx == -1:
                break
            positions.append(idx)
            start = idx + 1
        results[site_upper] = positions
    
    return results


__all__ = ["restriction_site_finder"]
