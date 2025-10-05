def transcribe_dna_to_rna(seq: str) -> str:
    """
    Transcribe a DNA sequence to RNA (replace T with U).

    Parameters
    ----------
    seq : str
        DNA sequence.

    Returns
    -------
    str
        RNA sequence.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters.

    Examples
    --------
    >>> transcribe_dna_to_rna('ATGC')
    'AUGC'
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    seq = seq.upper()
    if not all(base in 'ATCG' for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")
    return seq.replace('T', 'U')

__all__ = ["transcribe_dna_to_rna"]
