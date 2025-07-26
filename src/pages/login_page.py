"""
Login page object model.
"""
from typing import Dict, Any
from playwright.sync_api import Page
from src.pages.base_page import BasePage


class LoginPageLocators:
    """Locators for the login page elements."""

    # Form elements
    USERNAME_FIELD = "#username"
    PASSWORD_FIELD = "#password"
    SUBMIT_BUTTON = "#submit"

    # Messages
    ERROR_MESSAGE = "#error"
    SUCCESS_MESSAGE = ".post-title"

    # Page elements
    PAGE_TITLE = "h2"
    LOGIN_FORM = "#login"

    # Links
    LOGOUT_LINK = "a[href*='logout']"


class LoginPage(BasePage):
    """Page object for the login page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = LoginPageLocators()

    @property
    def url_path(self) -> str:
        """Return the URL path for the login page."""
        return "/practice-test-login/"

    def enter_username(self, username: str) -> 'LoginPage':
        """Enter username in the username field."""
        self.fill_text(self.locators.USERNAME_FIELD, username)
        return self

    def enter_password(self, password: str) -> 'LoginPage':
        """Enter password in the password field."""
        self.fill_text(self.locators.PASSWORD_FIELD, password)
        return self

    def click_submit(self) -> 'LoginPage':
        """Click the submit button."""
        self.click_element(self.locators.SUBMIT_BUTTON)
        return self

    def login_with_credentials(self, username: str, password: str) -> 'LoginPage':
        """Perform complete login with given credentials."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()
        return self

    def get_error_message(self) -> str:
        """Get the error message text."""
        if self.is_element_visible(self.locators.ERROR_MESSAGE):
            return self.get_element_text(self.locators.ERROR_MESSAGE)
        return ""

    def get_page_title(self) -> str:
        """Get the page title text."""
        return self.get_element_text(self.locators.PAGE_TITLE)

    def is_login_form_visible(self) -> bool:
        """Check if the login form is visible."""
        return self.is_element_visible(self.locators.LOGIN_FORM)

    def is_error_message_displayed(self) -> bool:
        """Check if an error message is displayed."""
        return self.is_element_visible(self.locators.ERROR_MESSAGE)

    def is_username_field_visible(self) -> bool:
        """Check if the username field is visible."""
        return self.is_element_visible(self.locators.USERNAME_FIELD)

    def is_password_field_visible(self) -> bool:
        """Check if the password field is visible."""
        return self.is_element_visible(self.locators.PASSWORD_FIELD)

    def is_submit_button_visible(self) -> bool:
        """Check if the submit button is visible."""
        return self.is_element_visible(self.locators.SUBMIT_BUTTON)

    def clear_username_field(self) -> 'LoginPage':
        """Clear the username field."""
        self.fill_text(self.locators.USERNAME_FIELD, "")
        return self

    def clear_password_field(self) -> 'LoginPage':
        """Clear the password field."""
        self.fill_text(self.locators.PASSWORD_FIELD, "")
        return self