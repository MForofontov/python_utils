import os
import tempfile

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.annotation_functions.parse_gtf import parse_gtf


def test_parse_gtf_typical() -> None:
    """
    Test case 1: Parse a valid GTF file.
    """
    gtf_content = 'chr1\tENSEMBL\tgene\t1\t100\t.\t+\t.\tgene_id "abc";'
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(gtf_content)
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_gtf(tmp_name))
        assert isinstance(result, list)
        assert result[0]["seqname"] == "chr1"
        assert result[0]["feature"] == "gene"
        assert result[0]["start"] == 1
        assert result[0]["end"] == 100
        assert "attribute" in result[0]
    finally:
        os.remove(tmp_name)


def test_parse_gtf_empty_file() -> None:
    """
    Test case 2: Empty GTF file yields no records.
    """
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_gtf(tmp_name))
        assert result == []
    finally:
        os.remove(tmp_name)


def test_parse_gtf_comment_and_invalid_lines() -> None:
    """
    Test case 3: GTF file with comment and invalid lines.
    """
    gtf_content = (
        '# comment\nchr1\tENSEMBL\tgene\t1\t100\t.\t+\t.\tgene_id "abc";\ninvalid_line'
    )
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(gtf_content)
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_gtf(tmp_name))
        assert len(result) == 1
        assert result[0]["seqname"] == "chr1"
    finally:
        os.remove(tmp_name)


def test_parse_gtf_type_error() -> None:
    """
    Test case 4: TypeError for non-string input.
    """
    with pytest.raises(TypeError):
        list(parse_gtf(123))


def test_parse_gtf_file_not_found() -> None:
    """
    Test case 5: FileNotFoundError for missing file.
    """
    with pytest.raises(FileNotFoundError):
        list(parse_gtf("nonexistent_file.gtf"))
