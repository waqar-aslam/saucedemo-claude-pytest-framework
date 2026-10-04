from decimal import Decimal

from models.product import LineItem
from pages.base_page import BasePage
from utils.money import parse_money


class CheckoutOverviewPage(BasePage):
    path = "/checkout-step-two.html"

    def __init__(self, page):
        super().__init__(page)
        self.title = self.by_test_id("title")
        self.rows = self.by_test_id("inventory-item")
        self.payment_info_label = self.by_test_id("payment-info-label")
        self.payment_info_value = self.by_test_id("payment-info-value")
        self.shipping_info_label = self.by_test_id("shipping-info-label")
        self.shipping_info_value = self.by_test_id("shipping-info-value")
        self.finish_button = self.by_test_id("finish")

    def items(self) -> list[LineItem]:
        return [self.read_line_item(row) for row in self.rows.all()]

    def item_total(self) -> Decimal:
        return parse_money(self.by_test_id("subtotal-label").inner_text())

    def tax(self) -> Decimal:
        return parse_money(self.by_test_id("tax-label").inner_text())

    def total(self) -> Decimal:
        return parse_money(self.by_test_id("total-label").inner_text())

    def finish(self) -> None:
        self.log.info("Placing order")
        self.finish_button.click()
