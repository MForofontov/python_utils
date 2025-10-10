def sequence_masking(seq: str, mask_char: str = "N", threshold: int = 3) -> str:
    """
    Mask low-complexity regions in a sequence by replacing runs of identical bases with a mask character.

    Parameters
    ----------
    seq : str
        Input sequence.
    mask_char : str, optional
        Character to use for masking (default: 'N').
    threshold : int, optional
        Minimum run length to mask (default: 3).

    Returns
    -------
    str
        Masked sequence.

    Raises
    ------
    TypeError
        If seq or mask_char is not a string, or threshold is not int.
    ValueError
        If threshold < 1 or mask_char is empty.

    Examples
    --------
    >>> sequence_masking('AAATTTCCCGGG', mask_char='N', threshold=3)
    'NNNTTTCCCGGG'
    """
    if not isinstance(seq, str):
        raise TypeError("seq must be str")
    if not isinstance(mask_char, str):
        raise TypeError("mask_char must be str")
    if not isinstance(threshold, int):
        raise TypeError("threshold must be int")
    if threshold < 1:
        raise ValueError("threshold must be >= 1")
    if not mask_char:
        raise ValueError("mask_char must not be empty")
    out = list(seq)
    i = 0
    while i < len(seq):
        run_len = 1
        while i + run_len < len(seq) and seq[i] == seq[i + run_len]:
            run_len += 1
        if run_len >= threshold:
            for j in range(run_len):
                out[i + j] = mask_char
        i += run_len
    return "".join(out)


__all__ = ["sequence_masking"]
