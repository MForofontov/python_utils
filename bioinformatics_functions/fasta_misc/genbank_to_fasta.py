import re


def genbank_to_fasta(genbank_str: str) -> str:
    """
    Convert GenBank format to FASTA format (simplified parser).

    Parameters
    ----------
    genbank_str : str
        GenBank format string containing one or more sequences.

    Returns
    -------
    str
        FASTA format string.

    Raises
    ------
    TypeError
        If genbank_str is not a string.
    ValueError
        If genbank_str is empty or doesn't contain sequence data.

    Examples
    --------
    >>> gb = "LOCUS       SEQ1\\nORIGIN\\n        1 atgcatgcat\\n//"
    >>> genbank_to_fasta(gb)
    '>SEQ1\\nATGCATGCAT\\n'
    >>> gb = "LOCUS       AB123\\nDEFINITION  Test\\nORIGIN\\n1 atgc\\n//"
    >>> genbank_to_fasta(gb)
    '>AB123\\nATGC\\n'

    Notes
    -----
    This is a simplified parser that extracts:
    - LOCUS name as the FASTA header
    - Sequence data from ORIGIN section

    GenBank format structure:
    - LOCUS line contains sequence ID
    - ORIGIN marks start of sequence data
    - // marks end of record
    - Sequence data has line numbers that are removed

    For full GenBank parsing, use Biopython.

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is total string length
    """
    # Input validation
    if not isinstance(genbank_str, str):
        raise TypeError(
            f"genbank_str must be a string, got {type(genbank_str).__name__}"
        )

    if len(genbank_str.strip()) == 0:
        raise ValueError("genbank_str cannot be empty")

    # Split into records (separated by //)
    records = genbank_str.split("//")
    fasta_entries = []

    for record in records:
        record = record.strip()
        if not record:
            continue

        lines = record.split("\n")

        # Extract LOCUS name
        locus_name = None
        for line in lines:
            if line.startswith("LOCUS"):
                # LOCUS line format: "LOCUS       name       ..."
                parts = line.split()
                if len(parts) >= 2:
                    locus_name = parts[1]
                break

        if locus_name is None:
            continue  # Skip records without LOCUS

        # Extract sequence from ORIGIN section
        in_origin = False
        sequence_parts = []

        for line in lines:
            if line.startswith("ORIGIN"):
                in_origin = True
                continue

            if in_origin:
                # Remove line numbers and whitespace
                # Example: "        1 atgcatgcat gcatgcatgc"
                cleaned = re.sub(r"^\s*\d+\s*", "", line)  # Remove leading numbers
                cleaned = cleaned.replace(" ", "")  # Remove spaces
                cleaned = cleaned.strip()

                if cleaned:
                    sequence_parts.append(cleaned)

        if not sequence_parts:
            continue  # Skip records without sequence

        # Combine sequence and convert to uppercase
        sequence = "".join(sequence_parts).upper()

        # Create FASTA entry
        fasta_header = f">{locus_name}"
        fasta_entries.append(f"{fasta_header}\n{sequence}")

    if len(fasta_entries) == 0:
        raise ValueError("No valid GenBank sequences found in input")

    return "\n".join(fasta_entries) + "\n"


__all__ = ["genbank_to_fasta"]
