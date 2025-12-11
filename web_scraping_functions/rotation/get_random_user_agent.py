"""
Get random user agent from list.
"""

import random


def get_random_user_agent(
    user_agents: list[str] | None = None,
) -> str:
    """
    Get random user agent from list or default list.

    Parameters
    ----------
    user_agents : list[str] | None, optional
        List of user agent strings (by default None uses built-in list).

    Returns
    -------
    str
        Random user agent string.

    Raises
    ------
    TypeError
        If user_agents is not a list or None.
    ValueError
        If user_agents list is empty.

    Examples
    --------
    >>> agent = get_random_user_agent()
    >>> len(agent) > 0
    True

    >>> custom_agents = ["Agent1", "Agent2"]
    >>> agent = get_random_user_agent(custom_agents)
    >>> agent in custom_agents
    True

    Notes
    -----
    Default list includes common browser user agents.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if user_agents is not None and not isinstance(user_agents, list):
        raise TypeError(
            f"user_agents must be a list or None, got {type(user_agents).__name__}"
        )
    
    if user_agents is None:
        # Default user agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        ]
    
    if not user_agents:
        raise ValueError("user_agents list cannot be empty")
    
    return random.choice(user_agents)


__all__ = ['get_random_user_agent']
