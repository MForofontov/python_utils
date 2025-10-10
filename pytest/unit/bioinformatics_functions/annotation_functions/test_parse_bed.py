import os
import tempfile

import pytest
from bioinformatics_functions.annotation_functions.parse_bed import parse_bed


def test_parse_bed_typical() -> None:
    """
    Test case 1: Parse a valid BED file.
    """
    bed_content = "chr1\t1\t100\tfeature1\nchr2\t5\t50\tfeature2"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(bed_content)
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_bed(tmp_name))
        assert isinstance(result, list)
        assert result[0]["chrom"] == "chr1"
        assert result[0]["start"] == 1
        assert result[0]["end"] == 100
        assert result[0]["name"] == "feature1"
        assert result[1]["chrom"] == "chr2"
        assert result[1]["start"] == 5
        assert result[1]["end"] == 50
        assert result[1]["name"] == "feature2"
    finally:
        os.remove(tmp_name)


def test_parse_bed_empty_file() -> None:
    """
    Test case 2: Empty BED file yields no records.
    """
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_bed(tmp_name))
        assert result == []
    finally:
        os.remove(tmp_name)


def test_parse_bed_comment_and_invalid_lines() -> None:
    """
    Test case 3: BED file with comment and invalid lines.
    """
    bed_content = "# comment\nchr1\t1\t100\tfeature1\nchr2\t5"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(bed_content)
        tmp.flush()
        tmp_name = tmp.name
    try:
        with pytest.raises(ValueError):
            list(parse_bed(tmp_name))
    finally:
        os.remove(tmp_name)


def test_parse_bed_type_error() -> None:
    """
    Test case 4: TypeError for non-string input.
    """
    with pytest.raises(TypeError):
        list(parse_bed(123))


def test_parse_bed_file_not_found() -> None:
    """
    Test case 5: FileNotFoundError for missing file.
    """
    with pytest.raises(FileNotFoundError):
        list(parse_bed("nonexistent_file.bed"))
