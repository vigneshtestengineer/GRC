"""
utilities/driver_factory.py
---------------------------
WebDriver factory for creating browser instances.

Changes vs original
~~~~~~~~~~~~~~~~~~~
- After creating a Chrome driver, both the stealth webdriver-flag patch AND
  the CAPTCHA canvas interceptor are injected via CDP so that any page loaded
  through this driver will have window._captchaText populated automatically.
- Firefox is left unchanged (no CDP support).
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.json_config import get_bool, get_int, get_str
from utilities.captcha_helper import inject_captcha_interceptor

BROWSER            = get_str("browser", "browser",           "chrome")
HEADLESS           = get_bool("browser", "headless",          False)
IMPLICIT_WAIT      = get_int("browser", "implicit_wait",      10)
PAGE_LOAD_TIMEOUT  = get_int("browser", "page_load_timeout",  30)


class DriverFactory:
    """Factory class to create and configure WebDriver instances."""

    # ── Chrome option builder ─────────────────────────────────────────────────
    @staticmethod
    def _build_chrome_options(force_headless: bool = False) -> ChromeOptions:


        """Build Chrome options with sensible defaults for local/CI runs."""
        opts = ChromeOptions()
        
        opts.page_load_strategy = 'eager'  # or 'none'
        if HEADLESS or force_headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--start-maximized")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-extensions")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--remote-debugging-port=9222")
        opts.add_argument("--disable-save-password-bubble")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            },
        )
        return opts

    # ── Chrome driver builder ─────────────────────────────────────────────────
    @staticmethod
    def _create_chrome_driver(chrome_options: ChromeOptions):
        """
        Create a Chrome driver.
        Priority:
          1) Explicit CHROMEDRIVER_PATH env variable
          2) webdriver-manager local cache
          3) Selenium Manager fallback
        """
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
        if chromedriver_path:
            return webdriver.Chrome(
                service=Service(chromedriver_path), options=chrome_options
            )

        os.environ.setdefault("WDM_LOCAL", "1")
        try:
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            return webdriver.Chrome(options=chrome_options)

    # ── CDP post-creation patches ─────────────────────────────────────────────
    @staticmethod
    def _apply_chrome_stealth(driver) -> None:
        """
        Hide the navigator.webdriver flag so the site does not detect
        Selenium automation.
        """
        try:
            driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """
                },
            )
        except Exception:
            pass  # non-critical

    @staticmethod
    def _apply_captcha_interceptor(driver) -> None:
        """
        Inject the canvas text interceptor so window._captchaText is populated
        before the CAPTCHA is rendered on any page loaded by this driver.
        Delegates to captcha_helper.inject_captcha_interceptor.
        """
        inject_captcha_interceptor(driver)

    # ── public factory method ─────────────────────────────────────────────────
    @staticmethod
    def get_driver(browser: str = None):
        """
        Create, configure, and return a WebDriver instance.

        Args:
            browser: 'chrome' (default) or 'firefox'.

        Returns:
            Configured Selenium WebDriver.
        """
        browser = (browser or BROWSER).lower()

        if browser == "chrome":
            chrome_options = DriverFactory._build_chrome_options()
            try:
                driver = DriverFactory._create_chrome_driver(chrome_options)
            except WebDriverException as exc:
                err = str(exc)
                if not HEADLESS and any(
                    token in err
                    for token in ("DevToolsActivePort", "Chrome failed to start",
                                  "chrome not reachable")
                ):
                    retry_opts = DriverFactory._build_chrome_options(force_headless=True)
                    driver = DriverFactory._create_chrome_driver(retry_opts)
                else:
                    raise

            # Inject CDP scripts BEFORE any page loads
            DriverFactory._apply_chrome_stealth(driver)
            DriverFactory._apply_captcha_interceptor(driver)

        elif browser == "firefox":
            firefox_options = FirefoxOptions()
            if HEADLESS:
                firefox_options.add_argument("--headless")
            service = Service(GeckoDriverManager().install())
            driver  = webdriver.Firefox(service=service, options=firefox_options)

        else:
            raise ValueError(f"Unsupported browser: {browser!r}")

        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.maximize_window()
        return driver
