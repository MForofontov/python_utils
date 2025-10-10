from collections.abc import Sequence


def fasta_concat(fasta_strs: Sequence[str]) -> str:
    """
    Concatenate multiple FASTA strings into one.

    Parameters
    ----------
    fasta_strs : Sequence[str]
        List of FASTA formatted strings.

    Returns
    -------
    str
        Concatenated FASTA string.

    Raises
    ------
    TypeError
        If fasta_strs is not a sequence of strings.

    Examples
    --------
    >>> fasta_concat(['>seq1\nATGC', '>seq2\nGGTT'])
    '>seq1\nATGC\n>seq2\nGGTT'
    """
    if not all(isinstance(s, str) for s in fasta_strs):
        raise TypeError("All elements must be strings")
    return "\n".join(s.strip() for s in fasta_strs if s.strip())


__all__ = ["fasta_concat"]
