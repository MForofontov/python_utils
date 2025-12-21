"""Write sequences to FASTA format."""

from collections.abc import Sequence


def write_fasta(records: Sequence[tuple[str, str]]) -> str:
    """
    Write (header, sequence) pairs to a FASTA-formatted string.

    Parameters
    ----------
    records : Sequence[Tuple[str, str]]
        List of (header, sequence) pairs.

    Returns
    -------
    str
        FASTA formatted string.

    Raises
    ------
    TypeError
        If records is not a sequence of (str, str) tuples.

    Examples
    --------
    >>> write_fasta([('seq1', 'ATGC'), ('seq2', 'GGTT')])
    '>seq1\nATGC\n>seq2\nGGTT\n'
    """
    lines = []
    for rec in records:
        if not (
            isinstance(rec, tuple)
            and len(rec) == 2
            and all(isinstance(x, str) for x in rec)
        ):
            raise TypeError("Each record must be a (str, str) tuple")
        header, seq = rec
        lines.append(f">{header}")
        lines.append(seq)
    return "\n".join(lines) + "\n"


__all__ = ["write_fasta"]
