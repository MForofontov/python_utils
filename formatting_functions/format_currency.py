"""Format numbers as currency strings."""

# Currency symbols mapping (common ones)
_CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "INR": "₹",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "CHF",
    "KRW": "₩",
    "BRL": "R$",
    "RUB": "₽",
    "ZAR": "R",
    "MXN": "$",
    "SGD": "S$",
    "HKD": "HK$",
    "NOK": "kr",
    "SEK": "kr",
    "DKK": "kr",
    "PLN": "zł",
    "THB": "฿",
    "IDR": "Rp",
    "MYR": "RM",
    "PHP": "₱",
    "CZK": "Kč",
    "ILS": "₪",
    "CLP": "$",
    "VND": "₫",
    "AED": "د.إ",
    "SAR": "﷼",
}

# Zero-decimal currencies (no fractional units)
_ZERO_DECIMAL_CURRENCIES = frozenset({
    "JPY",
    "KRW",
    "VND",
    "CLP",
    "ISK",
    "PYG",
    "UGX",
    "RWF",
    "XAF",
    "XOF",
    "BIF",
    "DJF",
    "GNF",
    "KMF",
    "XPF",
})


def format_currency(
    amount: int | float,
    currency: str = "USD",
    locale: str | None = None,
) -> str:
    """
    Format a number as a currency string.

    Parameters
    ----------
    amount : int | float
        Amount to format.
    currency : str, optional
        Three-letter ISO 4217 currency code (by default "USD").
    locale : str | None, optional
        Locale code for formatting (e.g., "en_US", "de_DE") (by default None).
        If None, uses simple formatting without locale-specific rules.

    Returns
    -------
    str
        Formatted currency string.

    Raises
    ------
    TypeError
        If amount is not a number, currency is not a string, or locale is not a string or None.
    ValueError
        If currency code is invalid or locale is invalid.

    Examples
    --------
    >>> format_currency(1234.56)
    '$1,234.56'
    >>> format_currency(1234.56, currency="EUR")
    '€1,234.56'
    >>> format_currency(1234.56, currency="GBP")
    '£1,234.56'
    >>> format_currency(1234.56, currency="JPY")
    '¥1,235'
    >>> format_currency(-50.25)
    '-$50.25'
    >>> format_currency(1000)
    '$1,000.00'
    >>> format_currency(0)
    '$0.00'

    Notes
    -----
    Common currency symbols: USD ($), EUR (€), GBP (£), JPY (¥), CNY (¥), INR (₹)
    
    Zero-decimal currencies (no fractional units): JPY, KRW, VND, CLP, etc.
    
    When locale is None, uses basic formatting with thousand separators and
    appropriate decimal places for the currency.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Input validation
    if not isinstance(amount, (int, float)):
        raise TypeError(f"amount must be a number, got {type(amount).__name__}")
    if not isinstance(currency, str):
        raise TypeError(f"currency must be a string, got {type(currency).__name__}")
    if locale is not None and not isinstance(locale, str):
        raise TypeError(
            f"locale must be a string or None, got {type(locale).__name__}"
        )

    # Validate and normalize currency code
    currency = currency.upper().strip()
    if len(currency) != 3:
        raise ValueError(f"currency must be a 3-letter ISO 4217 code, got: {currency}")

    # Get currency symbol
    symbol = _CURRENCY_SYMBOLS.get(currency, currency + " ")

    # Determine decimal places
    decimal_places = 0 if currency in _ZERO_DECIMAL_CURRENCIES else 2

    # Round amount to appropriate decimal places
    rounded_amount = round(amount, decimal_places)

    # Handle negative sign
    negative = rounded_amount < 0
    abs_amount = abs(rounded_amount)

    # Format with thousand separators
    if decimal_places > 0:
        formatted_number = f"{abs_amount:,.{decimal_places}f}"
    else:
        formatted_number = f"{int(abs_amount):,}"

    # Construct final string
    if negative:
        return f"-{symbol}{formatted_number}"
    else:
        return f"{symbol}{formatted_number}"


__all__ = ["format_currency"]
