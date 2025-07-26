"""
Navigate interaction for the Screenplay pattern.
"""
from typing import Optional, Dict, Any
from src.screenplay.base import Interaction, Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb


class Navigate(Interaction):
    """Interaction to navigate to a URL."""

    def __init__(self, url: str, options: Optional[Dict[str, Any]] = None):
        self.url = url
        self.options = options or {}

    @classmethod
    def to(cls, url: str, **options) -> 'Navigate':
        """Create a Navigate interaction to the given URL."""
        return cls(url, options)

    def perform_as(self, actor: Actor) -> None:
        """Perform the navigation as the given actor."""
        browse_ability = actor.ability_to(BrowseTheWeb)
        page = browse_ability.page

        # Navigate to the URL
        page.goto(self.url, **self.options)

        # Wait for the page to load
        page.wait_for_load_state("networkidle")

    def __str__(self) -> str:
        return f"Navigate to '{self.url}'"