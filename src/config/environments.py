"""
Environment-specific configurations.
"""
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class EnvironmentConfig:
    """Configuration for a specific environment."""
    name: str
    base_url: str
    api_base_url: str
    database_url: str
    timeout: int
    retry_count: int
    parallel_workers: int
    headless: bool
    video: bool
    trace: bool


class Environments:
    """Environment configurations for different testing environments."""

    DEV = EnvironmentConfig(
        name="dev",
        base_url="https://practicetestautomation.com",
        api_base_url="",
        database_url="",
        timeout=30000,
        retry_count=2,
        parallel_workers=1,
        headless=True,
        video=False,
        trace=False
    )

    STAGING = EnvironmentConfig(
        name="staging",
        base_url="https://staging.practicetestautomation.com",
        api_base_url="",
        database_url="",
        timeout=45000,
        retry_count=3,
        parallel_workers=2,
        headless=True,
        video=True,
        trace=True
    )

    PROD = EnvironmentConfig(
        name="prod",
        base_url="https://practicetestautomation.com",
        api_base_url="",
        database_url="",
        timeout=60000,
        retry_count=3,
        parallel_workers=1,
        headless=True,
        video=True,
        trace=True
    )

    LOCAL = EnvironmentConfig(
        name="local",
        base_url="http://localhost:3000",
        api_base_url="http://localhost:8000",
        database_url="sqlite:///test.db",
        timeout=15000,
        retry_count=1,
        parallel_workers=1,
        headless=False,
        video=False,
        trace=False
    )

    @classmethod
    def get_environment(cls, env_name: str) -> EnvironmentConfig:
        """Get environment configuration by name."""
        env_map = {
            "dev": cls.DEV,
            "staging": cls.STAGING,
            "prod": cls.PROD,
            "local": cls.LOCAL
        }

        if env_name not in env_map:
            raise ValueError(f"Unknown environment: {env_name}. Available: {list(env_map.keys())}")

        return env_map[env_name]

    @classmethod
    def get_all_environments(cls) -> Dict[str, EnvironmentConfig]:
        """Get all available environments."""
        return {
            "dev": cls.DEV,
            "staging": cls.STAGING,
            "prod": cls.PROD,
            "local": cls.LOCAL
        }