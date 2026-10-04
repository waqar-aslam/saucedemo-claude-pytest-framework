from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    path = "/checkout-complete.html"

    def __init__(self, page):
        super().__init__(page)
        self.title = self.by_test_id("title")
        self.confirmation_header = self.by_test_id("complete-header")
        self.text = self.by_test_id("complete-text")
        self.back_home_button = self.by_test_id("back-to-products")

    def header_text(self) -> str:
        return self.confirmation_header.inner_text()

    def back_home(self) -> None:
        self.back_home_button.click()
