"""Parse BED format files."""

from collections.abc import Iterator
from typing import Any


def parse_bed(bed_file: str) -> Iterator[dict[str, Any]]:
    """
    Parse a BED formatted file and yield annotation dictionaries.

    Parameters
    ----------
    bed_file : str
        Path to BED formatted file.

    Yields
    ------
    Dict[str, Any]
        Annotation dictionary for each feature.

    Raises
    ------
    TypeError
        If bed_file is not a string.
    FileNotFoundError
        If the file does not exist.
    ValueError
        If BED format is invalid.

    Examples
    --------
    >>> for record in parse_bed('example.bed'):
    ...     print(record)
    {'chrom': 'chr1', 'start': 1, 'end': 100, 'name': 'feature1'}
    """
    if not isinstance(bed_file, str):
        raise TypeError("bed_file must be str")
    try:
        with open(bed_file) as f:
            for line in f:
                if not line or line.startswith("#"):
                    continue
                parts = line.strip().split("\t")
                if len(parts) < 3:
                    raise ValueError("Invalid BED line: " + line)
                ann = {
                    "chrom": parts[0],
                    "start": int(parts[1]),
                    "end": int(parts[2]),
                }
                if len(parts) > 3:
                    ann["name"] = parts[3]
                yield ann
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {bed_file}") from e


__all__ = ["parse_bed"]
