"""
Logged in page object model.
"""
from playwright.sync_api import Page
from src.pages.base_page import BasePage


class LoggedInPageLocators:
    """Locators for the logged in page elements."""

    # Page elements
    SUCCESS_MESSAGE = ".post-title"
    CONTENT_AREA = ".post-content"
    LOGOUT_LINK = "a[href*='logout']"

    # Expected text elements
    CONGRATULATIONS_TEXT = "text=Congratulations"
    SUCCESSFULLY_LOGGED_IN_TEXT = "text=successfully logged in"


class LoggedInPage(BasePage):
    """Page object for the logged in successfully page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = LoggedInPageLocators()

    @property
    def url_path(self) -> str:
        """Return the URL path for the logged in page."""
        return "/logged-in-successfully/"

    def get_success_message(self) -> str:
        """Get the success message text."""
        return self.get_element_text(self.locators.SUCCESS_MESSAGE)

    def get_content_text(self) -> str:
        """Get the content area text."""
        return self.get_element_text(self.locators.CONTENT_AREA)

    def is_success_message_displayed(self) -> bool:
        """Check if the success message is displayed."""
        return self.is_element_visible(self.locators.SUCCESS_MESSAGE)

    def is_logout_link_visible(self) -> bool:
        """Check if the logout link is visible."""
        return self.is_element_visible(self.locators.LOGOUT_LINK)

    def click_logout(self) -> 'LoggedInPage':
        """Click the logout link."""
        self.click_element(self.locators.LOGOUT_LINK)
        return self

    def is_congratulations_text_present(self) -> bool:
        """Check if congratulations text is present."""
        return self.is_element_visible(self.locators.CONGRATULATIONS_TEXT)

    def is_successfully_logged_in_text_present(self) -> bool:
        """Check if successfully logged in text is present."""
        return self.is_element_visible(self.locators.SUCCESSFULLY_LOGGED_IN_TEXT)

    def verify_successful_login(self) -> bool:
        """Verify that login was successful by checking multiple indicators."""
        return (
            self.is_current_page() and
            self.is_success_message_displayed() and
            (self.is_congratulations_text_present() or
             self.is_successfully_logged_in_text_present())
        )