# Test Automation Framework with Playwright and Screenplay Pattern

A comprehensive, scalable test automation framework built with Python, Playwright, and pytest, implementing the Screenplay design pattern for maintainable and readable test code.

## 🚀 Features

- **Screenplay Pattern Implementation**: Clean separation of concerns with Actors, Tasks, Questions, and Abilities
- **Playwright Integration**: Modern browser automation with cross-browser support
- **Pytest Framework**: Robust testing framework with fixtures, markers, and plugins
- **Comprehensive Logging**: Structured logging with multiple output formats
- **Screenshot Management**: Automatic screenshot capture on failures and test steps
- **Data-Driven Testing**: Parameterized tests with external test data
- **Environment Management**: Multi-environment configuration support
- **Retry Mechanisms**: Built-in retry logic for flaky tests
- **Rich Reporting**: HTML reports, Allure integration, and custom test result tracking
- **Type Safety**: Full type hints throughout the codebase
- **CI/CD Ready**: Pre-configured for continuous integration pipelines

## 📁 Project Structure

```
automation-playwright-py/
├── src/
│   ├── screenplay/           # Screenplay pattern implementation
│   │   ├── base.py          # Base classes for Screenplay components
│   │   ├── actors/          # Actor implementations
│   │   ├── tasks/           # High-level business tasks
│   │   ├── questions/       # Questions about system state
│   │   ├── abilities/       # Actor abilities (e.g., BrowseTheWeb)
│   │   └── interactions/    # Low-level UI interactions
│   ├── pages/               # Page Object Models
│   │   ├── base_page.py     # Base page class
│   │   ├── login_page.py    # Login page implementation
│   │   └── logged_in_page.py # Logged in page implementation
│   ├── config/              # Configuration management
│   │   ├── settings.py      # Main settings configuration
│   │   └── environments.py  # Environment-specific configs
│   ├── data/                # Test data management
│   │   └── test_data.py     # Test data classes and generators
│   └── utils/               # Utility functions
│       ├── logger.py        # Logging configuration
│       ├── retry.py         # Retry mechanisms
│       ├── screenshot.py    # Screenshot utilities
│       └── fixtures.py      # Pytest fixtures
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
├── reports/                 # Test reports and artifacts
├── logs/                    # Log files
├── conftest.py             # Pytest configuration
├── pytest.ini             # Pytest settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md              # This file
```

## 🛠️ Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd automation-playwright-py
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install
   ```

5. **Configure environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env file with your specific settings
   ```

## 🎯 Quick Start

### Running Tests

1. **Run all tests**:
   ```bash
   pytest
   ```

2. **Run specific test categories**:
   ```bash
   # Run only smoke tests
   pytest -m smoke

   # Run only login tests
   pytest -m login

   # Run only UI tests
   pytest -m ui
   ```

3. **Run tests with specific browser**:
   ```bash
   # Run with Chrome (default)
   BROWSER_NAME=chromium pytest

   # Run with Firefox
   BROWSER_NAME=firefox pytest

   # Run with Safari
   BROWSER_NAME=webkit pytest
   ```

4. **Run tests in headed mode**:
   ```bash
   HEADLESS=false pytest
   ```

5. **Run tests with parallel execution**:
   ```bash
   pytest -n auto
   ```

### Example Test Execution

```bash
# Run login tests with Chrome in headed mode
BROWSER_NAME=chromium HEADLESS=false pytest tests/e2e/test_login.py -v

# Run all tests with HTML report
pytest --html=reports/report.html --self-contained-html

# Run tests with Allure reporting
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 🎭 Screenplay Pattern Usage

The framework implements the Screenplay pattern for clean, maintainable test code:

### Basic Example

```python
from src.screenplay.base import Actor
from src.screenplay.tasks.login import Login
from src.screenplay.questions.text import CurrentUrl
from src.screenplay.abilities.browse_the_web import BrowseTheWeb

def test_successful_login(actor: Actor):
    """Test successful login using Screenplay pattern."""

    # Actor performs a task
    actor.attempts_to(
        Login.with_valid_credentials()
    )

    # Actor asks a question about the system state
    current_url = actor.asks(CurrentUrl())
    assert "/logged-in-successfully/" in current_url
```

### Creating Custom Tasks

```python
from src.screenplay.base import Task, Actor
from src.screenplay.interactions.navigate import Navigate
from src.screenplay.interactions.click import Click

