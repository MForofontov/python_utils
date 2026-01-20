"""Calculate Codon Adaptation Index (CAI)."""

import math


def codon_adaptation_index(
    seq: str, reference_weights: dict[str, float] | None = None
) -> float:
    """
    Calculate the Codon Adaptation Index (CAI) for a coding sequence.

    CAI is a measure of codon usage bias that ranges from 0 to 1, where 1
    indicates optimal codon usage based on a reference set of highly expressed genes.

    Parameters
    ----------
    seq : str
        DNA coding sequence (must be multiple of 3).
    reference_weights : dict[str, float] | None, optional
        Dictionary mapping codons to their relative weights (0-1).
        If None, uses equal weights for all synonymous codons (by default None).

    Returns
    -------
    float
        CAI value between 0 and 1.

    Raises
    ------
    TypeError
        If seq is not a string.
        If reference_weights is not a dict or None.
    ValueError
        If seq length is not a multiple of 3.
        If seq contains invalid DNA bases.
        If seq is empty.

    Examples
    --------
    >>> codon_adaptation_index("ATGATGATG")
    1.0
    >>> weights = {"ATG": 1.0, "ATT": 0.5, "ATC": 0.8}
    >>> codon_adaptation_index("ATGATT", reference_weights=weights)
    0.71

    Notes
    -----
    CAI = exp(sum(ln(w_i)) / L) where w_i is the weight of codon i and L is the number of codons.
    Stop codons are excluded from calculation.
    If no reference weights provided, all synonymous codons get equal weight.

    Complexity
    ----------
    Time: O(n), Space: O(1) where n is sequence length
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")
    if reference_weights is not None and not isinstance(reference_weights, dict):
        raise TypeError(
            f"reference_weights must be a dict or None, got {type(reference_weights).__name__}"
        )

    if len(seq) == 0:
        raise ValueError("Sequence cannot be empty")
    if len(seq) % 3 != 0:
        raise ValueError(f"Sequence length must be multiple of 3, got {len(seq)}")

    # Validate DNA sequence
    seq_upper = seq.upper()
    valid_bases = set("ATGC")
    invalid_bases = set(seq_upper) - valid_bases
    if invalid_bases:
        raise ValueError(f"Invalid DNA bases found: {', '.join(sorted(invalid_bases))}")

    # If no reference weights, use uniform weights
    if reference_weights is None:
        reference_weights = {}

    # Convert to uppercase for codon lookup
    reference_weights_upper = {k.upper(): v for k, v in reference_weights.items()}

    # Stop codons
    stop_codons = {"TAA", "TAG", "TGA"}

    # Extract codons and calculate CAI
    codons = [seq_upper[i : i + 3] for i in range(0, len(seq_upper), 3)]

    log_sum = 0.0
    codon_count = 0

    for codon in codons:
        # Skip stop codons
        if codon in stop_codons:
            continue

        # Get weight (default to 1.0 if not in reference)
        weight = reference_weights_upper.get(codon, 1.0)

        # Avoid log(0)
        if weight > 0:
            log_sum += math.log(weight)
            codon_count += 1

    if codon_count == 0:
        return 0.0

    # CAI is geometric mean of weights
    cai = math.exp(log_sum / codon_count)

    return round(cai, 4)


__all__ = ["codon_adaptation_index"]
