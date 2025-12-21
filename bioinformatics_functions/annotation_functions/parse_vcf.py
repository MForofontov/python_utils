"""Parse VCF (Variant Call Format) files."""

from collections.abc import Iterator
from typing import Any


def parse_vcf(vcf_file: str) -> Iterator[dict[str, Any]]:
    """
    Parse a VCF (Variant Call Format) file and yield variant records as dictionaries.

    Parameters
    ----------
    vcf_file : str
        Path to the VCF file.

    Returns
    -------
    Iterator[Dict[str, Any]]
        Iterator over parsed variant records.

    Raises
    ------
    TypeError
        If vcf_file is not a string.
    FileNotFoundError
        If the file does not exist.

    Examples
    --------
    >>> for record in parse_vcf('example.vcf'):
    ...     print(record)
    {'chrom': 'chr1', 'pos': 12345, ...}

    Notes
    -----
    This function parses standard VCF files and extracts fields as a dictionary.

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(vcf_file, str):
        raise TypeError(f"vcf_file must be a string, got {type(vcf_file).__name__}")
    try:
        with open(vcf_file) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.strip().split("\t")
                if len(parts) < 8:
                    continue
                record = {
                    "chrom": parts[0],
                    "pos": int(parts[1]),
                    "id": parts[2],
                    "ref": parts[3],
                    "alt": parts[4],
                    "qual": parts[5],
                    "filter": parts[6],
                    "info": parts[7],
                }
                yield record
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {vcf_file}") from e


__all__ = ["parse_vcf"]
