from dataclasses import replace

import pytest
from playwright.sync_api import expect


@pytest.fixture
def at_checkout_info(logged_in, cart_page, checkout_info_page):
    logged_in.add_to_cart(logged_in.products()[0])
    logged_in.header.open_cart()
    cart_page.checkout()
    expect(checkout_info_page.title).to_have_text("Checkout: Your Information")
    return checkout_info_page


@pytest.mark.negative
@pytest.mark.parametrize(
    "missing, field_key",
    [("first_name", "first_name"), ("last_name", "last_name"), ("postal_code", "postal_code")],
)
def test_required_fields(at_checkout_info, checkout_info, checkout_data, missing, field_key):
    at_checkout_info.fill_and_continue(replace(checkout_info, **{missing: ""}))

    expect(at_checkout_info.error_banner).to_have_text(checkout_data["required_field_errors"][field_key])


def test_cancel_returns_to_cart(at_checkout_info, cart_page):
    at_checkout_info.cancel_button.click()

    expect(cart_page.title).to_have_text("Your Cart")


def test_overview_totals_are_consistent(at_checkout_info, checkout_info, checkout_overview_page):
    at_checkout_info.fill_and_continue(checkout_info)
    expect(checkout_overview_page.title).to_have_text("Checkout: Overview")

    expect(checkout_overview_page.rows).to_have_count(1)
    items = checkout_overview_page.items()
    item_total = checkout_overview_page.item_total()

    assert item_total == sum(i.price * i.quantity for i in items)
    assert checkout_overview_page.total() == item_total + checkout_overview_page.tax()
