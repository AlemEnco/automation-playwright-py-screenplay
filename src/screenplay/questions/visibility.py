"""
Visibility-related questions for the Screenplay pattern.
"""
from src.screenplay.base import Question, Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb


class Visibility(Question[bool]):
    """Question to check if an element is visible."""

    def __init__(self, locator: str):
        self.locator = locator

    @classmethod
    def of(cls, locator: str) -> 'Visibility':
        """Create a Visibility question for the given locator."""
        return cls(locator)

    def answered_by(self, actor: Actor) -> bool:
        """Check if the element is visible."""
        browse_ability = actor.ability_to(BrowseTheWeb)
        page = browse_ability.page

        try:
            return page.is_visible(self.locator)
        except Exception:
            return False

    def __str__(self) -> str:
        return f"Visibility of '{self.locator}'"


class Presence(Question[bool]):
    """Question to check if an element is present in the DOM."""

    def __init__(self, locator: str):
        self.locator = locator

    @classmethod
    def of(cls, locator: str) -> 'Presence':
        """Create a Presence question for the given locator."""
        return cls(locator)

    def answered_by(self, actor: Actor) -> bool:
        """Check if the element is present in the DOM."""
        browse_ability = actor.ability_to(BrowseTheWeb)
        page = browse_ability.page

        try:
            element = page.query_selector(self.locator)
            return element is not None
        except Exception:
            return False

    def __str__(self) -> str:
        return f"Presence of '{self.locator}'"