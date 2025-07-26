"""
Base classes for the Screenplay pattern implementation.
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, Optional
from playwright.sync_api import Page, Browser

# Type variables for generic classes
T = TypeVar('T')
ActorType = TypeVar('ActorType', bound='Actor')


class Performable(ABC):
    """Base class for all performable actions (Tasks and Interactions)."""

    @abstractmethod
    def perform_as(self, actor: 'Actor') -> Any:
        """Perform this action as the given actor."""
        pass


class Task(Performable):
    """Base class for high-level business tasks."""

    @abstractmethod
    def perform_as(self, actor: 'Actor') -> Any:
        """Perform this task as the given actor."""
        pass


class Interaction(Performable):
    """Base class for low-level UI interactions."""

    @abstractmethod
    def perform_as(self, actor: 'Actor') -> Any:
        """Perform this interaction as the given actor."""
        pass


class Question(ABC, Generic[T]):
    """Base class for questions that can be asked about the system state."""

    @abstractmethod
    def answered_by(self, actor: 'Actor') -> T:
        """Answer this question using the given actor's abilities."""
        pass


class Ability(ABC):
    """Base class for actor abilities."""

    @abstractmethod
    def as_actor(self, actor: 'Actor') -> 'Ability':
        """Return this ability bound to the given actor."""
        pass


class Actor:
    """
    An actor represents a user or system that can perform actions.
    Actors have abilities that allow them to interact with the system.
    """

    def __init__(self, name: str):
        self.name = name
        self._abilities: dict[type, Ability] = {}

    def who_can(self, *abilities: Ability) -> 'Actor':
        """Grant abilities to this actor."""
        for ability in abilities:
            self._abilities[type(ability)] = ability.as_actor(self)
        return self

    def attempts_to(self, *tasks: Performable) -> 'Actor':
        """Attempt to perform the given tasks."""
        for task in tasks:
            task.perform_as(self)
        return self

    def asks(self, question: Question[T]) -> T:
        """Ask a question and return the answer."""
        return question.answered_by(self)

    def has_ability_to(self, ability_class: type) -> bool:
        """Check if the actor has a specific ability."""
        return ability_class in self._abilities

    def ability_to(self, ability_class: type) -> Ability:
        """Get a specific ability."""
        if not self.has_ability_to(ability_class):
            raise ValueError(f"Actor {self.name} does not have the ability {ability_class.__name__}")
        return self._abilities[ability_class]

    def __str__(self) -> str:
        return f"Actor({self.name})"

    def __repr__(self) -> str:
        return self.__str__()