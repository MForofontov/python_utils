import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from pyutils_collection.bioinformatics_functions.annotation_functions.sort_annotations import (
    sort_annotations,
)


def test_sort_annotations_typical() -> None:
    """
    Test case 1: Sort by start ascending.
    """
    annots: list[dict[str, object]] = [{"start": 10}, {"start": 5}, {"start": 20}]
    result = sort_annotations(annots)
    assert result == [{"start": 5}, {"start": 10}, {"start": 20}]


def test_sort_annotations_reverse() -> None:
    """
    Test case 2: Sort by start descending.
    """
    annots: list[dict[str, object]] = [{"start": 10}, {"start": 5}, {"start": 20}]
    result = sort_annotations(annots, reverse=True)
    assert result == [{"start": 20}, {"start": 10}, {"start": 5}]


def test_sort_annotations_by_key() -> None:
    """
    Test case 3: Sort by custom key.
    """
    annots: list[dict[str, object]] = [{"end": 2}, {"end": 1}]
    result = sort_annotations(annots, by="end")
    assert result == [{"end": 1}, {"end": 2}]


def test_sort_annotations_type_error() -> None:
    """
    Test case 4: TypeError for non-list input.
    """
    with pytest.raises(TypeError):
        sort_annotations("not a list")


def test_sort_annotations_key_error() -> None:
    """
    Test case 5: KeyError for missing sort key.
    """
    annots: list[dict[str, object]] = [{"start": 1}, {}]
    with pytest.raises(KeyError):
        sort_annotations(annots)


def test_sort_annotations_by_type_error() -> None:
    """
    Test case 6: TypeError for non-string 'by' parameter.
    """
    annots: list[dict[str, object]] = [{"start": 1}]
    with pytest.raises(TypeError, match="by must be a string"):
        sort_annotations(annots, by=123)  # type: ignore


def test_sort_annotations_reverse_type_error() -> None:
    """
    Test case 7: TypeError for non-boolean 'reverse' parameter.
    """
    annots: list[dict[str, object]] = [{"start": 1}]
    with pytest.raises(TypeError, match="reverse must be a boolean"):
        sort_annotations(annots, reverse="yes")  # type: ignore
