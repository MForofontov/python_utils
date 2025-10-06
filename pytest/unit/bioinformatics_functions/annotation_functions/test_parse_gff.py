import pytest
from bioinformatics_functions.annotation_functions.parse_gff import parse_gff

def test_parse_gff_typical() -> None:
    """
    Test case 1: Parse a valid GFF string.
    """
    gff_str = 'chr1\tRefSeq\tgene\t1\t100\t.\t+\t.\tID=gene1;Name=abc'
    result = list(parse_gff(gff_str))
    assert isinstance(result, list)
    assert result[0]['seqid'] == 'chr1'
    assert result[0]['type'] == 'gene'
    assert result[0]['start'] == 1
    assert result[0]['end'] == 100
    assert result[0]['attributes']['ID'] == 'gene1'
    assert result[0]['attributes']['Name'] == 'abc'

def test_parse_gff_empty() -> None:
    """
    Test case 2: Empty GFF string yields no records.
    """
    gff_str = ''
    result = list(parse_gff(gff_str))
    assert result == []

def test_parse_gff_comment() -> None:
    """
    Test case 3: GFF string with comment line is ignored.
    """
    gff_str = '# comment\nchr1\tRefSeq\tgene\t1\t100\t.\t+\t.\tID=gene1;Name=abc'
    result = list(parse_gff(gff_str))
    assert len(result) == 1
    assert result[0]['seqid'] == 'chr1'

def test_parse_gff_type_error() -> None:
    """
    Test case 4: TypeError for non-string input.
    """
    with pytest.raises(TypeError):
        list(parse_gff(123))

def test_parse_gff_value_error() -> None:
    """
    Test case 5: ValueError for invalid GFF line.
    """
    gff_str = 'chr1\tRefSeq\tgene\t1\t100\t.\t+\t.'
    with pytest.raises(ValueError):
        list(parse_gff(gff_str))
