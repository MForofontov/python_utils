from typing import Iterator, Dict, Any

def parse_gff(gff_str: str) -> Iterator[Dict[str, Any]]:
    """
    Parse a GFF formatted string and yield annotation dictionaries.

    Parameters
    ----------
    gff_str : str
        GFF formatted string.

    Yields
    ------
    Dict[str, Any]
        Annotation dictionary for each feature.

    Raises
    ------
    TypeError
        If gff_str is not a string.
    ValueError
        If GFF format is invalid.

    Examples
    --------
    >>> list(parse_gff('chr1\tRefSeq\tgene\t1\t100\t.\t+\t.\tID=gene1;Name=abc'))
    [{'seqid': 'chr1', 'source': 'RefSeq', 'type': 'gene', 'start': 1, 'end': 100, 'score': '.', 'strand': '+', 'phase': '.', 'attributes': {'ID': 'gene1', 'Name': 'abc'}}]
    """
    if not isinstance(gff_str, str):
        raise TypeError("gff_str must be str")
    for line in gff_str.splitlines():
        if not line or line.startswith('#'):
            continue
        parts = line.split('\t')
        if len(parts) != 9:
            raise ValueError("Invalid GFF line: " + line)
        attr_dict = {}
        for attr in parts[8].split(';'):
            if '=' in attr:
                k, v = attr.split('=', 1)
                attr_dict[k] = v
        yield {
            'seqid': parts[0],
            'source': parts[1],
            'type': parts[2],
            'start': int(parts[3]),
            'end': int(parts[4]),
            'score': parts[5],
            'strand': parts[6],
            'phase': parts[7],
            'attributes': attr_dict,
        }

__all__ = ["parse_gff"]
