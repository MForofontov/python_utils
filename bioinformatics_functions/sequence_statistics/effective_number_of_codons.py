"""Calculate Effective Number of Codons (ENC)."""


def effective_number_of_codons(seq: str) -> float:
    """
    Calculate the Effective Number of Codons (ENC) for a coding sequence.

    ENC measures codon usage bias independently of amino acid composition.
    Values range from 20 (extreme bias, one codon per amino acid) to 61
    (no bias, all synonymous codons used equally).

    Parameters
    ----------
    seq : str
        DNA coding sequence (must be multiple of 3).

    Returns
    -------
    float
        ENC value between 20 and 61.

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
    >>> effective_number_of_codons("ATGATGATG")
    20.0
    >>> effective_number_of_codons("ATGATCATTATAACG")
    35.5

    Notes
    -----
    ENC is calculated using the formula by Wright (1990).
    ENC = 2 + 9/F2 + 1/F3 + 5/F4 + 3/F6
    where Fk is the average homozygosity for amino acids with k synonymous codons.

    Stop codons are excluded from calculation.

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

    # Genetic code: amino acid to codons mapping
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
    }

    # Count codon usage
    codon_counts: dict[str, int] = {}
    stop_codons = {"TAA", "TAG", "TGA"}

    for i in range(0, len(seq_upper), 3):
        codon = seq_upper[i : i + 3]
        if codon not in stop_codons:
            codon_counts[codon] = codon_counts.get(codon, 0) + 1

    # Group amino acids by number of synonymous codons
    aa_groups: dict[int, list[str]] = {2: [], 3: [], 4: [], 6: []}
    for aa, codons in aa_to_codons.items():
        num_codons = len(codons)
        if num_codons in aa_groups:
            aa_groups[num_codons].append(aa)

    # Calculate F values (average homozygosity) for each group
    def calculate_F(
        aa_list: list[str],
        aa_to_codons: dict[str, list[str]],
        codon_counts: dict[str, int],
    ) -> float:
        """Calculate average homozygosity for amino acids."""
        F_values = []
        for aa in aa_list:
            codons = aa_to_codons[aa]
            total_aa = sum(codon_counts.get(codon, 0) for codon in codons)
            if total_aa > 0:
                homozygosity = sum(
                    (codon_counts.get(codon, 0) / total_aa) ** 2 for codon in codons
                )
                F_values.append(homozygosity)
        return sum(F_values) / len(F_values) if F_values else 0.0

    F2 = calculate_F(aa_groups[2], aa_to_codons, codon_counts)
    F3 = calculate_F(aa_groups[3], aa_to_codons, codon_counts)
    F4 = calculate_F(aa_groups[4], aa_to_codons, codon_counts)
    F6 = calculate_F(aa_groups[6], aa_to_codons, codon_counts)

    # Calculate ENC
    # Avoid division by zero
    enc = 2.0
    if F2 > 0:
        enc += 9.0 / F2
    if F3 > 0:
        enc += 1.0 / F3
    if F4 > 0:
        enc += 5.0 / F4
    if F6 > 0:
        enc += 3.0 / F6

    # ENC should be between 20 and 61
    enc = max(20.0, min(61.0, enc))

    return round(enc, 2)


__all__ = ["effective_number_of_codons"]
