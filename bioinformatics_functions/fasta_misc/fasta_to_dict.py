
from .fasta_parser import parse_fasta


def fasta_to_dict(fasta_str: str) -> dict[str, str]:
    """
    Convert FASTA string to a dictionary {header: sequence}.

    Parameters
    ----------
    fasta_str : str
        FASTA formatted string.

    Returns
    -------
    Dict[str, str]
        Dictionary mapping header to sequence.

    Raises
    ------
    ValueError
        If duplicate headers are found.

    Examples
    --------
    >>> fasta_to_dict('>seq1\nATGC\n>seq2\nGGTT')
    {'seq1': 'ATGC', 'seq2': 'GGTT'}
    """
    result = {}
    for header, seq in parse_fasta(fasta_str):
        if header in result:
            raise ValueError(f"Duplicate header found: {header}")
        result[header] = seq
    return result


__all__ = ["fasta_to_dict"]
