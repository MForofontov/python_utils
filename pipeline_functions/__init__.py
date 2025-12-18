"""
Pipeline functions module: Composable data transformation pipelines.

This module provides utilities for building functional data processing
pipelines with transformation steps that can be composed and reused.
"""

from .pipeline_builder import Pipeline, pipeline_builder

__all__ = [
    "Pipeline",
    "pipeline_builder",
]

__version__ = "1.0.0"
