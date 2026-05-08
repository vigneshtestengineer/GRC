from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import json
import sys
import os

from pages.cgm.unit_master import UNIT_MASTER_DATA

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base.date_picker import DatePicker
from utilities.json_config import get_str

# LEGAL_ENTITY = get_str("auth", "legal_entity", "")

UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)

CONTRACTOR_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Contractor_Master_Data.json"
)

SHIFT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Shift_Master_Details.json"
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

try:
    with open(SHIFT_MASTER_DATA_FILE, "r", encoding="utf-8") as f:
        shift_data = json.load(f)
        SHIFT_NAME        = shift_data.get("Shift_Master_Details", {}).get("Shift_Name", "")
        SHIFT_START_FROM  = shift_data.get("Shift_Master_Details", {}).get("Shift_Start_From", "")
        SHIFT_END_TO      = shift_data.get("Shift_Master_Details", {}).get("Shift_End_To", "")
        INTERVAL_START_FROM = shift_data.get("Shift_Master_Details", {}).get("Interval_start_From", "")
        INTERVAL_END_TO   = shift_data.get("Shift_Master_Details", {}).get("Interval_End_To", "")
        PUNCH_BEFORE_SHIFT = shift_data.get("Shift_Master_Details", {}).get("Punch_Before_Shift", "")
        PUNCH_AFTER_SHIFT = shift_data.get("Shift_Master_Details", {}).get("Punch_After_Shift", "")
        SHIFT_COLOR       = shift_data.get("Shift_Master_Details", {}).get("Shift_Color", "")
        SHIFT_MASTER_REMARKS = shift_data.get("Shift_Master_Details", {}).get("Shift_Master_Remarks", "")
except (FileNotFoundError, json.JSONDecodeError):
    SHIFT_NAME = SHIFT_START_FROM = SHIFT_END_TO = ""
    INTERVAL_START_FROM = INTERVAL_END_TO = ""
    PUNCH_BEFORE_SHIFT = PUNCH_AFTER_SHIFT = ""
    SHIFT_COLOR = SHIFT_MASTER_REMARKS = ""


