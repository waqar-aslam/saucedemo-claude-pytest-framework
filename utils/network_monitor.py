from playwright.sync_api import ConsoleMessage, Page, Request, Response

from utils.logger import get_logger

log = get_logger(__name__)

# Third-party noise (analytics/error reporting) is not part of the app under test.
_IGNORED_HOSTS = ("backtrace.io", "events.backtrace.io")


class NetworkMonitor:
    """Collects failed requests, HTTP >= 400 responses and console errors for a page."""

    def __init__(self, page: Page):
        self.failed_requests: list[str] = []
        self.error_responses: list[str] = []
        self.console_errors: list[str] = []
        page.on("requestfailed", self._on_request_failed)
        page.on("response", self._on_response)
        page.on("console", self._on_console)

    @staticmethod
    def _ignored(url: str) -> bool:
        return any(host in url for host in _IGNORED_HOSTS)

    def _on_request_failed(self, request: Request) -> None:
        if not self._ignored(request.url):
            self.failed_requests.append(f"{request.method} {request.url} - {request.failure}")

    def _on_response(self, response: Response) -> None:
        if response.status >= 400 and not self._ignored(response.url):
            self.error_responses.append(f"{response.status} {response.url}")

    def _on_console(self, message: ConsoleMessage) -> None:
        if message.type == "error" and not self._ignored(message.location.get("url", "")):
            self.console_errors.append(message.text)

    @property
    def problems(self) -> list[str]:
        return self.failed_requests + self.error_responses + self.console_errors
