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

CONTRACTOR_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Contractor_Master_Data.json"
)
UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)
WORK_ORDER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Work_Order_Data.json"
)


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class WorkOrderMaster(BasePage):

    # ── CGM Navigation ────────────────────────────────────────────────────────
    # MENU_BUTTON                = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    # GENERAL_MASTER_EXEC_CARD   = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    # EXECUTIVE_URL              = "http://13.203.6.58:5002/#/home/welcome"
    # SEARCH_LEGAL_ENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    # SELECT_LEGAL_ENTITY_ROW    = (By.XPATH, "//table//tbody//tr[1]//td")
    # SELECT_LEGAL_ENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Sidebar ───────────────────────────────────────────────────────────────
    # OPEN_GENERAL_MASTER_MENU     = (By.XPATH, "//span[normalize-space()='General Master(s)']")
    CLICK_WORK_ORDER_MASTER_MENU = (By.XPATH, "//span[normalize-space()='Work Order Master']")

    # ── Work Order Master form ────────────────────────────────────────────────
    SPLASH_SCREEN_OVERLAY      = (By.TAG_NAME, "compfie-splash-screen")
    ADD_WORK_ORDER_BTN         = (By.XPATH, "//button[.//span[contains(@class,'mat-button-wrapper') and contains(normalize-space(),'Add')]]")
    CLICK_UNIT_DROPDOWN        = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    DROPDOWN_SEARCH            = (By.XPATH, "//input[@aria-label='dropdown search']")
    SELECT_DROPDOWN_OPTION     = (By.XPATH, "(//mat-option[@role='option'])[2]")
    # Workorder master Basic Information
    CLICK_CATEGORY_OF_WORKORDER_DROPDOWN = (By.XPATH, "//span[contains(text(),'Category of Work Order')]")
    ENTER_WORKORDER_NUMBER = (By.XPATH, "(//input[contains(@class,'mat-input-element')])[1]")
    ENTER_WORKORDER_STRENGTH = (By.XPATH, "//div[contains(@class,'mat-form-field-infix')]//input[@maxlength='8']")
    ENTER_WORKORDER_VALUE = (By.XPATH, "//mat-label[contains(.,'Work Order Value')]/ancestor::div[contains(@class,'mat-form-field-infix')]//input")
    CLICK_WORKORDER_TYPE_DROPDOWN = (By.XPATH, "//div[contains(@class,'mat-select-value')]//span[contains(text(),'Choose Work Order Type')]")
    SELECT_WORKORDER_TYPE = (By.XPATH, "//mat-option//span[normalize-space()='Permanent']")
    ENTER_WORKORDER_DESCRIPTION = (By.XPATH, "//mat-form-field[.//mat-label[contains(.,'Work Order Description')]]//input")
    OPEN_LIST_OF_CONTRACTORS = (By.XPATH, "//p[normalize-space()='List of Contractor(s)']")
    CLICK_CONTRACTOR_DROPDOWN = (By.XPATH, "//mat-select[.//span[normalize-space()='Choose Contractor']]")
    SELECT_CONTRACTOR = None
    ENTER_WORKORDER_STRENGTH_VALUE = (By.XPATH, "//input[@placeholder='Value']")


    # Workorder master Statutory Information
    STATUTORY_INFO_TAB         = (By.XPATH, "//span[normalize-space()='STATUTORY INFORMATION']")
    CLICK_WAGE_TYPE_DROPDOWN = (By.XPATH, "//mat-select[@placeholder='Choose Wage Type']")
    SELECT_WAGE_TYPE = (By.XPATH, "//span[contains(text(),'Monthly Wage')]")
    CLICK_WAGE_BASED_ON_DROPDOWN = (By.XPATH, "//mat-select[.//span[normalize-space()='Choose Wage based on']]")
    SELECT_WAGE_BASED_ON = (By.XPATH, "//span[contains(text(),'Skill')]")
    CLICK_WAGE_DISTRIBUTION_BASED_ON_DROPDOWN = (By.XPATH, "(//div[contains(@class,'mat-select-value')])[6]")
    SELECT_WAGE_DISTRIBUTION_BASED_ON = (By.XPATH, "//mat-option//span[normalize-space()='Skill']")
    SAVE_BTN                   = (By.XPATH, "//button[.//span[normalize-space()='Submit as save']]")

    def __init__(self, driver):
        super().__init__(driver)
        self._contractor_data = _load_json(CONTRACTOR_DATA_FILE)
        self._unit_data       = _load_json(UNIT_MASTER_DATA_FILE)
        self._workorder_data  = _load_json(WORK_ORDER_DATA_FILE)
        self._ci  = self._contractor_data.get("Contractor_Information", {})
        self._si  = self._contractor_data.get("Statutory_Information", {})
        self._basic_information = self._workorder_data.get("Basic Information", {})
        self._statutory_information = self._workorder_data.get("STATUTORY INFORMATION", {})
        self._unit_name = self._unit_data.get("Unit_Details", {}).get("unit_name", "")
        _ura = self._unit_data.get("Unit_Rights_Allocation", {})
        self._cgm_exe   = _ura.get("CGM_EXE", "")
        self._cgm_admin = _ura.get("CGM_ADMIN", "")

        work_order_number = self.generate_work_order_number()
        self._basic_information["Work Order Number"] = work_order_number
        self.save_json_value(WORK_ORDER_DATA_FILE, "Basic Information", "Work Order Number", work_order_number)

        contractor_name       = self._ci.get("Contractor_Name", "") or self.generate_contractor_name()
        contractor_code       = self._ci.get("Contractor_Code", "") or self.generate_contractor_code()
        contractor_short_name = self._ci.get("Contractor_Short_Name", "") or self.generate_contractor_short_name()
        pf_code = self._si.get("PF_CODE", "") or self.generate_contractor_PF_code()
        esi_code = self._si.get("ESI_CODE", "") or self.generate_contractor_ESI_code()

        self._ci["Contractor_Name"]       = contractor_name
        self._ci["Contractor_Code"]       = contractor_code
        self._ci["Contractor_Short_Name"] = contractor_short_name
        self._si["PF_CODE"] = pf_code
        self._si["ESI_CODE"] = esi_code

        self.SELECT_CONTRACTOR = (
            By.XPATH,
            f"//mat-option//span[contains(text(),\"{self._ci.get('Contractor_Name', '')}\")]"
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

    # ── Step 1: Navigate to Work Order Master ─────────────────────────────────
    def navigate_to_workorder_master(self):
        # self.scroll_to_element(self.OPEN_GENERAL_MASTER_MENU)
        # self.sleep(0.3)
        # parent_el = self.find_element(self.OPEN_GENERAL_MASTER_MENU)
        # self.driver.execute_script("arguments[0].click();", parent_el)
        # self.logger.info("Clicked General Master(s) menu.")

        self.click(self.CLICK_WORK_ORDER_MASTER_MENU, timeout=10)
        self.logger.info("Navigated to Work Order Master.")
        self.click(self.ADD_WORK_ORDER_BTN, timeout=20)
        self.sleep(0.5)

    # ── Step 3: Select unit ───────────────────────────────────────────────────
    def _select_unit(self):
        self.click(self.CLICK_UNIT_DROPDOWN, timeout=10)
        self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
        self.enter_text(self.DROPDOWN_SEARCH, self._unit_name)
        self.sleep(0.5)
        self.click(
            (By.XPATH, f"//mat-option//span[contains(text(),'{self._unit_name}')]"),
            timeout=8,
        )
        self.logger.info("Unit selected: '%s'", self._unit_name)

    # ── Step 4: Fill Basic Information ───────────────────────────────────
    def fill_basic_information(self):
        category = self._basic_information.get("Category", "")
        workorder_number = self._basic_information.get("Work Order Number", "")
        workorder_strength = self._basic_information.get("Work Order strength", "")
        workorder_value = self._basic_information.get("Work Order Value", "")
        workorder_type = self._basic_information.get("Work Order Type", "")
        description = self._basic_information.get("Description", "")
        effective_from = self._basic_information.get("Effective FROM", "")

        self.logger.info(
            "Filling Basic Information — category: '%s', number: '%s', strength: '%s', value: '%s', type: '%s'",
            category, workorder_number, workorder_strength, workorder_value, workorder_type
        )

        self.click(self.CLICK_CATEGORY_OF_WORKORDER_DROPDOWN, timeout=10)
        if category:
            self.click((By.XPATH, f"//mat-option//span[normalize-space()='{category}']"), timeout=8)
            self.logger.info("Category selected: '%s'", category)
        
        self.enter_text(self.ENTER_WORKORDER_NUMBER, workorder_number)
        self.logger.info("Work Order Number entered: '%s'", workorder_number)
        
        self.enter_text(self.ENTER_WORKORDER_STRENGTH, workorder_strength)
        self.logger.info("Work Order Strength entered: '%s'", workorder_strength)
        
        self.enter_text(self.ENTER_WORKORDER_VALUE, workorder_value)
        self.logger.info("Work Order Value entered: '%s'", workorder_value)
        
        self.click(self.CLICK_WORKORDER_TYPE_DROPDOWN, timeout=10)
        if workorder_type:
            self.click((By.XPATH, f"//mat-option//span[normalize-space()='{workorder_type}']"), timeout=8)
            self.logger.info("Work Order Type selected: '%s'", workorder_type)
        
        self.enter_text(self.ENTER_WORKORDER_DESCRIPTION, description)
        self.logger.info("Description entered: '%s'", description)
        
        if effective_from:
            DatePicker(self.driver).set_date(
                "(//button[@aria-label='Open calendar'])[1]", effective_from
            )
            self.logger.info("Effective From date set: '%s'", effective_from)
        
        self.click(self.OPEN_LIST_OF_CONTRACTORS, timeout=10)
        self.logger.info("List of Contractors section opened.")
        
        self.click(self.CLICK_CONTRACTOR_DROPDOWN, timeout=10)
        self.click(self.SELECT_CONTRACTOR, timeout=8)
        self.logger.info("Contractor selected: '%s'", self._ci.get('Contractor_Name', 'Unknown'))
        
        self.enter_text(self.ENTER_WORKORDER_STRENGTH_VALUE, workorder_strength)
        self.logger.info("Contractor strength value entered: '%s'", workorder_strength)
        
        self.logger.info("Basic Information filled successfully.")
        self.sleep(2)
    # ── Step 5: Fill Statutory Information ───────────────────────────────────
    def fill_workorder_statutory_information(self):
        wage_type = self._statutory_information.get("Wage Type", "")
        wage_based_on = self._statutory_information.get("Wage Based on", "")
        wage_distribution_based_on = self._statutory_information.get("Wage Distribution based on", "")

        self.logger.info(
            "Filling Statutory Information — wage_type: '%s', wage_based_on: '%s', wage_distribution_based_on: '%s'",
            wage_type, wage_based_on, wage_distribution_based_on
        )

        self.click(self.STATUTORY_INFO_TAB, timeout=10)
        self.logger.info("Statutory Information tab opened.")
        
        self.click(self.CLICK_CONTRACTOR_DROPDOWN, timeout=10)
        self.click(self.SELECT_CONTRACTOR, timeout=8)
        self.logger.info("Contractor selected in Statutory tab: '%s'", self._ci.get('Contractor_Name', 'Unknown'))
        
        self.click(self.CLICK_WAGE_TYPE_DROPDOWN, timeout=10)
        if wage_type:
            self.click((By.XPATH, f"//mat-option//span[normalize-space()='{wage_type}']"), timeout=8)
            self.logger.info("Wage Type selected: '%s'", wage_type)
        
        self.click(self.CLICK_WAGE_BASED_ON_DROPDOWN, timeout=10)
        if wage_based_on:
            self.click((By.XPATH, f"//mat-option//span[normalize-space()='{wage_based_on}']"), timeout=8)
            self.logger.info("Wage Based On selected: '%s'", wage_based_on)
        
        self.click(self.CLICK_WAGE_DISTRIBUTION_BASED_ON_DROPDOWN, timeout=10)
        if wage_distribution_based_on:
            self.click((By.XPATH, f"//mat-option//span[normalize-space()='{wage_distribution_based_on}']"), timeout=8)
            self.logger.info("Wage Distribution Based On selected: '%s'", wage_distribution_based_on)
        
        self.click(self.SAVE_BTN, timeout=10)
        self.click(self.SAVE_BTN, timeout=10)  # Click twice to ensure save action is triggered
        self.logger.info("Save button clicked.")
        
        self.logger.info("Statutory Information filled successfully.")
        self.sleep(2)
        self.logger.info("Refreshing page...")
        self.driver.refresh()
        self.sleep(5)
        self.logger.info("Page refreshed after Work Order Master creation.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def add_workorder_master(self):
        self.logger.info("=== Add Work Order Master flow started ===")
        # self.open_cgm_executive()
        self.navigate_to_workorder_master()
        self._select_unit()
        self.fill_basic_information()
        self.fill_workorder_statutory_information()
        self.logger.info("=== Add Work Order Master flow completed ===")
