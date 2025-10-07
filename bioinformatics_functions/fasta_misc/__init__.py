"""
fasta_misc: Miscellaneous FASTA-related utilities.
"""

from .degenerate_primer_generator import degenerate_primer_generator
from .generate_primers import generate_primers

__all__ = [
    "degenerate_primer_generator",
    "generate_primers",
]
