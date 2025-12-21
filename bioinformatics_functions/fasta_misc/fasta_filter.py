"""Filter FASTA sequences by custom criteria."""

from collections.abc import Callable, Iterator

from .fasta_parser import parse_fasta


def fasta_filter(
    fasta_str: str, predicate: Callable[[str, str], bool]
) -> Iterator[tuple[str, str]]:
    """
    Filter FASTA records by a predicate function.

    Parameters
    ----------
    fasta_str : str
        FASTA formatted string.
    predicate : Callable[[str, str], bool]
        Function that returns True to keep a record.

    Yields
    ------
    Tuple[str, str]
        (header, sequence) pairs passing the predicate.

    Examples
    --------
    >>> list(fasta_filter('>seq1\nATGC\n>seq2\nGGTT', lambda h, s: len(s) > 4))
    []
    """
    for header, seq in parse_fasta(fasta_str):
        if predicate(header, seq):
            yield (header, seq)


__all__ = ["fasta_filter"]
