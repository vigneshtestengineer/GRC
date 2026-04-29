from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.json_config import get_str

LEGAL_ENTITY    = get_str("auth", "legal_entity", "")
CUSTOM_PATTERN  = get_str("contractor_pattern", "custom_pattern", "")
EXECUTIVE_URL = "http://13.203.6.58:5002/#/home/welcome"

UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)

try:
    with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as _f:
        _data = json.load(_f)
    UNIT_NAME = _data.get("Unit_Details", {}).get("unit_name", "")
except (FileNotFoundError, json.JSONDecodeError):
    UNIT_NAME = ""


class ContractorPatternConfig(BasePage):
    """Page object for Contractor Pattern Configuration under General Master(s)."""

    # ── App switcher / CGM navigation ────────────────────────────────────────
    MENU_BUTTON                   = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXECUTIVE_CARD = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    SPLASH_SCREEN                 = (By.TAG_NAME, "compfie-splash-screen")

    # ── Legal entity selection ────────────────────────────────────────────────
    SEARCH_LEGALENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGALENTITY        = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGALENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Sidebar navigation ────────────────────────────────────────────────────
    OPEN_GENERAL_MASTER_MENU      = (By.XPATH, "//span[normalize-space()='General Master(s)']")
    OPEN_PATTERN_CONFIG_MENU      = (By.XPATH, "//span[normalize-space()='Pattern Configuration']")
    SELECT_CONTRACTOR_MENU        = (By.XPATH, "//a[.//span[normalize-space()='Contractor(s)']]")
    
    # Pattern Configuration Addition Locators
    ADD_PATTERN_CONFIG_BUTTON     = (By.XPATH, "//button[contains(.,'Add')]")
    UNIT_DROPDOWN                 = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    SEARCH = (By.XPATH, "//input[@aria-label='dropdown search']")
    CONTRACTOR_BASED_CODE_PATTERN = (By.XPATH, "(//mat-radio-button[.//input[@value='M']])[1]")
    CONTRACTOR_BASED_SUBCONTRACTOR_PATTERN = (By.XPATH, "((//mat-radio-button)[6]//input[@type='radio'])[1]")
    PATTERN_CONFIG_SAVE = (By.XPATH, "(//button[.//span[contains(.,'Submit as save')]])[1]")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("ContractorPatternConfig page initialized.")

    # ── Step 1: Open CGM Executive via app-switcher ───────────────────────────
    def open_cgm_executive(self):
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=30)
        previous_windows = self.driver.window_handles

        self.click(self.MENU_BUTTON, timeout=15)
        self.logger.info("Clicked app-switcher menu.")

        self.wait_for_element_to_be_clickable(self.GENERAL_MASTER_EXECUTIVE_CARD, timeout=10)
        self.click(self.GENERAL_MASTER_EXECUTIVE_CARD, timeout=10)
        self.logger.info("Clicked 'General Master-Executive' card.")

        self._switch_to_new_window_if_opened(previous_windows)

        WebDriverWait(self.driver, 15).until(EC.url_contains(EXECUTIVE_URL))
        self.logger.info("✓ Redirected to CGM Executive URL.")

        self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=30)

    # ── Step 2: Select Legal Entity ───────────────────────────────────────────
    def select_legal_entity(self):
        self.wait_for_element(self.SEARCH_LEGALENTITY, timeout=10)
        self.enter_text(self.SEARCH_LEGALENTITY, LEGAL_ENTITY)
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*self.SEARCH_LEGALENTITY)
            .get_attribute("value")
            .strip() == LEGAL_ENTITY
        )
        self._select_legal_entity_row()
        self.scroll_to_element(self.SELECT_LEGALENTITY_BUTTON)
        self.click(self.SELECT_LEGALENTITY_BUTTON, timeout=8)
        self.logger.info("✓ Legal entity '%s' selected.", LEGAL_ENTITY)

    # ── Step 3: Expand General Master(s) menu ────────────────────────────────
    def open_general_master_menu(self):
        if self.is_element_visible(self.OPEN_PATTERN_CONFIG_MENU, timeout=2):
            self.logger.info("General Master menu already expanded.")
            return

        for attempt in range(1, 3):
            try:
                self.click(self.OPEN_GENERAL_MASTER_MENU, timeout=8)
                self.wait_for_element_to_be_clickable(self.OPEN_PATTERN_CONFIG_MENU, timeout=8)
                self.logger.info(
                    "General Master menu expanded%s.",
                    " on retry" if attempt > 1 else "",
                )
                return
            except Exception as exc:
                self.logger.debug("Attempt %d failed: %s", attempt, exc)

        raise RuntimeError("Could not expand 'General Master(s)' menu after 2 attempts.")

    # ── Step 4: Open Pattern Configuration → Contractor ──────────────────────
    def open_contractor_pattern_config(self):
        self.click(self.OPEN_PATTERN_CONFIG_MENU, timeout=8)
        self.logger.info("Clicked 'Pattern Configuration' menu.")

        self.wait_for_element_to_be_clickable(self.SELECT_CONTRACTOR_MENU, timeout=8)
        self.click(self.SELECT_CONTRACTOR_MENU, timeout=8)
        self.logger.info("✓ 'Contractor' menu selected.")

    def create_contractor_pattern_config(self, pattern_type="Contractor Based Code Pattern", digits=5, starting_value=1, increment=1):
        """Creates a contractor pattern configuration with specified parameters."""
        self.click(self.ADD_PATTERN_CONFIG_BUTTON, timeout=8)
        self.logger.info("Clicked 'Add Pattern Configuration' button.")
        unit_name = self._get_unit_name()
        self.click(self.UNIT_DROPDOWN, timeout=8)
        self.wait_for_element(self.SEARCH, timeout=8)
        self.enter_text(self.SEARCH, unit_name)
        self.logger.info("Searched for unit: %s", unit_name)
        self.sleep(0.5)
        self.click((By.XPATH, f"//mat-option//span[contains(text(),'{unit_name}')]"), timeout=8)
        self.logger.info("Selected unit: %s", unit_name)
        self.click(self.CONFIG_PATTERN, timeout=8)
        self.click(self.CONTRACTOR_BASED_CODE_PATTERN, timeout=8)
        self.click(self.CONTRACTOR_BASED_SUBCONTRACTOR_PATTERN, timeout=8)
        self.click(self.PATTERN_CONFIG_SAVE, timeout=8)
        self.logger.info("✓ Contractor pattern configuration created and saved.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def navigate_to_contractor_config(self):
        """Full sequence: CGM login → legal entity → General Master → Contractor."""
        from pages.login.grc_login_page import GRCLoginPage

        username = get_str("auth", "username", "")
        password = get_str("auth", "password", "")
        group    = get_str("auth", "group", "")

        self.logger.info("Logging in as '%s' …", username)
        GRCLoginPage(self.driver).login(username, password, group)
        self.logger.info("✓ Login complete.")

        self.open_cgm_executive()
        self.select_legal_entity()
        self.open_general_master_menu()
        self.open_contractor_pattern_config()
        self.create_contractor_pattern_config()

        self.logger.info("✓ Contractor Pattern Configuration page is open.")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _get_unit_name(self):
        """Read unit name from Unit_Master_Data.json at runtime."""
        try:
            with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("Unit_Details", {}).get("unit_name", UNIT_NAME)
        except Exception:
            return UNIT_NAME

    def _switch_to_new_window_if_opened(self, previous_windows):
        current_windows = self.driver.window_handles
        new_windows = [h for h in current_windows if h not in previous_windows]
        if new_windows:
            self.driver.switch_to.window(new_windows[-1])
            self.logger.info("Switched to new tab: %s", new_windows[-1])

    def _select_legal_entity_row(self):
        for attempt in range(1, 3):
            self.wait_for_element(self.SELECT_LEGALENTITY, timeout=8)
            self.scroll_to_element(self.SELECT_LEGALENTITY)
            row_cell = self.find_element(self.SELECT_LEGALENTITY)

            try:
                row_cell.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", row_cell)

            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.execute_script(
                        """
                        const btn = arguments[0];
                        return !btn.disabled &&
                               btn.getAttribute('disabled') === null &&
                               btn.getAttribute('aria-disabled') !== 'true';
                        """,
                        d.find_element(*self.SELECT_LEGALENTITY_BUTTON),
                    )
                )
                self.logger.info("Legal entity row selected.")
                return
            except Exception:
                self.logger.warning(
                    "Select button not enabled on attempt %d — retrying.", attempt
                )

        raise RuntimeError("Legal entity row clicked but select button did not enable.")
