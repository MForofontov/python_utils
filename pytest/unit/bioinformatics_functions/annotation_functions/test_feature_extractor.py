import pytest
from bioinformatics_functions.annotation_functions.extract_features import feature_extractor

def test_feature_extractor_typical() -> None:
    """
    Test case 1: Typical feature extraction.
    """
    annots = [
        {'feature': 'exon', 'start': 1, 'end': 100},
        {'feature': 'intron', 'start': 101, 'end': 200}
    ]
    result = feature_extractor(annots, 'exon')
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['feature'] == 'exon'

def test_feature_extractor_empty() -> None:
    """
    Test case 2: Empty annotation list returns empty list.
    """
    result = feature_extractor([], 'exon')
    assert result == []

def test_feature_extractor_missing_feature() -> None:
    """
    Test case 3: Feature not present returns empty list.
    """
    annots = [{'feature': 'intron', 'start': 101, 'end': 200}]
    result = feature_extractor(annots, 'exon')
    assert result == []

def test_feature_extractor_type_error() -> None:
    """
    Test case 4: TypeError for non-list/tuple input.
    """
    with pytest.raises(TypeError):
        feature_extractor('not a list', 'exon')
