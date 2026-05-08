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

LEGAL_ENTITY = get_str("auth", "legal_entity", "")

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


class WeeklyHolidayMaster(BasePage):
    """Page object for Weekly Holiday Master under General Component(s)."""

    # ── CGM Executive navigation ──────────────────────────────────────────────
    MENU_BUTTON                = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXEC_CARD   = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    EXECUTIVE_URL              = "http://13.203.6.58:5002/#/home/welcome"
    SPLASH_SCREEN              = (By.TAG_NAME, "compfie-splash-screen")
    SEARCH_LEGAL_ENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGAL_ENTITY_ROW    = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGAL_ENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Sidebar navigation ────────────────────────────────────────────────────
    OPEN_GENERAL_MASTER_MENU = (By.XPATH, "//span[normalize-space()='General Master(s)']")

    # ── Weekly Holiday Master page ────────────────────────────────────────────
    CLICK_WEEKLY_HOLIDAY_MASTER = (By.XPATH, "//span[text()=' Weekly holiday ']")
    ADD_WEEKLY_HOLIDAY_BUTTON = (By.XPATH, "//button[contains(.,'Add')]")
    UNIT_DROPDOWN            = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    DROPDOWN_SEARCH          = (By.XPATH, "//input[@aria-label='dropdown search']")
    SELECT_DROPDOWN_DATA      = (By.XPATH, "(//mat-option[contains(@class,'mat-option')])[2]")
    CONTRACTOR_DROPDOWN        = (By.XPATH, "//span[normalize-space()='Contractor']")
    SELECT_WEEKOFF_BASED     = (By.XPATH, "//input[@type='radio' and @value='E']")
    COMPONENT_DROPDOWN          = (By.XPATH, "//span[normalize-space()='Choose Component *']")
    SELECT_COMPONENT_DATA        = (By.XPATH, "(//mat-option[contains(@class,'mat-option')])[1]")
    SELECT_COMP_OFF      = (By.XPATH, "(//span[contains(@class,'mat-checkbox-ripple')])[8]")
    COMP_OFF_WITHIN     = (By.XPATH, "//input[@id='mat-input-5']")
    CHOOSE_PERIODICITY        = (By.XPATH, "//span[normalize-space()='Choose Periodicity *']")
    CHOOSE_PERIODICITY_DATA   = (By.XPATH, "//mat-option//span[normalize-space()='Day(s)']")
    SAVE_WEEKLY_HOLIDAY_BUTTON = (By.XPATH, "(//button[.//span[contains(.,'Submit as save')]])[1]")


    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("WeeklyHolidayMaster page initialized.")
        self.unit_master_data  = UNIT_MASTER_DATA
        self.Unit_Details      = self.unit_master_data.get("Unit_Details", {})
        self.date_of_creation  = self.Unit_Details.get("Date_of_Creation", "")

    # ── CGM Executive: open via app-switcher ─────────────────────────────────
    def open_cgm_executive(self):
        self.wait_for_element_to_be_clickable(self.MENU_BUTTON, timeout=30)
        self.click(self.MENU_BUTTON)
        self.logger.info("Clicked app-switcher menu.")

        # Capture existing windows BEFORE the click that opens the new one
        previous_windows = self.driver.window_handles
        self.wait_for_element_to_be_clickable(self.GENERAL_MASTER_EXEC_CARD, timeout=10)
        self.click(self.GENERAL_MASTER_EXEC_CARD)

        # Switch to the newly opened window and wait for it to fully load
        self._switch_to_new_window(previous_windows)
        WebDriverWait(self.driver, 30).until(EC.url_contains(self.EXECUTIVE_URL))
        self.logger.info("CGM Executive tab active.")

        self.wait_for_element(self.SEARCH_LEGAL_ENTITY, timeout=15)
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
            # Wait until a brand-new window handle appears
            WebDriverWait(self.driver, 15).until(
                lambda d: len(d.window_handles) > len(previous_windows)
            )
            new_handles = [h for h in self.driver.window_handles if h not in previous_windows]
            if new_handles:
                self.driver.switch_to.window(new_handles[-1])
                self.logger.info("Switched to new CGM Executive window.")
            else:
                self.logger.warning("No new window found — staying in current window.")
        except Exception as e:
            self.logger.warning(f"Window switch failed: {e} — continuing in current window.")

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

    # ── Step 1: Expand General Master(s) menu ────────────────────────────────
    def general_master_menu(self):
        self.scroll_to_element(self.OPEN_GENERAL_MASTER_MENU)
        self.sleep(0.3)
        parent_el = self.find_element(self.OPEN_GENERAL_MASTER_MENU)
        self.driver.execute_script("arguments[0].click();", parent_el)
        self.logger.info("Clicked General Master(s) menu.")


    # ── Step 2: Fill and save Shift Master form ───────────────────────────────
    def weekly_holiday_master(self):

        self.click(self.CLICK_WEEKLY_HOLIDAY_MASTER)
        self.click(self.ADD_WEEKLY_HOLIDAY_BUTTON)
        self.click(self.UNIT_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, self._get_unit_name())
        self.click(self.SELECT_DROPDOWN_DATA)
        self.click(self.CONTRACTOR_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, CONTRACTOR_NAME)
        self.click(self.SELECT_DROPDOWN_DATA)
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        self.click(self.SELECT_WEEKOFF_BASED)
        self.click(self.COMPONENT_DROPDOWN)
        self.click(self.SELECT_COMPONENT_DATA)
        self.sleep(0.5)
        DatePicker(self.driver).set_date(
            "(//button[@aria-label='Open calendar'])[1]", self.date_of_creation
        )
        self.sleep(30)
        self.click(self.SELECT_COMP_OFF)
        self.enter_text(self.COMP_OFF_WITHIN, "5")
        self.click(self.CHOOSE_PERIODICITY)
        self.click(self.CHOOSE_PERIODICITY_DATA)
        self.click(self.SAVE_WEEKLY_HOLIDAY_BUTTON)
        self.sleep(0.5)
        self.driver.refresh()
        self.logger.info("Weekly Holiday Master form filled and submitted.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def navigate_to_weekly_holiday_master(self):
        self.open_cgm_executive()
        self.general_master_menu()
        self.weekly_holiday_master()
        self.logger.info("✓ Weekly Holiday Master completed.")

    # ── Helper ────────────────────────────────────────────────────────────────
    def _get_unit_name(self) -> str:
        try:
            with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("Unit_Details", {}).get("unit_name", UNIT_NAME)
        except Exception:
            return UNIT_NAME