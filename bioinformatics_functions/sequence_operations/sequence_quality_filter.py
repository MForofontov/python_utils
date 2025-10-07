from typing import Any


def sequence_quality_filter(
    seq: str,
    min_length: int | None = None,
    max_length: int | None = None,
    min_gc: float | None = None,
    max_gc: float | None = None,
    max_n_content: float | None = None
) -> dict[str, Any]:
    """
    Filter sequence based on quality metrics and return detailed report.

    Parameters
    ----------
    seq : str
        DNA sequence to evaluate.
    min_length : int | None, optional
        Minimum allowed sequence length (by default None).
    max_length : int | None, optional
        Maximum allowed sequence length (by default None).
    min_gc : float | None, optional
        Minimum GC content percentage (0-100) (by default None).
    max_gc : float | None, optional
        Maximum GC content percentage (0-100) (by default None).
    max_n_content : float | None, optional
        Maximum N content percentage (0-100) (by default None).

    Returns
    -------
    dict[str, Any]
        Report containing:
        - 'passes_filter': bool, whether sequence passes all filters
        - 'length': int, sequence length
        - 'gc_content': float, GC content percentage
        - 'n_content': float, N content percentage
        - 'failed_filters': list[str], list of failed filter names

    Raises
    ------
    TypeError
        If seq is not a string.
        If numeric parameters are not int/float or None.
    ValueError
        If min/max values are invalid or out of range.

    Examples
    --------
    >>> sequence_quality_filter("ATGCATGC", min_length=5)
    {'passes_filter': True, 'length': 8, 'gc_content': 50.0, ...}
    >>> sequence_quality_filter("AT", min_length=5)
    {'passes_filter': False, 'length': 2, 'failed_filters': ['min_length'], ...}
    >>> sequence_quality_filter("NNNATGC", max_n_content=20.0)
    {'passes_filter': False, 'n_content': 42.86, 'failed_filters': ['max_n_content'], ...}

    Notes
    -----
    Filters are optional - only specified filters are applied.
    Case-insensitive for base detection.
    
    Complexity
    ----------
    Time: O(n), Space: O(1) where n is sequence length
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")
    
    for param_name, param_value in [
        ('min_length', min_length), ('max_length', max_length),
        ('min_gc', min_gc), ('max_gc', max_gc), ('max_n_content', max_n_content)
    ]:
        if param_value is not None and not isinstance(param_value, (int, float)):
            raise TypeError(f"{param_name} must be a number or None, got {type(param_value).__name__}")
    
    if min_length is not None and min_length < 0:
        raise ValueError(f"min_length must be non-negative, got {min_length}")
    if max_length is not None and max_length < 0:
        raise ValueError(f"max_length must be non-negative, got {max_length}")
    if min_length is not None and max_length is not None and min_length > max_length:
        raise ValueError(f"min_length ({min_length}) cannot be greater than max_length ({max_length})")
    
    for param_name, param_value in [('min_gc', min_gc), ('max_gc', max_gc), ('max_n_content', max_n_content)]:
        if param_value is not None and not (0.0 <= param_value <= 100.0):
            raise ValueError(f"{param_name} must be between 0 and 100, got {param_value}")
    
    if min_gc is not None and max_gc is not None and min_gc > max_gc:
        raise ValueError(f"min_gc ({min_gc}) cannot be greater than max_gc ({max_gc})")
    
    # Calculate metrics
    seq_upper = seq.upper()
    length = len(seq)
    
    gc_count = sum(1 for base in seq_upper if base in 'GC')
    gc_content = (gc_count / length * 100.0) if length > 0 else 0.0
    
    n_count = seq_upper.count('N')
    n_content = (n_count / length * 100.0) if length > 0 else 0.0
    
    # Apply filters
    failed_filters = []
    
    if min_length is not None and length < min_length:
        failed_filters.append('min_length')
    if max_length is not None and length > max_length:
        failed_filters.append('max_length')
    if min_gc is not None and gc_content < min_gc:
        failed_filters.append('min_gc')
    if max_gc is not None and gc_content > max_gc:
        failed_filters.append('max_gc')
    if max_n_content is not None and n_content > max_n_content:
        failed_filters.append('max_n_content')
    
    passes_filter = len(failed_filters) == 0
    
    report: dict[str, Any] = {
        'passes_filter': passes_filter,
        'length': length,
        'gc_content': round(gc_content, 2),
        'n_content': round(n_content, 2),
        'failed_filters': failed_filters
    }
    
    return report


__all__ = ['sequence_quality_filter']
