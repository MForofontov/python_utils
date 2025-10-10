import random
from collections.abc import Iterator

from .fasta_parser import parse_fasta


def fasta_subsample(fasta_str: str, n: int) -> Iterator[tuple[str, str]]:
    """
    Randomly subsample n sequences from a FASTA string.

    Parameters
    ----------
    fasta_str : str
        FASTA formatted string.
    n : int
        Number of sequences to sample.

    Yields
    ------
    Tuple[str, str]
        (header, sequence) pairs.

    Raises
    ------
    ValueError
        If n is negative or exceeds number of sequences.

    Examples
    --------
    >>> list(fasta_subsample('>seq1\nATGC\n>seq2\nGGTT', 1))
    [('seq2', 'GGTT')]  # Output may vary
    """
    records = list(parse_fasta(fasta_str))
    if n < 0 or n > len(records):
        raise ValueError("n must be between 0 and number of sequences")
    for rec in random.sample(records, n):
        yield rec


__all__ = ["fasta_subsample"]
