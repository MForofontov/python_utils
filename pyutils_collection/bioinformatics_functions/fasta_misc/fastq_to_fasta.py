"""Convert FASTQ format to FASTA format."""


def fastq_to_fasta(fastq_str: str, min_quality: int | None = None) -> str:
    """
    Convert FASTQ format to FASTA format with optional quality filtering.

    Parameters
    ----------
    fastq_str : str
        FASTQ format string containing one or more sequences.
    min_quality : int | None, optional
        Minimum average Phred quality score. Sequences below this are excluded.
        If None, no quality filtering (by default None).

    Returns
    -------
    str
        FASTA format string.

    Raises
    ------
    TypeError
        If fastq_str is not a string.
        If min_quality is not an integer or None.
    ValueError
        If fastq_str is empty or malformed.
        If min_quality is negative.

    Examples
    --------
    >>> fastq = "@SEQ1\\nATGC\\n+\\nIIII\\n"
    >>> fastq_to_fasta(fastq)
    '>SEQ1\\nATGC\\n'
    >>> fastq = "@SEQ1\\nATGC\\n+\\n!!!!\\n@SEQ2\\nGGCC\\n+\\nIIII\\n"
    >>> fastq_to_fasta(fastq, min_quality=20)
    '>SEQ2\\nGGCC\\n'

    Notes
    -----
    FASTQ format has 4 lines per sequence:
    1. Header line starting with '@'
    2. Sequence line
    3. Plus line starting with '+'
    4. Quality line (same length as sequence)

    Phred quality scores: Q = -10 * log10(P)
    Common ASCII offset: 33 (Sanger/Illumina 1.8+)

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is total string length
    """
    # Input validation
    if not isinstance(fastq_str, str):
        raise TypeError(f"fastq_str must be a string, got {type(fastq_str).__name__}")
    if min_quality is not None and not isinstance(min_quality, int):
        raise TypeError(
            f"min_quality must be an integer or None, got {type(min_quality).__name__}"
        )

    if len(fastq_str.strip()) == 0:
        raise ValueError("fastq_str cannot be empty")
    if min_quality is not None and min_quality < 0:
        raise ValueError(f"min_quality must be non-negative, got {min_quality}")

    lines = fastq_str.strip().split("\n")

    if len(lines) % 4 != 0:
        raise ValueError(
            f"FASTQ format requires 4 lines per sequence, got {len(lines)} lines"
        )

    fasta_entries = []

    # Process each FASTQ record (4 lines per record)
    for i in range(0, len(lines), 4):
        if i + 3 >= len(lines):
            break

        header_line = lines[i]
        sequence_line = lines[i + 1]
        plus_line = lines[i + 2]
        quality_line = lines[i + 3]

        # Validate format
        if not header_line.startswith("@"):
            raise ValueError(
                f"FASTQ header must start with '@', got: {header_line[:20]}"
            )
        if not plus_line.startswith("+"):
            raise ValueError(
                f"FASTQ separator must start with '+', got: {plus_line[:20]}"
            )
        if len(sequence_line) != len(quality_line):
            raise ValueError(
                f"Sequence and quality lengths must match: {len(sequence_line)} vs {len(quality_line)}"
            )

        # Apply quality filtering if requested
        if min_quality is not None:
            # Calculate average quality (assuming Phred+33 encoding)
            qualities = [ord(q) - 33 for q in quality_line]
            avg_quality = sum(qualities) / len(qualities) if qualities else 0

            if avg_quality < min_quality:
                continue  # Skip this sequence

        # Convert header from @ to >
        fasta_header = ">" + header_line[1:]
        fasta_entries.append(f"{fasta_header}\n{sequence_line}")

    if len(fasta_entries) == 0:
        return ""

    return "\n".join(fasta_entries) + "\n"


__all__ = ["fastq_to_fasta"]
