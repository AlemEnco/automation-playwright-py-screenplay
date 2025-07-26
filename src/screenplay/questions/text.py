"""
Text-related questions for the Screenplay pattern.
"""
from typing import Optional
from src.screenplay.base import Question, Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb


class Text(Question[str]):
    """Question to get text content from an element."""

    def __init__(self, locator: str):
        self.locator = locator

    @classmethod
    def of(cls, locator: str) -> 'Text':
        """Create a Text question for the given locator."""
        return cls(locator)

    def answered_by(self, actor: Actor) -> str:
        """Get the text content of the element."""
        browse_ability = actor.ability_to(BrowseTheWeb)
        page = browse_ability.page

        # Wait for element to be visible
        page.wait_for_selector(self.locator, state="visible")

        # Get the text content
        return page.text_content(self.locator) or ""

    def __str__(self) -> str:
        return f"Text of '{self.locator}'"


class CurrentUrl(Question[str]):
    """Question to get the current URL."""

    def answered_by(self, actor: Actor) -> str:
        """Get the current URL."""
        browse_ability = actor.ability_to(BrowseTheWeb)
        page = browse_ability.page
        return page.url

    def __str__(self) -> str:
        return "Current URL"


class PageTitle(Question[str]):
    """Question to get the page title."""

    def answered_by(self, actor: Actor) -> str:
        """Get the page title."""
        browse_ability = actor.ability_to(BrowseTheWeb)
        page = browse_ability.page
        return page.title()

    def __str__(self) -> str:
        return "Page title"