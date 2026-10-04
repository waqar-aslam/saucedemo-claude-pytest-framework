import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_valid_login_lands_on_inventory(page: Page, login_page, inventory_page, users):
    login_page.open()
    login_page.login(**users["standard"])

    expect(page).to_have_url(f"{page.url.split('/inventory.html')[0]}/inventory.html")
    expect(inventory_page.title).to_have_text("Products")
    assert login_page.session_username() == users["standard"]["username"]


@pytest.mark.negative
@pytest.mark.parametrize("user_key, error_key", [("locked_out", "locked_out"), ("invalid", "invalid")])
def test_rejected_login_shows_error(page: Page, login_page, users, checkout_data, user_key, error_key):
    login_page.open()
    login_page.login(**users[user_key])

    expect(login_page.error_banner).to_contain_text(checkout_data["login_errors"][error_key])
    expect(page).not_to_have_url(re.compile(r"inventory\.html"))


@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("", "", "Username is required"),
        ("someone", "", "Password is required"),
    ],
)
def test_missing_credentials(login_page, username, password, expected):
    login_page.open()
    login_page.login(username, password)

    expect(login_page.error_banner).to_contain_text(expected)


@pytest.mark.smoke
def test_logout_returns_to_login(page: Page, logged_in, login_page):
    logged_in.header.logout()

    expect(login_page.login_button).to_be_visible()
    assert login_page.session_username() is None
