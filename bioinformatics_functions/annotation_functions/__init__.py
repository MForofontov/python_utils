"""
annotation_functions: Sequence annotation utilities.
"""

from .merge_annotations import merge_annotations
from .parse_gff import parse_gff
from .parse_bed import parse_bed
from .feature_extractor import extract_features

__all__ = [
    "merge_annotations",
    "parse_gff",
    "parse_bed",
    "extract_features",
]
