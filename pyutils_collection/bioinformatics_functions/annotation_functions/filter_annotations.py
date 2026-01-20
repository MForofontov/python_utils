"""Filter genomic annotations by criteria."""

from collections.abc import Iterator, Sequence
from typing import Any


def filter_annotations(
    annotations: Sequence[dict[str, Any]],
    feature_type: str | None = None,
    chrom: str | None = None,
) -> Iterator[dict[str, Any]]:
    """
    Filter annotation records by feature type and/or chromosome.

    Parameters
    ----------
    annotations : Sequence[Dict[str, Any]]
        List of annotation records.
    feature_type : str, optional
        Feature type to filter (e.g., 'exon', 'gene').
    chrom : str, optional
        Chromosome to filter (e.g., 'chr1').

    Returns
    -------
    Iterator[Dict[str, Any]]
        Filtered annotation records.

    Raises
    ------
    TypeError
        If input types are incorrect.

    Examples
    --------
    >>> annots = [{'feature': 'exon', 'seqname': 'chr1'}, ...]
    >>> list(filter_annotations(annots, feature_type='exon'))
    [{'feature': 'exon', 'seqname': 'chr1'}]

    Notes
    -----
    Filters by feature type and/or chromosome if provided.

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(annotations, (list, tuple)):
        raise TypeError(
            f"annotations must be a list or tuple, got {type(annotations).__name__}"
        )
    if feature_type is not None and not isinstance(feature_type, str):
        raise TypeError(
            f"feature_type must be str or None, got {type(feature_type).__name__}"
        )
    if chrom is not None and not isinstance(chrom, str):
        raise TypeError(f"chrom must be str or None, got {type(chrom).__name__}")
    for record in annotations:
        if feature_type and record.get("feature") != feature_type:
            continue
        if chrom and (record.get("seqname") or record.get("chrom")) != chrom:
            continue
        yield record


__all__ = ["filter_annotations"]
