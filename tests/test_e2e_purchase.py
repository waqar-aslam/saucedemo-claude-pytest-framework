import pytest
from playwright.sync_api import expect

from models.order import OrderRecord


@pytest.mark.e2e
def test_purchase_journey(
    logged_in,
    cart_page,
    checkout_info_page,
    checkout_overview_page,
    checkout_complete_page,
    checkout_info,
    checkout_data,
    network_monitor,
):
    # Baseline captured from the inventory page is the reference for every later step.
    products = logged_in.products()[:2]
    for product in products:
        logged_in.add_to_cart(product)
    expect(logged_in.header.cart_badge).to_have_text(str(len(products)))

    logged_in.header.open_cart()
    expect(cart_page.title).to_have_text("Your Cart")
    expect(cart_page.rows).to_have_count(len(products))
    cart_items = cart_page.items()
    assert [(i.id, i.name, i.price, i.quantity) for i in cart_items] == [
        (p.id, p.name, p.price, 1) for p in products
    ]

    cart_page.checkout()
    checkout_info_page.fill_and_continue(checkout_info)

    expect(checkout_overview_page.title).to_have_text("Checkout: Overview")
    expect(checkout_overview_page.rows).to_have_count(len(products))
    assert checkout_overview_page.items() == cart_items
    order = OrderRecord(
        products=tuple(products),
        item_total=checkout_overview_page.item_total(),
        tax=checkout_overview_page.tax(),
        total=checkout_overview_page.total(),
    )
    assert order.item_total == sum(p.price for p in order.products)
    assert order.total == order.item_total + order.tax

    checkout_overview_page.finish()

    expect(checkout_complete_page.title).to_have_text("Checkout: Complete!")
    expect(checkout_complete_page.confirmation_header).to_have_text(checkout_data["confirmation_header"])

    checkout_complete_page.back_home()
    expect(logged_in.title).to_have_text("Products")
    expect(logged_in.header.cart_badge).to_have_count(0)

    assert network_monitor.problems == []
