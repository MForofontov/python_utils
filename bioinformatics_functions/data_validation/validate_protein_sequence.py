from typing import Any


def validate_protein_sequence(seq: str) -> dict[str, Any]:
    """
    Validate a protein sequence and return detailed validation report.

    Parameters
    ----------
    seq : str
        Protein sequence to validate (single-letter amino acid codes).

    Returns
    -------
    dict[str, Any]
        Validation report containing:
        - 'is_valid': bool, whether sequence is valid
        - 'length': int, sequence length
        - 'invalid_chars': list[str], list of invalid characters found
        - 'has_lowercase': bool, whether sequence contains lowercase
        - 'has_stop_codon': bool, whether sequence contains stop codon (*)
        - 'molecular_weight': float, approximate molecular weight in Daltons

    Raises
    ------
    TypeError
        If seq is not a string.

    Examples
    --------
    >>> validate_protein_sequence("ACDEFGHIKLMNPQRSTVWY")
    {'is_valid': True, 'length': 20, 'invalid_chars': [], 'has_lowercase': False, ...}
    >>> validate_protein_sequence("ACDEFX")
    {'is_valid': False, 'length': 6, 'invalid_chars': ['X'], ...}
    >>> validate_protein_sequence("acdef")
    {'is_valid': True, 'length': 5, 'invalid_chars': [], 'has_lowercase': True, ...}
    >>> validate_protein_sequence("ACDEF*")
    {'is_valid': True, 'length': 6, 'invalid_chars': [], 'has_stop_codon': True, ...}

    Notes
    -----
    Valid amino acid codes: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y
    Also allows: B (Asx), Z (Glx), X (unknown), * (stop codon)
    Molecular weight calculated using average residue weights.
    
    Complexity
    ----------
    Time: O(n), Space: O(k) where n is sequence length, k is unique invalid chars
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")
    
    # Define valid amino acid codes (standard 20 + ambiguous + stop)
    valid_aa = set('ACDEFGHIKLMNPQRSTVWYBZX*')
    
    # Check for lowercase
    has_lowercase = seq != seq.upper()
    
    # Convert to uppercase for validation
    seq_upper = seq.upper()
    
    # Find invalid characters
    seq_chars = set(seq_upper)
    invalid_chars = sorted(seq_chars - valid_aa)
    
    # Determine if valid
    is_valid = len(invalid_chars) == 0
    
    # Check for stop codon
    has_stop_codon = '*' in seq_upper
    
    # Calculate approximate molecular weight (average residue weights in Da)
    aa_weights = {
        'A': 89.1, 'C': 121.2, 'D': 133.1, 'E': 147.1, 'F': 165.2,
        'G': 75.1, 'H': 155.2, 'I': 131.2, 'K': 146.2, 'L': 131.2,
        'M': 149.2, 'N': 132.1, 'P': 115.1, 'Q': 146.2, 'R': 174.2,
        'S': 105.1, 'T': 119.1, 'V': 117.1, 'W': 204.2, 'Y': 181.2,
        'B': 132.6, 'Z': 146.6, 'X': 110.0, '*': 0.0
    }
    
    molecular_weight = sum(aa_weights.get(aa, 0.0) for aa in seq_upper)
    
    # Build report
    report: dict[str, Any] = {
        'is_valid': is_valid,
        'length': len(seq),
        'invalid_chars': invalid_chars,
        'has_lowercase': has_lowercase,
        'has_stop_codon': has_stop_codon,
        'molecular_weight': round(molecular_weight, 2)
    }
    
    return report


__all__ = ['validate_protein_sequence']
