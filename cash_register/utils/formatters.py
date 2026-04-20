"""
formatters.py — Pure formatting helpers. No UI, no data dependency.
"""


def money(value: float, symbol: str = "Rs") -> str:
    """Format a float as a currency string, e.g. Rs 1,234.56"""
    if value == 0.0:
        return f"{symbol} 0.00"
    return f"{symbol} {value:,.2f}"


def money_or_dash(value: float, symbol: str = "Rs") -> str:
    """Return '—' for zero, otherwise formatted money."""
    return "—" if value == 0.0 else money(value, symbol)


def parse_amount(text: str) -> float:
    """
    Parse a user-typed amount string to float.
    Accepts: '1234', '1,234', '1234.56', '1,234.56'
    Raises ValueError for invalid input or negative numbers.
    """
    cleaned = text.strip().replace(",", "")
    if not cleaned:
        return 0.0
    value = float(cleaned)
    if value < 0:
        raise ValueError(f"Amount cannot be negative: {value}")
    return value
