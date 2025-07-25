def get_max_min_values(
    input_collection: list[int | float] | set[int | float] | tuple[int | float, ...],
) -> tuple[int | float, int | float]:
    """
    From an input list, set, or tuple, return the maximum and minimum integer or float values.

    Parameters
    ----------
    input_collection : list[int] or list[float] or set[int] or set[float] or tuple[int] or tuple[float]
        Collection containing integer or float values.

    Returns
    -------
    tuple
        A tuple containing the largest and smallest values in the input collection.

    Raises
    ------
    TypeError
        If input_collection is not a list, set, or tuple, or contains non-numeric elements.
    ValueError
        If input_collection is empty.
    """
    if not isinstance(input_collection, (list, set, tuple)):
        raise TypeError("input_collection must be a list, set, or tuple")
    if not all(isinstance(item, (int, float)) for item in input_collection):
        raise TypeError("input_collection must contain only integers or floats")
    if not input_collection:
        raise ValueError("input_collection must not be empty")

    return max(input_collection), min(input_collection)
