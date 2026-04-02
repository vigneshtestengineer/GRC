"""
Pytest fixtures and hooks for OrangeHRM automation
"""
import pytest
import sys
import os
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.driver_factory import DriverFactory
from utilities.screenshot import Screenshot
from utilities.logger import Logger
from config.config import Config

logger = Logger.get_logger(__name__)

@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture - creates and quits driver for each test
    """
    logger.info("=" * 80)
    logger.info("Initializing WebDriver")
    driver = DriverFactory.get_driver()
    yield driver
    logger.info("Quitting WebDriver")
    driver.quit()
    logger.info("=" * 80)

@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    """
    Session-level setup and teardown
    """
    logger.info("=" * 80)
    logger.info("TEST SESSION STARTED - OrangeHRM Automation")
    logger.info("=" * 80)
    yield
    logger.info("=" * 80)
    logger.info("TEST SESSION COMPLETED")
    logger.info("=" * 80)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.failed:
            driver = item.funcargs.get('driver')
            if driver:
                test_name = item.name
                screenshot_path = Screenshot.take_screenshot(driver, test_name)
                logger.error(f"Test failed: {test_name}")
                logger.info(f"Screenshot saved: {screenshot_path}")
        elif report.passed:
            logger.info(f"Test passed: {item.name}")


@pytest.fixture(autouse=True)
def clear_captcha_folder():
    """Clear the reports/captchas folder before every test."""
    captcha_dir = Config.CAPTCHA_IMAGE_DIR
    if os.path.exists(captcha_dir):
        for entry in os.scandir(captcha_dir):
            try:
                if entry.is_file() or entry.is_symlink():
                    os.remove(entry.path)
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
            except OSError as exc:
                logger.warning(f"Could not remove {entry.path}: {exc}")
    else:
        os.makedirs(captcha_dir, exist_ok=True)
    yield


def pytest_configure(config):
    """Configure pytest"""
    if hasattr(config.option, "reruns"):
        config.option.reruns = 0
    if hasattr(config.option, "reruns_delay"):
        config.option.reruns_delay = 0
    config.option.maxfail = 1

    config.addinivalue_line(
        "markers", "smoke: Smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: Regression tests"
    )
    config.addinivalue_line(
        "markers", "e2e: End-to-end tests"
    )
