import pytest
from typing import Any
from bioinformatics_functions.annotation_functions.merge_annotations import merge_annotations

def test_merge_annotations_typical() -> None:
    """
    Test case 1: Merge multiple annotation dicts.
    """
    annots: list[dict[str, Any]] = [
        {'gene': 'abc', 'start': 1, 'end': 100},
        {'exon': 1, 'start': 1, 'end': 50}
    ]
    result = merge_annotations(annots)
    assert isinstance(result, dict)
    assert result['gene'] == 'abc'
    assert result['exon'] == 1
    assert result['start'] == 1
    assert result['end'] == 50

def test_merge_annotations_type_error() -> None:
    """
    Test case 2: TypeError for non-dict in annotations.
    """
    annots = [{'gene': 'abc'}, 42]  # 42 is not a dict
    with pytest.raises(TypeError, match="All annotations must be dictionaries"):
        merge_annotations(annots)  # type: ignore[arg-type]
