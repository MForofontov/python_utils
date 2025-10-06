import pytest
from bioinformatics_functions.annotation_functions.annotation_to_gff import annotation_to_gff

def test_annotation_to_gff_basic_conversion() -> None:
    """
    Test case 1: Basic conversion to GFF format.
    """
    annotations = [
        {'seqid': 'chr1', 'source': '.', 'feature': 'exon', 'start': 1, 'end': 100, 'score': '.', 'strand': '+', 'frame': '.', 'attribute': 'gene_id "gene1";'},
        {'seqid': 'chr2', 'source': 'source', 'feature': 'gene', 'start': 200, 'end': 300, 'score': '0.5', 'strand': '-', 'frame': '0', 'attribute': 'gene_id "gene2";'}
    ]
    result = annotation_to_gff(annotations)
    assert isinstance(result, list)
    assert result[0].startswith('chr1')
    assert result[1].startswith('chr2')

def test_annotation_to_gff_empty_input() -> None:
    """
    Test case 2: Empty input returns empty list.
    """
    assert annotation_to_gff([]) == []

def test_annotation_to_gff_missing_key_error() -> None:
    """
    Test case 3: Missing required key raises KeyError.
    """
    annotations = [{'seqid': 'chr1', 'source': '.', 'feature': 'exon'}]
    with pytest.raises(KeyError):
        annotation_to_gff(annotations)

def test_annotation_to_gff_type_error_non_list_input() -> None:
    """
    Test case 4: Non-list input raises TypeError.
    """
    with pytest.raises(TypeError):
        annotation_to_gff('not_a_list')
