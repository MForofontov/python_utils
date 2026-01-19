import os
import tempfile

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from python_utils.bioinformatics_functions.annotation_functions.parse_gff import parse_gff


def test_parse_gff_typical() -> None:
    """
    Test case 1: Parse a valid GFF file.
    """
    gff_content = "chr1\tRefSeq\tgene\t1\t100\t.\t+\t.\tID=gene1;Name=abc"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(gff_content)
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_gff(tmp_name))
        assert isinstance(result, list)
        assert result[0]["seqid"] == "chr1"
        assert result[0]["type"] == "gene"
        assert result[0]["start"] == 1
        assert result[0]["end"] == 100
        assert result[0]["attributes"]["ID"] == "gene1"
        assert result[0]["attributes"]["Name"] == "abc"
    finally:
        os.remove(tmp_name)


def test_parse_gff_empty_file() -> None:
    """
    Test case 2: Empty GFF file yields no records.
    """
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_gff(tmp_name))
        assert result == []
    finally:
        os.remove(tmp_name)


def test_parse_gff_comment_and_invalid_lines() -> None:
    """
    Test case 3: GFF file with comment and invalid lines.
    """
    gff_content = "# comment\nchr1\tRefSeq\tgene\t1\t100\t.\t+\t.\tID=gene1;Name=abc\ninvalid_line"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(gff_content)
        tmp.flush()
        tmp_name = tmp.name
    try:
        with pytest.raises(ValueError):
            list(parse_gff(tmp_name))
    finally:
        os.remove(tmp_name)


def test_parse_gff_type_error() -> None:
    """
    Test case 4: TypeError for non-string input.
    """
    with pytest.raises(TypeError):
        list(parse_gff(123))


def test_parse_gff_file_not_found() -> None:
    """
    Test case 5: FileNotFoundError for missing file.
    """
    with pytest.raises(FileNotFoundError):
        list(parse_gff("nonexistent_file.gff"))
