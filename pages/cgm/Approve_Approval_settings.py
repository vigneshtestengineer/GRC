from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.driver_factory import DriverFactory
from utilities.json_config import get_str
import json
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Data loading ─────────────────────────────────────────────────────────────
UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)
APPROVER_LOGIN_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Approver_Login.json"
)

# Load Unit Master Data
try:
    with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as file:
        UNIT_MASTER_DATA = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    UNIT_MASTER_DATA = {}

# Load Approver Login Data
try:
    with open(APPROVER_LOGIN_FILE, "r", encoding="utf-8") as file:
        APPROVER_LOGIN_DATA = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    APPROVER_LOGIN_DATA = {}

UNIT_DETAILS    = UNIT_MASTER_DATA.get("Unit_Details", {})
APPROVAL_MODULE = UNIT_MASTER_DATA.get("Approval_Module", {})   # ✅ fixed: was Approver_Login.get(...)

UNIT_NAME      = UNIT_DETAILS.get("unit_name", "")
CGM_MODULE_VAL = APPROVAL_MODULE.get("CGM_MODULE", "")
TAMS_MODULE    = APPROVAL_MODULE.get("TAMS_MODULE", "")
PAYROLL_MODULE = APPROVAL_MODULE.get("PAYROLL_MODULE", "")

# ── Approver credentials (from Approver_Login.json) ──────────────────────────
APPROVER_LOGIN    = APPROVER_LOGIN_DATA.get("approver_login", {})
APPROVER_USERNAME = APPROVER_LOGIN.get("username", "")
APPROVER_PASSWORD = APPROVER_LOGIN.get("password", "")
APPROVER_GROUP    = APPROVER_LOGIN.get("group", "")
APPROVER_LEGAL_ENTITY = APPROVER_LOGIN.get("legal_entity", "")

# ── Auth / Login credentials (existing session browser) ──────────────────────
LOGIN_URL    = get_str("auth", "login_url", "")
LEGAL_ENTITY = get_str("auth", "legal_entity", "")

CGM_EXECUTIVE_URL = "http://13.203.6.58:5002/#/home/welcome"


