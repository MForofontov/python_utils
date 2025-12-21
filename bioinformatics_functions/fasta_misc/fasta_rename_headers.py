"""Rename FASTA sequence headers."""

from collections.abc import Callable, Iterator

from .fasta_parser import parse_fasta


def fasta_rename_headers(
    fasta_str: str, rename_fn: Callable[[str], str]
) -> Iterator[tuple[str, str]]:
    """
    Rename FASTA headers using a mapping function.

    Parameters
    ----------
    fasta_str : str
        FASTA formatted string.
    rename_fn : Callable[[str], str]
        Function to rename headers.

    Yields
    ------
    Tuple[str, str]
        (new_header, sequence) pairs.

    Examples
    --------
    >>> list(fasta_rename_headers('>seq1\nATGC', lambda h: h + '_renamed'))
    [('seq1_renamed', 'ATGC')]
    """
    for header, seq in parse_fasta(fasta_str):
        yield (rename_fn(header), seq)


__all__ = ["fasta_rename_headers"]
