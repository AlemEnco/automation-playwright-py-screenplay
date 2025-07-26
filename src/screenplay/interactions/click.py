"""
Click interaction for the Screenplay pattern.
"""
from typing import Optional, Dict, Any
from src.screenplay.base import Interaction, Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb


class Click(Interaction):
    """Interaction to click on an element."""

    def __init__(self, locator: str, options: Optional[Dict[str, Any]] = None):
        self.locator = locator
        self.options = options or {}

    @classmethod
    def on(cls, locator: str, **options) -> 'Click':
        """Create a Click interaction for the given locator."""
        return cls(locator, options)

    def perform_as(self, actor: Actor) -> None:
        """Perform the click action as the given actor."""
        browse_ability = actor.ability_to(BrowseTheWeb)
        page = browse_ability.page

        # Wait for element to be visible and clickable
        page.wait_for_selector(self.locator, state="visible")
        page.click(self.locator, **self.options)

    def __str__(self) -> str:
        return f"Click on '{self.locator}'"