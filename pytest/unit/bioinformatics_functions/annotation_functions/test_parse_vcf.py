import os
import tempfile

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.bioinformatics]
from bioinformatics_functions.annotation_functions.parse_vcf import parse_vcf


def test_parse_vcf_typical() -> None:
    """
    Test case 1: Parse a valid VCF file.
    """
    vcf_content = "# header\nchr1\t12345\trs1\tA\tT\t99\tPASS\tDP=100"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(vcf_content)
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_vcf(tmp_name))
        assert isinstance(result, list)
        assert result[0]["chrom"] == "chr1"
        assert result[0]["pos"] == 12345
        assert result[0]["id"] == "rs1"
        assert result[0]["ref"] == "A"
        assert result[0]["alt"] == "T"
        assert result[0]["qual"] == "99"
        assert result[0]["filter"] == "PASS"
        assert result[0]["info"] == "DP=100"
    finally:
        os.remove(tmp_name)


def test_parse_vcf_empty_file() -> None:
    """
    Test case 2: Empty VCF file yields no records.
    """
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_vcf(tmp_name))
        assert result == []
    finally:
        os.remove(tmp_name)


def test_parse_vcf_comment_and_invalid_lines() -> None:
    """
    Test case 3: VCF file with comment and invalid lines.
    """
    vcf_content = "# comment\nchr1\t12345\trs1\tA\tT\t99\tPASS\tDP=100\ninvalid_line"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(vcf_content)
        tmp.flush()
        tmp_name = tmp.name
    try:
        result = list(parse_vcf(tmp_name))
        assert len(result) == 1
        assert result[0]["chrom"] == "chr1"
    finally:
        os.remove(tmp_name)


def test_parse_vcf_type_error() -> None:
    """
    Test case 4: TypeError for non-string input.
    """
    with pytest.raises(TypeError):
        list(parse_vcf(123))


def test_parse_vcf_file_not_found() -> None:
    """
    Test case 5: FileNotFoundError for missing file.
    """
    with pytest.raises(FileNotFoundError):
        list(parse_vcf("nonexistent_file.vcf"))
