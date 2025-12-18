"""
Circuit breaker functions module: Resilience patterns for fault tolerance.

This module provides production-ready resilience patterns to prevent cascading
failures in distributed systems and handle service degradation gracefully.
"""

from .adaptive_timeout import adaptive_timeout
from .bulkhead import Bulkhead
from .circuit_breaker import CircuitBreaker
from .fallback_chain import fallback_chain

__all__ = [
    "CircuitBreaker",
    "Bulkhead",
    "adaptive_timeout",
    "fallback_chain",
]

__version__ = "1.0.0"
