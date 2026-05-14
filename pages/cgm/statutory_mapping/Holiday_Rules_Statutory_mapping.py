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
from pages.base.date_picker import DatePicker
from utilities.json_config import get_str

# LEGAL_ENTITY = get_str("auth", "legal_entity", "")

CONTRACT_LABOUR_DATA_FILE = (
    Path(__file__).resolve().parents[3] / "config" / "Contract_Labour_Data.json"
)
CONTRACTOR_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[3] / "config" / "Contractor_Master_Data.json"
)
UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[3] / "config" / "Unit_Master_Data.json"
)
STATUTORY_MAPPING_DATA_FILE = (
    Path(__file__).resolve().parents[3] / "config" / "Statutory_Mapping_Data.json"
)


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class HolidayRulesStatutoryMapping(BasePage):

    # # ── CGM Navigation ────────────────────────────────────────────────────────
    # MENU_BUTTON                = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    # GENERAL_MASTER_EXEC_CARD   = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    # EXECUTIVE_URL              = "http://13.203.6.58:5002/#/home/welcome"
    # SEARCH_LEGAL_ENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    # SELECT_LEGAL_ENTITY_ROW    = (By.XPATH, "//table//tbody//tr[1]//td")
    # SELECT_LEGAL_ENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # # ── Sidebar ───────────────────────────────────────────────────────────────
    # OPEN_STATUTORY_MAPPING     = (By.XPATH, "//span[normalize-space()='Statutory Master(s)']")
    # CLICK_STATUTORY_MAPPING_MENU = (By.XPATH, "//a[.//span[normalize-space()='Statutory Mapping']]")

    # ── HOLIDAY RULES STATUTORY MAPPING ────────────────────────────────────────────────
    SPLASH_SCREEN_OVERLAY      = (By.TAG_NAME, "compfie-splash-screen")
    ADD_STATUTORY_MAPPING_BTN  = (By.XPATH, "//button[.//span[contains(@class,'mat-button-wrapper') and contains(normalize-space(),'Add')]]")
    STATE_DROPDOWN              = (By.XPATH, "//span[normalize-space()='Choose State']")
    SEARCH                      = (By.XPATH, "//input[@aria-label='dropdown search']")
    SELECT_DROPDOWN_OPTION      = (By.XPATH, "(//mat-option//span[@class='mat-option-text'])[2]")
    UNIT_DROPDOWN               = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    SELECT_UNIT                 = (By.XPATH, "(//mat-option[@role='option'])[2]")

    # OPEN HOLIDAY RULES STATUTORY MAPPING DETAILS
    OPEN_HOLIDAY_RULES_STATUTORY_MAPPING_DETAILS = (By.XPATH, "(//mat-expansion-panel-header)[11]")
    ENABLE_HOLIDAY_RULES_STATUTORY_MAPPING     = (By.XPATH, "(//input[@role='switch'])[11]")
    HOLIDAY_TYPE_DROPDOWN              = (By.XPATH, "(//mat-select//div[contains(@class,'mat-select-trigger')])[23]")
    PRIMARY_SETTINGS              = (By.XPATH, "(//mat-select//div[contains(@class,'mat-select-trigger')])[24]")
    SAVE_BTN                   = (By.XPATH, "//button[.//span[normalize-space()='Submit as save']]")

    def __init__(self, driver):
        super().__init__(driver)

        _contractor_data  = _load_json(CONTRACTOR_MASTER_DATA_FILE)
        _unit_data        = _load_json(UNIT_MASTER_DATA_FILE)
        _statutory_data   = _load_json(STATUTORY_MAPPING_DATA_FILE)

        contractor_info   = _contractor_data.get("Contractor_Information", {})
        unit_details      = _unit_data.get("Unit_Details", {})
        holiday_rules_data = _statutory_data.get("Holiday_Rules", {})

        self._unit_name        = unit_details.get("unit_name", "")
        self._state            = unit_details.get("State", "")
        self._contractor_name  = contractor_info.get("Contractor_Name", "")

        _holiday_rules_primary_setting  = holiday_rules_data.get("Holiday Rules Primary settings", "")
        self._applied_from   = holiday_rules_data.get("Applied_From", "")
        _holiday_type = holiday_rules_data.get("Holiday_Type", "")
        self.SELECT_PRIMARY_SETTING = (
            By.XPATH, f"//span[contains(text(),'{_holiday_rules_primary_setting}')]"
        )
        self.SELECT_HOLIDAY_TYPE = (
            By.XPATH, f"//span[contains(text(),'{_holiday_type}')]"
        )


    # # ── Step 1: Open CGM Executive ────────────────────────────────────────────
    # def open_cgm_executive(self):
    #     self.wait_for_element_to_be_clickable(self.MENU_BUTTON, timeout=30)
    #     self.click(self.MENU_BUTTON)
    #     self.logger.info("Clicked app-switcher menu.")

    #     previous_windows = self.driver.window_handles
    #     self.wait_for_element_to_be_clickable(self.GENERAL_MASTER_EXEC_CARD, timeout=8)
    #     self.click(self.GENERAL_MASTER_EXEC_CARD)
    #     self._switch_to_new_window(previous_windows)

    #     WebDriverWait(self.driver, 20).until(EC.url_contains(self.EXECUTIVE_URL))
    #     self.logger.info("CGM Executive tab active.")

    #     self.wait_for_element(self.SEARCH_LEGAL_ENTITY, timeout=10)
    #     self.enter_text(self.SEARCH_LEGAL_ENTITY, LEGAL_ENTITY)
    #     WebDriverWait(self.driver, 10).until(
    #         lambda d: d.find_element(*self.SEARCH_LEGAL_ENTITY)
    #                    .get_attribute("value").strip() == LEGAL_ENTITY
    #     )
    #     self._select_legal_entity()

    #     self.wait_for_element_to_be_clickable(self.SELECT_LEGAL_ENTITY_BUTTON, timeout=8)
    #     self.scroll_to_element(self.SELECT_LEGAL_ENTITY_BUTTON)
    #     self.click(self.SELECT_LEGAL_ENTITY_BUTTON)
    #     self.logger.info("Legal entity selected and confirmed.")

    # def _switch_to_new_window(self, previous_windows):
    #     try:
    #         WebDriverWait(self.driver, 10).until(
    #             lambda d: len(d.window_handles) > len(previous_windows)
    #         )
    #         new = [h for h in self.driver.window_handles if h not in previous_windows]
    #         if new:
    #             self.driver.switch_to.window(new[-1])
    #             self.logger.info("Switched to new CGM Executive window.")
    #     except Exception:
    #         self.logger.info("No new window opened — continuing in current window.")

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
    #                 lambda d: not d.find_element(*self.SELECT_LEGAL_ENTITY_BUTTON).get_attribute("disabled")
    #             )
    #             self.logger.info("Legal entity row selected (attempt %d).", attempt)
    #             return
    #         except Exception:
    #             self.logger.warning("Legal entity click attempt %d did not enable button.", attempt)
    #     raise RuntimeError("Legal entity row was clicked but the select button did not become enabled.")

    # # ── Step 1: Navigate to Statutory Mapping ─────────────────────────────────

    # def navigate_to_statutory_mapping(self):
    #     self.wait_for_element(self.OPEN_STATUTORY_MAPPING, timeout=15)
    #     self.click(self.OPEN_STATUTORY_MAPPING)
    #     self.wait_for_element(self.CLICK_STATUTORY_MAPPING_MENU, timeout=10)
    #     self.click(self.CLICK_STATUTORY_MAPPING_MENU)
    #     self.wait_for_element(self.ADD_STATUTORY_MAPPING_BTN, timeout=15)
    #     self.logger.info("Navigated to Statutory Mapping page.")

    # ── Step 3: MAPPING THE STATUTORY SETTINGS ───────────────────────────────────────────────────
    def _add_holiday_rules_statutory_mapping(self):
        self.click(self.ADD_STATUTORY_MAPPING_BTN)
        self.wait_for_element(self.STATE_DROPDOWN, timeout=10)
        self.click(self.STATE_DROPDOWN)
        self.sleep(1)
        self.enter_text(self.SEARCH, self._state)
        self.sleep(1)
        self.click(self.SELECT_DROPDOWN_OPTION)
        self.click(self.UNIT_DROPDOWN)
        self.sleep(1)
        self.enter_text(self.SEARCH, self._unit_name)
        self.sleep(1)
        self.click(self.SELECT_UNIT)
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        self.sleep(1)

        # Adding the Minimum wage details

        self.click(self.OPEN_HOLIDAY_RULES_STATUTORY_MAPPING_DETAILS)
        self.sleep(0.5)
        self.logger.info("Selected state '%s' and unit '%s'.", self._state, self._unit_name)
        self.click(self.ENABLE_HOLIDAY_RULES_STATUTORY_MAPPING)
        self.sleep(0.5)
        self.click(self.HOLIDAY_TYPE_DROPDOWN)
        self.sleep(1)
        self.click(self.SELECT_HOLIDAY_TYPE)
        self.sleep(0.5)
        self.click(self.PRIMARY_SETTINGS)
        self.scroll_to_element(self.SELECT_PRIMARY_SETTING)
        self.click(self.SELECT_PRIMARY_SETTING)
        DatePicker(self.driver).set_date(
            "(//button[@aria-label='Open calendar'])[1]", self._applied_from
        )
        self.click(self.SAVE_BTN)
        self.sleep(5)
        self.driver.refresh()
        self.sleep(5)

    # ── Public orchestration ──────────────────────────────────────────────────
    def add_holiday_rules_statutory_mapping(self):
        self.logger.info("=== Add Holiday Rules Statutory Mapping flow started ===")
        # self.open_cgm_executive()
        # self.navigate_to_statutory_mapping()
        self._add_holiday_rules_statutory_mapping()

        self.logger.info("=== Add Holiday Rules Statutory Mapping flow completed ===")

