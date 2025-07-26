"""
Logging configuration and utilities for the test automation framework.
"""
import sys
import os
from pathlib import Path
from typing import Optional
from loguru import logger
from src.config.settings import settings


class TestLogger:
    """Custom logger for test automation framework."""

    def __init__(self):
        self._configured = False
        self.setup_logger()

    def setup_logger(self) -> None:
        """Configure the logger with appropriate handlers and formatting."""
        if self._configured:
            return

        # Remove default handler
        logger.remove()

        # Create logs directory if it doesn't exist
        logs_dir = Path(settings.test.logs_path)
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Console handler with colored output
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                   "<level>{message}</level>",
            level="INFO",
            colorize=True
        )

        # File handler for all logs
        logger.add(
            logs_dir / "test_automation.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="30 days",
            compression="zip"
        )

        # File handler for errors only
        logger.add(
            logs_dir / "errors.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level="ERROR",
            rotation="5 MB",
            retention="30 days",
            compression="zip"
        )

        # File handler for test results
        logger.add(
            logs_dir / "test_results.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
            level="INFO",
            filter=lambda record: "TEST_RESULT" in record["extra"],
            rotation="10 MB",
            retention="30 days"
        )

        self._configured = True

    def get_logger(self, name: Optional[str] = None) -> logger:
        """Get a logger instance."""
        if name:
            return logger.bind(name=name)
        return logger

    def log_test_start(self, test_name: str, test_description: str = "") -> None:
        """Log the start of a test."""
        logger.bind(TEST_RESULT=True).info(f"TEST STARTED: {test_name} - {test_description}")

    def log_test_pass(self, test_name: str, duration: float = 0.0) -> None:
        """Log a test pass."""
        logger.bind(TEST_RESULT=True).info(f"TEST PASSED: {test_name} (Duration: {duration:.2f}s)")

    def log_test_fail(self, test_name: str, error_message: str, duration: float = 0.0) -> None:
        """Log a test failure."""
        logger.bind(TEST_RESULT=True).error(f"TEST FAILED: {test_name} (Duration: {duration:.2f}s) - {error_message}")

    def log_test_skip(self, test_name: str, reason: str) -> None:
        """Log a test skip."""
        logger.bind(TEST_RESULT=True).warning(f"TEST SKIPPED: {test_name} - {reason}")

    def log_step(self, step_description: str) -> None:
        """Log a test step."""
        logger.info(f"STEP: {step_description}")

    def log_action(self, action: str, target: str = "", details: str = "") -> None:
        """Log an action performed during testing."""
        message = f"ACTION: {action}"
        if target:
            message += f" on '{target}'"
        if details:
            message += f" - {details}"
        logger.debug(message)

    def log_assertion(self, assertion: str, result: bool, expected: str = "", actual: str = "") -> None:
        """Log an assertion result."""
        status = "PASSED" if result else "FAILED"
        message = f"ASSERTION {status}: {assertion}"
        if expected and actual:
            message += f" (Expected: {expected}, Actual: {actual})"

        if result:
            logger.debug(message)
        else:
            logger.error(message)


# Global logger instance
test_logger = TestLogger()

# Convenience functions
def get_logger(name: Optional[str] = None):
    """Get a logger instance."""
    return test_logger.get_logger(name)

def log_test_start(test_name: str, test_description: str = ""):
    """Log the start of a test."""
    test_logger.log_test_start(test_name, test_description)

def log_test_pass(test_name: str, duration: float = 0.0):
    """Log a test pass."""
    test_logger.log_test_pass(test_name, duration)

def log_test_fail(test_name: str, error_message: str, duration: float = 0.0):
    """Log a test failure."""
    test_logger.log_test_fail(test_name, error_message, duration)

def log_test_skip(test_name: str, reason: str):
    """Log a test skip."""
    test_logger.log_test_skip(test_name, reason)

def log_step(step_description: str):
    """Log a test step."""
    test_logger.log_step(step_description)

def log_action(action: str, target: str = "", details: str = ""):
    """Log an action performed during testing."""
    test_logger.log_action(action, target, details)

def log_assertion(assertion: str, result: bool, expected: str = "", actual: str = ""):
    """Log an assertion result."""
    test_logger.log_assertion(assertion, result, expected, actual)