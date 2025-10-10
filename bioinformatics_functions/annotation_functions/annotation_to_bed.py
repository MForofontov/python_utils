from collections.abc import Sequence
from typing import Any


def annotation_to_bed(annotations: Sequence[dict[str, Any]]) -> list[str]:
    """
    Convert annotation records to BED format strings.

    Parameters
    ----------
    annotations : Sequence[Dict[str, Any]]
        List of annotation records.

    Returns
    -------
    list[str]
        List of BED format strings.

    Raises
    ------
    TypeError
        If input types are incorrect.
    KeyError
        If required keys are missing in any record.

    Examples
    --------
    >>> annots = [{'seqname': 'chr1', 'start': 10, 'end': 20, 'feature': 'exon'}]
    >>> annotation_to_bed(annots)
    ['chr1\t9\t20\texon']

    Notes
    -----
    BED format uses 0-based start, 1-based end.

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(annotations, (list, tuple)):
        raise TypeError(
            f"annotations must be a list or tuple, got {type(annotations).__name__}"
        )
    bed_lines = []
    for record in annotations:
        try:
            chrom = record["seqname"] if "seqname" in record else record["chrom"]
            start = int(record["start"]) - 1  # BED is 0-based
            end = int(record["end"])
            name = record.get("feature", ".")
            bed_lines.append(f"{chrom}\t{start}\t{end}\t{name}")
        except KeyError as e:
            raise KeyError(f"Missing required key in record: {e}")
    return bed_lines


__all__ = ["annotation_to_bed"]
