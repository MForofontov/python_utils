"""Split sequences into k-mers."""


def sequence_to_kmers(seq: str, k: int) -> list[str]:
    """
    Split a sequence into k-mers of length k.

    Parameters
    ----------
    seq : str
        Input sequence.
    k : int
        Length of each k-mer.

    Returns
    -------
    List[str]
        List of k-mers.

    Raises
    ------
    TypeError
        If seq is not a string or k is not an integer.
    ValueError
        If k is not positive or longer than sequence.

    Examples
    --------
    >>> sequence_to_kmers('ATGCGA', 3)
    ['ATG', 'TGC', 'GCG', 'CGA']
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    if not isinstance(k, int):
        raise TypeError(f"k must be int, got {type(k).__name__}")
    if k <= 0:
        raise ValueError("k must be positive")
    if k > len(seq):
        raise ValueError("k cannot be longer than sequence")
    return [seq[i : i + k] for i in range(len(seq) - k + 1)]


__all__ = ["sequence_to_kmers"]
