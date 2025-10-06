from typing import Iterator, Dict, Any

def parse_gff(gff_file: str) -> Iterator[Dict[str, Any]]:
    """
    Parse a GFF formatted file and yield annotation dictionaries.

    Parameters
    ----------
    gff_file : str
        Path to GFF formatted file.

    Yields
    ------
    Dict[str, Any]
        Annotation dictionary for each feature.

    Raises
    ------
    TypeError
        If gff_file is not a string.
    FileNotFoundError
        If the file does not exist.
    ValueError
        If GFF format is invalid.

    Examples
    --------
    >>> for record in parse_gff('example.gff'):
    ...     print(record)
    {'seqid': 'chr1', 'source': 'RefSeq', 'type': 'gene', 'start': 1, 'end': 100, 'score': '.', 'strand': '+', 'phase': '.', 'attributes': {'ID': 'gene1', 'Name': 'abc'}}
    """
    if not isinstance(gff_file, str):
        raise TypeError("gff_file must be str")
    try:
        with open(gff_file) as f:
            for line in f:
                if not line or line.startswith('#'):
                    continue
                parts = line.strip().split('\t')
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
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {gff_file}")

__all__ = ["parse_gff"]
