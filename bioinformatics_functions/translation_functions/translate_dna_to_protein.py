

def translate_dna_to_protein(seq: str) -> str:
    """
    Translate a DNA sequence to a protein sequence using the standard genetic code.

    Parameters
    ----------
    seq : str
        DNA sequence (A, T, C, G).

    Returns
    -------
    str
        Protein sequence (single-letter amino acids).

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters or length is not a multiple of 3.

    Examples
    --------
    >>> translate_dna_to_protein('ATGGCC')
    'MA'
    """
    codon_table: dict[str, str] = {
        "ATA": "I",
        "ATC": "I",
        "ATT": "I",
        "ATG": "M",
        "ACA": "T",
        "ACC": "T",
        "ACG": "T",
        "ACT": "T",
        "AAC": "N",
        "AAT": "N",
        "AAA": "K",
        "AAG": "K",
        "AGC": "S",
        "AGT": "S",
        "AGA": "R",
        "AGG": "R",
        "CTA": "L",
        "CTC": "L",
        "CTG": "L",
        "CTT": "L",
        "CCA": "P",
        "CCC": "P",
        "CCG": "P",
        "CCT": "P",
        "CAC": "H",
        "CAT": "H",
        "CAA": "Q",
        "CAG": "Q",
        "CGA": "R",
        "CGC": "R",
        "CGG": "R",
        "CGT": "R",
        "GTA": "V",
        "GTC": "V",
        "GTG": "V",
        "GTT": "V",
        "GCA": "A",
        "GCC": "A",
        "GCG": "A",
        "GCT": "A",
        "GAC": "D",
        "GAT": "D",
        "GAA": "E",
        "GAG": "E",
        "GGA": "G",
        "GGC": "G",
        "GGG": "G",
        "GGT": "G",
        "TCA": "S",
        "TCC": "S",
        "TCG": "S",
        "TCT": "S",
        "TTC": "F",
        "TTT": "F",
        "TTA": "L",
        "TTG": "L",
        "TAC": "Y",
        "TAT": "Y",
        "TAA": "*",
        "TAG": "*",
        "TGC": "C",
        "TGT": "C",
        "TGA": "*",
        "TGG": "W",
    }
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    seq = seq.upper()
    if not all(base in "ATCG" for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")
    if len(seq) % 3 != 0:
        raise ValueError("Sequence length must be a multiple of 3")
    protein = ""
    for i in range(0, len(seq), 3):
        codon = seq[i : i + 3]
        protein += codon_table.get(codon, "X")
    return protein


__all__ = ["translate_dna_to_protein"]
