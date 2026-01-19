import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.annotation_functions.filter_annotations import (
    filter_annotations,
)


def test_filter_annotations_typical() -> None:
    """
    Test case 1: Typical filtering by feature.
    """
    annots = [
        {"feature": "exon", "start": 1, "end": 100},
        {"feature": "intron", "start": 101, "end": 200},
        {"feature": "exon", "start": 201, "end": 300},
    ]
    result = list(filter_annotations(annots, feature_type="exon"))
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(a["feature"] == "exon" for a in result)


def test_filter_annotations_empty() -> None:
    """
    Test case 2: Empty annotation list returns empty list.
    """
    result = list(filter_annotations([], feature_type="exon"))
    assert result == []


def test_filter_annotations_missing_feature() -> None:
    """
    Test case 3: Filtering with feature not present returns empty list.
    """
    annots = [{"feature": "intron", "start": 101, "end": 200}]
    result = list(filter_annotations(annots, feature_type="exon"))
    assert result == []


def test_filter_annotations_type_error() -> None:
    """
    Test case 4: TypeError for non-list/tuple input.
    """
    with pytest.raises(TypeError):
        list(filter_annotations("not a list", feature_type="exon"))
