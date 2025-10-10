

def find_cpg_islands(
    seq: str, window: int = 200, min_gc: float = 0.5, min_obs_exp: float = 0.6
) -> list[tuple[int, int]]:
    """
    Identify CpG islands in a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence (A, T, C, G).
    window : int, optional
        Sliding window size (default: 200).
    min_gc : float, optional
        Minimum GC content (default: 0.5).
    min_obs_exp : float, optional
        Minimum observed/expected CpG ratio (default: 0.6).

    Returns
    -------
    List[Tuple[int, int]]
        List of (start, end) positions of CpG islands.

    Raises
    ------
    TypeError
        If seq is not a string or parameters have wrong types.
    ValueError
        If seq contains invalid characters or parameters are invalid.

    Examples
    --------
    >>> find_cpg_islands('GCGCGCGCGC' * 20, window=50)
    [(0, 50), (1, 51), ...]

    Notes
    -----
    CpG islands are regions with high GC content and CpG dinucleotide frequency.
    Often found near gene promoters.

    Complexity
    ----------
    Time: O(n*w), Space: O(k) where k is number of islands
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    if not isinstance(window, int):
        raise TypeError(f"window must be int, got {type(window).__name__}")
    if not isinstance(min_gc, (int, float)):
        raise TypeError(f"min_gc must be a number, got {type(min_gc).__name__}")
    if not isinstance(min_obs_exp, (int, float)):
        raise TypeError(
            f"min_obs_exp must be a number, got {type(min_obs_exp).__name__}"
        )

    seq = seq.upper()
    if not all(base in "ATCG" for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")

    if window <= 0 or window > len(seq):
        raise ValueError("window must be positive and <= sequence length")
    if not 0 <= min_gc <= 1:
        raise ValueError("min_gc must be between 0 and 1")
    if min_obs_exp < 0:
        raise ValueError("min_obs_exp must be non-negative")

    cpg_islands: list[tuple[int, int]] = []

    for i in range(len(seq) - window + 1):
        subseq = seq[i : i + window]

        # Calculate GC content
        gc_count = subseq.count("G") + subseq.count("C")
        gc_content = gc_count / window

        if gc_content < min_gc:
            continue

        # Calculate observed/expected CpG ratio
        cpg_count = subseq.count("CG")
        c_count = subseq.count("C")
        g_count = subseq.count("G")

        if c_count > 0 and g_count > 0:
            expected_cpg = (c_count * g_count) / window
            obs_exp_ratio = cpg_count / expected_cpg if expected_cpg > 0 else 0

            if obs_exp_ratio >= min_obs_exp:
                cpg_islands.append((i, i + window))

    return cpg_islands


__all__ = ["find_cpg_islands"]
