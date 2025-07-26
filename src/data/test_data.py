"""
Test data management for the automation framework.
"""
from typing import Dict, List, Any
from dataclasses import dataclass
from faker import Faker

fake = Faker()


@dataclass
class LoginCredentials:
    """Data class for login credentials."""
    username: str
    password: str
    description: str = ""
    expected_result: str = "success"  # "success" or "failure"


@dataclass
class UserData:
    """Data class for test user information."""
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    role: str = "user"


class LoginTestData:
    """Test data for login scenarios."""

    # Valid credentials
    VALID_USER = LoginCredentials(
        username="student",
        password="Password123",
        description="Valid user credentials",
        expected_result="success"
    )

    # Invalid credentials scenarios
    INVALID_USERNAME = LoginCredentials(
        username="incorrectUser",
        password="Password123",
        description="Invalid username with valid password",
        expected_result="failure"
    )

    INVALID_PASSWORD = LoginCredentials(
        username="student",
        password="incorrectPassword",
        description="Valid username with invalid password",
        expected_result="failure"
    )

    BOTH_INVALID = LoginCredentials(
        username="incorrectUser",
        password="incorrectPassword",
        description="Both username and password invalid",
        expected_result="failure"
    )

    EMPTY_USERNAME = LoginCredentials(
        username="",
        password="Password123",
        description="Empty username with valid password",
        expected_result="failure"
    )

    EMPTY_PASSWORD = LoginCredentials(
        username="student",
        password="",
        description="Valid username with empty password",
        expected_result="failure"
    )

    BOTH_EMPTY = LoginCredentials(
        username="",
        password="",
        description="Both username and password empty",
        expected_result="failure"
    )

    # Special characters and edge cases
    SPECIAL_CHARS_USERNAME = LoginCredentials(
        username="user@#$%",
        password="Password123",
        description="Username with special characters",
        expected_result="failure"
    )

    LONG_USERNAME = LoginCredentials(
        username="a" * 100,
        password="Password123",
        description="Very long username",
        expected_result="failure"
    )

    LONG_PASSWORD = LoginCredentials(
        username="student",
        password="a" * 100,
        description="Very long password",
        expected_result="failure"
    )

    @classmethod
    def get_all_test_cases(cls) -> List[LoginCredentials]:
        """Get all login test cases."""
        return [
            cls.VALID_USER,
            cls.INVALID_USERNAME,
            cls.INVALID_PASSWORD,
            cls.BOTH_INVALID,
            cls.EMPTY_USERNAME,
            cls.EMPTY_PASSWORD,
            cls.BOTH_EMPTY,
            cls.SPECIAL_CHARS_USERNAME,
            cls.LONG_USERNAME,
            cls.LONG_PASSWORD
        ]

    @classmethod
    def get_valid_test_cases(cls) -> List[LoginCredentials]:
        """Get only valid login test cases."""
        return [case for case in cls.get_all_test_cases() if case.expected_result == "success"]

    @classmethod
    def get_invalid_test_cases(cls) -> List[LoginCredentials]:
        """Get only invalid login test cases."""
        return [case for case in cls.get_all_test_cases() if case.expected_result == "failure"]


class TestDataGenerator:
    """Generate random test data using Faker."""

    @staticmethod
    def generate_random_user() -> UserData:
        """Generate a random test user."""
        return UserData(
            username=fake.user_name(),
            password=fake.password(length=12),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role="user"
        )

    @staticmethod
    def generate_random_credentials() -> LoginCredentials:
        """Generate random login credentials."""
        return LoginCredentials(
            username=fake.user_name(),
            password=fake.password(length=12),
            description="Randomly generated credentials",
            expected_result="failure"  # Assuming random credentials are invalid
        )