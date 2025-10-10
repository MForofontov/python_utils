from collections.abc import Iterator
from typing import Any


def parse_gtf(gtf_file: str) -> Iterator[dict[str, Any]]:
    """
    Parse a GTF (Gene Transfer Format) file and yield annotation records as dictionaries.

    Parameters
    ----------
    gtf_file : str
        Path to the GTF file.

    Returns
    -------
    Iterator[Dict[str, Any]]
        Iterator over parsed annotation records.

    Raises
    ------
    TypeError
        If gtf_file is not a string.
    FileNotFoundError
        If the file does not exist.

    Examples
    --------
    >>> for record in parse_gtf('example.gtf'):
    ...     print(record)
    {'seqname': 'chr1', 'source': 'ENSEMBL', ...}

    Notes
    -----
    This function parses standard GTF files and extracts attributes as a dictionary.

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(gtf_file, str):
        raise TypeError(f"gtf_file must be a string, got {type(gtf_file).__name__}")
    try:
        with open(gtf_file) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.strip().split("\t")
                if len(parts) != 9:
                    continue
                record = {
                    "seqname": parts[0],
                    "source": parts[1],
                    "feature": parts[2],
                    "start": int(parts[3]),
                    "end": int(parts[4]),
                    "score": parts[5],
                    "strand": parts[6],
                    "frame": parts[7],
                    "attribute": parts[8],
                }
                yield record
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {gtf_file}")


__all__ = ["parse_gtf"]
