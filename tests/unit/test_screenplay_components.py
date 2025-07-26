"""
Unit tests for Screenplay pattern components.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.screenplay.base import Actor, Task, Question, Ability
from src.screenplay.abilities.browse_the_web import BrowseTheWeb
from src.screenplay.interactions.click import Click
from src.screenplay.interactions.type import Type
from src.screenplay.interactions.navigate import Navigate
from src.screenplay.questions.text import Text, CurrentUrl
from src.screenplay.questions.visibility import Visibility


class TestActor:
    """Test cases for the Actor class."""

    def test_actor_creation(self):
        """Test that an actor can be created with a name."""
        actor = Actor("TestUser")
        assert actor.name == "TestUser"
        assert len(actor._abilities) == 0

    def test_actor_can_be_granted_abilities(self):
        """Test that an actor can be granted abilities."""
        mock_ability = Mock(spec=Ability)
        mock_ability.as_actor.return_value = mock_ability

        actor = Actor("TestUser")
        result = actor.who_can(mock_ability)

        assert result is actor  # Should return self for chaining
        assert actor.has_ability_to(type(mock_ability))
        mock_ability.as_actor.assert_called_once_with(actor)

    def test_actor_can_check_for_abilities(self):
        """Test that an actor can check if it has specific abilities."""
        mock_ability = Mock(spec=Ability)
        mock_ability.as_actor.return_value = mock_ability

        actor = Actor("TestUser")

        # Should not have ability initially
        assert not actor.has_ability_to(type(mock_ability))

        # Should have ability after granting it
        actor.who_can(mock_ability)
        assert actor.has_ability_to(type(mock_ability))

    def test_actor_can_retrieve_abilities(self):
        """Test that an actor can retrieve specific abilities."""
        mock_ability = Mock(spec=Ability)
        mock_ability.as_actor.return_value = mock_ability

        actor = Actor("TestUser")
        actor.who_can(mock_ability)

        retrieved_ability = actor.ability_to(type(mock_ability))
        assert retrieved_ability is mock_ability

    def test_actor_raises_error_for_missing_ability(self):
        """Test that an actor raises an error when trying to use a missing ability."""
        actor = Actor("TestUser")

        with pytest.raises(ValueError, match="does not have the ability"):
            actor.ability_to(BrowseTheWeb)

    def test_actor_can_perform_tasks(self):
        """Test that an actor can perform tasks."""
        mock_task = Mock(spec=Task)
        actor = Actor("TestUser")

        result = actor.attempts_to(mock_task)

        assert result is actor  # Should return self for chaining
        mock_task.perform_as.assert_called_once_with(actor)

    def test_actor_can_ask_questions(self):
        """Test that an actor can ask questions."""
        mock_question = Mock(spec=Question)
        mock_question.answered_by.return_value = "test_answer"

        actor = Actor("TestUser")
        answer = actor.asks(mock_question)

        assert answer == "test_answer"
        mock_question.answered_by.assert_called_once_with(actor)


class TestBrowseTheWebAbility:
    """Test cases for the BrowseTheWeb ability."""

    def test_browse_the_web_creation_with_browser(self):
        """Test creating BrowseTheWeb ability with a browser."""
        mock_browser = Mock()
        ability = BrowseTheWeb.using(mock_browser)

        assert ability._browser is mock_browser
        assert ability._context is None
        assert ability._page is None

    def test_browse_the_web_creation_with_page(self):
        """Test creating BrowseTheWeb ability with an existing page."""
        mock_page = Mock()
        mock_context = Mock()
        mock_browser = Mock()
        mock_page.context = mock_context
        mock_context.browser = mock_browser

        ability = BrowseTheWeb.using_page(mock_page)

        assert ability._browser is mock_browser
        assert ability._context is mock_context
        assert ability._page is mock_page

    def test_browse_the_web_as_actor(self):
        """Test binding BrowseTheWeb ability to an actor."""
        mock_browser = Mock()
        mock_actor = Mock(spec=Actor)
        mock_actor.name = "TestUser"

        ability = BrowseTheWeb.using(mock_browser)
        bound_ability = ability.as_actor(mock_actor)

        assert bound_ability._actor is mock_actor
        assert bound_ability._browser is mock_browser

    def test_browse_the_web_context_creation(self):
        """Test that context is created when accessed."""
        mock_browser = Mock()
        mock_context = Mock()
        mock_browser.new_context.return_value = mock_context

        ability = BrowseTheWeb.using(mock_browser)
        context = ability.context

        assert context is mock_context
        mock_browser.new_context.assert_called_once()

    def test_browse_the_web_page_creation(self):
        """Test that page is created when accessed."""
        mock_browser = Mock()
        mock_context = Mock()
        mock_page = Mock()
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        ability = BrowseTheWeb.using(mock_browser)
        page = ability.page

        assert page is mock_page
        mock_context.new_page.assert_called_once()


class TestInteractions:
    """Test cases for interaction classes."""

    def test_click_interaction(self):
        """Test Click interaction."""
        mock_actor = Mock(spec=Actor)
        mock_ability = Mock(spec=BrowseTheWeb)
        mock_page = Mock()
        mock_ability.page = mock_page
        mock_actor.ability_to.return_value = mock_ability

        click = Click.on("#test-button")
        click.perform_as(mock_actor)

        mock_actor.ability_to.assert_called_once_with(BrowseTheWeb)
        mock_page.wait_for_selector.assert_called_once_with("#test-button", state="visible")
        mock_page.click.assert_called_once_with("#test-button")

    def test_type_interaction(self):
        """Test Type interaction."""
        mock_actor = Mock(spec=Actor)
        mock_ability = Mock(spec=BrowseTheWeb)
        mock_page = Mock()
        mock_ability.page = mock_page
        mock_actor.ability_to.return_value = mock_ability

        type_action = Type.the_text("test text").into("#test-input")
        type_action.perform_as(mock_actor)

        mock_actor.ability_to.assert_called_once_with(BrowseTheWeb)
        mock_page.wait_for_selector.assert_called_once_with("#test-input", state="visible")
        mock_page.fill.assert_called_once_with("#test-input", "")
        mock_page.type.assert_called_once_with("#test-input", "test text")

    def test_navigate_interaction(self):
        """Test Navigate interaction."""
        mock_actor = Mock(spec=Actor)
        mock_ability = Mock(spec=BrowseTheWeb)
        mock_page = Mock()
        mock_ability.page = mock_page
        mock_actor.ability_to.return_value = mock_ability

        navigate = Navigate.to("https://example.com")
        navigate.perform_as(mock_actor)

        mock_actor.ability_to.assert_called_once_with(BrowseTheWeb)
        mock_page.goto.assert_called_once_with("https://example.com")
        mock_page.wait_for_load_state.assert_called_once_with("networkidle")


class TestQuestions:
    """Test cases for question classes."""

    def test_text_question(self):
        """Test Text question."""
        mock_actor = Mock(spec=Actor)
        mock_ability = Mock(spec=BrowseTheWeb)
        mock_page = Mock()
        mock_ability.page = mock_page
        mock_actor.ability_to.return_value = mock_ability
        mock_page.text_content.return_value = "test text"

        text_question = Text.of("#test-element")
        result = text_question.answered_by(mock_actor)

        assert result == "test text"
        mock_actor.ability_to.assert_called_once_with(BrowseTheWeb)
        mock_page.wait_for_selector.assert_called_once_with("#test-element", state="visible")
        mock_page.text_content.assert_called_once_with("#test-element")

    def test_current_url_question(self):
        """Test CurrentUrl question."""
        mock_actor = Mock(spec=Actor)
        mock_ability = Mock(spec=BrowseTheWeb)
        mock_page = Mock()
        mock_ability.page = mock_page
        mock_actor.ability_to.return_value = mock_ability
        mock_page.url = "https://example.com/current"

        url_question = CurrentUrl()
        result = url_question.answered_by(mock_actor)

        assert result == "https://example.com/current"
        mock_actor.ability_to.assert_called_once_with(BrowseTheWeb)

    def test_visibility_question(self):
        """Test Visibility question."""
        mock_actor = Mock(spec=Actor)
        mock_ability = Mock(spec=BrowseTheWeb)
        mock_page = Mock()
        mock_ability.page = mock_page
        mock_actor.ability_to.return_value = mock_ability
        mock_page.is_visible.return_value = True

        visibility_question = Visibility.of("#test-element")
        result = visibility_question.answered_by(mock_actor)

        assert result is True
        mock_actor.ability_to.assert_called_once_with(BrowseTheWeb)
        mock_page.is_visible.assert_called_once_with("#test-element")