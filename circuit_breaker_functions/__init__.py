"""
Circuit Breaker functions module: Resilience and fault tolerance patterns.

This module provides utilities for implementing circuit breakers, bulkheads,
adaptive timeouts, and fallback chains for robust distributed systems.
"""

from .adaptive_timeout import AdaptiveTimeout
from .bulkhead import Bulkhead
from .circuit_breaker import CircuitBreaker, CircuitState
from .fallback_chain import FallbackChain, fallback_chain

__all__ = [
    "CircuitBreaker",
    "CircuitState",
    "Bulkhead",
    "AdaptiveTimeout",
    "FallbackChain",
    "fallback_chain",
]

__version__ = "1.0.0"