class LogoutFromApplication(Task):
    """Task to logout from the application."""

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(
            Click.on("#logout-button"),
            # Add any additional steps
        )
```

### Creating Custom Questions

```python
from src.screenplay.base import Question, Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb

class ErrorMessage(Question[str]):
    """Question to get error message text."""

    def __init__(self, locator: str):
        self.locator = locator

    def answered_by(self, actor: Actor) -> str:
        page = actor.ability_to(BrowseTheWeb).page
        return page.text_content(self.locator) or ""
```

## ⚙️ Configuration

### Environment Variables

The framework supports configuration through environment variables:

```bash
# Browser Settings
BROWSER_NAME=chromium          # chromium, firefox, webkit
HEADLESS=true                  # true, false
SLOW_MO=0                     # Milliseconds to slow down operations
TIMEOUT=30000                 # Default timeout in milliseconds
VIEWPORT_WIDTH=1920           # Browser viewport width
VIEWPORT_HEIGHT=1080          # Browser viewport height
VIDEO=false                   # Record videos of test runs
SCREENSHOT=only-on-failure    # Screenshot capture mode
TRACE=false                   # Enable Playwright tracing

# Application URLs
BASE_URL=https://practicetestautomation.com
API_BASE_URL=                 # API base URL if applicable

# Test Credentials
VALID_USERNAME=student
VALID_PASSWORD=Password123
INVALID_USERNAME=incorrectUser
INVALID_PASSWORD=incorrectPassword

# Test Execution
RETRY_COUNT=2                 # Number of retries for failed tests
PARALLEL_WORKERS=1            # Number of parallel test workers
ENVIRONMENT=dev               # Environment name (dev, staging, prod)
```

### Multi-Environment Support

The framework supports multiple environments through configuration:

```python
from src.config.environments import Environments

# Get environment-specific configuration
dev_config = Environments.get_environment("dev")
staging_config = Environments.get_environment("staging")
prod_config = Environments.get_environment("prod")
```

## 📊 Reporting and Logging

### HTML Reports

Generate comprehensive HTML reports:

```bash
pytest --html=reports/report.html --self-contained-html
```

### Allure Reports

Generate interactive Allure reports:

```bash
# Generate test results
pytest --alluredir=reports/allure-results

# Serve the report
allure serve reports/allure-results
```

### Logging

The framework provides structured logging with multiple output formats:

- **Console Output**: Colored, formatted logs for development
- **File Logging**: Detailed logs saved to files with rotation
- **Test Results**: Separate log file for test execution results
- **Error Tracking**: Dedicated error log for debugging

Log files are saved in the `logs/` directory:
- `test_automation.log`: All framework logs
- `errors.log`: Error-level logs only
- `test_results.log`: Test execution results

## 🧪 Test Data Management

### Static Test Data

```python
from src.data.test_data import LoginTestData

# Use predefined test cases
valid_credentials = LoginTestData.VALID_USER
invalid_credentials = LoginTestData.INVALID_USERNAME

# Get all test cases for parameterized tests
all_invalid_cases = LoginTestData.get_invalid_test_cases()
```

### Dynamic Test Data

```python
from src.data.test_data import TestDataGenerator

# Generate random test data
random_user = TestDataGenerator.generate_random_user()
random_credentials = TestDataGenerator.generate_random_credentials()
```

## 🔄 Retry Mechanisms

The framework includes built-in retry mechanisms for handling flaky tests:

### Decorator-based Retries

```python
from src.utils.retry import retry

@retry(max_attempts=3, delay=1.0, backoff=2.0)
def flaky_operation():
    # Operation that might fail
    pass
```

### Fluent Interface Retries

```python
from src.utils.retry import with_retry

result = with_retry(some_function, arg1, arg2) \
    .with_max_attempts(3) \
    .with_delay(1.0) \
    .with_backoff(2.0) \
    .on_exceptions(TimeoutError, ConnectionError) \
    .execute()
```

## 📸 Screenshot Management

Automatic screenshot capture for debugging and documentation:

```python
from src.utils.screenshot import take_screenshot, take_failure_screenshot

# Manual screenshot
take_screenshot(page, "login_form", test_name="test_login")

