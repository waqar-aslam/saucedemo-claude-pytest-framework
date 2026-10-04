from playwright.sync_api import Locator, Page


class Header:
    """App header shared by all post-login pages: cart icon/badge and burger menu."""

    def __init__(self, page: Page):
        self.page = page
        self.cart_link: Locator = page.get_by_test_id("shopping-cart-link")
        self.cart_badge: Locator = page.get_by_test_id("shopping-cart-badge")
        self.menu_button: Locator = page.get_by_role("button", name="Open Menu")
        self.logout_link: Locator = page.get_by_test_id("logout-sidebar-link")

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()