class ShiftMasterCreation(BasePage):
    """Page object for Shift Master Creation under General Component(s)."""

    # ── CGM Executive navigation ──────────────────────────────────────────────
    # MENU_BUTTON                = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    # GENERAL_MASTER_EXEC_CARD   = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    # EXECUTIVE_URL              = "http://13.203.6.58:5002/#/home/welcome"
    # SPLASH_SCREEN              = (By.TAG_NAME, "compfie-splash-screen")
    # SEARCH_LEGAL_ENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    # SELECT_LEGAL_ENTITY_ROW    = (By.XPATH, "//table//tbody//tr[1]//td")
    # SELECT_LEGAL_ENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Sidebar navigation ────────────────────────────────────────────────────
    OPEN_GENERAL_MASTER_MENU = (By.XPATH, "//span[normalize-space()='General Master(s)']")
    CLICK_SHIFT_MASTER_MENU  = (By.XPATH, "//span[normalize-space()='Shift Master']")

    # ── Shift Master page ─────────────────────────────────────────────────────
    ADD_SHIFT_MASTER_BUTTON  = (By.XPATH, "//button[contains(.,'Add')]")
    UNIT_DROPDOWN            = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    DROPDOWN_SEARCH          = (By.XPATH, "//input[@aria-label='dropdown search']")
    SELECT_UNIT              = (By.XPATH, "(//mat-option[contains(@class,'mat-option')])[2]")
    ADD_SHIFT                = (By.XPATH, "//button[@mat-mini-fab]")

    # ── Shift form fields ─────────────────────────────────────────────────────
    SHIFT_NAME_INPUT         = (By.XPATH, "//input[@id='mat-input-2']")
    SHIFT_START_FROM_INPUT   = (By.XPATH, "//input[@id='mat-input-4']")
    SHIFT_END_TO_INPUT       = (By.XPATH, "//input[@id='mat-input-5']")
    INTERVAL_START_FROM_INPUT= (By.XPATH, "//input[@id='mat-input-6']")
    INTERVAL_END_TO_INPUT    = (By.XPATH, "//input[@id='mat-input-7']")
    BEFORE_SHIFT_INPUT       = (By.XPATH, "//input[@id='mat-input-10']")
    AFTER_SHIFT_INPUT        = (By.XPATH, "//input[@id='mat-input-11']")
    ENTER_COLOR_CODE         = (By.XPATH, "//span[contains(@class,'gt-xs')]//input")
    SHIFT_MASTER_REMARKS_INPUT = (By.XPATH, "//textarea[@id='mat-input-16']")
    SAVE_SHIFT_BUTTON        = (By.XPATH, "//span[contains(normalize-space(),'Save & Close')]")
    SAVE_SHIFT_MASTER_BUTTON = (By.XPATH, "(//button[.//span[contains(.,'Submit as save')]])[1]")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("ShiftMasterCreation page initialized.")
        self.unit_master_data  = UNIT_MASTER_DATA
        self.Unit_Details      = self.unit_master_data.get("Unit_Details", {})
        self.date_of_creation  = self.Unit_Details.get("Date_of_Creation", "")

    # # ── CGM Executive: open via app-switcher ─────────────────────────────────
    # def open_cgm_executive(self):
    #     self.wait_for_element_to_be_clickable(self.MENU_BUTTON, timeout=30)
    #     self.click(self.MENU_BUTTON)
    #     self.logger.info("Clicked app-switcher menu.")

    #     # Capture existing windows BEFORE the click that opens the new one
    #     previous_windows = self.driver.window_handles
    #     self.wait_for_element_to_be_clickable(self.GENERAL_MASTER_EXEC_CARD, timeout=10)
    #     self.click(self.GENERAL_MASTER_EXEC_CARD)

    #     # Switch to the newly opened window and wait for it to fully load
    #     self._switch_to_new_window(previous_windows)
    #     WebDriverWait(self.driver, 30).until(EC.url_contains(self.EXECUTIVE_URL))
    #     self.logger.info("CGM Executive tab active.")

    #     self.wait_for_element(self.SEARCH_LEGAL_ENTITY, timeout=15)
    #     self.enter_text(self.SEARCH_LEGAL_ENTITY, LEGAL_ENTITY)
    #     WebDriverWait(self.driver, 10).until(
    #         lambda d: d.find_element(*self.SEARCH_LEGAL_ENTITY)
    #                    .get_attribute("value").strip() == LEGAL_ENTITY
    #     )
    #     self._select_legal_entity()

    #     self.wait_for_element_to_be_clickable(self.SELECT_LEGAL_ENTITY_BUTTON, timeout=8)
    #     self.scroll_to_element(self.SELECT_LEGAL_ENTITY_BUTTON)
    #     self.click(self.SELECT_LEGAL_ENTITY_BUTTON)
    #     self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=30)
    #     self.logger.info("Legal entity selected — CGM Executive ready.")

    # def _switch_to_new_window(self, previous_windows):
    #     try:
    #         # Wait until a brand-new window handle appears
    #         WebDriverWait(self.driver, 15).until(
    #             lambda d: len(d.window_handles) > len(previous_windows)
    #         )
    #         new_handles = [h for h in self.driver.window_handles if h not in previous_windows]
    #         if new_handles:
    #             self.driver.switch_to.window(new_handles[-1])
    #             self.logger.info("Switched to new CGM Executive window.")
    #         else:
    #             self.logger.warning("No new window found — staying in current window.")
    #     except Exception as e:
    #         self.logger.warning(f"Window switch failed: {e} — continuing in current window.")

    # def _select_legal_entity(self):
    #     for attempt in range(1, 3):
    #         self.wait_for_element(self.SELECT_LEGAL_ENTITY_ROW, timeout=8)
    #         self.scroll_to_element(self.SELECT_LEGAL_ENTITY_ROW)
    #         row = self.find_element(self.SELECT_LEGAL_ENTITY_ROW)
    #         try:
    #             row.click()
    #         except Exception:
    #             self.driver.execute_script("arguments[0].click();", row)
    #         try:
    #             WebDriverWait(self.driver, 5).until(
    #                 lambda d: not d.find_element(*self.SELECT_LEGAL_ENTITY_BUTTON)
    #                            .get_attribute("disabled")
    #             )
    #             self.logger.info("Legal entity row selected (attempt %d).", attempt)
    #             return
    #         except Exception:
    #             self.logger.warning("Attempt %d: select button not yet enabled.", attempt)
    #     raise RuntimeError("Legal entity row clicked but select button did not become enabled.")

    # # ── Step 1: Expand General Master(s) menu ────────────────────────────────
    # def general_master_menu(self):
    #     self.scroll_to_element(self.OPEN_GENERAL_MASTER_MENU)
    #     self.sleep(0.3)
    #     parent_el = self.find_element(self.OPEN_GENERAL_MASTER_MENU)
    #     self.driver.execute_script("arguments[0].click();", parent_el)
    #     self.logger.info("Clicked General Master(s) menu.")

    def _click_shift_master(self):
        """Scrolls to and JS-clicks the Shift Master menu item."""
        self.scroll_to_element(self.CLICK_SHIFT_MASTER_MENU)
        self.sleep(0.3)
        el = self.find_element(self.CLICK_SHIFT_MASTER_MENU)
        self.driver.execute_script("arguments[0].click();", el)
        self.logger.info("Clicked 'Shift Master' menu item.")

    # ── Step 2: Fill and save Shift Master form ───────────────────────────────
    def shift_master_creation(self):
        """Fills the Shift Master form and saves."""
        self._click_shift_master()

        self.click(self.ADD_SHIFT_MASTER_BUTTON, timeout=8)
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
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        self.sleep(1)

        self.click(self.ADD_SHIFT, timeout=8)
        self.sleep(1)
        self.enter_text(self.SHIFT_NAME_INPUT, SHIFT_NAME)
        DatePicker(self.driver).set_date(
            "//button[@aria-label='Open calendar']", self.date_of_creation
        )
        self.sleep(0.5)
        self.enter_text(self.SHIFT_START_FROM_INPUT, SHIFT_START_FROM)
        self.enter_text(self.SHIFT_END_TO_INPUT, SHIFT_END_TO)
        self.enter_text(self.INTERVAL_START_FROM_INPUT, INTERVAL_START_FROM)
        self.enter_text(self.INTERVAL_END_TO_INPUT, INTERVAL_END_TO)
        self.enter_text(self.BEFORE_SHIFT_INPUT, PUNCH_BEFORE_SHIFT)
        self.enter_text(self.AFTER_SHIFT_INPUT, PUNCH_AFTER_SHIFT)
        self.enter_text(self.ENTER_COLOR_CODE, SHIFT_COLOR)
        self.enter_text(self.SHIFT_MASTER_REMARKS_INPUT, SHIFT_MASTER_REMARKS)
        self.click(self.SAVE_SHIFT_BUTTON, timeout=8)
        self.sleep(0.5)
        self.wait_for_element_to_be_clickable(self.SAVE_SHIFT_MASTER_BUTTON, timeout=8)
        self.click(self.SAVE_SHIFT_MASTER_BUTTON, timeout=8)
        self.logger.info("✓ Shift Master saved.")
        self.sleep(0.5)
        self.driver.refresh()
        self.sleep(2)
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN, timeout=15)
        self.logger.info("Page refreshed after save.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def navigate_to_shift_master(self):
        self.shift_master_creation() # fills and saves the form
        self.logger.info("✓ Shift Master Creation completed.")

    # ── Helper ────────────────────────────────────────────────────────────────
    def _get_unit_name(self) -> str:
        try:
            with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("Unit_Details", {}).get("unit_name", UNIT_NAME)
        except Exception:
            return UNIT_NAME