# Automatic failure screenshots (configured in fixtures)
# Screenshots are automatically taken when tests fail
```

Screenshots are organized by test name and saved in `reports/screenshots/`.

## 🚀 CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install

    - name: Run tests
      run: |
        pytest --html=reports/report.html --alluredir=reports/allure-results
      env:
        HEADLESS: true
        BROWSER_NAME: chromium

    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: reports/
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && playwright install'
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest --html=reports/report.html --alluredir=reports/allure-results'
            }
        }

        stage('Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
        }
    }
}
```

## 🧩 Extending the Framework

### Adding New Page Objects

1. Create a new page class inheriting from `BasePage`:

```python
from src.pages.base_page import BasePage

class NewPageLocators:
    ELEMENT_1 = "#element1"
    ELEMENT_2 = ".element2"

class NewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.locators = NewPageLocators()

    @property
    def url_path(self) -> str:
        return "/new-page/"

    def perform_action(self):
        self.click_element(self.locators.ELEMENT_1)
        return self
```

### Adding New Tasks

1. Create a new task class:

```python
from src.screenplay.base import Task, Actor
from src.screenplay.interactions.click import Click

class PerformNewAction(Task):
    def __init__(self, parameter: str):
        self.parameter = parameter

    @classmethod
    def with_parameter(cls, parameter: str) -> 'PerformNewAction':
        return cls(parameter)

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(
            Click.on(f"#element-{self.parameter}")
        )
```

### Adding New Questions

1. Create a new question class:

```python
from src.screenplay.base import Question, Actor
from src.screenplay.abilities.browse_the_web import BrowseTheWeb

class NewQuestion(Question[str]):
    def __init__(self, locator: str):
        self.locator = locator

    @classmethod
    def about(cls, locator: str) -> 'NewQuestion':
        return cls(locator)

    def answered_by(self, actor: Actor) -> str:
        page = actor.ability_to(BrowseTheWeb).page
        return page.get_attribute(self.locator, "value") or ""
```

## 🔧 Troubleshooting

### Common Issues

1. **Browser Installation Issues**:
   ```bash
   # Reinstall browsers
   playwright install --force

   # Install specific browser
   playwright install chromium
   ```

2. **Permission Issues**:
   ```bash
   # On macOS/Linux, ensure proper permissions
   chmod +x venv/bin/activate
   ```

3. **Import Errors**:
   ```bash
   # Ensure src directory is in Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

4. **Test Timeouts**:
   ```bash
   # Increase timeout for slow environments
   TIMEOUT=60000 pytest
   ```

### Debug Mode

Run tests with debug information:

```bash
# Enable debug logging
pytest --log-cli-level=DEBUG

# Run with trace enabled
TRACE=true pytest

# Run single test with maximum verbosity
pytest tests/e2e/test_login.py::TestLogin::test_successful_login -vvv
```

## 📚 Best Practices

### Test Organization

1. **Use descriptive test names** that explain what is being tested
2. **Group related tests** in classes with clear naming
3. **Use appropriate markers** for test categorization
4. **Keep tests independent** - each test should be able to run in isolation

### Screenplay Pattern

1. **Tasks should represent business actions** (e.g., "Login", "PlaceOrder")
2. **Interactions should be low-level UI actions** (e.g., "Click", "Type")
3. **Questions should ask about system state** (e.g., "CurrentUrl", "ErrorMessage")
4. **Use fluent interfaces** for better readability

### Page Objects

1. **Keep locators in separate classes** for better organization
2. **Use method chaining** for fluent interfaces
3. **Implement proper waiting strategies** for dynamic content
4. **Return page objects** from methods for chaining

### Data Management

1. **Use data classes** for structured test data
2. **Separate test data from test logic**
3. **Use parameterized tests** for data-driven scenarios
4. **Generate dynamic data** when appropriate

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run code quality checks
black src/ tests/
flake8 src/ tests/
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) for the excellent browser automation library
- [pytest](https://pytest.org/) for the robust testing framework
- [Screenplay Pattern](https://serenity-js.org/handbook/design/screenplay-pattern/) for the design inspiration
- [Allure](https://docs.qameta.io/allure/) for beautiful test reporting

## 📞 Support

For questions, issues, or contributions, please:

1. Check the [Issues](../../issues) page for existing problems
2. Create a new issue with detailed information
3. Join our [Discussions](../../discussions) for general questions
4. Review the [Wiki](../../wiki) for additional documentation

---

**Happy Testing! 🎉**
```
```