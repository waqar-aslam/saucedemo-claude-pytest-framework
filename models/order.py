from dataclasses import dataclass
from decimal import Decimal

from models.product import Product


@dataclass(frozen=True)
class OrderRecord:
    """Order built on the test side from the baseline products and overview totals."""
    products: tuple[Product, ...]
    item_total: Decimal
    tax: Decimal
    total: Decimal
