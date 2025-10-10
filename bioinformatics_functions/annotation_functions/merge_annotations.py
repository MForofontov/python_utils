from collections.abc import Sequence
from typing import Any


def merge_annotations(annotations: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """
    Merge multiple annotation dictionaries (e.g., GFF, BED, custom) for a sequence.

    Parameters
    ----------
    annotations : Sequence[Dict[str, Any]]
        List of annotation dictionaries.

    Returns
    -------
    Dict[str, Any]
        Merged annotation dictionary.

    Raises
    ------
    TypeError
        If input is not a sequence of dicts.

    Examples
    --------
    >>> merge_annotations([
    ...     {'gene': 'abc', 'start': 1, 'end': 100},
    ...     {'exon': 1, 'start': 1, 'end': 50}
    ... ])
    {'gene': 'abc', 'start': 1, 'end': 100, 'exon': 1}
    """
    if not all(isinstance(a, dict) for a in annotations):
        raise TypeError("All annotations must be dictionaries")
    merged = {}
    for ann in annotations:
        merged.update(ann)
    return merged


__all__ = ["merge_annotations"]
