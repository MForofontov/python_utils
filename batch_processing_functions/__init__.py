"""
Batch Processing functions module: Efficient batch data processing utilities.

This module provides utilities for processing large datasets in chunks,
streaming aggregation, and memory-aware batch operations.
"""

from .chunked_processor import ChunkedProcessor, chunked_processor
from .streaming_aggregator import StreamingAggregator

__all__ = [
    "chunked_processor",
    "ChunkedProcessor",
    "StreamingAggregator",
]

__version__ = "1.0.0"
