

def blast_score_ratio(reference_score: float, target_score: float) -> float:
    """
    Calculate the Blast Score Ratio (BSR) for a query sequence.

    Parameters
    ----------
    reference_score : float
        BLAST score against the reference genome.
    target_score : float
        BLAST score against the target genome.

    Returns
    -------
    float
        BSR value (0 to 1).

    Raises
    ------
    TypeError
        If scores are not floats or ints.
    ValueError
        If reference_score is zero or negative.

    Examples
    --------
    >>> blast_score_ratio(200.0, 150.0)
    0.75
    >>> blast_score_ratio(100.0, 100.0)
    1.0
    """
    if not isinstance(reference_score, (int, float)):
        raise TypeError(
            f"reference_score must be a number, got {type(reference_score).__name__}"
        )
    if not isinstance(target_score, (int, float)):
        raise TypeError(
            f"target_score must be a number, got {type(target_score).__name__}"
        )
    if reference_score <= 0:
        raise ValueError("reference_score must be positive and non-zero")
    return target_score / reference_score


__all__ = ["blast_score_ratio"]
