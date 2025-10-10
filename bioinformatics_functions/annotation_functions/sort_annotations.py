from collections.abc import Sequence
from typing import Any


def sort_annotations(
    annotations: Sequence[dict[str, Any]],
    by: str = "start",
    reverse: bool = False,
) -> list[dict[str, Any]]:
    """
    Sort annotation records by a specified key (default: 'start').

    Parameters
    ----------
    annotations : Sequence[Dict[str, Any]]
        List of annotation records.
    by : str, optional
        Key to sort by (default: 'start').
    reverse : bool, optional
        Sort in descending order (default: False).

    Returns
    -------
    list[Dict[str, Any]]
        Sorted annotation records.

    Raises
    ------
    TypeError
        If input types are incorrect.
    KeyError
        If the sort key is missing in any record.

    Examples
    --------
    >>> annots = [{'start': 10}, {'start': 5}]
    >>> sort_annotations(annots)
    [{'start': 5}, {'start': 10}]

    Notes
    -----
    Sorts by the specified key, ascending or descending.

    Complexity
    ----------
    Time: O(n log n), Space: O(n)
    """
    if not isinstance(annotations, (list, tuple)):
        raise TypeError(
            f"annotations must be a list or tuple, got {type(annotations).__name__}"
        )
    if not isinstance(by, str):
        raise TypeError(f"by must be a string, got {type(by).__name__}")
    if not isinstance(reverse, bool):
        raise TypeError(f"reverse must be a boolean, got {type(reverse).__name__}")
    try:
        return sorted(annotations, key=lambda x: x[by], reverse=reverse)
    except KeyError as e:
        raise KeyError(f"Sort key missing in record: {e}")


__all__ = ["sort_annotations"]
