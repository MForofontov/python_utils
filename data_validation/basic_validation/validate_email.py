"""
Email validation utility with multiple validation strategies.

This module provides comprehensive email validation using regex patterns,
format checking, and optional domain validation.
"""

import re


def validate_email(
    email: str,
    allow_unicode: bool = False,
    check_mx: bool = False,
    param_name: str = "email",
) -> None:
    """
    Validate email address format and optionally check domain existence.

    Provides comprehensive email validation using regex patterns with support
    for Unicode characters and optional MX record checking.

    Parameters
    ----------
    email : str
        The email address to validate.
    allow_unicode : bool, optional
        Whether to allow Unicode characters in email (by default False).
    check_mx : bool, optional
        Whether to check if domain has MX record (by default False).
    param_name : str, optional
        Name of the parameter being validated for error messages (by default "email").

    Returns
    -------
    None
        This function returns None if validation passes.

    Raises
    ------
    TypeError
        If email is not a string.
    ValueError
        If email format is invalid or domain doesn't exist (when check_mx=True).

    Examples
    --------
    >>> validate_email("user@example.com")  # Passes
    >>> validate_email("user.name+tag@domain.co.uk")  # Passes
    >>> validate_email("invalid-email")  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: email format is invalid

    >>> validate_email("user@üñíçøðé.com", allow_unicode=True)  # Passes
    >>> validate_email("user@üñíçøðé.com", allow_unicode=False)  # Raises ValueError
    Traceback (most recent call last):
        ...
    ValueError: email contains non-ASCII characters but allow_unicode=False

    >>> validate_email("user@nonexistent-domain-12345.com", check_mx=True)  # May raise ValueError
    Traceback (most recent call last):
        ...
    ValueError: email domain does not have valid MX record

    Notes
    -----
    This function provides comprehensive email validation including:
    - RFC 5322 compliant regex pattern matching
    - Unicode character support (when enabled)
    - Basic format validation (local@domain structure)
    - Optional MX record checking for domain existence
    - Length limits for local and domain parts
    - Special character handling

    The regex patterns used are:
    - ASCII only: Strict RFC 5322 compliance
    - Unicode: Extended pattern allowing international characters

    When check_mx=True, the function will perform a DNS lookup to verify
    that the domain has a valid MX (Mail Exchange) record. This requires
    an active internet connection and may be slower.

    Complexity
    ----------
    Time: O(1) for regex validation, O(network) for MX checking
    Space: O(1)
    """
    # Validate input parameters
    if not isinstance(email, str):
        raise TypeError(f"{param_name} must be str, got {type(email).__name__}")
    if not isinstance(allow_unicode, bool):
        raise TypeError(
            f"allow_unicode must be bool, got {type(allow_unicode).__name__}"
        )
    if not isinstance(check_mx, bool):
        raise TypeError(f"check_mx must be bool, got {type(check_mx).__name__}")
    if not isinstance(param_name, str):
        raise TypeError(f"param_name must be str, got {type(param_name).__name__}")

    # Basic length and format checks
    if len(email) == 0:
        raise ValueError(f"{param_name} cannot be empty")
    if email.count("@") != 1:
        raise ValueError(f"{param_name} must contain exactly one @ symbol")
    if len(email) > 254:
        raise ValueError(f"{param_name} exceeds maximum length of 254 characters")

    # Split into local and domain parts
    local_part, domain_part = email.rsplit("@", 1)
    if len(local_part) == 0:
        raise ValueError(f"{param_name} local part cannot be empty")
    if len(local_part) > 64:
        raise ValueError(
            f"{param_name} local part exceeds maximum length of 64 characters"
        )
    if len(domain_part) == 0:
        raise ValueError(f"{param_name} domain part cannot be empty")
    if len(domain_part) > 253:
        raise ValueError(
            f"{param_name} domain part exceeds maximum length of 253 characters"
        )

    # Unicode check
    if not allow_unicode:
        try:
            email.encode("ascii")
        except UnicodeEncodeError as exc:
            raise ValueError(
                f"{param_name} contains non-ASCII characters but allow_unicode=False"
            ) from exc

    # Structure checks before regex
    if domain_part.startswith(".") or domain_part.endswith("."):
        raise ValueError(f"{param_name} domain cannot start or end with a dot")
    if ".." in domain_part:
        raise ValueError(f"{param_name} domain cannot contain consecutive dots")
    if "." not in domain_part:
        raise ValueError(f"{param_name} domain must contain at least one dot")

    # Regex patterns
    if allow_unicode:
        local_pattern = r"[\w\u0080-\uFFFF!#$%&'*+/=?^_`{|}~-]+(?:\.[\w\u0080-\uFFFF!#$%&'*+/=?^_`{|}~-]+)*"
        domain_pattern = r"[a-zA-Z0-9\u0080-\uFFFF](?:[a-zA-Z0-9\u0080-\uFFFF-]{0,61}[a-zA-Z0-9\u0080-\uFFFF])?(?:\.[a-zA-Z0-9\u0080-\uFFFF](?:[a-zA-Z0-9\u0080-\uFFFF-]{0,61}[a-zA-Z0-9\u0080-\uFFFF])?)*"
    else:
        local_pattern = (
            r"[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
        )
        domain_pattern = r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"

    if not re.fullmatch(local_pattern, local_part):
        raise ValueError(f"{param_name} local part format is invalid")
    if not re.fullmatch(domain_pattern, domain_part):
        raise ValueError(f"{param_name} domain part format is invalid")

    # Optional MX record checking
    if check_mx:
        try:
            import socket

            try:
                import dns.resolver

                try:
                    mx_records = dns.resolver.resolve(domain_part, "MX")
                    if not mx_records:
                        raise ValueError(
                            f"{param_name} domain does not have valid MX record"
                        )
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as exc:
                    raise ValueError(
                        f"{param_name} domain does not have valid MX record"
                    ) from exc
                except Exception:
                    try:
                        socket.gethostbyname(domain_part)
                    except socket.gaierror as socket_error:
                        raise ValueError(
                            f"{param_name} domain does not exist"
                        ) from socket_error
            except ImportError:
                socket.gethostbyname(domain_part)
        except Exception:
            raise ValueError(f"{param_name} domain does not exist")


__all__ = ["validate_email"]
