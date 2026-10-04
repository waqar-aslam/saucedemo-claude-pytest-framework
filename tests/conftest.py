import pytest
from playwright.sync_api import Page, expect

from config.settings import load_json, settings
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_factory import CheckoutInfo, make_checkout_info
from utils.network_monitor import NetworkMonitor


@pytest.fixture(scope="session", autouse=True)
def _test_id_attribute(playwright):
    # The app marks elements with data-test, not Playwright's default data-testid.
    playwright.selectors.set_test_id_attribute(settings.test_id_attribute)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": settings.base_url,
        "viewport": {"width": settings.viewport_width, "height": settings.viewport_height},
    }


@pytest.fixture(autouse=True)
def _default_timeout(page: Page):
    page.set_default_timeout(settings.default_timeout_ms)


@pytest.fixture(scope="session")
def users() -> dict:
    return load_json("users.json")


@pytest.fixture(scope="session")
def checkout_data() -> dict:
    return load_json("checkout.json")


@pytest.fixture
def network_monitor(page: Page) -> NetworkMonitor:
    return NetworkMonitor(page)


# --- page objects ---------------------------------------------------------------------

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_info_page(page: Page) -> CheckoutInfoPage:
    return CheckoutInfoPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)


# --- state ----------------------------------------------------------------------------

@pytest.fixture
def logged_in(page: Page, login_page: LoginPage, inventory_page: InventoryPage, users: dict) -> InventoryPage:
    """Standard user logged in and sitting on the inventory page."""
    login_page.open()
    login_page.login(**users["standard"])
    page.wait_for_url("**/inventory.html")
    expect(inventory_page.items.first).to_be_visible()
    return inventory_page


@pytest.fixture
def checkout_info() -> CheckoutInfo:
    return make_checkout_info()
