"""Calculate statistics for genomic annotations."""

from collections.abc import Sequence
from typing import Any


def annotation_statistics(annotations: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """
    Compute statistics from annotation records (counts, coverage, etc.).

    Parameters
    ----------
    annotations : Sequence[Dict[str, Any]]
        List of annotation records.

    Returns
    -------
    Dict[str, Any]
        Dictionary of statistics (feature counts, total coverage, etc.).

    Raises
    ------
    TypeError
        If input types are incorrect.

    Examples
    --------
    >>> annots = [{'feature': 'exon', 'start': 10, 'end': 20}, ...]
    >>> annotation_statistics(annots)
    {'feature_counts': {'exon': 1}, 'total_coverage': 10}

    Notes
    -----
    Computes feature counts and total coverage.

    Complexity
    ----------
    Time: O(n), Space: O(k) where k is number of unique features
    """
    if not isinstance(annotations, (list, tuple)):
        raise TypeError(
            f"annotations must be a list or tuple, got {type(annotations).__name__}"
        )
    feature_counts: dict[str, int] = {}
    total_coverage = 0
    for record in annotations:
        feature = record.get("feature", ".")
        feature_counts[feature] = feature_counts.get(feature, 0) + 1
        start = record.get("start")
        end = record.get("end")
        if isinstance(start, int) and isinstance(end, int):
            total_coverage += end - start + 1
    return {
        "feature_counts": feature_counts,
        "total_coverage": total_coverage,
    }


__all__ = ["annotation_statistics"]
