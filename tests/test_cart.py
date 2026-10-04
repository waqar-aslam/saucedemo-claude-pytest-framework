import pytest
from playwright.sync_api import expect


def _assert_matches(line_items, products):
    assert [(i.id, i.name, i.price, i.quantity) for i in line_items] == [
        (p.id, p.name, p.price, 1) for p in products
    ]


@pytest.mark.smoke
def test_added_product_appears_in_cart(logged_in, cart_page):
    product = logged_in.products()[0]

    logged_in.add_to_cart(product)
    expect(logged_in.header.cart_badge).to_have_text("1")
    logged_in.header.open_cart()

    expect(cart_page.title).to_have_text("Your Cart")
    expect(cart_page.rows).to_have_count(1)
    _assert_matches(cart_page.items(), [product])


def test_multiple_products_in_cart(logged_in, cart_page):
    chosen = logged_in.products()[:3]

    for product in chosen:
        logged_in.add_to_cart(product)
    expect(logged_in.header.cart_badge).to_have_text(str(len(chosen)))
    logged_in.header.open_cart()

    expect(cart_page.rows).to_have_count(len(chosen))
    _assert_matches(cart_page.items(), chosen)


def test_remove_from_inventory_page(logged_in):
    product = logged_in.products()[0]

    logged_in.add_to_cart(product)
    expect(logged_in.header.cart_badge).to_have_text("1")
    logged_in.remove_from_cart(product)

    expect(logged_in.header.cart_badge).to_have_count(0)


def test_remove_from_cart_page(logged_in, cart_page):
    first, second = logged_in.products()[:2]
    logged_in.add_to_cart(first)
    logged_in.add_to_cart(second)
    logged_in.header.open_cart()
    expect(cart_page.rows).to_have_count(2)

    cart_page.remove(cart_page.items()[0])

    expect(cart_page.rows).to_have_count(1)
    _assert_matches(cart_page.items(), [second])


def test_cart_persists_across_navigation(logged_in, cart_page):
    product = logged_in.products()[0]
    logged_in.add_to_cart(product)
    logged_in.header.open_cart()

    cart_page.continue_shopping_button.click()
    expect(logged_in.header.cart_badge).to_have_text("1")
    logged_in.header.open_cart()
    expect(cart_page.rows).to_have_count(1)

    _assert_matches(cart_page.items(), [product])
