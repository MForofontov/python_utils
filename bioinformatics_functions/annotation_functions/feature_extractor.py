from typing import Sequence, Dict, Any

def extract_features(annotations: Sequence[Dict[str, Any]], feature_type: str) -> Sequence[Dict[str, Any]]:
    """
    Extract features of a given type from annotation dictionaries.

    Parameters
    ----------
    annotations : Sequence[Dict[str, Any]]
        List of annotation dictionaries.
    feature_type : str
        Feature type to extract (e.g., 'gene', 'exon').

    Returns
    -------
    Sequence[Dict[str, Any]]
        List of matching features.

    Raises
    ------
    TypeError
        If input is not a sequence of dicts.

    Examples
    --------
    >>> extract_features([
    ...     {'type': 'gene', 'start': 1},
    ...     {'type': 'exon', 'start': 2}
    ... ], 'gene')
    [{'type': 'gene', 'start': 1}]
    """
    if not all(isinstance(a, dict) for a in annotations):
        raise TypeError("All annotations must be dictionaries")
    return [a for a in annotations if a.get('type') == feature_type]

__all__ = ["extract_features"]
