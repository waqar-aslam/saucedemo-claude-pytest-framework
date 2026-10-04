from pages.base_page import BasePage
from utils.data_factory import CheckoutInfo


class CheckoutInfoPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page):
        super().__init__(page)
        self.title = self.by_test_id("title")
        self.first_name_input = self.by_test_id("firstName")
        self.last_name_input = self.by_test_id("lastName")
        self.postal_code_input = self.by_test_id("postalCode")
        self.continue_button = self.by_test_id("continue")
        self.cancel_button = self.by_test_id("cancel")
        self.error_banner = self.by_test_id("error")

    def fill(self, info: CheckoutInfo) -> None:
        self.first_name_input.fill(info.first_name)
        self.last_name_input.fill(info.last_name)
        self.postal_code_input.fill(info.postal_code)

    def submit(self) -> None:
        self.continue_button.click()

    def fill_and_continue(self, info: CheckoutInfo) -> None:
        self.log.info("Submitting checkout info for %s %s", info.first_name, info.last_name)
        self.fill(info)
        self.submit()

    def error_text(self) -> str:
        return self.error_banner.inner_text()
