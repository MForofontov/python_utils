import pytest
from bioinformatics_functions.annotation_functions.parse_bed import parse_bed

def test_parse_bed_typical() -> None:
    """
    Test case 1: Parse a valid BED string.
    """
    bed_str = 'chr1\t1\t100\tfeature1\nchr2\t5\t50\tfeature2'
    result = list(parse_bed(bed_str))
    assert isinstance(result, list)
    assert result[0]['chrom'] == 'chr1'
    assert result[0]['start'] == 1
    assert result[0]['end'] == 100
    assert result[0]['name'] == 'feature1'
    assert result[1]['chrom'] == 'chr2'
    assert result[1]['start'] == 5
    assert result[1]['end'] == 50
    assert result[1]['name'] == 'feature2'

def test_parse_bed_empty() -> None:
    """
    Test case 2: Empty BED string yields no records.
    """
    bed_str = ''
    result = list(parse_bed(bed_str))
    assert result == []

def test_parse_bed_comment() -> None:
    """
    Test case 3: BED string with comment line is ignored.
    """
    bed_str = '# comment\nchr1\t1\t100\tfeature1'
    result = list(parse_bed(bed_str))
    assert len(result) == 1
    assert result[0]['chrom'] == 'chr1'

def test_parse_bed_type_error() -> None:
    """
    Test case 4: TypeError for non-string input.
    """
    with pytest.raises(TypeError):
        list(parse_bed(123))

def test_parse_bed_value_error() -> None:
    """
    Test case 5: ValueError for invalid BED line.
    """
    bed_str = 'chr1\t1'
    with pytest.raises(ValueError):
        list(parse_bed(bed_str))
