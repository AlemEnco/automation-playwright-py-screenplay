"""
Base page class for page object model implementation.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from playwright.sync_api import Page
from src.config.settings import settings


class BasePage(ABC):
    """Base class for all page objects."""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.browser.timeout

    @property
    @abstractmethod
    def url_path(self) -> str:
        """Return the URL path for this page."""
        pass

    @property
    def full_url(self) -> str:
        """Return the full URL for this page."""
        return f"{settings.environment.base_url}{self.url_path}"

    def navigate_to(self) -> None:
        """Navigate to this page."""
        self.page.goto(self.full_url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_page_load(self) -> None:
        """Wait for the page to fully load."""
        self.page.wait_for_load_state("networkidle")

    def is_current_page(self) -> bool:
        """Check if this is the current page."""
        current_url = self.page.url
        return self.url_path in current_url or self.full_url == current_url

    def wait_for_element(self, locator: str, state: str = "visible", timeout: Optional[int] = None) -> None:
        """Wait for an element to be in a specific state."""
        wait_timeout = timeout or self.timeout
        self.page.wait_for_selector(locator, state=state, timeout=wait_timeout)

    def is_element_visible(self, locator: str) -> bool:
        """Check if an element is visible."""
        try:
            return self.page.is_visible(locator)
        except Exception:
            return False

    def is_element_present(self, locator: str) -> bool:
        """Check if an element is present in the DOM."""
        try:
            element = self.page.query_selector(locator)
            return element is not None
        except Exception:
            return False

    def get_element_text(self, locator: str) -> str:
        """Get text content of an element."""
        self.wait_for_element(locator)
        return self.page.text_content(locator) or ""

    def click_element(self, locator: str, **options) -> None:
        """Click on an element."""
        self.wait_for_element(locator)
        self.page.click(locator, **options)

    def type_text(self, locator: str, text: str, clear: bool = True, **options) -> None:
        """Type text into an element."""
        self.wait_for_element(locator)
        if clear:
            self.page.fill(locator, "")
        self.page.type(locator, text, **options)

    def fill_text(self, locator: str, text: str, **options) -> None:
        """Fill text into an element (faster than typing)."""
        self.wait_for_element(locator)
        self.page.fill(locator, text, **options)