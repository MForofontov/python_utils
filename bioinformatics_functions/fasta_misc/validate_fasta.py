"""Validate FASTA format."""

import re


def validate_fasta(fasta_str: str) -> bool:
    """
    Validate if a string is in proper FASTA format.

    Parameters
    ----------
    fasta_str : str
        FASTA formatted string.

    Returns
    -------
    bool
        True if valid, False otherwise.

    Raises
    ------
    TypeError
        If fasta_str is not a string.

    Examples
    --------
    >>> validate_fasta('>seq1\nATGC\n>seq2\nGGTT')
    True
    >>> validate_fasta('seq1\nATGC')
    False
    """
    if not isinstance(fasta_str, str):
        raise TypeError(f"fasta_str must be str, got {type(fasta_str).__name__}")
    lines = fasta_str.splitlines()
    if not lines or not any(line.startswith(">") for line in lines):
        return False
    header_seen = False
    for line in lines:
        if line.startswith(">"):
            if not line[1:].strip():
                return False
            header_seen = True
        elif header_seen:
            if not re.fullmatch(r"[A-Za-z\-\.]+", line.strip()):
                return False
        elif line.strip():
            return False
    return True


__all__ = ["validate_fasta"]
