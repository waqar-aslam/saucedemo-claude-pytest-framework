import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_products_have_complete_details(logged_in):
    products = logged_in.products()

    assert products, "inventory is empty"
    assert len({p.id for p in products}) == len(products), "duplicate product ids"
    for p in products:
        assert p.name and p.description
        assert p.price > 0


@pytest.mark.parametrize(
    "option, key, reverse",
    [
        ("az", lambda p: p.name, False),
        ("za", lambda p: p.name, True),
        ("lohi", lambda p: p.price, False),
        ("hilo", lambda p: p.price, True),
    ],
)
def test_sorting(logged_in, option, key, reverse):
    baseline = logged_in.products()
    expected = [p.id for p in sorted(baseline, key=key, reverse=reverse)]

    logged_in.sort_by(option)

    # Ties (equal price) may be ordered either way, so compare keys rather than ids.
    actual = logged_in.products()
    assert [key(p) for p in actual] == [key(p) for p in sorted(baseline, key=key, reverse=reverse)]
    assert sorted(p.id for p in actual) == sorted(expected)


def test_every_product_has_an_image(logged_in):
    expect(logged_in.items.first).to_be_visible()
    sources = logged_in.displayed_image_sources()

    assert len(sources) == len(logged_in.products())
    assert all(sources)
