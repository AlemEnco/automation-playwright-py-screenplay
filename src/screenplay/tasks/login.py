"""
Login-related tasks for the Screenplay pattern.
"""
from src.screenplay.base import Task, Actor
from src.screenplay.interactions.navigate import Navigate
from src.screenplay.interactions.type import Type
from src.screenplay.interactions.click import Click
from src.pages.login_page import LoginPageLocators
from src.config.settings import settings


class Login(Task):
    """Task to perform login with credentials."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def with_credentials(cls, username: str, password: str) -> 'Login':
        """Create a Login task with specific credentials."""
        return cls(username, password)

    @classmethod
    def with_valid_credentials(cls) -> 'Login':
        """Create a Login task with valid credentials from config."""
        credentials = settings.get_credentials()["valid"]
        return cls(credentials["username"], credentials["password"])

    @classmethod
    def with_invalid_credentials(cls) -> 'Login':
        """Create a Login task with invalid credentials from config."""
        credentials = settings.get_credentials()["invalid"]
        return cls(credentials["username"], credentials["password"])

    def perform_as(self, actor: Actor) -> None:
        """Perform the login task as the given actor."""
        actor.attempts_to(
            Navigate.to(settings.get_test_urls()["login"]),
            Type.the_text(self.username).into(LoginPageLocators.USERNAME_FIELD),
            Type.the_text(self.password).into(LoginPageLocators.PASSWORD_FIELD),
            Click.on(LoginPageLocators.SUBMIT_BUTTON)
        )

    def __str__(self) -> str:
        return f"Login with username '{self.username}'"


class NavigateToLoginPage(Task):
    """Task to navigate to the login page."""

    def perform_as(self, actor: Actor) -> None:
        """Navigate to the login page."""
        actor.attempts_to(
            Navigate.to(settings.get_test_urls()["login"])
        )

    def __str__(self) -> str:
        return "Navigate to login page"


class EnterCredentials(Task):
    """Task to enter credentials without submitting."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def with_values(cls, username: str, password: str) -> 'EnterCredentials':
        """Create an EnterCredentials task with specific values."""
        return cls(username, password)

    def perform_as(self, actor: Actor) -> None:
        """Enter credentials without submitting."""
        actor.attempts_to(
            Type.the_text(self.username).into(LoginPageLocators.USERNAME_FIELD),
            Type.the_text(self.password).into(LoginPageLocators.PASSWORD_FIELD)
        )

    def __str__(self) -> str:
        return f"Enter credentials (username: '{self.username}')"


class SubmitLoginForm(Task):
    """Task to submit the login form."""

    def perform_as(self, actor: Actor) -> None:
        """Submit the login form."""
        actor.attempts_to(
            Click.on(LoginPageLocators.SUBMIT_BUTTON)
        )

    def __str__(self) -> str:
        return "Submit login form"