class Approve_Approval_Settings(BasePage):
    """
    Handles:
      1. Waiting until ApprovalSettingsCreation finishes (queue confirmed).
      2. Spawning a fresh Firefox browser.
      3. Logging in as the Approver (from Approver_Login.json).
      4. Navigating to the CGM module.
    """

    # ── Approval-list page locators ──────────────────────────────────────────
    GENERAL_SETTINGS_MENU         = (By.XPATH, "//span[normalize-space()='General Setting(s)']")
    SELECT_APPROVAL_SETTINGS_MENU = (By.XPATH, "//span[normalize-space()='Approval Setting(s)']")
    APPROVAL_LIST_ROW             = (By.XPATH, "//table//tbody//tr[1]//td | //mat-row[1]")

    # Success toast
    SUCCESS_NOTIFICATION_CONTENT = (
        By.XPATH,
        "//div[contains(@class,'compfie-toast-notification-content')]",
    )
    TOAST_CLOSE_BUTTON = (By.XPATH, "//mat-icon[@data-mat-icon-name='x']")

    # ── Login page locators ──────────────────────────────────────────────────
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='Username' or @id='username' or @name='username']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON   = (By.XPATH, "//button[contains(normalize-space(),'Login') or contains(normalize-space(),'Sign In')]")

    # Legal-entity selection
    SEARCH_LEGALENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGALENTITY        = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGALENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # Menu / CGM navigation
    MENU_BUTTON                   = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXECUTIVE_CARD = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    OPEN_CGM_MENU                 = (By.XPATH, "//span[normalize-space()='Compliances']")
    CGM_MODULE_LINK               = (By.XPATH, "//span[normalize-space()='CGM']")

    # ── Constructor ──────────────────────────────────────────────────────────
    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("Approve_Approval_Settings page initialized.")
        self.cgm_driver = None
        self.wait_for_page_load()

    # ── 1. Wait for approval settings page to be ready ───────────────────────
    def wait_for_page_load(self):
        """Wait until the Approval Settings menu is visible (current browser)."""
        self.wait_for_element(self.GENERAL_SETTINGS_MENU, timeout=10)
        self.logger.info("Approve_Approval_Settings: page loaded successfully.")

    # ── 2. Poll until all three module rows appear in the queue ──────────────
    def wait_for_approval_queue_completion(self, timeout: int = 60):
        """Block until ≥ 3 rows appear in the approval-settings list."""
        self.logger.info("Waiting for approval queue to be fully populated …")

        self.scroll_to_element(self.GENERAL_SETTINGS_MENU)
        self.click(self.GENERAL_SETTINGS_MENU, timeout=6)
        self.wait_for_element(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=6)
        self.click(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=6)

        all_rows_locator = (By.XPATH, "//table//tbody//tr | //mat-row")

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(*all_rows_locator)) >= 3
            )
            row_count = len(self.driver.find_elements(*all_rows_locator))
            self.logger.info(
                "Approval queue confirmed: %d row(s) found (expected ≥ 3).", row_count
            )
        except TimeoutException:
            self.logger.error(
                "Approval queue did not reach 3 rows within %d seconds.", timeout
            )
            raise RuntimeError(
                "Approval Settings queue incomplete — fewer than 3 module rows found."
            )

    # ── 3. Spawn a new Firefox browser ───────────────────────────────────────
    def _open_new_firefox_browser(self):
        """Launch a second independent Firefox WebDriver instance."""
        self.logger.info("Spawning new Firefox browser for CGM approval …")
        self.cgm_driver = DriverFactory.get_driver(browser="firefox")
        self.logger.info("New Firefox browser launched successfully.")
        return self.cgm_driver

    # ── 4. Log in as Approver on the new browser ─────────────────────────────
    def _login_on_new_browser(self, new_driver):
        """
        Log in using Approver credentials from Approver_Login.json
        (username, password, legal_entity).
        """
        self.logger.info(
            "Logging in as approver '%s' on new browser …", APPROVER_USERNAME
        )
        new_driver.get(LOGIN_URL)
        new_driver.maximize_window()

        wait = WebDriverWait(new_driver, 15)

        # Enter approver username
        username_el = wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        username_el.clear()
        username_el.send_keys(APPROVER_USERNAME)           # ✅ approver username
        self.logger.info("Entered approver username: %s", APPROVER_USERNAME)

        # Enter approver password
        password_el = new_driver.find_element(*self.PASSWORD_INPUT)
        password_el.clear()
        password_el.send_keys(APPROVER_PASSWORD)           # ✅ approver password
        self.logger.info("Entered approver password.")

        # Click login
        new_driver.find_element(*self.LOGIN_BUTTON).click()
        self.logger.info("Clicked login button.")

        # Wait for legal-entity search to appear
        wait.until(EC.visibility_of_element_located(self.SEARCH_LEGALENTITY))

        # Search for approver's legal entity
        le_input = new_driver.find_element(*self.SEARCH_LEGALENTITY)
        le_input.clear()
        le_input.send_keys(APPROVER_LEGAL_ENTITY)          # ✅ approver legal entity
        self.logger.info(
            "Searched for approver legal entity: %s", APPROVER_LEGAL_ENTITY
        )

        wait.until(
            lambda d: d.find_element(*self.SEARCH_LEGALENTITY)
            .get_attribute("value")
            .strip() == APPROVER_LEGAL_ENTITY
        )

        # Select the first matching row
        wait.until(EC.element_to_be_clickable(self.SELECT_LEGALENTITY))
        new_driver.find_element(*self.SELECT_LEGALENTITY).click()

        # Wait until the select button is enabled, then click it
        select_btn = wait.until(
            lambda d: d.find_element(*self.SELECT_LEGALENTITY_BUTTON)
            if not d.find_element(*self.SELECT_LEGALENTITY_BUTTON)
            .get_attribute("disabled")
            else False
        )
        select_btn.click()
        self.logger.info(
            "Legal entity '%s' selected for approver.", APPROVER_LEGAL_ENTITY
        )

    # ── 5. Open the CGM module on the new browser ────────────────────────────
    def _open_cgm_module(self, new_driver):
        """Navigate via app-switcher → General Master-Executive → CGM module."""
        wait = WebDriverWait(new_driver, 15)

        # Click the 9-dot app-switcher menu
        wait.until(EC.element_to_be_clickable(self.MENU_BUTTON))
        new_driver.find_element(*self.MENU_BUTTON).click()
        self.logger.info("Clicked app-switcher menu.")

        previous_windows = new_driver.window_handles

        # Click General Master-Executive card
        wait.until(EC.element_to_be_clickable(self.GENERAL_MASTER_EXECUTIVE_CARD))
        new_driver.find_element(*self.GENERAL_MASTER_EXECUTIVE_CARD).click()
        self.logger.info("Clicked 'General Master-Executive' card.")

        # Switch to new tab if one opened
        current_windows = new_driver.window_handles
        if len(current_windows) > len(previous_windows):
            new_win = [h for h in current_windows if h not in previous_windows]
            if new_win:
                new_driver.switch_to.window(new_win[-1])
                self.logger.info("Switched to new browser tab for CGM Executive.")

        # Verify correct URL
        wait.until(EC.url_contains(CGM_EXECUTIVE_URL))
        self.logger.info("Verified CGM Executive URL: %s", CGM_EXECUTIVE_URL)

        # Expand CGM menu and click module link
        wait.until(EC.element_to_be_clickable(self.OPEN_CGM_MENU))
        new_driver.find_element(*self.OPEN_CGM_MENU).click()
        self.logger.info("Expanded CGM menu.")

        wait.until(EC.element_to_be_clickable(self.CGM_MODULE_LINK))
        new_driver.find_element(*self.CGM_MODULE_LINK).click()
        self.logger.info("CGM module opened successfully.")

    # ── Public orchestration method ──────────────────────────────────────────
    def approve_and_open_cgm(self):
        """
        Full flow:
          1. Confirm ≥ 3 approval rows exist in the queue.
          2. Open a new Firefox browser.
          3. Log in as Approver (Approver_Login.json credentials).
          4. Navigate to the CGM module.

        Returns:
            new_driver: the secondary WebDriver so the caller can continue.
        """
        # Step 1 — confirm queue is populated
        self.wait_for_approval_queue_completion(timeout=60)
        self.logger.info("✓ Approval queue verified.")

        # Step 2 — new browser
        new_driver = self._open_new_firefox_browser()

        try:
            # Step 3 — login as approver
            self._login_on_new_browser(new_driver)
            self.logger.info("✓ Approver login successful on new Firefox browser.")

            # Step 4 — open CGM module
            self._open_cgm_module(new_driver)
            self.logger.info("✓ CGM module opened in new Firefox browser.")

        except Exception as exc:
            self.logger.error(
                "Failed during approver CGM flow: %s", exc, exc_info=True
            )
            new_driver.save_screenshot("cgm_approver_failure.png")
            raise

        return new_driver

    # ── Cleanup ──────────────────────────────────────────────────────────────
    def quit_cgm_browser(self):
        """Quit the secondary Firefox browser if still open."""
        if self.cgm_driver:
            try:
                self.cgm_driver.quit()
                self.logger.info("Secondary Firefox browser closed.")
            except Exception:
                pass
            finally:
                self.cgm_driver = None