import re

from playwright.sync_api import Locator, Page

from components.header import Header
from models.product import LineItem
from utils.logger import get_logger
from utils.money import parse_money

_ITEM_ID_RE = re.compile(r"item_(\d+)_")


class BasePage:
    """Common behaviour for every page object. Page objects act and return data; they never assert."""

    path = "/"

    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)
        self.log = get_logger(type(self).__name__)

    def open(self) -> None:
        self.log.info("Opening %s", self.path)
        self.page.goto(self.path)

    def by_test_id(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(test_id)

    # --- helpers shared by inventory / cart / overview item rows -------------------------

    @staticmethod
    def read_item_id(row: Locator) -> str:
        """Product id is encoded in the title link id, e.g. 'item_4_title_link' -> '4'."""
        link_id = row.locator("a[id$='_title_link']").get_attribute("id")
        match = _ITEM_ID_RE.search(link_id or "")
        if not match:
            raise ValueError(f"Cannot derive product id from link id {link_id!r}")
        return match.group(1)

    def read_line_item(self, row: Locator) -> LineItem:
        quantity_loc = row.get_by_test_id("item-quantity")
        quantity = int(quantity_loc.inner_text()) if quantity_loc.count() else 1
        return LineItem(
            id=self.read_item_id(row),
            name=row.get_by_test_id("inventory-item-name").inner_text(),
            description=row.get_by_test_id("inventory-item-desc").inner_text(),
            price=parse_money(row.get_by_test_id("inventory-item-price").inner_text()),
            quantity=quantity,
        )
