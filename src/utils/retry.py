"""
Retry mechanisms and error handling utilities.
"""
import time
import functools
from typing import Callable, Any, Type, Tuple, Optional, Union
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RetryError(Exception):
    """Exception raised when all retry attempts are exhausted."""

    def __init__(self, message: str, last_exception: Exception):
        super().__init__(message)
        self.last_exception = last_exception


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    on_retry: Optional[Callable[[int, Exception], None]] = None
):
    """
    Decorator to retry a function on failure.

    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts in seconds
        backoff: Multiplier for delay after each attempt
        exceptions: Exception types to catch and retry on
        on_retry: Callback function called on each retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    logger.debug(f"Attempting {func.__name__} (attempt {attempt}/{max_attempts})")
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        logger.info(f"{func.__name__} succeeded on attempt {attempt}")
                    return result

                except exceptions as e:
                    last_exception = e
                    logger.warning(f"{func.__name__} failed on attempt {attempt}: {str(e)}")

                    if attempt == max_attempts:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts")
                        raise RetryError(
                            f"Function {func.__name__} failed after {max_attempts} attempts",
                            last_exception
                        )

                    if on_retry:
                        on_retry(attempt, e)

                    logger.debug(f"Waiting {current_delay:.2f} seconds before retry")
                    time.sleep(current_delay)
                    current_delay *= backoff

            # This should never be reached, but just in case
            raise RetryError(f"Unexpected error in retry logic for {func.__name__}", last_exception)

        return wrapper
    return decorator


class RetryableAction:
    """Class for creating retryable actions with fluent interface."""

    def __init__(self, action: Callable, *args, **kwargs):
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.max_attempts = 3
        self.delay = 1.0
        self.backoff = 2.0
        self.exceptions = (Exception,)
        self.on_retry_callback = None

    def with_max_attempts(self, attempts: int) -> 'RetryableAction':
        """Set maximum number of attempts."""
        self.max_attempts = attempts
        return self

    def with_delay(self, delay: float) -> 'RetryableAction':
        """Set initial delay between attempts."""
        self.delay = delay
        return self

    def with_backoff(self, backoff: float) -> 'RetryableAction':
        """Set backoff multiplier."""
        self.backoff = backoff
        return self

    def on_exceptions(self, *exceptions: Type[Exception]) -> 'RetryableAction':
        """Set which exceptions to retry on."""
        self.exceptions = exceptions
        return self

    def on_retry(self, callback: Callable[[int, Exception], None]) -> 'RetryableAction':
        """Set callback to call on each retry."""
        self.on_retry_callback = callback
        return self

    def execute(self) -> Any:
        """Execute the action with retry logic."""
        current_delay = self.delay
        last_exception = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                logger.debug(f"Executing action (attempt {attempt}/{self.max_attempts})")
                result = self.action(*self.args, **self.kwargs)
                if attempt > 1:
                    logger.info(f"Action succeeded on attempt {attempt}")
                return result

            except self.exceptions as e:
                last_exception = e
                logger.warning(f"Action failed on attempt {attempt}: {str(e)}")

                if attempt == self.max_attempts:
                    logger.error(f"Action failed after {self.max_attempts} attempts")
                    raise RetryError(
                        f"Action failed after {self.max_attempts} attempts",
                        last_exception
                    )

                if self.on_retry_callback:
                    self.on_retry_callback(attempt, e)

                logger.debug(f"Waiting {current_delay:.2f} seconds before retry")
                time.sleep(current_delay)
                current_delay *= self.backoff

        raise RetryError(f"Unexpected error in retry logic", last_exception)


def with_retry(action: Callable, *args, **kwargs) -> RetryableAction:
    """Create a retryable action."""
    return RetryableAction(action, *args, **kwargs)