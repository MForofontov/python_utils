"""
Rotate user agents for requests.
"""

from typing import Iterator


def rotate_user_agent(
    user_agents: list[str],
) -> Iterator[str]:
    """
    Create user agent rotator that cycles through user agent list.

    Parameters
    ----------
    user_agents : list[str]
        List of user agent strings.

    Yields
    ------
    str
        User agent string.

    Raises
    ------
    TypeError
        If user_agents is not a list.
    ValueError
        If user_agents list is empty.

    Examples
    --------
    >>> agents = ["Mozilla/5.0 (Windows)", "Mozilla/5.0 (Mac)"]
    >>> rotator = rotate_user_agent(agents)
    >>> next(rotator)
    'Mozilla/5.0 (Windows)'
    >>> next(rotator)
    'Mozilla/5.0 (Mac)'

    Notes
    -----
    Infinitely cycles through user agent list.

    Complexity
    ----------
    Time: O(1) per iteration, Space: O(1)
    """
    if not isinstance(user_agents, list):
        raise TypeError(f"user_agents must be a list, got {type(user_agents).__name__}")
    
    if not user_agents:
        raise ValueError("user_agents list cannot be empty")
    
    index = 0
    while True:
        yield user_agents[index % len(user_agents)]
        index += 1


__all__ = ['rotate_user_agent']
