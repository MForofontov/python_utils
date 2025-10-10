import pytest
from bioinformatics_functions.annotation_functions.annotation_to_bed import (
    annotation_to_bed,
)


def test_annotation_to_bed_typical() -> None:
    """
    Test case 1: Typical conversion to BED format.
    """
    annots: list[dict[str, object]] = [
        {"seqname": "chr1", "start": 10, "end": 20, "feature": "exon"},
        {"seqname": "chr2", "start": 5, "end": 15, "feature": "intron"},
    ]
    result = annotation_to_bed(annots)
    assert isinstance(result, list)
    assert result == ["chr1\t9\t20\texon", "chr2\t4\t15\tintron"]


def test_annotation_to_bed_chrom_key() -> None:
    """
    Test case 2: Accepts 'chrom' as alternative to 'seqname'.
    """
    annots: list[dict[str, object]] = [
        {"chrom": "chrX", "start": 1, "end": 100, "feature": "gene"}
    ]
    result = annotation_to_bed(annots)
    assert result == ["chrX\t0\t100\tgene"]


def test_annotation_to_bed_missing_feature() -> None:
    """
    Test case 3: Missing 'feature' key defaults to '.'.
    """
    annots: list[dict[str, object]] = [{"seqname": "chr1", "start": 2, "end": 5}]
    result = annotation_to_bed(annots)
    assert result == ["chr1\t1\t5\t."]


def test_annotation_to_bed_empty() -> None:
    """
    Test case 4: Empty annotation list returns empty list.
    """
    annots: list[dict[str, object]] = []
    result = annotation_to_bed(annots)
    assert result == []


def test_annotation_to_bed_type_error() -> None:
    """
    Test case 5: TypeError for non-list/tuple input.
    """
    with pytest.raises(TypeError):
        annotation_to_bed("not a list")


def test_annotation_to_bed_key_error() -> None:
    """
    Test case 6: KeyError for missing required keys.
    """
    annots: list[dict[str, object]] = [{"start": 1, "end": 2}]
    with pytest.raises(KeyError):
        annotation_to_bed(annots)
