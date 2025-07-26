"""
Type interaction for the Screenplay pattern.
"""
from typing import Optional, Dict, Any
from src.screenplay.base import Interaction, Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb


class Type(Interaction):
    """Interaction to type text into an element."""

    def __init__(self, text: str, locator: str, options: Optional[Dict[str, Any]] = None):
        self.text = text
        self.locator = locator
        self.options = options or {}

    @classmethod
    def the_text(cls, text: str) -> 'TypeBuilder':
        """Start building a Type interaction with the given text."""
        return TypeBuilder(text)

    def perform_as(self, actor: Actor) -> None:
        """Perform the type action as the given actor."""
        browse_ability = actor.ability_to(BrowseTheWeb)
        page = browse_ability.page

        # Wait for element to be visible
        page.wait_for_selector(self.locator, state="visible")

        # Clear the field first if specified
        if self.options.get('clear', True):
            page.fill(self.locator, "")

        # Type the text
        page.type(self.locator, self.text, **{k: v for k, v in self.options.items() if k != 'clear'})

    def __str__(self) -> str:
        return f"Type '{self.text}' into '{self.locator}'"


class TypeBuilder:
    """Builder class for Type interactions."""

    def __init__(self, text: str):
        self.text = text

    def into(self, locator: str, **options) -> Type:
        """Specify the target element for typing."""
        return Type(self.text, locator, options)