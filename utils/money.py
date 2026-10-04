import re
from decimal import Decimal

_MONEY_RE = re.compile(r"-?\d+(?:,\d{3})*(?:\.\d+)?")


def parse_money(text: str) -> Decimal:
    """'$29.99' or 'Item total: $29.99' -> Decimal('29.99')."""
    match = _MONEY_RE.search(text)
    if not match:
        raise ValueError(f"No monetary amount found in {text!r}")
    return Decimal(match.group().replace(",", ""))


def format_money(amount: Decimal) -> str:
    return f"${amount:.2f}"
