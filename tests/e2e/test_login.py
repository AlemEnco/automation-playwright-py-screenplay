"""
End-to-end tests for login functionality using the Screenplay pattern.
"""
import pytest
import allure
from src.screenplay.base import Actor
from src.screenplay.tasks.login import Login, NavigateToLoginPage
from src.screenplay.questions.text import Text, CurrentUrl
from src.screenplay.questions.visibility import Visibility
from src.pages.login_page import LoginPageLocators
from src.pages.logged_in_page import LoggedInPageLocators
from src.data.test_data import LoginTestData
from src.utils.logger import log_step
from src.config.settings import settings


@allure.epic("Authentication")
@allure.feature("Login")
class TestLogin:
    """Test suite for login functionality."""

    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login_with_valid_credentials(self, actor: Actor):
        """Test successful login with valid credentials."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Verify login page is displayed"):
            log_step("Verify login page is displayed")
            assert actor.asks(Visibility.of(LoginPageLocators.USERNAME_FIELD))
            assert actor.asks(Visibility.of(LoginPageLocators.PASSWORD_FIELD))
            assert actor.asks(Visibility.of(LoginPageLocators.SUBMIT_BUTTON))

        with allure.step("Login with valid credentials"):
            log_step("Login with valid credentials")
            actor.attempts_to(Login.with_valid_credentials())

        with allure.step("Verify successful login"):
            log_step("Verify successful login")
            # Check URL contains logged-in path
            current_url = actor.asks(CurrentUrl())
            assert "/logged-in-successfully/" in current_url

            # Check success message is displayed
            assert actor.asks(Visibility.of(LoggedInPageLocators.SUCCESS_MESSAGE))

            # Verify success message text
            success_text = actor.asks(Text.of(LoggedInPageLocators.SUCCESS_MESSAGE))
            assert "Congratulations" in success_text or "logged in successfully" in success_text.lower()

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_invalid_username(self, actor: Actor):
        """Test login failure with invalid username."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Login with invalid username"):
            log_step("Login with invalid username")
            credentials = LoginTestData.INVALID_USERNAME
            actor.attempts_to(
                Login.with_credentials(credentials.username, credentials.password)
            )

        with allure.step("Verify login failure"):
            log_step("Verify login failure")
            # Should remain on login page
            current_url = actor.asks(CurrentUrl())
            assert "/practice-test-login/" in current_url

            # Error message should be displayed
            assert actor.asks(Visibility.of(LoginPageLocators.ERROR_MESSAGE))

            # Verify error message text
            error_text = actor.asks(Text.of(LoginPageLocators.ERROR_MESSAGE))
            assert "username" in error_text.lower() or "invalid" in error_text.lower()

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_invalid_password(self, actor: Actor):
        """Test login failure with invalid password."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Login with invalid password"):
            log_step("Login with invalid password")
            credentials = LoginTestData.INVALID_PASSWORD
            actor.attempts_to(
                Login.with_credentials(credentials.username, credentials.password)
            )

        with allure.step("Verify login failure"):
            log_step("Verify login failure")
            # Should remain on login page
            current_url = actor.asks(CurrentUrl())
            assert "/practice-test-login/" in current_url

            # Error message should be displayed
            assert actor.asks(Visibility.of(LoginPageLocators.ERROR_MESSAGE))

            # Verify error message text
            error_text = actor.asks(Text.of(LoginPageLocators.ERROR_MESSAGE))
            assert "password" in error_text.lower() or "invalid" in error_text.lower()

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_both_invalid_credentials(self, actor: Actor):
        """Test login failure with both invalid username and password."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Login with both invalid credentials"):
            log_step("Login with both invalid credentials")
            credentials = LoginTestData.BOTH_INVALID
            actor.attempts_to(
                Login.with_credentials(credentials.username, credentials.password)
            )

        with allure.step("Verify login failure"):
            log_step("Verify login failure")
            # Should remain on login page
            current_url = actor.asks(CurrentUrl())
            assert "/practice-test-login/" in current_url

            # Error message should be displayed
            assert actor.asks(Visibility.of(LoginPageLocators.ERROR_MESSAGE))

            # Verify error message is present
            error_text = actor.asks(Text.of(LoginPageLocators.ERROR_MESSAGE))
            assert len(error_text.strip()) > 0

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_empty_username(self, actor: Actor):
        """Test login failure with empty username."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Login with empty username"):
            log_step("Login with empty username")
            credentials = LoginTestData.EMPTY_USERNAME
            actor.attempts_to(
                Login.with_credentials(credentials.username, credentials.password)
            )

        with allure.step("Verify login failure"):
            log_step("Verify login failure")
            # Should remain on login page
            current_url = actor.asks(CurrentUrl())
            assert "/practice-test-login/" in current_url

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_empty_password(self, actor: Actor):
        """Test login failure with empty password."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Login with empty password"):
            log_step("Login with empty password")
            credentials = LoginTestData.EMPTY_PASSWORD
            actor.attempts_to(
                Login.with_credentials(credentials.username, credentials.password)
            )

        with allure.step("Verify login failure"):
            log_step("Verify login failure")
            # Should remain on login page
            current_url = actor.asks(CurrentUrl())
            assert "/practice-test-login/" in current_url

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_both_empty_fields(self, actor: Actor):
        """Test login failure with both empty fields."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Login with both empty fields"):
            log_step("Login with both empty fields")
            credentials = LoginTestData.BOTH_EMPTY
            actor.attempts_to(
                Login.with_credentials(credentials.username, credentials.password)
            )

        with allure.step("Verify login failure"):
            log_step("Verify login failure")
            # Should remain on login page
            current_url = actor.asks(CurrentUrl())
            assert "/practice-test-login/" in current_url


@allure.epic("Authentication")
@allure.feature("Login UI")
class TestLoginUI:
    """Test suite for login UI elements and interactions."""

    @allure.story("Login Page Elements")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.login
    def test_login_page_elements_are_visible(self, actor: Actor):
        """Test that all login page elements are visible and accessible."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Verify all login elements are visible"):
            log_step("Verify all login elements are visible")

            # Check form elements
            assert actor.asks(Visibility.of(LoginPageLocators.USERNAME_FIELD))
            assert actor.asks(Visibility.of(LoginPageLocators.PASSWORD_FIELD))
            assert actor.asks(Visibility.of(LoginPageLocators.SUBMIT_BUTTON))
            assert actor.asks(Visibility.of(LoginPageLocators.LOGIN_FORM))

            # Check page title
            assert actor.asks(Visibility.of(LoginPageLocators.PAGE_TITLE))
            page_title = actor.asks(Text.of(LoginPageLocators.PAGE_TITLE))
            assert len(page_title.strip()) > 0

    @allure.story("Login Page Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.login
    def test_login_page_url_and_title(self, actor: Actor):
        """Test login page URL and title are correct."""

        with allure.step("Navigate to login page"):
            log_step("Navigate to login page")
            actor.attempts_to(NavigateToLoginPage())

        with allure.step("Verify URL and page title"):
            log_step("Verify URL and page title")

            # Check URL
            current_url = actor.asks(CurrentUrl())
            assert "/practice-test-login/" in current_url

            # Check page has content
            page_title = actor.asks(Text.of(LoginPageLocators.PAGE_TITLE))
            assert len(page_title.strip()) > 0


@allure.epic("Authentication")
@allure.feature("Data-Driven Login Tests")
class TestLoginDataDriven:
    """Data-driven tests for login functionality."""

    @allure.story("Invalid Login Scenarios")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.parametrize("credentials", LoginTestData.get_invalid_test_cases())
    def test_login_with_invalid_credentials_parametrized(self, actor: Actor, credentials):
        """Test login with various invalid credential combinations."""

        with allure.step(f"Test case: {credentials.description}"):
            log_step(f"Testing: {credentials.description}")

            with allure.step("Navigate to login page"):
                actor.attempts_to(NavigateToLoginPage())

            with allure.step(f"Login with credentials: {credentials.username}"):
                actor.attempts_to(
                    Login.with_credentials(credentials.username, credentials.password)
                )

            with allure.step("Verify login failure"):
                # Should remain on login page for all invalid cases
                current_url = actor.asks(CurrentUrl())
                assert "/practice-test-login/" in current_url

                # For non-empty credentials, error message should be displayed
                if credentials.username.strip() and credentials.password.strip():
                    assert actor.asks(Visibility.of(LoginPageLocators.ERROR_MESSAGE))