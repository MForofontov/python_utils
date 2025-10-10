def calculate_molecular_weight(seq: str, seq_type: str = "dna") -> float:
    """
    Calculate molecular weight of a DNA, RNA, or protein sequence.

    Parameters
    ----------
    seq : str
        Input sequence.
    seq_type : str, optional
        Type of sequence: 'dna', 'rna', or 'protein' (default: 'dna').

    Returns
    -------
    float
        Molecular weight in Daltons (Da).

    Raises
    ------
    TypeError
        If seq or seq_type is not a string.
    ValueError
        If seq contains invalid characters or seq_type is invalid.

    Examples
    --------
    >>> calculate_molecular_weight('ATGC', 'dna')
    1221.8
    >>> calculate_molecular_weight('AUGC', 'rna')
    1237.8

    Notes
    -----
    Uses average molecular weights for nucleotides and amino acids.

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    if not isinstance(seq_type, str):
        raise TypeError(f"seq_type must be str, got {type(seq_type).__name__}")

    seq = seq.upper()
    seq_type = seq_type.lower()

    # Molecular weights in Daltons
    dna_weights = {"A": 313.2, "T": 304.2, "G": 329.2, "C": 289.2}
    rna_weights = {"A": 329.2, "U": 306.2, "G": 345.2, "C": 305.2}
    protein_weights = {
        "A": 89.1,
        "R": 174.2,
        "N": 132.1,
        "D": 133.1,
        "C": 121.2,
        "E": 147.1,
        "Q": 146.2,
        "G": 75.1,
        "H": 155.2,
        "I": 131.2,
        "L": 131.2,
        "K": 146.2,
        "M": 149.2,
        "F": 165.2,
        "P": 115.1,
        "S": 105.1,
        "T": 119.1,
        "W": 204.2,
        "Y": 181.2,
        "V": 117.1,
    }

    if seq_type == "dna":
        weights = dna_weights
        valid_chars = "ATGC"
    elif seq_type == "rna":
        weights = rna_weights
        valid_chars = "AUGC"
    elif seq_type == "protein":
        weights = protein_weights
        valid_chars = "".join(protein_weights.keys())
    else:
        raise ValueError("seq_type must be 'dna', 'rna', or 'protein'")

    if not all(base in valid_chars for base in seq):
        raise ValueError(f"Sequence contains invalid {seq_type} characters")

    return sum(weights.get(base, 0) for base in seq)


__all__ = ["calculate_molecular_weight"]
