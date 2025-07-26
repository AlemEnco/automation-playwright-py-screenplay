"""
BrowseTheWeb ability for web browser interactions.
"""
from typing import Optional
from playwright.sync_api import Page, Browser, BrowserContext
from src.screenplay.base import Ability, Actor


class BrowseTheWeb(Ability):
    """
    Ability to browse the web using Playwright.
    This ability provides access to browser, context, and page objects.
    """

    def __init__(self, browser: Browser, context: Optional[BrowserContext] = None, page: Optional[Page] = None):
        self._browser = browser
        self._context = context
        self._page = page
        self._actor: Optional[Actor] = None

    @classmethod
    def using(cls, browser: Browser) -> 'BrowseTheWeb':
        """Create a new BrowseTheWeb ability using the given browser."""
        return cls(browser)

    @classmethod
    def using_page(cls, page: Page) -> 'BrowseTheWeb':
        """Create a new BrowseTheWeb ability using an existing page."""
        return cls(page.context.browser, page.context, page)

    def as_actor(self, actor: Actor) -> 'BrowseTheWeb':
        """Bind this ability to an actor."""
        ability = BrowseTheWeb(self._browser, self._context, self._page)
        ability._actor = actor
        return ability

    @property
    def browser(self) -> Browser:
        """Get the browser instance."""
        return self._browser

    @property
    def context(self) -> BrowserContext:
        """Get or create a browser context."""
        if self._context is None:
            self._context = self._browser.new_context()
        return self._context

    @property
    def page(self) -> Page:
        """Get or create a page."""
        if self._page is None:
            self._page = self.context.new_page()
        return self._page

    def new_page(self) -> Page:
        """Create a new page in the current context."""
        return self.context.new_page()

    def close_page(self) -> None:
        """Close the current page."""
        if self._page:
            self._page.close()
            self._page = None

    def close_context(self) -> None:
        """Close the current context."""
        if self._context:
            self._context.close()
            self._context = None
            self._page = None

    def close_browser(self) -> None:
        """Close the browser."""
        if self._browser:
            self._browser.close()

    def __str__(self) -> str:
        actor_name = self._actor.name if self._actor else "Unknown"
        return f"BrowseTheWeb(actor={actor_name})"