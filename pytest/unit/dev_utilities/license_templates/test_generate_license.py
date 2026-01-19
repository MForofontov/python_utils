"""
Test case 1: Test license generation functionality.
"""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.dev_utilities]
from python_utils.dev_utilities.license_templates.generate_license import (
    generate_license,
    save_license_file,
)


def test_generate_license_mit() -> None:
    """
    Test case 1: Generate MIT license successfully.
    """
    # Arrange
    author = "John Doe"
    year = 2024

    # Act
    result = generate_license("MIT", author, year)

    # Assert
    assert "MIT License" in result
    assert f"Copyright (c) {year} {author}" in result
    assert "Permission is hereby granted" in result


def test_generate_license_apache() -> None:
    """
    Test case 2: Generate Apache 2.0 license successfully.
    """
    # Arrange
    author = "Jane Smith"
    year = 2023

    # Act
    result = generate_license("Apache-2.0", author, year)

    # Assert
    assert "Apache License" in result
    assert f"Copyright {year} {author}" in result
    assert "http://www.apache.org/licenses/" in result


def test_generate_license_gpl() -> None:
    """
    Test case 3: Generate GPL 3.0 license successfully.
    """
    # Arrange
    author = "Bob Johnson"
    year = 2024
    project_name = "MyProject"

    # Act
    result = generate_license("GPL-3.0", author, year, project_name)

    # Assert
    assert f"Copyright (C) {year} {author}" in result
    assert project_name in result
    assert "GNU General Public License" in result


def test_generate_license_bsd3() -> None:
    """
    Test case 4: Generate BSD 3-Clause license successfully.
    """
    # Arrange
    author = "Alice Brown"
    year = 2024

    # Act
    result = generate_license("BSD-3-Clause", author, year)

    # Assert
    assert "BSD 3-Clause License" in result
    assert f"Copyright (c) {year}, {author}" in result
    assert "Redistribution and use" in result


def test_generate_license_invalid_type_raises_error() -> None:
    """
    Test case 5: ValueError for invalid license type.
    """
    # Arrange
    invalid_type = "INVALID"
    expected_message = "license_type must be one of"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_license(invalid_type, "Author")  # type: ignore


def test_generate_license_empty_author_raises_error() -> None:
    """
    Test case 6: ValueError for empty author name.
    """
    # Arrange
    empty_author = "   "
    expected_message = "author cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_license("MIT", empty_author)


def test_generate_license_invalid_year_raises_error() -> None:
    """
    Test case 7: ValueError for invalid year.
    """
    # Arrange
    invalid_year = 1800
    expected_message = "year must be between 1900 and"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        generate_license("MIT", "Author", invalid_year)


def test_generate_license_default_current_year() -> None:
    """
    Test case 8: Use current year when year is None.
    """
    # Arrange
    author = "Test Author"
    current_year = datetime.now().year

    # Act
    result = generate_license("MIT", author, year=None)

    # Assert
    assert f"{current_year}" in result


def test_save_license_file_creates_file() -> None:
    """
    Test case 9: Save license file successfully.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "LICENSE"

        # Act
        save_license_file("MIT", "Test Author", output_path, 2024)

        # Assert
        assert output_path.exists()
        content = output_path.read_text()
        assert "MIT License" in content


def test_generate_license_invalid_author_type_raises_error() -> None:
    """
    Test case 10: TypeError for invalid author type.
    """
    # Arrange
    invalid_author = 123
    expected_message = "author must be str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        generate_license("MIT", invalid_author)  # type: ignore


def test_generate_license_bsd2() -> None:
    """
    Test case 11: Generate BSD 2-Clause license successfully.
    """
    # Arrange
    author = "Developer Name"
    year = 2024

    # Act
    result = generate_license("BSD-2-Clause", author, year)

    # Assert
    assert "BSD 2-Clause License" in result
    assert f"Copyright (c) {year}, {author}" in result
