from decimal import Decimal

from playwright.sync_api import Locator

from models.product import Product
from pages.base_page import BasePage
from utils.money import parse_money


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page):
        super().__init__(page)
        self.title = self.by_test_id("title")
        self.items = self.by_test_id("inventory-item")
        self.sort_dropdown = self.by_test_id("product-sort-container")

    def _row_for(self, product: Product) -> Locator:
        return self.items.filter(has=self.by_test_id("inventory-item-name").get_by_text(product.name, exact=True))

    def products(self) -> list[Product]:
        """Scrape the inventory into the test baseline (source of truth for later steps)."""
        rows = self.items.all()
        return [
            Product(
                id=self.read_item_id(row),
                name=row.get_by_test_id("inventory-item-name").inner_text(),
                description=row.get_by_test_id("inventory-item-desc").inner_text(),
                price=parse_money(row.get_by_test_id("inventory-item-price").inner_text()),
            )
            for row in rows
        ]

    def add_to_cart(self, product: Product) -> None:
        self.log.info("Adding to cart: %s", product.name)
        self._row_for(product).locator("button[data-test^='add-to-cart']").click()

    def remove_from_cart(self, product: Product) -> None:
        self.log.info("Removing from cart: %s", product.name)
        self._row_for(product).locator("button[data-test^='remove']").click()

    def sort_by(self, option_value: str) -> None:
        """Option values: az, za, lohi, hilo."""
        self.sort_dropdown.select_option(option_value)

    def displayed_prices(self) -> list[Decimal]:
        return [parse_money(t) for t in self.by_test_id("inventory-item-price").all_inner_texts()]

    def displayed_image_sources(self) -> list[str]:
        return [img.get_attribute("src") or "" for img in self.items.locator("img.inventory_item_img").all()]
