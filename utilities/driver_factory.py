"""
WebDriver factory for creating browser instances
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

BROWSER = get_str("browser", "browser", "chrome")
HEADLESS = get_bool("browser", "headless", False)
IMPLICIT_WAIT = get_int("browser", "implicit_wait", 10)
PAGE_LOAD_TIMEOUT = get_int("browser", "page_load_timeout", 30)

class DriverFactory:
    """Factory class to create WebDriver instances"""

    @staticmethod
    def _build_chrome_options(force_headless=False):
        """
        Build Chrome options with sensible defaults for local/CI runs.
        """
        chrome_options = ChromeOptions()
        headless = HEADLESS or force_headless
        if headless:
            # "new" headless is more stable in modern Chrome.
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-save-password-bubble")
        # Hide Selenium automation infobar and reduce automation fingerprints.
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            },
        )
        return chrome_options

    @staticmethod
    def _create_chrome_driver(chrome_options):
        """
        Create Chrome driver.
        Priority:
        1) Explicit CHROMEDRIVER_PATH
        2) webdriver-manager local cache
        3) Selenium Manager fallback
        """
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
        if chromedriver_path:
            return webdriver.Chrome(
                service=Service(chromedriver_path),
                options=chrome_options
            )

        # Store webdriver-manager artifacts under project folder to avoid
        # permission issues in user profile directories.
        os.environ.setdefault("WDM_LOCAL", "1")
        try:
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            # Fallback to Selenium Manager if webdriver-manager can't download.
            return webdriver.Chrome(options=chrome_options)
    
    @staticmethod
    def get_driver(browser=None):
        """
        Creates and returns WebDriver instance
        Args:
            browser (str): Browser name (chrome, firefox)
        Returns:
            WebDriver: Selenium WebDriver instance
        """
        browser = browser or BROWSER
        
        if browser.lower() == "chrome":
            chrome_options = DriverFactory._build_chrome_options()
            try:
                driver = DriverFactory._create_chrome_driver(chrome_options)
            except WebDriverException as exc:
                error_text = str(exc)
                should_retry_headless = (
                    not HEADLESS and (
                        "DevToolsActivePort" in error_text
                        or "Chrome failed to start" in error_text
                        or "chrome not reachable" in error_text
                    )
                )
                if should_retry_headless:
                    retry_options = DriverFactory._build_chrome_options(force_headless=True)
                    driver = DriverFactory._create_chrome_driver(retry_options)
                else:
                    raise
            DriverFactory._apply_chrome_stealth(driver)
            
        elif browser.lower() == "firefox":
            firefox_options = FirefoxOptions()
            if HEADLESS:
                firefox_options.add_argument("--headless")
            
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
            
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.maximize_window()
        
        return driver

    @staticmethod
    def _apply_chrome_stealth(driver):
        """
        Apply browser-level JS patches to reduce automation detection signals.
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
            # Non-critical: continue even if CDP command is unavailable.
            pass
