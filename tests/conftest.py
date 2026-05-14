"""
Pytest fixtures and hooks for GRC automation

Overall Purpose

This file does 5 main things:

1. Creates and destroys WebDriver
2. Logs test execution
3. Takes screenshots on failure
4. Cleans CAPTCHA folder before each test
5. Configures Pytest behavior

"""
import pytest
import sys
import os
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.driver_factory import DriverFactory
from utilities.screenshot import Screenshot
from utilities.logger import Logger
from utilities.json_config import get_path
from utilities.Report_Generator import ReportGenerator

logger = Logger.get_logger(__name__)
CAPTCHA_DIR = get_path("paths", "captcha_image_dir", "reports/captchas")
SCREENSHOT_DIR = get_path("paths", "screenshot_dir", "reports/screenshots")

_failed_tests: set = set()


TEST_ORDER = [
    "test_login",
    "unitmaster",
    "approval_settings",
    "approve_approval_settings",
    "contractor_pattern_config",
    "add_contractor_master",
    "work_order_master",
    "employee_pattern_config",
    "employee_component_creation",
    "employee_component_mapping",
    "shift_master_creation",
    "weekly_holiday_master",
    "contract_labour_master",
    "pf_statutory_mapping",
    "esi_statutory_mapping",
    "ptax_statutory_mapping",
    "minimum_wage_statutory_mapping",
    "holiday_rules_statutory_mapping",
    "holiday_mapping"
    # add next test module keywords here in execution order
]


def pytest_collection_modifyitems(config, items):
    """Run tests in the order defined by TEST_ORDER; unmatched tests run last."""
    def sort_key(item):
        nodeid = item.nodeid.lower()
        for index, keyword in enumerate(TEST_ORDER):
            if keyword in nodeid:
                return index
        return len(TEST_ORDER)

    items.sort(key=sort_key)


@pytest.fixture(scope="session")
def driver(request):
    """WebDriver fixture - single browser session shared across all tests."""
    try:
        logger.info("=" * 80)
        logger.info("Initializing WebDriver")
    except Exception:
        pass
    driver = DriverFactory.get_driver()
    yield driver
    try:
        logger.info("Quitting WebDriver")
        driver.quit()
        logger.info("=" * 80)
    except Exception:
        pass


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    """Session-level setup and teardown."""
    try:
        logger.info("=" * 80)
        logger.info("TEST SESSION STARTED - GRC Automation")
        logger.info("=" * 80)
    except Exception:
        pass

    screenshot_dir = SCREENSHOT_DIR
    if os.path.exists(screenshot_dir):
        for entry in os.scandir(screenshot_dir):
            try:
                if entry.is_file() or entry.is_symlink():
                    os.remove(entry.path)
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
            except OSError as exc:
                logger.warning(f"Could not remove screenshot {entry.path}: {exc}")
        logger.info(f"Cleared screenshots folder: {screenshot_dir}")
    else:
        os.makedirs(screenshot_dir, exist_ok=True)

    ReportGenerator.clear_output_dir()
    logger.info(f"Cleared reports folder: {ReportGenerator.REPORT_DIR}")

    yield

    try:
        logger.info("=" * 80)
        logger.info("TEST SESSION COMPLETED")
        logger.info("=" * 80)
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results and take screenshots on failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        screenshot_filename = None
        if report.failed:
            _failed_tests.add(item.nodeid)
            driver = item.funcargs.get("driver")
            if driver:
                test_name = item.name
                screenshot_path = Screenshot.take_screenshot(driver, test_name)
                logger.error(f"Test failed: {test_name}")
                if screenshot_path:
                    logger.info(f"Screenshot saved: {screenshot_path}")
                    screenshot_filename = os.path.basename(screenshot_path)
        elif report.passed:
            logger.info(f"Test passed: {item.name}")

        ReportGenerator.add_result(
            nodeid=item.nodeid,
            name=item.name,
            status="PASSED" if report.passed else "FAILED",
            duration=getattr(report, "duration", 0),
            screenshot=screenshot_filename,
            module=getattr(item.module, "MODULE_NAME", None),
        )


def pytest_runtest_logreport(report):
    """Stop execution immediately after any test failure."""
    if report.when == "call" and report.failed:
        pytest.exit(f"Stopping execution: {report.nodeid} failed", returncode=1)


def pytest_sessionfinish(session, exitstatus):
    """Generate HTML test report after the session ends."""
    report_path = ReportGenerator.generate()
    if report_path:
        try:
            logger.info(f"HTML report saved: {report_path}")
        except Exception:
            pass


@pytest.fixture(autouse=True)
def skip_login_if_unit_master_failed(request):
    """Skip test_login if any unit_master test has failed."""
    if "test_login" in request.node.nodeid:
        if any("unitmaster" in f.lower() for f in _failed_tests):
            pytest.skip("Skipped: unit_master test failed.")


@pytest.fixture(autouse=True)
def clear_captcha_folder():
    """Clear the reports/captchas folder before every test."""
    captcha_dir = CAPTCHA_DIR
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
    """Configure pytest."""
    if hasattr(config.option, "reruns"):
        config.option.reruns = 0
    if hasattr(config.option, "reruns_delay"):
        config.option.reruns_delay = 0

    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
