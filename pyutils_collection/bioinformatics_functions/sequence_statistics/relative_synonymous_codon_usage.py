"""Calculate Relative Synonymous Codon Usage (RSCU)."""


def relative_synonymous_codon_usage(seq: str) -> dict[str, float]:
    """
    Calculate Relative Synonymous Codon Usage (RSCU) for a coding sequence.

    RSCU measures the relative usage of each codon compared to equal usage
    of synonymous codons. RSCU = 1.0 means equal usage, >1.0 means preferred,
    <1.0 means avoided.

    Parameters
    ----------
    seq : str
        DNA coding sequence (must be multiple of 3).

    Returns
    -------
    dict[str, float]
        Dictionary mapping each codon to its RSCU value.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq length is not a multiple of 3.
        If seq contains invalid DNA bases.
        If seq is too short (< 3 bases).

    Examples
    --------
    >>> relative_synonymous_codon_usage("ATGATGATG")
    {'ATG': 1.0, ...}
    >>> rscu = relative_synonymous_codon_usage("TTTTTTTTCTTT")
    >>> rscu['TTT']  # TTT is used more than TTC
    1.5
    >>> rscu['TTC']  # TTC is used less than TTT
    0.5

    Notes
    -----
    RSCU = (observed frequency of codon) / (1 / number of synonymous codons)
    Stop codons are included in calculation.
    Codons not present in sequence will have RSCU = 0.0

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is sequence length
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")

    if len(seq) < 3:
        raise ValueError(f"Sequence must be at least 3 bases long, got {len(seq)}")
    if len(seq) % 3 != 0:
        raise ValueError(f"Sequence length must be multiple of 3, got {len(seq)}")

    # Validate DNA sequence
    seq_upper = seq.upper()
    valid_bases = set("ATGC")
    invalid_bases = set(seq_upper) - valid_bases
    if invalid_bases:
        raise ValueError(f"Invalid DNA bases found: {', '.join(sorted(invalid_bases))}")

    # Genetic code: amino acid to codons mapping (including stop codons)
    aa_to_codons: dict[str, list[str]] = {
        "F": ["TTT", "TTC"],
        "L": ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
        "I": ["ATT", "ATC", "ATA"],
        "M": ["ATG"],
        "V": ["GTT", "GTC", "GTA", "GTG"],
        "S": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
        "P": ["CCT", "CCC", "CCA", "CCG"],
        "T": ["ACT", "ACC", "ACA", "ACG"],
        "A": ["GCT", "GCC", "GCA", "GCG"],
        "Y": ["TAT", "TAC"],
        "H": ["CAT", "CAC"],
        "Q": ["CAA", "CAG"],
        "N": ["AAT", "AAC"],
        "K": ["AAA", "AAG"],
        "D": ["GAT", "GAC"],
        "E": ["GAA", "GAG"],
        "C": ["TGT", "TGC"],
        "W": ["TGG"],
        "R": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
        "G": ["GGT", "GGC", "GGA", "GGG"],
        "*": ["TAA", "TAG", "TGA"],  # Stop codons
    }

    # Create reverse mapping: codon to amino acid
    codon_to_aa: dict[str, str] = {}
    for aa, codons in aa_to_codons.items():
        for codon in codons:
            codon_to_aa[codon] = aa

    # Count codon usage
    codon_counts: dict[str, int] = {}
    for i in range(0, len(seq_upper), 3):
        codon = seq_upper[i : i + 3]
        codon_counts[codon] = codon_counts.get(codon, 0) + 1

    # Calculate RSCU for each codon
    rscu: dict[str, float] = {}

    for _aa, codons in aa_to_codons.items():
        # Count total usage of this amino acid
        total_aa_usage = sum(codon_counts.get(codon, 0) for codon in codons)

        if total_aa_usage > 0:
            # Number of synonymous codons for this amino acid
            num_synonymous = len(codons)

            # Calculate RSCU for each codon encoding this amino acid
            for codon in codons:
                observed = codon_counts.get(codon, 0)
                expected = total_aa_usage / num_synonymous

                if expected > 0:
                    rscu[codon] = round(observed / expected, 4)
                else:
                    rscu[codon] = 0.0
        else:
            # Amino acid not used in sequence
            for codon in codons:
                rscu[codon] = 0.0

    return rscu


__all__ = ["relative_synonymous_codon_usage"]
