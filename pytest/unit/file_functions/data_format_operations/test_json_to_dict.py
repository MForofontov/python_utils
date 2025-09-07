import json
from pathlib import Path

import pytest

from file_functions.json_to_dict import json_to_dict


def test_json_to_dict_reads_valid_json(tmp_path: Path) -> None:
    """Test case 1: Ensure valid JSON is parsed into a dictionary."""
    data: dict[str, object] = {"a": 1, "b": [1, 2]}
    file: Path = tmp_path / "sample.json"
    file.write_text(json.dumps(data))
    result: dict[str, object] = json_to_dict(str(file))
    assert result == data


def test_json_to_dict_empty_file_raises_jsondecodeerror(tmp_path: Path) -> None:
    """Test case 2: Empty file should raise JSONDecodeError."""
    file: Path = tmp_path / "empty.json"
    file.write_text("")
    with pytest.raises(json.JSONDecodeError):
        json_to_dict(str(file))


def test_json_to_dict_missing_file_raises_filenotfounderror(tmp_path: Path) -> None:
    """Test case 3: Missing file should raise FileNotFoundError."""
    missing_file: Path = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        json_to_dict(str(missing_file))
