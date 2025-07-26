"""
Configuration settings for the test automation framework.
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class BrowserSettings(BaseModel):
    """Browser configuration settings."""

    browser_name: str = Field(default="chromium")
    headless: bool = Field(default=True)
    slow_mo: int = Field(default=0)
    timeout: int = Field(default=30000)
    viewport_width: int = Field(default=1920)
    viewport_height: int = Field(default=1080)
    video: bool = Field(default=False)
    screenshot: str = Field(default="only-on-failure")
    trace: bool = Field(default=False)

    def __init__(self, **kwargs):
        # Get values from environment variables with fallbacks
        data = {
            'browser_name': os.getenv('BROWSER_NAME', 'chromium'),
            'headless': os.getenv('HEADLESS', 'true').lower() == 'true',
            'slow_mo': int(os.getenv('SLOW_MO', '0')),
            'timeout': int(os.getenv('TIMEOUT', '30000')),
            'viewport_width': int(os.getenv('VIEWPORT_WIDTH', '1920')),
            'viewport_height': int(os.getenv('VIEWPORT_HEIGHT', '1080')),
            'video': os.getenv('VIDEO', 'false').lower() == 'true',
            'screenshot': os.getenv('SCREENSHOT', 'only-on-failure'),
            'trace': os.getenv('TRACE', 'false').lower() == 'true',
        }
        data.update(kwargs)
        super().__init__(**data)


class EnvironmentSettings(BaseModel):
    """Environment-specific settings."""

    environment: str = Field(default="dev")
    base_url: str = Field(default="https://practicetestautomation.com")
    api_base_url: str = Field(default="")

    # Test data
    valid_username: str = Field(default="student")
    valid_password: str = Field(default="Password123")
    invalid_username: str = Field(default="incorrectUser")
    invalid_password: str = Field(default="incorrectPassword")

    def __init__(self, **kwargs):
        # Get values from environment variables with fallbacks
        data = {
            'environment': os.getenv('ENVIRONMENT', 'dev'),
            'base_url': os.getenv('BASE_URL', 'https://practicetestautomation.com'),
            'api_base_url': os.getenv('API_BASE_URL', ''),
            'valid_username': os.getenv('VALID_USERNAME', 'student'),
            'valid_password': os.getenv('VALID_PASSWORD', 'Password123'),
            'invalid_username': os.getenv('INVALID_USERNAME', 'incorrectUser'),
            'invalid_password': os.getenv('INVALID_PASSWORD', 'incorrectPassword'),
        }
        data.update(kwargs)
        super().__init__(**data)


class TestSettings(BaseModel):
    """Test execution settings."""

    retry_count: int = Field(default=2)
    parallel_workers: int = Field(default=1)
    test_data_path: str = Field(default="src/data")
    reports_path: str = Field(default="reports")
    logs_path: str = Field(default="logs")
    screenshots_path: str = Field(default="reports/screenshots")

    def __init__(self, **kwargs):
        # Get values from environment variables with fallbacks
        data = {
            'retry_count': int(os.getenv('RETRY_COUNT', '2')),
            'parallel_workers': int(os.getenv('PARALLEL_WORKERS', '1')),
            'test_data_path': os.getenv('TEST_DATA_PATH', 'src/data'),
            'reports_path': os.getenv('REPORTS_PATH', 'reports'),
            'logs_path': os.getenv('LOGS_PATH', 'logs'),
            'screenshots_path': os.getenv('SCREENSHOTS_PATH', 'reports/screenshots'),
        }
        data.update(kwargs)
        super().__init__(**data)


class Settings:
    """Main settings class that combines all configuration."""

    def __init__(self):
        self.browser = BrowserSettings()
        self.environment = EnvironmentSettings()
        self.test = TestSettings()
        self.project_root = Path(__file__).parent.parent.parent

    def get_browser_config(self) -> Dict[str, Any]:
        """Get browser configuration for Playwright."""
        return {
            "headless": self.browser.headless,
            "slow_mo": self.browser.slow_mo,
            "viewport": {
                "width": self.browser.viewport_width,
                "height": self.browser.viewport_height
            },
            "video": "on" if self.browser.video else "off",
            "screenshot": self.browser.screenshot,
            "trace": "on" if self.browser.trace else "off"
        }

    def get_test_urls(self) -> Dict[str, str]:
        """Get test URLs for different pages."""
        return {
            "login": f"{self.environment.base_url}/practice-test-login/",
            "logged_in": f"{self.environment.base_url}/logged-in-successfully/",
            "home": self.environment.base_url
        }

    def get_credentials(self) -> Dict[str, Dict[str, str]]:
        """Get test credentials."""
        return {
            "valid": {
                "username": self.environment.valid_username,
                "password": self.environment.valid_password
            },
            "invalid": {
                "username": self.environment.invalid_username,
                "password": self.environment.invalid_password
            }
        }


# Global settings instance
settings = Settings()