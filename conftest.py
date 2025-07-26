"""
Pytest configuration and shared fixtures.
"""
import pytest
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
import sys
sys.path.insert(0, str(src_path))

# Import all fixtures from utils.fixtures
from src.utils.fixtures import *

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    # Register custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login functionality test")
    config.addinivalue_line("markers", "ui: mark test as UI test")
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "skip_in_ci: skip test in CI environment")

    # Create necessary directories
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "screenshots").mkdir(exist_ok=True)
    (reports_dir / "videos").mkdir(exist_ok=True)
    (reports_dir / "traces").mkdir(exist_ok=True)
    (reports_dir / "allure-results").mkdir(exist_ok=True)

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location and name."""
    for item in items:
        # Add markers based on test file location
        if "login" in str(item.fspath).lower():
            item.add_marker(pytest.mark.login)

        if "ui" in str(item.fspath).lower() or "e2e" in str(item.fspath).lower():
            item.add_marker(pytest.mark.ui)

        # Add markers based on test name
        if "smoke" in item.name.lower():
            item.add_marker(pytest.mark.smoke)

        if "regression" in item.name.lower():
            item.add_marker(pytest.mark.regression)

        # Skip tests in CI if marked
        if item.get_closest_marker("skip_in_ci") and os.getenv("CI"):
            item.add_marker(pytest.mark.skip(reason="Skipped in CI environment"))


# HTML report customization hooks are handled by pytest-html plugin automatically


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up the test environment before running tests."""
    from src.utils.logger import get_logger
    logger = get_logger(__name__)

    logger.info("Setting up test environment...")

    # Clean up old screenshots if needed
    from src.utils.screenshot import screenshot_manager
    screenshot_manager.cleanup_old_screenshots(days_to_keep=7)

    yield

    logger.info("Test environment cleanup completed")