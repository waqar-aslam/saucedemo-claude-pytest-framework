from models.product import LineItem
from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.title = self.by_test_id("title")
        self.rows = self.by_test_id("inventory-item")
        self.checkout_button = self.by_test_id("checkout")
        self.continue_shopping_button = self.by_test_id("continue-shopping")

    def items(self) -> list[LineItem]:
        return [self.read_line_item(row) for row in self.rows.all()]

    def remove(self, item: LineItem) -> None:
        self.log.info("Removing from cart page: %s", item.name)
        self.rows.filter(has=self.by_test_id("inventory-item-name").get_by_text(item.name, exact=True)) \
            .locator("button[data-test^='remove']").click()

    def checkout(self) -> None:
        self.checkout_button.click()
