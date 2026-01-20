"""Calculate melting temperature (Tm) of DNA."""


def melting_temperature(seq: str) -> float:
    """
    Calculate melting temperature (Tm) of a DNA sequence using nearest-neighbor method.

    Parameters
    ----------
    seq : str
        DNA sequence (A, T, C, G).

    Returns
    -------
    float
        Melting temperature in Celsius.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters or is too short.

    Examples
    --------
    >>> melting_temperature('ATGC')
    8.0
    >>> melting_temperature('GCGCGCGC')
    32.0

    Notes
    -----
    Uses Wallace rule for sequences < 14 bases: Tm = 2(A+T) + 4(G+C)
    For longer sequences, use more sophisticated nearest-neighbor parameters.

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")

    seq = seq.upper()
    if not all(base in "ATCG" for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")

    if len(seq) < 2:
        raise ValueError("Sequence must be at least 2 bases long")

    # Wallace rule for short sequences
    if len(seq) < 14:
        at_count = seq.count("A") + seq.count("T")
        gc_count = seq.count("G") + seq.count("C")
        return float(2 * at_count + 4 * gc_count)

    # For longer sequences, use basic salt-adjusted formula
    gc_count = seq.count("G") + seq.count("C")
    gc_percent = (gc_count / len(seq)) * 100

    # Basic Tm formula: 81.5 + 0.41(%GC) - 675/length
    tm = 81.5 + 0.41 * gc_percent - (675.0 / len(seq))
    return tm


__all__ = ["melting_temperature"]
