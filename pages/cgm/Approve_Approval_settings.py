from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.driver_factory import DriverFactory
import json
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Data loading ─────────────────────────────────────────────────────────────
APPROVER_LOGIN_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Approver_Login.json"
)

try:
    with open(APPROVER_LOGIN_FILE, "r", encoding="utf-8") as file:
        APPROVER_LOGIN_DATA = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    APPROVER_LOGIN_DATA = {}

# ── Approver credentials (from Approver_Login.json) ──────────────────────────
APPROVER_LOGIN        = APPROVER_LOGIN_DATA.get("approver_login", {})
APPROVER_USERNAME     = APPROVER_LOGIN.get("username", "")
APPROVER_PASSWORD     = APPROVER_LOGIN.get("password", "")
APPROVER_GROUP        = APPROVER_LOGIN.get("group", "")
APPROVER_LEGAL_ENTITY = APPROVER_LOGIN.get("legal_entity", "")

CGM_ADMIN_URL = "http://13.203.6.58:5002/#/home/welcome"


class Approve_Approval_Settings(BasePage):
    """
    Opens its own Firefox browser and runs this exact sequence:
      1. Login (CAPTCHA handled by GRCLoginPage)
      2. Open CGM Admin via app-switcher
      3. Switch to new tab → redirected to CGM Admin URL
      4. Select Legal Entity
      5. Click General Settings → Approval Settings
    """

    # ── Legal-entity selection ────────────────────────────────────────────────
    SEARCH_LEGALENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGALENTITY        = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGALENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Menu / CGM navigation ─────────────────────────────────────────────────
    SPLASH_SCREEN                 = (By.TAG_NAME, "compfie-splash-screen")
    MENU_BUTTON                   = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXECUTIVE_CARD = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    SELECT_ADMIN_ROLE             = (By.XPATH, "//span[@class='group-name' and normalize-space()='admin']")
    GENERAL_SETTINGS_MENU         = (By.XPATH, "//span[normalize-space()='General Setting(s)']")
    SELECT_APPROVAL_SETTINGS_MENU = (By.XPATH, "//span[normalize-space()='Approval Setting(s)']")
    SELECT_ALL_CHECKBOX           = (By.XPATH, "(//span[contains(@class,'mat-checkbox-inner-container')])[1]")
    CLICK_APPROVE_BUTTON          = (By.XPATH, "//span[normalize-space()='Approve']")
    # ── Constructor ───────────────────────────────────────────────────────────
    def __init__(self):
        firefox_driver = DriverFactory.get_driver(browser="firefox")
        super().__init__(firefox_driver)
        firefox_driver.maximize_window()
        self.logger.info("Approve_Approval_Settings: Firefox browser opened.")

    # ── Step 1: Login ─────────────────────────────────────────────────────────
    def _login_as_approver(self):
        """
        Login via GRCLoginPage (handles CAPTCHA automatically).
        No legal entity selection here — that happens AFTER CGM redirect.
        """
        from pages.login.grc_login_page import GRCLoginPage

        self.logger.info("Logging in as approver '%s' …", APPROVER_USERNAME)
        login_page = GRCLoginPage(self.driver)
        login_page.login(APPROVER_USERNAME, APPROVER_PASSWORD, APPROVER_GROUP)
        self.logger.info("✓ Approver login submitted via GRCLoginPage.")

    # ── Step 2: Open CGM Admin via app-switcher ───────────────────────────────
    def _open_cgm_admin(self):
        """
        Click the 9-dot app-switcher → General Master-Admin card →
        Select Admin role → wait for the new CGM Admin tab to open
        and switch to it → verify the CGM Admin URL.
        """
        previous_windows = self.driver.window_handles

        # Wait for any loading splash screen to clear before interacting
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=30)
        self.click(self.MENU_BUTTON, timeout=15)
        self.logger.info("Clicked app-switcher menu.")

        self.sleep(1)
        self.click(self.GENERAL_MASTER_EXECUTIVE_CARD, timeout=15)
        self.logger.info("Clicked 'General Master-Admin' card.")

        self.click(self.SELECT_ADMIN_ROLE, timeout=15)
        self.logger.info("Selected admin role.")

        # Wait for the new CGM Admin tab to open then switch to it
        WebDriverWait(self.driver, 15).until(
            lambda d: len(d.window_handles) > len(previous_windows)
        )
        new_win = [h for h in self.driver.window_handles if h not in previous_windows]
        if new_win:
            self.driver.switch_to.window(new_win[-1])
            self.logger.info("Switched to new CGM Admin tab.")

        # Confirm we are on the correct CGM Admin URL
        WebDriverWait(self.driver, 15).until(EC.url_contains(CGM_ADMIN_URL))
        self.logger.info("✓ Redirected and verified CGM Admin URL: %s", CGM_ADMIN_URL)

        # Wait for the CGM Admin splash screen to clear before any further clicks
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=30)

    # ── Step 3: Select Legal Entity (after CGM redirect) ─────────────────────
    def _select_legal_entity(self):
        """
        After the CGM Admin tab opens, search for and select the
        approver's legal entity before navigating further.
        Skipped gracefully if the selection page is not shown.
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located(self.SEARCH_LEGALENTITY))

            le_input = self.driver.find_element(*self.SEARCH_LEGALENTITY)
            le_input.clear()
            le_input.send_keys(APPROVER_LEGAL_ENTITY)
            self.logger.info("Searched for legal entity: '%s'.", APPROVER_LEGAL_ENTITY)

            # Wait until the typed value is exactly what we want
            wait.until(
                lambda d: d.find_element(*self.SEARCH_LEGALENTITY)
                .get_attribute("value")
                .strip() == APPROVER_LEGAL_ENTITY
            )

            # Click the first matching row (JS fallback handles any overlay)
            self.click(self.SELECT_LEGALENTITY, timeout=10)
            self.logger.info("Clicked first legal entity row.")

            # Click the Select button once it becomes enabled
            self.click(self.SELECT_LEGALENTITY_BUTTON, timeout=10)
            self.logger.info("✓ Legal entity '%s' selected.", APPROVER_LEGAL_ENTITY)

        except TimeoutException:
            self.logger.info(
                "Legal entity selection page not shown — "
                "account redirected directly to home."
            )

    # ── Step 4: Navigate to Approval Settings ────────────────────────────────
    def _navigate_to_approval_settings(self):
        """
        Click General Setting(s) → Approval Setting(s) in the CGM Admin sidebar.
        Called only after the legal entity has been confirmed. And Approve the Approval settings
        """
        self.click(self.GENERAL_SETTINGS_MENU, timeout=15)
        self.logger.info("Expanded 'General Setting(s)' menu.")
        self.click(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=15)
        self.logger.info("✓ Navigated to 'Approval Setting(s)' page.")
        self.sleep(2)
        self.click(self.SELECT_ALL_CHECKBOX, timeout=15)
        self.click(self.CLICK_APPROVE_BUTTON, timeout=15)
        self.logger.info("Clicked Approve button — waiting for success notification …")

        self._wait_for_approval_success()

    # ── Step 5: Poll until success or error toast appears ────────────────────
    def _wait_for_approval_success(self):
        """Poll every second until success or error toast appears.
        Closes the browser and raises immediately if an error toast is detected.
        """
        SUCCESS_TOAST = (
            By.XPATH,
            "//div[contains(@class,'compfie-toast-notification-message')"
            " and normalize-space()='Approved Successfully']",
        )
        ERROR_TOAST = (
            By.XPATH,
            "//div[contains(@class,'compfie-toast-notification-container')]",
        )
        TOAST_CLOSE = (By.XPATH, "//mat-icon[@data-mat-icon-name='x']")

        self.logger.info("Polling for approval toast …")
        while True:
            # Check for success
            try:
                el = self.driver.find_element(*SUCCESS_TOAST)
                if el.is_displayed():
                    self.logger.info("✓ 'Approved Successfully' notification received.")
                    break
            except Exception:
                pass

            # Check for error — close browser immediately and raise
            try:
                err_el = self.driver.find_element(*ERROR_TOAST)
                if err_el.is_displayed():
                    error_msg = err_el.text.strip() or "Unknown error"
                    self.logger.error("Error toast appeared: '%s'. Closing browser.", error_msg)
                    self.quit_cgm_browser()
                    raise RuntimeError(f"Approval failed — error toast: '{error_msg}'")
            except RuntimeError:
                raise
            except Exception:
                pass

            self.sleep(1)

        # Dismiss the success toast if the close button is present
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(TOAST_CLOSE)
            )
            self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=15)
            self.click(TOAST_CLOSE, timeout=5)
            self.logger.info("Closed success toast.")
        except TimeoutException:
            pass

    # ── Public orchestration ──────────────────────────────────────────────────
    def approve_and_open_cgm(self):
        """
        Runs the full sequence in the correct order:

          Step 1 → Login as Approver (CAPTCHA handled internally)
          Step 2 → Open CGM Admin via app-switcher (new tab opens + switched)
          Step 3 → Select Legal Entity (on the CGM Admin tab)
          Step 4 → Click General Settings → Approval Settings
        """
        try:
            # Step 1
            self._login_as_approver()

            # Step 2
            self._open_cgm_admin()

            # Step 3 — legal entity selected AFTER redirect to CGM Admin tab
            self._select_legal_entity()

            # Step 4 — navigate to Approval Settings only after entity confirmed
            self._navigate_to_approval_settings()

            self.logger.info(
                "✓ Full approver flow complete — Approval Settings page is open."
            )

        except Exception as exc:
            self.logger.error("Approver flow failed: %s", exc, exc_info=True)
            self.driver.save_screenshot("cgm_approver_failure.png")
            raise

    # ── Cleanup ───────────────────────────────────────────────────────────────
    def quit_cgm_browser(self):
        """Quit the Firefox browser when the approver flow is fully complete."""
        try:
            self.driver.quit()
            self.logger.info("Firefox browser closed.")
        except Exception:
            pass