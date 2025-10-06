from typing import Sequence, Dict, Any

def annotation_to_gff(
    annotations: Sequence[Dict[str, Any]]
) -> list[str]:
    """
    Convert annotation records to GFF format strings.

    Parameters
    ----------
    annotations : Sequence[Dict[str, Any]]
        List of annotation records.

    Returns
    -------
    list of str
        List of GFF format strings.

    Raises
    ------
    TypeError
        If input types are incorrect.
    KeyError
        If required keys are missing in any record.

    Examples
    --------
    >>> annotation_to_gff([
    ...     {'seqid': 'chr1', 'source': '.', 'type': 'gene', 'start': 1, 'end': 100, 'score': '.', 'strand': '+', 'phase': '.', 'attributes': 'ID=gene1'}
    ... ])
    ['chr1\t.\tgene\t1\t100\t.\t+\t.\tID=gene1']
    """
    if not isinstance(annotations, (list, tuple)):
        raise TypeError(f"annotations must be a list or tuple, got {type(annotations).__name__}")
    result = []
    for record in annotations:
        for key in ("seqid", "source", "type", "start", "end", "score", "strand", "phase", "attributes"):
            if key not in record:
                raise KeyError(f"Missing required GFF key: {key}")
        result.append(
            f"{record['seqid']}\t{record['source']}\t{record['type']}\t{record['start']}\t{record['end']}\t"
            f"{record['score']}\t{record['strand']}\t{record['phase']}\t{record['attributes']}"
        )
    return result

__all__ = ['annotation_to_gff']
