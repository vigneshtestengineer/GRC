from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from pathlib import Path
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.json_config import get_str

CUSTOM_PATTERN = get_str("contractor_pattern", "custom_pattern", "")

UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)

try:
    with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as _f:
        UNIT_NAME = json.load(_f).get("Unit_Details", {}).get("unit_name", "")
except (FileNotFoundError, json.JSONDecodeError):
    UNIT_NAME = ""


class ContractorPatternConfig(BasePage):
    """Page object for Contractor Pattern Configuration under General Master(s)."""

    # ── Sidebar navigation ────────────────────────────────────────────────────
    OPEN_GENERAL_MASTER_MENU = (By.XPATH, "//span[normalize-space()='General Master(s)']")
    OPEN_PATTERN_CONFIG_MENU = (By.XPATH, "//span[normalize-space()='Pattern Configuration']")
    SELECT_CONTRACTOR_MENU   = (By.XPATH, "//a[.//span[normalize-space()='Contractor(s)']]")

    # ── Pattern Configuration form locators ───────────────────────────────────
    ADD_PATTERN_CONFIG_BUTTON               = (By.XPATH, "//button[contains(.,'Add')]")
    UNIT_DROPDOWN                           = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    SEARCH                                  = (By.XPATH, "//input[@aria-label='dropdown search']")
    CONTRACTOR_BASED_CODE_PATTERN           = (By.XPATH, "(//mat-radio-button[.//input[@value='M']])[1]")
    CONTRACTOR_BASED_SUBCONTRACTOR_PATTERN  = (By.XPATH, "((//mat-radio-button)[6]//input[@type='radio'])[1]")
    PATTERN_CONFIG_SAVE                     = (By.XPATH, "(//button[.//span[contains(.,'Submit as save')]])[1]")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("ContractorPatternConfig page initialized.")

    # ── Step 1: Expand General Master(s) menu ────────────────────────────────
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

    # ── Step 2: Open Pattern Configuration → Contractor ──────────────────────
    def open_contractor_pattern_config(self):
        self.click(self.OPEN_PATTERN_CONFIG_MENU, timeout=8)
        self.logger.info("Clicked 'Pattern Configuration' menu.")

        self.wait_for_element_to_be_clickable(self.SELECT_CONTRACTOR_MENU, timeout=8)
        self.click(self.SELECT_CONTRACTOR_MENU, timeout=8)
        self.logger.info("✓ 'Contractor' menu selected.")

    # ── Step 3: Create the pattern config entry ───────────────────────────────
    def create_contractor_pattern_config(self):
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

        self.click(self.CONTRACTOR_BASED_CODE_PATTERN, timeout=8)
        self.click(self.CONTRACTOR_BASED_SUBCONTRACTOR_PATTERN, timeout=8)
        self.click(self.PATTERN_CONFIG_SAVE, timeout=8)
        self.logger.info("✓ Contractor pattern configuration created and saved.")
        self.sleep(2)

    # ── Public orchestration ──────────────────────────────────────────────────
    def navigate_to_contractor_config(self):
        """Continues from the existing CGM Executive session after Approve Approval Settings.
        The shared driver is already authenticated and on the Approval Settings page.
        Navigates via sidebar: General Master(s) → Pattern Configuration → Contractor.
        """
        self.open_general_master_menu()
        self.open_contractor_pattern_config()
        self.create_contractor_pattern_config()
        self.logger.info("✓ Contractor Pattern Configuration completed.")

    # ── Helper ────────────────────────────────────────────────────────────────
    def _get_unit_name(self):
        try:
            with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("Unit_Details", {}).get("unit_name", UNIT_NAME)
        except Exception:
            return UNIT_NAME
