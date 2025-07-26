#!/usr/bin/env python3
"""
Test runner script for the automation framework.
Provides convenient ways to run different types of tests.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def setup_environment():
    """Set up the environment for running tests."""
    # Add src directory to Python path
    src_path = Path(__file__).parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # Set PYTHONPATH environment variable
    current_pythonpath = os.environ.get("PYTHONPATH", "")
    if str(src_path) not in current_pythonpath:
        os.environ["PYTHONPATH"] = f"{src_path}:{current_pythonpath}" if current_pythonpath else str(src_path)


def run_command(command, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"\n🚀 {description}")

    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print(f"❌ Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    else:
        print("✅ Command completed successfully")


def main():
    parser = argparse.ArgumentParser(description="Test runner for automation framework")
    parser.add_argument("--type", choices=["all", "unit", "integration", "e2e", "smoke"],
                       default="all", help="Type of tests to run")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"],
                       default="chromium", help="Browser to use for tests")
    parser.add_argument("--headless", action="store_true", default=True,
                       help="Run tests in headless mode")
    parser.add_argument("--headed", action="store_true",
                       help="Run tests in headed mode (overrides --headless)")
    parser.add_argument("--parallel", type=int, default=1,
                       help="Number of parallel workers")
    parser.add_argument("--html-report", action="store_true",
                       help="Generate HTML report")
    parser.add_argument("--allure-report", action="store_true",
                       help="Generate Allure report")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug logging")

    args = parser.parse_args()

    # Setup environment
    setup_environment()

    # Set environment variables
    os.environ["BROWSER_NAME"] = args.browser
    os.environ["HEADLESS"] = "false" if args.headed else "true"

    if args.debug:
        os.environ["LOG_LEVEL"] = "DEBUG"

    # Create necessary directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Build pytest command
    pytest_args = ["pytest"]

    # Add test path based on type
    if args.type == "unit":
        pytest_args.append("tests/unit/")
    elif args.type == "integration":
        pytest_args.append("tests/integration/")
    elif args.type == "e2e":
        pytest_args.append("tests/e2e/")
    elif args.type == "smoke":
        pytest_args.extend(["-m", "smoke"])
    else:  # all
        pytest_args.append("tests/")

    # Add parallel execution
    if args.parallel > 1:
        pytest_args.extend(["-n", str(args.parallel)])

    # Add verbosity
    if args.verbose:
        pytest_args.append("-v")

    # Add HTML report
    if args.html_report:
        pytest_args.extend(["--html=reports/report.html", "--self-contained-html"])

    # Add Allure report
    if args.allure_report:
        pytest_args.append("--alluredir=reports/allure-results")

    # Add debug logging
    if args.debug:
        pytest_args.append("--log-cli-level=DEBUG")

    # Run tests
    command = " ".join(pytest_args)
    run_command(command, f"Running {args.type} tests with {args.browser}")

    # Generate Allure report if requested
    if args.allure_report:
        print("\n📊 Generating Allure report...")
        print("Run 'allure serve reports/allure-results' to view the report")

    print(f"\n🎉 {args.type.capitalize()} tests completed successfully!")


if __name__ == "__main__":
    main()