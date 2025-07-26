"""
Pytest fixtures for the test automation framework.
"""
import pytest
from typing import Generator
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from src.config.settings import settings
from src.screenplay.base import Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb
from src.utils.logger import get_logger, log_test_start, log_test_pass, log_test_fail
from src.utils.screenshot import take_failure_screenshot

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Provide a Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Provide a browser instance for the test session."""
    browser_config = settings.get_browser_config()

    # Launch browser based on configuration
    if settings.browser.browser_name.lower() == "chromium":
        browser = playwright_instance.chromium.launch(
            headless=browser_config["headless"],
            slow_mo=browser_config["slow_mo"]
        )
    elif settings.browser.browser_name.lower() == "firefox":
        browser = playwright_instance.firefox.launch(
            headless=browser_config["headless"],
            slow_mo=browser_config["slow_mo"]
        )
    elif settings.browser.browser_name.lower() == "webkit":
        browser = playwright_instance.webkit.launch(
            headless=browser_config["headless"],
            slow_mo=browser_config["slow_mo"]
        )
    else:
        raise ValueError(f"Unsupported browser: {settings.browser.browser_name}")

    logger.info(f"Browser launched: {settings.browser.browser_name}")
    yield browser
    browser.close()
    logger.info("Browser closed")


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Provide a browser context for each test."""
    browser_config = settings.get_browser_config()

    context = browser.new_context(
        viewport=browser_config["viewport"],
        record_video_dir="reports/videos" if browser_config["video"] == "on" else None,
        record_video_size=browser_config["viewport"] if browser_config["video"] == "on" else None
    )

    # Enable tracing if configured
    if browser_config["trace"] == "on":
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # Save trace if enabled
    if browser_config["trace"] == "on":
        context.tracing.stop(path="reports/traces/trace.zip")

    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Provide a page for each test."""
    page = context.new_page()

    # Set default timeout
    page.set_default_timeout(settings.browser.timeout)

    yield page
    page.close()


@pytest.fixture(scope="function")
def actor(page: Page) -> Generator[Actor, None, None]:
    """Provide an actor with BrowseTheWeb ability for each test."""
    test_actor = Actor("TestUser").who_can(BrowseTheWeb.using_page(page))
    yield test_actor


@pytest.fixture(scope="function")
def admin_actor(page: Page) -> Generator[Actor, None, None]:
    """Provide an admin actor for tests requiring admin privileges."""
    admin_actor = Actor("AdminUser").who_can(BrowseTheWeb.using_page(page))
    yield admin_actor


@pytest.fixture(autouse=True)
def test_logging(request):
    """Automatically log test start, pass, and fail for all tests."""
    test_name = request.node.name
    test_description = request.node.function.__doc__ or ""

    # Log test start
    log_test_start(test_name, test_description.strip())

    # Track test duration
    import time
    start_time = time.time()

    def log_test_result():
        duration = time.time() - start_time

        if hasattr(request.node, 'rep_call'):
            if request.node.rep_call.passed:
                log_test_pass(test_name, duration)
            elif request.node.rep_call.failed:
                error_message = str(request.node.rep_call.longrepr)
                log_test_fail(test_name, error_message, duration)

    # Register finalizer to log result
    request.addfinalizer(log_test_result)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """Automatically take screenshot on test failure."""
    yield

    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        test_name = request.node.name
        error_message = str(request.node.rep_call.longrepr)
        take_failure_screenshot(page, test_name, error_message)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for logging and screenshots."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def test_data():
    """Provide test data for tests."""
    from src.data.test_data import LoginTestData
    return LoginTestData


@pytest.fixture(scope="function")
def valid_credentials():
    """Provide valid login credentials."""
    return settings.get_credentials()["valid"]


@pytest.fixture(scope="function")
def invalid_credentials():
    """Provide invalid login credentials."""
    return settings.get_credentials()["invalid"]


@pytest.fixture(scope="function")
def test_urls():
    """Provide test URLs."""
    return settings.get_test_urls()