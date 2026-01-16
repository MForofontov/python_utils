"""Unit tests for format_currency function."""

import pytest
from formatting_functions.format_currency import format_currency


def test_format_currency_default_usd() -> None:
    """
    Test case 1: Format with default USD currency.
    """
    # Arrange & Act & Assert
    assert format_currency(1234.56) == "$1,234.56"
    assert format_currency(1000) == "$1,000.00"
    assert format_currency(0) == "$0.00"


def test_format_currency_major_currencies() -> None:
    """
    Test case 2: Format with major world currencies.
    """
    # Arrange & Act & Assert
    assert format_currency(1234.56, currency="EUR") == "€1,234.56"
    assert format_currency(1234.56, currency="GBP") == "£1,234.56"
    assert format_currency(1234.56, currency="JPY") == "¥1,235"  # No decimals
    assert format_currency(1234.56, currency="CNY") == "¥1,234.56"


def test_format_currency_zero_decimal_currencies() -> None:
    """
    Test case 3: Format currencies with no decimal places.
    """
    # Arrange & Act & Assert
    assert format_currency(1234.56, currency="JPY") == "¥1,235"
    assert format_currency(1234.56, currency="KRW") == "₩1,235"
    assert format_currency(1234.99, currency="VND") == "₫1,235"
    assert format_currency(999.4, currency="JPY") == "¥999"
    assert format_currency(999.5, currency="JPY") == "¥1,000"


def test_format_currency_thousand_separators() -> None:
    """
    Test case 4: Verify thousand separators.
    """
    # Arrange & Act & Assert
    assert format_currency(1000000) == "$1,000,000.00"
    assert format_currency(1234567.89) == "$1,234,567.89"
    assert format_currency(999) == "$999.00"


def test_format_currency_decimal_rounding() -> None:
    """
    Test case 5: Verify decimal rounding.
    """
    # Arrange & Act & Assert
    assert format_currency(1.234) == "$1.23"  # Rounds down
    assert format_currency(1.235) == "$1.24"  # Rounds up
    assert format_currency(1.999) == "$2.00"


def test_format_currency_various_currencies() -> None:
    """
    Test case 6: Test various currency symbols.
    """
    # Arrange & Act & Assert
    assert format_currency(100, currency="AUD") == "A$100.00"
    assert format_currency(100, currency="CAD") == "C$100.00"
    assert format_currency(100, currency="INR") == "₹100.00"
    assert format_currency(100, currency="BRL") == "R$100.00"
    assert format_currency(100, currency="RUB") == "₽100.00"


def test_format_currency_integer_and_float_amounts() -> None:
    """
    Test case 7: Handle various integer and float amounts.
    """
    # Arrange & Act & Assert
    # Integer amounts
    assert format_currency(100) == "$100.00"
    assert format_currency(1000) == "$1,000.00"
    assert format_currency(1000000) == "$1,000,000.00"

    # Float amounts
    assert format_currency(12.3) == "$12.30"
    assert format_currency(12.34) == "$12.34"
    assert format_currency(12.345) == "$12.35"  # Rounds
    assert format_currency(0.5) == "$0.50"


def test_format_currency_case_insensitive() -> None:
    """
    Test case 8: Currency code is case-insensitive.
    """
    # Arrange & Act & Assert
    assert format_currency(100, currency="usd") == "$100.00"
    assert format_currency(100, currency="Usd") == "$100.00"
    assert format_currency(100, currency="EUR") == "€100.00"
    assert format_currency(100, currency="eur") == "€100.00"


def test_format_currency_whitespace_handling() -> None:
    """
    Test case 9: Handle whitespace in currency code.
    """
    # Arrange & Act & Assert
    assert format_currency(100, currency=" USD ") == "$100.00"
    assert format_currency(100, currency="EUR ") == "€100.00"


def test_format_currency_negative_amounts() -> None:
    """
    Test case 10: Format negative amounts.
    """
    # Arrange & Act & Assert
    assert format_currency(-50.25) == "-$50.25"
    assert format_currency(-1234.56) == "-$1,234.56"
    assert format_currency(-1000000) == "-$1,000,000.00"


def test_format_currency_large_amounts() -> None:
    """
    Test case 11: Format very large amounts.
    """
    # Arrange & Act & Assert
    assert format_currency(1_000_000_000) == "$1,000,000,000.00"
    assert format_currency(999_999_999.99) == "$999,999,999.99"


def test_format_currency_small_amounts() -> None:
    """
    Test case 12: Format small fractional amounts.
    """
    # Arrange & Act & Assert
    assert format_currency(0.01) == "$0.01"
    assert format_currency(0.99) == "$0.99"
    assert format_currency(0.001) == "$0.00"  # Rounds to zero


def test_format_currency_unknown_currency() -> None:
    """
    Test case 13: Unknown currency uses code as prefix.
    """
    # Arrange & Act & Assert
    assert format_currency(100, currency="XXX") == "XXX 100.00"
    assert format_currency(1234.56, currency="ABC") == "ABC 1,234.56"


def test_format_currency_invalid_type_amount() -> None:
    """
    Test case 14: TypeError for invalid amount type.
    """
    # Arrange
    expected_message = "amount must be a number, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_currency("100")


def test_format_currency_invalid_type_currency() -> None:
    """
    Test case 15: TypeError for invalid currency type.
    """
    # Arrange
    expected_message = "currency must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_currency(100, currency=840)  # USD numeric code


def test_format_currency_invalid_type_locale() -> None:
    """
    Test case 16: TypeError for invalid locale type.
    """
    # Arrange
    expected_message = "locale must be a string or None, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        format_currency(100, locale=123)


def test_format_currency_invalid_currency_code_length() -> None:
    """
    Test case 17: ValueError for invalid currency code length.
    """
    # Arrange
    expected_message = "currency must be a 3-letter ISO 4217 code"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        format_currency(100, currency="US")

    with pytest.raises(ValueError, match=expected_message):
        format_currency(100, currency="USDA")

    with pytest.raises(ValueError, match=expected_message):
        format_currency(100, currency="")
