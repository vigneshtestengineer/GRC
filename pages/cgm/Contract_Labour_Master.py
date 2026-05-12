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

LEGAL_ENTITY = get_str("auth", "legal_entity", "")

CONTRACT_LABOUR_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Contract_Labour_Data.json"
)
CONTRACTOR_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Contractor_Master_Data.json"
)
UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class ContractLabourMaster(BasePage):

    # ── CGM Navigation ────────────────────────────────────────────────────────
    MENU_BUTTON                = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXEC_CARD   = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    EXECUTIVE_URL              = "http://13.203.6.58:5002/#/home/welcome"
    SEARCH_LEGAL_ENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGAL_ENTITY_ROW    = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGAL_ENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Sidebar ───────────────────────────────────────────────────────────────
    OPEN_GENERAL_MASTER_MENU     = (By.XPATH, "//span[normalize-space()='General Master(s)']")
    CLICK_CONTRACTOR_LABOUR_MENU = (By.XPATH, "//a[@href='#/general-master/contract-labour-master']")

    # ── Contractor Master form ────────────────────────────────────────────────
    SPLASH_SCREEN_OVERLAY      = (By.TAG_NAME, "compfie-splash-screen")
    ADD_CONTRACTOR_LABOUR_BTN  = (By.XPATH, "//button[.//span[contains(@class,'mat-button-wrapper') and contains(normalize-space(),'Add')]]")
    CLICK_UNIT_DROPDOWN        = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    DROPDOWN_SEARCH            = (By.XPATH, "//input[@aria-label='dropdown search']")
    SELECT_DROPDOWN_SEARCHED_DATA = (By.XPATH, "(//mat-option[contains(@class,'mat-option')])[2]")
    CLICK_CONTRACTOR_DROPDOWN  = (By.XPATH, "//span[normalize-space()='Contractor']")
    CLICK_SHOW_DETAILS         = (By.XPATH, "//button[.//mat-icon[normalize-space()='sort'] and .//span[contains(.,'Show Detail')]]")

    # Contractor Information
    ENTER_CONTRACTOR_LABOUR_CODE = (By.XPATH, "//input[@maxlength='50']")
    ENTER_CONTRACTOR_LABOUR_NAME      = (By.XPATH, "(//input[@maxlength='150'])[1]")
    CHOOSE_GENDER_DROPDOWN       = (By.XPATH, "//span[text()='Choose Gender']")
    FATHERS_NAME               = (By.XPATH, "(//input[@maxlength='150'])[2]")
    ENTER_ADDRESS_1            = (By.XPATH, "(//textarea[@maxlength='450'])[1]")
    CLICK_STATE_DROPDOWN       = (By.XPATH, "(//span[normalize-space()='Choose State'])[1]")
    CLICK_CITY_DROPDOWN        = (By.XPATH, "(//span[normalize-space()='Choose City'])[1]")
    ENTER_PINCODE              = (By.XPATH, "(//input[@maxlength='6'])[1]")
    DESIGNATION_DROPDOWN       = (By.XPATH, "//span[normalize-space()='Choose Designation']")
    DEPARTMENT_DROPDOWN         = (By.XPATH, "//span[normalize-space()='Choose Department']")
    SKILL_DROPDOWN              = (By.XPATH, "//span[normalize-space()='Choose skill']")
    CATEGORY_DROPDOWN           = (By.XPATH, "//span[normalize-space()='Choose category']")
    UAN_NUMBER                   = (By.XPATH, "//input[@name='uanNo']")

    SAVE_BTN                   = (By.XPATH, "//button[.//span[normalize-space()='Submit as save']]")

    def __init__(self, driver):
        super().__init__(driver)
        _labour_data     = _load_json(CONTRACT_LABOUR_DATA_FILE)
        _contractor_data = _load_json(CONTRACTOR_MASTER_DATA_FILE)
        _unit_data       = _load_json(UNIT_MASTER_DATA_FILE)

        personal          = _labour_data.get("Personal_Details", {})
        professional      = _labour_data.get("Professional_Details", {})
        contractor_info   = _contractor_data.get("Contractor_Information", {})
        unit_details      = _unit_data.get("Unit_Details", {})

        self._unit_name        = unit_details.get("unit_name", "")
        self._contractor_name  = contractor_info.get("Contractor_Name", "")
        self._contractor_code  = self.generate_contract_labour_code(
            CONTRACT_LABOUR_DATA_FILE, CONTRACTOR_MASTER_DATA_FILE
        )
        self._labour_name, self._gender = self.generate_labour_name(CONTRACT_LABOUR_DATA_FILE)
        self._fathers_name     = personal.get("Father_Name", "")
        self._address          = personal.get("Address", "")
        self._state            = personal.get("State", "")
        self._city             = personal.get("City", "")
        self._pincode          = personal.get("Pin_Code", "")
        self._designation      = professional.get("Designation", "")
        self._department       = professional.get("Department", "")
        self._skill            = professional.get("Skill", "")
        self._category         = professional.get("Category", "")
        self._date_of_joining  = professional.get("Date_of_Joining", "")
        self._uan_number       = self.generate_uan_number(CONTRACT_LABOUR_DATA_FILE)
        self._date_of_birth     = personal.get("Date_of_Birth", "")


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

    # ── Step 1: Navigate to Contractor Labour Master ─────────────────────────────────

    def navigate_to_contractor_labour_master(self):
        # self.scroll_to_element(self.OPEN_GENERAL_MASTER_MENU)
        # self.sleep(0.3)
        # parent_el = self.find_element(self.OPEN_GENERAL_MASTER_MENU)
        # self.driver.execute_script("arguments[0].click();", parent_el)
        # self.logger.info("Expanded General Master(s) menu.")
        self.wait_for_element(self.CLICK_CONTRACTOR_LABOUR_MENU, timeout=8)
        menu_el = self.find_element(self.CLICK_CONTRACTOR_LABOUR_MENU)
        self.driver.execute_script("arguments[0].click();", menu_el)
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN_OVERLAY, timeout=15)
        self.click(self.ADD_CONTRACTOR_LABOUR_BTN, timeout=20)
        self.logger.info("Navigated to Contractor Labour Master.")

    # ── Step 3: Select unit ───────────────────────────────────────────────────
    def _select_unit_and_contractor(self):
        self.click(self.CLICK_UNIT_DROPDOWN, timeout=10)
        self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
        self.enter_text(self.DROPDOWN_SEARCH, self._unit_name)
        self.sleep(0.5)
        self.click(self.SELECT_DROPDOWN_SEARCHED_DATA)
        self.logger.info("Unit selected: '%s'", self._unit_name)
        self.click(self.CLICK_CONTRACTOR_DROPDOWN, timeout=10)
        self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
        self.enter_text(self.DROPDOWN_SEARCH, self._contractor_name)
        self.sleep(0.5)
        self.click(self.SELECT_DROPDOWN_SEARCHED_DATA)

    # ── Step 4: Fill Contractor Information ───────────────────────────────────
    def fill_contract_labour_information(self):
        self.enter_text(self.ENTER_CONTRACTOR_LABOUR_CODE, self._contractor_code)
        self.enter_text(self.ENTER_CONTRACTOR_LABOUR_NAME, self._labour_name)
        self.click(self.CHOOSE_GENDER_DROPDOWN)
        self.click((By.XPATH, f"//mat-option[.//span[normalize-space()='{self._gender}']]"))
        self.enter_text(self.FATHERS_NAME, self._fathers_name)
        self.enter_text(self.ENTER_ADDRESS_1, self._address)
        DatePicker(self.driver).set_date(
            "(//button[@aria-label='Open calendar'])[1]", self._date_of_birth
        )
        self.click(self.CLICK_STATE_DROPDOWN)
        self.click((By.XPATH, f"//mat-option//span[contains(text(),'{self._state}')]"))
        self.click(self.CLICK_CITY_DROPDOWN)
        self.click((By.XPATH, f"//mat-option//span[contains(text(),'{self._city}')]"))
        self.enter_text(self.ENTER_PINCODE, self._pincode)
        self.click(self.DESIGNATION_DROPDOWN)
        self.click((By.XPATH, f"//mat-option//span[contains(text(),'{self._designation}')]"))
        self.click(self.DEPARTMENT_DROPDOWN)
        self.click((By.XPATH, f"//mat-option//span[contains(text(),'{self._department}')]"))
        self.click(self.SKILL_DROPDOWN)
        self.click((By.XPATH, f"//mat-option//span[contains(text(),'{self._skill}')]"))
        self.click(self.CATEGORY_DROPDOWN)
        self.click((By.XPATH, f"//mat-option//span[contains(text(),'{self._category}')]"))
        DatePicker(self.driver).set_date(
            "(//button[@aria-label='Open calendar'])[2]", self._date_of_joining
        )
        self.enter_text(self.UAN_NUMBER, self._uan_number)
        self.logger.info("Filled contractor labour information for '%s'.", self._labour_name)
        self.click(self.SAVE_BTN)
        self.logger.info("Contractor labour information submitted for '%s'.", self._labour_name)
        self.sleep(5)
        self.driver.refresh()
        self.sleep(5)

    # ── Public orchestration ──────────────────────────────────────────────────
    def add_contract_labour_master(self):
        self.logger.info("=== Add Contract Labour Master flow started ===")
        # self.open_cgm_executive()
        self.navigate_to_contractor_labour_master()
        self._select_unit_and_contractor()
        self.click(self.CLICK_SHOW_DETAILS, timeout=10)
        self.fill_contract_labour_information()
        self.logger.info("=== Add Contract Labour Master flow completed ===")

