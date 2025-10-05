from typing import Tuple
from .fasta_parser import parse_fasta

def fasta_stats(fasta_str: str) -> Tuple[int, float, float]:
    """
    Compute statistics for a FASTA string: (num_sequences, avg_length, avg_gc_content).

    Parameters
    ----------
    fasta_str : str
        FASTA formatted string.

    Returns
    -------
    Tuple[int, float, float]
        Number of sequences, average length, average GC content.

    Examples
    --------
    >>> fasta_stats('>seq1\nATGC\n>seq2\nGGTT')
    (2, 4.0, 0.5)
    """
    num = 0
    total_len = 0
    total_gc = 0
    for _, seq in parse_fasta(fasta_str):
        num += 1
        total_len += len(seq)
        total_gc += (seq.count('G') + seq.count('C')) / len(seq) if seq else 0
    avg_len = total_len / num if num else 0.0
    avg_gc = total_gc / num if num else 0.0
    return num, avg_len, avg_gc

__all__ = ["fasta_stats"]
