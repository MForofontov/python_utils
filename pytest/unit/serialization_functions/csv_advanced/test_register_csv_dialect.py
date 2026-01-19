"""Tests for register_csv_dialect module."""

import csv

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.serialization]
from python_utils.serialization_functions.csv_advanced.register_csv_dialect import (
    register_csv_dialect,
)


def test_register_csv_dialect_basic() -> None:
    """
    Test case 1: Test basic dialect registration.
    """
    # Arrange
    dialect_name = "test_dialect_basic"

    # Act
    register_csv_dialect(dialect_name, delimiter="|")

    # Assert
    assert dialect_name in csv.list_dialects()

    # Cleanup
    csv.unregister_dialect(dialect_name)


def test_register_csv_dialect_custom_parameters() -> None:
    """
    Test case 2: Test registering dialect with custom parameters.
    """
    # Arrange
    dialect_name = "test_custom"

    # Act
    register_csv_dialect(
        dialect_name,
        delimiter="\t",
        quotechar="'",
        doublequote=False,
        skipinitialspace=True,
    )

    # Assert
    assert dialect_name in csv.list_dialects()
    dialect = csv.get_dialect(dialect_name)
    assert dialect.delimiter == "\t"
    assert dialect.quotechar == "'"

    # Cleanup
    csv.unregister_dialect(dialect_name)


def test_register_csv_dialect_can_be_used(tmp_path) -> None:
    """
    Test case 3: Test that registered dialect can be used in CSV operations.
    """
    # Arrange
    import io

    dialect_name = "test_usage"
    register_csv_dialect(dialect_name, delimiter="|")

    output = io.StringIO()
    writer = csv.writer(output, dialect=dialect_name)

    # Act
    writer.writerow(["A", "B", "C"])

    # Assert
    result = output.getvalue()
    assert "A|B|C" in result

    # Cleanup
    csv.unregister_dialect(dialect_name)


def test_register_csv_dialect_with_quoting() -> None:
    """
    Test case 4: Test registering dialect with different quoting styles.
    """
    # Arrange
    dialect_name = "test_quoting"

    # Act
    register_csv_dialect(dialect_name, quoting=csv.QUOTE_ALL)

    # Assert
    assert dialect_name in csv.list_dialects()

    # Cleanup
    csv.unregister_dialect(dialect_name)


def test_register_csv_dialect_with_line_terminator() -> None:
    """
    Test case 5: Test registering dialect with custom line terminator.
    """
    # Arrange
    dialect_name = "test_line_term"

    # Act
    register_csv_dialect(dialect_name, lineterminator="\n")

    # Assert
    assert dialect_name in csv.list_dialects()

    # Cleanup
    csv.unregister_dialect(dialect_name)


def test_register_csv_dialect_invalid_name_type_raises_error() -> None:
    """
    Test case 6: Test TypeError for invalid name type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="name must be a string"):
        register_csv_dialect(123)


def test_register_csv_dialect_invalid_delimiter_type_raises_error() -> None:
    """
    Test case 7: Test TypeError for invalid delimiter type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="delimiter must be a string"):
        register_csv_dialect("test", delimiter=123)


def test_register_csv_dialect_invalid_delimiter_length_raises_error() -> None:
    """
    Test case 8: Test ValueError for multi-character delimiter.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="delimiter must be a single character"):
        register_csv_dialect("test", delimiter="||")


def test_register_csv_dialect_invalid_quotechar_type_raises_error() -> None:
    """
    Test case 9: Test TypeError for invalid quotechar type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="quotechar must be a string"):
        register_csv_dialect("test", quotechar=123)


def test_register_csv_dialect_invalid_quotechar_length_raises_error() -> None:
    """
    Test case 10: Test ValueError for multi-character quotechar.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="quotechar must be a single character"):
        register_csv_dialect("test", quotechar='""')


def test_register_csv_dialect_invalid_doublequote_type_raises_error() -> None:
    """
    Test case 11: Test TypeError for invalid doublequote type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="doublequote must be a boolean"):
        register_csv_dialect("test", doublequote="yes")


def test_register_csv_dialect_invalid_skipinitialspace_type_raises_error() -> None:
    """
    Test case 12: Test TypeError for invalid skipinitialspace type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="skipinitialspace must be a boolean"):
        register_csv_dialect("test", skipinitialspace="yes")


def test_register_csv_dialect_invalid_lineterminator_type_raises_error() -> None:
    """
    Test case 13: Test TypeError for invalid lineterminator type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="lineterminator must be a string"):
        register_csv_dialect("test", lineterminator=123)


def test_register_csv_dialect_invalid_quoting_type_raises_error() -> None:
    """
    Test case 14: Test TypeError for invalid quoting type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="quoting must be an integer"):
        register_csv_dialect("test", quoting="invalid")
