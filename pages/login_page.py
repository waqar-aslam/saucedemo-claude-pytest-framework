from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = self.by_test_id("username")
        self.password_input = self.by_test_id("password")
        self.login_button = self.by_test_id("login-button")
        self.error_banner = self.by_test_id("error")

    def login(self, username: str, password: str) -> None:
        self.log.info("Logging in as %s", username)
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def error_text(self) -> str:
        return self.error_banner.inner_text()

    def session_username(self) -> str | None:
        """Value of the 'session-username' cookie set by a successful login."""
        for cookie in self.page.context.cookies():
            if cookie["name"] == "session-username":
                return cookie["value"]
        return None
