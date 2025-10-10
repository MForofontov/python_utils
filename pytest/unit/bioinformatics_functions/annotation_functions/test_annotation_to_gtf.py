import pytest
from bioinformatics_functions.annotation_functions.annotation_to_gtf import (
    annotation_to_gtf,
)


def test_annotation_to_gtf_basic_conversion() -> None:
    """
    Test case 1: Basic conversion of annotation records to GTF format.
    """
    annotations = [
        {
            "seqid": "chr1",
            "source": ".",
            "feature": "exon",
            "start": 1,
            "end": 100,
            "score": ".",
            "strand": "+",
            "frame": ".",
            "attribute": 'gene_id "gene1";',
        },
        {
            "seqid": "chr2",
            "source": "source",
            "feature": "gene",
            "start": 200,
            "end": 300,
            "score": "0.5",
            "strand": "-",
            "frame": "0",
            "attribute": 'gene_id "gene2";',
        },
    ]
    expected = [
        'chr1\t.\texon\t1\t100\t.\t+\t.\tgene_id "gene1";',
        'chr2\tsource\tgene\t200\t300\t0.5\t-\t0\tgene_id "gene2";',
    ]
    result = annotation_to_gtf(annotations)
    assert result == expected


def test_annotation_to_gtf_empty_input() -> None:
    """
    Test case 2: Conversion with empty input list.
    """
    assert annotation_to_gtf([]) == []


def test_annotation_to_gtf_boundary_values() -> None:
    """
    Test case 3: Conversion with minimal and maximal field values.
    """
    annotations = [
        {
            "seqid": "",
            "source": "",
            "feature": "",
            "start": 0,
            "end": 999999,
            "score": "",
            "strand": ".",
            "frame": "",
            "attribute": "",
        }
    ]
    expected = ["\t\t\t0\t999999\t\t.\t\t"]
    result = annotation_to_gtf(annotations)
    assert result == expected


def test_annotation_to_gtf_missing_required_key() -> None:
    """
    Test case 4: Error raised when a required key is missing.
    """
    annotations = [
        {
            "seqid": "chr1",
            "source": ".",
            "feature": "exon",
            "start": 1,
            "end": 100,
            "score": ".",
            "strand": "+",
            "frame": ".",  # 'attribute' missing
        }
    ]
    with pytest.raises(KeyError, match=r"Missing required GTF key: attribute"):
        annotation_to_gtf(annotations)


def test_annotation_to_gtf_invalid_input_type() -> None:
    """
    Test case 5: Error raised when input is not a list or tuple.
    """
    with pytest.raises(TypeError, match=r"annotations must be a list or tuple"):
        annotation_to_gtf("not_a_list")  # type: ignore[arg-type]


def test_annotation_to_gtf_invalid_record_type() -> None:
    """
    Test case 6: Error raised when a record is not a dict.
    """
    annotations = ["not_a_dict"]
    with pytest.raises(TypeError, match=r"record must be a dict"):
        # Patch annotation_to_gtf to raise TypeError for non-dict records
        # For now, this will raise KeyError for missing keys, but best practice is TypeError
        try:
            annotation_to_gtf(annotations)
        except KeyError as e:
            # If KeyError is raised, fail the test with a message
            pytest.fail(f"Expected TypeError for non-dict record, got KeyError: {e}")
