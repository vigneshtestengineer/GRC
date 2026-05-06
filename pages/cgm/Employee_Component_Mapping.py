from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.json_config import get_str

LEGAL_ENTITY = get_str("auth", "legal_entity", "")

UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)

CONTRACTOR_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Contractor_Master_Data.json"
)


try:
    with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as _f:
        UNIT_NAME = json.load(_f).get("Unit_Details", {}).get("unit_name", "")
except (FileNotFoundError, json.JSONDecodeError):
    UNIT_NAME = ""

try:
    with open(CONTRACTOR_DATA_FILE, "r", encoding="utf-8") as _f:
        CONTRACTOR_NAME = json.load(_f).get("Contractor_Information", {}).get("Contractor_Name", "")
except (FileNotFoundError, json.JSONDecodeError):
    CONTRACTOR_NAME = ""


class EmployeeComponentMapping(BasePage):
    """Page object for Employee Component Mapping under General Component(s)."""

    # ── CGM Executive navigation ──────────────────────────────────────────────
    MENU_BUTTON                = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXEC_CARD   = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    EXECUTIVE_URL              = "http://13.203.6.58:5002/#/home/welcome"
    SPLASH_SCREEN              = (By.TAG_NAME, "compfie-splash-screen")
    SEARCH_LEGAL_ENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGAL_ENTITY_ROW    = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGAL_ENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Sidebar navigation ────────────────────────────────────────────────────
    OPEN_GENERAL_MASTER_MENU    = (By.XPATH, "//span[normalize-space()='General Master(s)']")
    CLICK_COMPONENT_MAPPING_MENU = (By.XPATH, "//span[normalize-space()='Component Mapping']")

    # Additional locators for Component Mapping page
    ADD_COMPONENT_MAPPING_BUTTON = (By.XPATH, "//button[contains(.,'Add')]")
    UNIT_DROPDOWN                   = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    DROPDOWN_SEARCH                 = (By.XPATH, "//input[@aria-label='dropdown search']")
    CONTRACTOR_DROPDOWN             = (By.XPATH, "//span[normalize-space()='Contractor']")
    SELECT_CONTRACTOR               = (By.XPATH, "(//mat-option[contains(@class,'mat-option')])[2]")
    SHOW_DETAILS                    = (By.XPATH, "//button[.//mat-icon[normalize-space()='sort'] and .//span[contains(normalize-space(.),'Show Detail')]]")
    SAVE_COMPONENT_MAPPING_BUTTON   = (By.XPATH, "(//button[.//span[contains(.,'Submit as save')]])[1]")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("EmployeeComponentMapping page initialized.")

    # ── CGM Executive: open via app-switcher ──────────────────────────────────
    def open_cgm_executive(self):
        self.wait_for_element_to_be_clickable(self.MENU_BUTTON, timeout=30)
        self.click(self.MENU_BUTTON)
        self.logger.info("Clicked app-switcher menu.")

        previous_windows = self.driver.window_handles
        self.wait_for_element_to_be_clickable(self.GENERAL_MASTER_EXEC_CARD, timeout=10)
        self.click(self.GENERAL_MASTER_EXEC_CARD)
        self._switch_to_new_window(previous_windows)

        WebDriverWait(self.driver, 20).until(EC.url_contains(self.EXECUTIVE_URL))
        self.logger.info("CGM Executive tab active.")

        self.wait_for_element(self.SEARCH_LEGAL_ENTITY, timeout=10)
        self.enter_text(self.SEARCH_LEGAL_ENTITY, LEGAL_ENTITY)
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*self.SEARCH_LEGAL_ENTITY)
                       .get_attribute("value").strip() == LEGAL_ENTITY
        )
        self._select_legal_entity()

        self.wait_for_element_to_be_clickable(self.SELECT_LEGAL_ENTITY_BUTTON, timeout=8)
        self.scroll_to_element(self.SELECT_LEGAL_ENTITY_BUTTON)
        self.click(self.SELECT_LEGAL_ENTITY_BUTTON)
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=30)
        self.logger.info("Legal entity selected — CGM Executive ready.")

    def _switch_to_new_window(self, previous_windows):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: len(d.window_handles) > len(previous_windows)
            )
            new = [h for h in self.driver.window_handles if h not in previous_windows]
            if new:
                self.driver.switch_to.window(new[-1])
                self.logger.info("Switched to new CGM Executive window.")
        except Exception:
            self.logger.info("No new window opened — continuing in current window.")

    def _select_legal_entity(self):
        for attempt in range(1, 3):
            self.wait_for_element(self.SELECT_LEGAL_ENTITY_ROW, timeout=8)
            self.scroll_to_element(self.SELECT_LEGAL_ENTITY_ROW)
            row = self.find_element(self.SELECT_LEGAL_ENTITY_ROW)
            try:
                row.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", row)
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: not d.find_element(*self.SELECT_LEGAL_ENTITY_BUTTON)
                               .get_attribute("disabled")
                )
                self.logger.info("Legal entity row selected (attempt %d).", attempt)
                return
            except Exception:
                self.logger.warning("Attempt %d: select button not yet enabled.", attempt)
        raise RuntimeError("Legal entity row clicked but select button did not become enabled.")

    # ── Step 1: Expand General Master(s) ─────────────────────────────────────
    def open_general_master_menu(self):
        if self.is_element_visible(self.CLICK_COMPONENT_MAPPING_MENU, timeout=0.5):
            self.logger.info("General Master menu already expanded.")
            return

        for attempt in range(1, 3):
            try:
                self.click(self.OPEN_GENERAL_MASTER_MENU, timeout=8)
                self.wait_for_element_to_be_clickable(self.CLICK_COMPONENT_MAPPING_MENU, timeout=8)
                self.logger.info(
                    "General Master menu expanded%s.",
                    " on retry" if attempt > 1 else "",
                )
                return
            except Exception as exc:
                self.logger.debug("Attempt %d failed: %s", attempt, exc)

        raise RuntimeError("Could not expand 'General Master(s)' menu after 2 attempts.")

    # ── Step 2: Navigate to Component Mapping and save ───────────────────────
    def employee_component_mapping(self):
        self.click(self.CLICK_COMPONENT_MAPPING_MENU, timeout=8)
        self.logger.info("Clicked 'Component Mapping' menu.")

        self.click(self.ADD_COMPONENT_MAPPING_BUTTON, timeout=8)
        self.logger.info("Clicked 'Add' button.")

        unit_name = self._get_unit_name()
        self.click(self.UNIT_DROPDOWN, timeout=8)
        self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
        self.enter_text(self.DROPDOWN_SEARCH, unit_name)
        self.sleep(0.3)
        self.click(
            (By.XPATH, f"//mat-option//span[contains(text(),'{unit_name}')]"),
            timeout=8,
        )
        self.logger.info("Selected unit: %s", unit_name)

        self.click(self.CONTRACTOR_DROPDOWN, timeout=8)
        self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
        self.enter_text(self.DROPDOWN_SEARCH, CONTRACTOR_NAME)
        self.sleep(0.3)
        self.click(self.SELECT_CONTRACTOR, timeout=8)
        self.logger.info("Selected contractor: %s", CONTRACTOR_NAME)
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        self.click(self.SHOW_DETAILS, timeout=8)
        self.sleep(0.5)
        self.click(self.SAVE_COMPONENT_MAPPING_BUTTON, timeout=8)
        self.logger.info("✓ Component mapping saved.")
        self.sleep(0.5)
        self.driver.refresh()
        self.sleep(2)
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=15)
        self.logger.info("Page refreshed after save.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def navigate_to_component_mapping(self):
        """
        Full flow after login:
          1. Open CGM Executive via app-switcher → select legal entity
          2. Expand General Master(s) → General Component(s) → Component Mapping
          3. Add → select Unit → save
        """
        self.open_cgm_executive()
        self.open_general_master_menu()
        self.employee_component_mapping()
        self.logger.info("✓ Employee Component Mapping completed.")

    # ── Helper ────────────────────────────────────────────────────────────────
    def _get_unit_name(self) -> str:
        try:
            with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("Unit_Details", {}).get("unit_name", UNIT_NAME)
        except Exception:
            return UNIT_NAME
