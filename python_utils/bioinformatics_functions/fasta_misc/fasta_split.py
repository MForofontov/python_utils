"""Split FASTA sequences into individual records."""

from collections.abc import Iterator

from .fasta_parser import parse_fasta


def fasta_split(fasta_str: str) -> Iterator[str]:
    """
    Split a FASTA string into individual record strings.

    Parameters
    ----------
    fasta_str : str
        FASTA formatted string.

    Yields
    ------
    str
        Individual FASTA record strings.

    Examples
    --------
    >>> list(fasta_split('>seq1\nATGC\n>seq2\nGGTT'))
    ['>seq1\nATGC', '>seq2\nGGTT']
    """
    for header, seq in parse_fasta(fasta_str):
        yield f">{header}\n{seq}"


__all__ = ["fasta_split"]
