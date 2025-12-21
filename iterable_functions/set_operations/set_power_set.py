"""Set power set utilities."""

from typing import TypeVar

T = TypeVar("T")


def set_power_set(input_set: set[T]) -> set[frozenset[T]]:
    """
    Generate the power set of a given set.

    The power set of a set S is the set of all possible subsets of S,
    including the empty set and S itself.

    Parameters
    ----------
    input_set : set[T]
        The input set to generate power set for.

    Returns
    -------
    set[FrozenSet[T]]
        Power set of the input set, where each subset is a frozenset.

    Raises
    ------
    TypeError
        If input_set is not a set.

    Examples
    --------
    >>> s = {1, 2, 3}
    >>> power_set = set_power_set(s)
    >>> len(power_set)
    8
    >>> frozenset() in power_set  # empty set
    True
    >>> frozenset({1, 2, 3}) in power_set  # full set
    True
    >>> frozenset({1, 2}) in power_set  # subset
    True

    >>> set_power_set(set())
    {frozenset()}

    >>> set_power_set({1})
    {frozenset(), frozenset({1})}

    Notes
    -----
    For a set S with n elements:
    P(S) = {T | T ⊆ S}

    The power set has 2^n elements.

    Complexity
    ----------
    Time: O(2^n * n), Space: O(2^n * n)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    # Convert to list for indexing
    elements = list(input_set)
    n = len(elements)

    # Generate all possible subsets using bit manipulation
    power_set: set[frozenset[T]] = set()

    for i in range(2**n):
        subset: frozenset[T] = frozenset()
        for j in range(n):
            if i & (1 << j):
                subset = subset | {elements[j]}
        power_set.add(subset)

    return power_set


__all__ = ["set_power_set"]
