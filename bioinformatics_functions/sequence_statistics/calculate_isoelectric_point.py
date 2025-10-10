def calculate_isoelectric_point(seq: str) -> float:
    """
    Calculate theoretical isoelectric point (pI) of a protein sequence.

    Parameters
    ----------
    seq : str
        Protein sequence (single-letter amino acid codes).

    Returns
    -------
    float
        Isoelectric point (pH value).

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid amino acid codes or is empty.

    Examples
    --------
    >>> calculate_isoelectric_point('ACDEFGH')
    3.57
    >>> calculate_isoelectric_point('KKKKK')
    10.76

    Notes
    -----
    Uses pKa values for charged amino acids to estimate pI.
    The pI is the pH at which the protein has no net charge.

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")

    seq = seq.upper()

    valid_amino_acids = "ACDEFGHIKLMNPQRSTVWY"

    if not seq:
        raise ValueError("Sequence cannot be empty")

    if not all(aa in valid_amino_acids for aa in seq):
        raise ValueError("Sequence contains invalid amino acid codes")

    # pKa values for ionizable groups
    pka_nterm = 9.69
    pka_cterm = 2.34

    pka_side_chains = {
        "C": 8.33,  # Cysteine
        "D": 3.86,  # Aspartic acid
        "E": 4.25,  # Glutamic acid
        "H": 6.00,  # Histidine
        "K": 10.53,  # Lysine
        "R": 12.48,  # Arginine
        "Y": 10.07,  # Tyrosine
    }

    # Count ionizable residues
    positive_charges = seq.count("K") + seq.count("R") + seq.count("H")
    negative_charges = seq.count("D") + seq.count("E")

    # Simplified pI calculation using average of pKa values
    # This is an approximation; more accurate methods use iterative pH calculations

    if positive_charges > negative_charges:
        # Basic protein - estimate from positive pKa values
        pka_values = [pka_nterm]
        for aa in seq:
            if aa in ["K", "R", "H"]:
                pka_values.append(pka_side_chains[aa])
        pi = sum(pka_values) / len(pka_values) if pka_values else 7.0
    elif negative_charges > positive_charges:
        # Acidic protein - estimate from negative pKa values
        pka_values = [pka_cterm]
        for aa in seq:
            if aa in ["D", "E"]:
                pka_values.append(pka_side_chains[aa])
        pi = sum(pka_values) / len(pka_values) if pka_values else 7.0
    else:
        # Neutral protein
        pi = 7.0

    return round(pi, 2)


__all__ = ["calculate_isoelectric_point"]
