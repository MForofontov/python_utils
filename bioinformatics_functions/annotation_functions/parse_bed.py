from typing import Iterator, Dict, Any

def parse_bed(bed_str: str) -> Iterator[Dict[str, Any]]:
    """
    Parse a BED formatted string and yield annotation dictionaries.

    Parameters
    ----------
    bed_str : str
        BED formatted string.

    Yields
    ------
    Dict[str, Any]
        Annotation dictionary for each feature.

    Raises
    ------
    TypeError
        If bed_str is not a string.
    ValueError
        If BED format is invalid.

    Examples
    --------
    >>> list(parse_bed('chr1\t1\t100\tfeature1'))
    [{'chrom': 'chr1', 'start': 1, 'end': 100, 'name': 'feature1'}]
    """
    if not isinstance(bed_str, str):
        raise TypeError("bed_str must be str")
    for line in bed_str.splitlines():
        if not line or line.startswith('#'):
            continue
        parts = line.split('\t')
        if len(parts) < 3:
            raise ValueError("Invalid BED line: " + line)
        ann = {
            'chrom': parts[0],
            'start': int(parts[1]),
            'end': int(parts[2]),
        }
        if len(parts) > 3:
            ann['name'] = parts[3]
        yield ann

__all__ = ["parse_bed"]
