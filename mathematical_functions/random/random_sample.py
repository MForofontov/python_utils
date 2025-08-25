"""Generate random samples from a list."""

import random
from typing import Any


def random_sample(population: list[Any], count: int, replace: bool = False) -> list[Any]:
    """
    Generate random samples from a population list.

    Parameters
    ----------
    population : list[Any]
        The population to sample from.
    count : int
        Number of samples to generate.
    replace : bool, optional
        If True, sampling is done with replacement (same element can be chosen 
        multiple times). If False (default), sampling is without replacement.

    Returns
    -------
    list[Any]
        List of random samples from the population.

    Raises
    ------
    TypeError
        If population is not a list, count is not an integer, or replace is not boolean.
    ValueError
        If count is negative, population is empty, or count exceeds population 
        size when replace=False.

    Examples
    --------
    >>> population = [1, 2, 3, 4, 5]
    >>> len(random_sample(population, 3))
    3
    >>> all(x in population for x in random_sample(population, 2))
    True
    >>> len(random_sample(population, 10, replace=True))
    10
    """
    if not isinstance(population, list):
        raise TypeError("population must be a list")
    
    if not isinstance(count, int):
        raise TypeError("count must be an integer")
    
    if not isinstance(replace, bool):
        raise TypeError("replace must be a boolean")
    
    if count < 0:
        raise ValueError("count must be non-negative")
    
    if len(population) == 0:
        raise ValueError("population cannot be empty")
    
    if not replace and count > len(population):
        raise ValueError("count cannot exceed population size when replace=False")
    
    if replace:
        return [random.choice(population) for _ in range(count)]
    else:
        return random.sample(population, count)


__all__ = ['random_sample']
