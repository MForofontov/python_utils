"""
Avro operations module.

Provides utilities for validating data against Apache Avro schemas.
"""

from .validate_avro_data import validate_avro_data

__all__ = [
    'validate_avro_data',
]
