"""
Batch processing functions module: Memory-efficient batch processing patterns.

This module provides utilities for processing large datasets efficiently with
backpressure control, streaming aggregation, and memory management.
"""

from .chunked_processor import chunked_processor
from .streaming_aggregator import StreamingAggregator

__all__ = [
    "chunked_processor",
    "StreamingAggregator",
]

__version__ = "1.0.0"
