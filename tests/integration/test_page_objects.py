"""
Integration tests for page objects.
"""
import pytest
from playwright.sync_api import Page
from src.pages.login_page import LoginPage
from src.pages.logged_in_page import LoggedInPage
from src.config.settings import settings


class TestLoginPageIntegration:
    """Integration tests for LoginPage."""

    @pytest.mark.integration
    def test_login_page_navigation(self, page: Page):
        """Test navigation to login page."""
        login_page = LoginPage(page)
        login_page.navigate_to()

        assert login_page.is_current_page()
        assert login_page.is_login_form_visible()

    @pytest.mark.integration
    def test_login_page_elements_visibility(self, page: Page):
        """Test that all login page elements are visible."""
        login_page = LoginPage(page)
        login_page.navigate_to()

        assert login_page.is_username_field_visible()
        assert login_page.is_password_field_visible()
        assert login_page.is_submit_button_visible()

    @pytest.mark.integration
    def test_login_page_form_interaction(self, page: Page):
        """Test basic form interactions on login page."""
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Test entering username
        login_page.enter_username("testuser")

        # Test entering password
        login_page.enter_password("testpass")

        # Test clearing fields
        login_page.clear_username_field()
        login_page.clear_password_field()

    @pytest.mark.integration
    def test_successful_login_flow(self, page: Page):
        """Test successful login flow using page objects."""
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Get valid credentials
        credentials = settings.get_credentials()["valid"]

        # Perform login
        login_page.login_with_credentials(
            credentials["username"],
            credentials["password"]
        )

        # Verify we're on the logged in page
        logged_in_page = LoggedInPage(page)
        assert logged_in_page.is_current_page()
        assert logged_in_page.verify_successful_login()

    @pytest.mark.integration
    def test_failed_login_flow(self, page: Page):
        """Test failed login flow using page objects."""
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Get invalid credentials
        credentials = settings.get_credentials()["invalid"]

        # Perform login with invalid credentials
        login_page.login_with_credentials(
            credentials["username"],
            credentials["password"]
        )

        # Should remain on login page
        assert login_page.is_current_page()
        assert login_page.is_error_message_displayed()

        # Error message should contain relevant text
        error_message = login_page.get_error_message()
        assert len(error_message.strip()) > 0


class TestLoggedInPageIntegration:
    """Integration tests for LoggedInPage."""

    @pytest.mark.integration
    def test_logged_in_page_after_successful_login(self, page: Page):
        """Test logged in page state after successful login."""
        # First login successfully
        login_page = LoginPage(page)
        login_page.navigate_to()

        credentials = settings.get_credentials()["valid"]
        login_page.login_with_credentials(
            credentials["username"],
            credentials["password"]
        )

        # Test logged in page
        logged_in_page = LoggedInPage(page)

        assert logged_in_page.is_current_page()
        assert logged_in_page.is_success_message_displayed()

        # Check success message content
        success_message = logged_in_page.get_success_message()
        assert len(success_message.strip()) > 0

        # Check content area
        content_text = logged_in_page.get_content_text()
        assert len(content_text.strip()) > 0

    @pytest.mark.integration
    def test_logged_in_page_verification_methods(self, page: Page):
        """Test various verification methods on logged in page."""
        # First login successfully
        login_page = LoginPage(page)
        login_page.navigate_to()

        credentials = settings.get_credentials()["valid"]
        login_page.login_with_credentials(
            credentials["username"],
            credentials["password"]
        )

        # Test verification methods
        logged_in_page = LoggedInPage(page)

        assert logged_in_page.verify_successful_login()
        assert logged_in_page.is_congratulations_text_present() or \
               logged_in_page.is_successfully_logged_in_text_present()


class TestPageObjectsInteraction:
    """Integration tests for page object interactions."""

    @pytest.mark.integration
    def test_page_transition_login_to_logged_in(self, page: Page):
        """Test page transition from login to logged in page."""
        # Start on login page
        login_page = LoginPage(page)
        login_page.navigate_to()

        initial_url = page.url
        assert "/practice-test-login/" in initial_url

        # Perform successful login
        credentials = settings.get_credentials()["valid"]
        login_page.login_with_credentials(
            credentials["username"],
            credentials["password"]
        )

        # Verify transition to logged in page
        final_url = page.url
        assert "/logged-in-successfully/" in final_url
        assert initial_url != final_url

        # Verify logged in page is properly loaded
        logged_in_page = LoggedInPage(page)
        assert logged_in_page.is_current_page()

    @pytest.mark.integration
    def test_page_object_error_handling(self, page: Page):
        """Test page object error handling for missing elements."""
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Test checking for non-existent elements
        assert not login_page.is_element_visible("#non-existent-element")
        assert not login_page.is_element_present("#non-existent-element")

    @pytest.mark.integration
    def test_page_object_wait_mechanisms(self, page: Page):
        """Test page object wait mechanisms."""
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Test waiting for elements
        login_page.wait_for_element(login_page.locators.USERNAME_FIELD)
        login_page.wait_for_element(login_page.locators.PASSWORD_FIELD)
        login_page.wait_for_element(login_page.locators.SUBMIT_BUTTON)

        # Elements should be visible after waiting
        assert login_page.is_username_field_visible()
        assert login_page.is_password_field_visible()
        assert login_page.is_submit_button_visible()