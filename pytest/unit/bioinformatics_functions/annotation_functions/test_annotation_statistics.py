import pytest
from bioinformatics_functions.annotation_functions.annotation_statistics import annotation_statistics


def test_annotation_statistics_typical() -> None:
    """
    Test case 1: Typical annotation statistics calculation.
    """
    annots: list[dict[str, object]] = [
        {'feature': 'exon', 'start': 10, 'end': 20},
        {'feature': 'intron', 'start': 21, 'end': 30},
        {'feature': 'exon', 'start': 31, 'end': 40},
    ]
    result = annotation_statistics(annots)
    assert isinstance(result, dict)
    assert result['feature_counts'] == {'exon': 2, 'intron': 1}
    assert result['total_coverage'] == (20-10+1) + (30-21+1) + (40-31+1)


def test_annotation_statistics_missing_fields() -> None:
    """
    Test case 2: Annotation records missing start/end fields.
    """
    annots: list[dict[str, object]] = [
        {'feature': 'exon'},
        {'feature': 'intron', 'start': 5},
        {'feature': 'exon', 'end': 10},
    ]
    result = annotation_statistics(annots)
    assert result['feature_counts'] == {'exon': 2, 'intron': 1}
    assert result['total_coverage'] == 0


def test_annotation_statistics_empty() -> None:
    """
    Test case 3: Empty annotation list returns zero counts and coverage.
    """
    annots: list[dict[str, object]] = []
    result = annotation_statistics(annots)
    assert result['feature_counts'] == {}
    assert result['total_coverage'] == 0


def test_annotation_statistics_type_error() -> None:
    """
    Test case 4: TypeError for non-list/tuple input.
    """
    with pytest.raises(TypeError):
        annotation_statistics('not a list')
