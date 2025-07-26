"""
Screenshot utilities for test automation.
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from playwright.sync_api import Page
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ScreenshotManager:
    """Manager for taking and organizing screenshots during test execution."""

    def __init__(self):
        self.screenshots_dir = Path(settings.test.screenshots_path)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    def take_screenshot(
        self,
        page: Page,
        name: str,
        test_name: Optional[str] = None,
        full_page: bool = True
    ) -> str:
        """
        Take a screenshot and save it with a descriptive name.

        Args:
            page: Playwright page object
            name: Descriptive name for the screenshot
            test_name: Name of the test (for organization)
            full_page: Whether to capture the full page or just viewport

        Returns:
            Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

        # Create filename
        if test_name:
            filename = f"{test_name}_{name}_{timestamp}.png"
        else:
            filename = f"{name}_{timestamp}.png"

        # Sanitize filename
        filename = self._sanitize_filename(filename)

        # Create test-specific directory if test_name is provided
        if test_name:
            test_dir = self.screenshots_dir / self._sanitize_filename(test_name)
            test_dir.mkdir(exist_ok=True)
            screenshot_path = test_dir / filename
        else:
            screenshot_path = self.screenshots_dir / filename

        try:
            # Take screenshot
            page.screenshot(path=str(screenshot_path), full_page=full_page)
            logger.debug(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)

        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return ""

    def take_screenshot_on_failure(
        self,
        page: Page,
        test_name: str,
        error_message: str = ""
    ) -> str:
        """
        Take a screenshot when a test fails.

        Args:
            page: Playwright page object
            test_name: Name of the failed test
            error_message: Error message from the failure

        Returns:
            Path to the saved screenshot
        """
        name = "failure"
        if error_message:
            # Use first few words of error message in filename
            error_words = error_message.split()[:3]
            name = f"failure_{'_'.join(error_words)}"

        screenshot_path = self.take_screenshot(page, name, test_name)

        if screenshot_path:
            logger.error(f"Failure screenshot saved: {screenshot_path}")

        return screenshot_path

    def take_step_screenshot(
        self,
        page: Page,
        step_name: str,
        test_name: Optional[str] = None
    ) -> str:
        """
        Take a screenshot for a specific test step.

        Args:
            page: Playwright page object
            step_name: Name of the test step
            test_name: Name of the test

        Returns:
            Path to the saved screenshot
        """
        return self.take_screenshot(page, f"step_{step_name}", test_name)

    def take_before_after_screenshots(
        self,
        page: Page,
        action_name: str,
        test_name: Optional[str] = None
    ) -> tuple[str, callable]:
        """
        Take a 'before' screenshot and return a function to take the 'after' screenshot.

        Args:
            page: Playwright page object
            action_name: Name of the action being performed
            test_name: Name of the test

        Returns:
            Tuple of (before_screenshot_path, after_screenshot_function)
        """
        before_path = self.take_screenshot(page, f"before_{action_name}", test_name)

        def take_after():
            return self.take_screenshot(page, f"after_{action_name}", test_name)

        return before_path, take_after

    def cleanup_old_screenshots(self, days_to_keep: int = 7) -> None:
        """
        Clean up old screenshots to save disk space.

        Args:
            days_to_keep: Number of days to keep screenshots
        """
        try:
            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)

            for screenshot_file in self.screenshots_dir.rglob("*.png"):
                if screenshot_file.stat().st_mtime < cutoff_time:
                    screenshot_file.unlink()
                    logger.debug(f"Deleted old screenshot: {screenshot_file}")

        except Exception as e:
            logger.error(f"Error cleaning up screenshots: {str(e)}")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to be filesystem-safe."""
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # Remove multiple consecutive underscores
        while '__' in filename:
            filename = filename.replace('__', '_')

        # Limit length
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:196] + ext

        return filename


# Global screenshot manager instance
screenshot_manager = ScreenshotManager()

# Convenience functions
def take_screenshot(page: Page, name: str, test_name: Optional[str] = None, full_page: bool = True) -> str:
    """Take a screenshot."""
    return screenshot_manager.take_screenshot(page, name, test_name, full_page)

def take_failure_screenshot(page: Page, test_name: str, error_message: str = "") -> str:
    """Take a screenshot on test failure."""
    return screenshot_manager.take_screenshot_on_failure(page, test_name, error_message)

def take_step_screenshot(page: Page, step_name: str, test_name: Optional[str] = None) -> str:
    """Take a screenshot for a test step."""
    return screenshot_manager.take_step_screenshot(page, step_name, test_name)