from collections.abc import Sequence
from typing import Any


def annotation_to_gtf(annotations: Sequence[dict[str, Any]]) -> list[str]:
    """
    Convert annotation records to GTF format strings.

    Parameters
    ----------
    annotations : Sequence[Dict[str, Any]]
        List of annotation records.

    Returns
    -------
    list of str
        List of GTF format strings.

    Raises
    ------
    TypeError
        If input types are incorrect.
    KeyError
        If required keys are missing in any record.

    Examples
    --------
    >>> annotation_to_gtf([
    ...     {'seqid': 'chr1', 'source': '.', 'feature': 'exon', 'start': 1, 'end': 100, 'score': '.', 'strand': '+', 'frame': '.', 'attribute': 'gene_id "gene1";'}
    ... ])
    ['chr1\t.\texon\t1\t100\t.\t+\t.\tgene_id "gene1";']
    """
    if not isinstance(annotations, (list, tuple)):
        raise TypeError(
            f"annotations must be a list or tuple, got {type(annotations).__name__}"
        )
    result = []
    for record in annotations:
        if not isinstance(record, dict):
            raise TypeError("record must be a dict")
        for key in (
            "seqid",
            "source",
            "feature",
            "start",
            "end",
            "score",
            "strand",
            "frame",
            "attribute",
        ):
            if key not in record:
                raise KeyError(f"Missing required GTF key: {key}")
        result.append(
            f"{record['seqid']}\t{record['source']}\t{record['feature']}\t{record['start']}\t{record['end']}\t"
            f"{record['score']}\t{record['strand']}\t{record['frame']}\t{record['attribute']}"
        )
    return result


__all__ = ["annotation_to_gtf"]
