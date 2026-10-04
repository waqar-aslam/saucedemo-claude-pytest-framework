from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    """A product as captured from the inventory page (the test baseline)."""
    id: str
    name: str
    description: str
    price: Decimal


@dataclass(frozen=True)
class LineItem:
    """A row shown on the cart or checkout overview page."""
    id: str
    name: str
    description: str
    price: Decimal
    quantity: int
