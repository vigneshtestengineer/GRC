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

LOAN_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Loan_Master_Data.json"
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

try:
    with open(LOAN_MASTER_DATA_FILE, "r", encoding="utf-8") as _f:
        _loan_raw = json.load(_f).get("Loan Master Details", {})
        LOAN_CODE                = _loan_raw.get("Loan_Code", "")
        LOAN_DESCRIPTION         = _loan_raw.get("Loan_Description", "")
        TYPE_OF_CREDIT           = _loan_raw.get("Type_Of_Credit", "")
        INTEREST_APPLICABLE      = _loan_raw.get("Interest_Applicable", "False").strip().lower() == "true"
        PRINCIPAL_LOAN           = _loan_raw.get("Principal_Loan", "")
        INTEREST_LOAN            = _loan_raw.get("Interest_Loan", "")
        INTEREST_TYPE_VALUE      = _loan_raw.get("Type_Of_Interest", "")
        LOAN_INTEREST_PERCENTAGE = _loan_raw.get("Loan_Interest_Percentage", "")
        SBI_PERCENTAGE           = _loan_raw.get("SBI_Percentage", "")
except (FileNotFoundError, json.JSONDecodeError):
    LOAN_CODE = LOAN_DESCRIPTION = TYPE_OF_CREDIT = ""
    INTEREST_APPLICABLE = False
    PRINCIPAL_LOAN = INTEREST_LOAN = INTEREST_TYPE_VALUE = ""
    LOAN_INTEREST_PERCENTAGE = SBI_PERCENTAGE = ""


class LoanMaster(BasePage):
    """Page object for Loan Master."""

    # ── CGM Executive navigation ──────────────────────────────────────────────
    MENU_BUTTON                = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXEC_CARD   = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    EXECUTIVE_URL              = "http://13.203.6.58:5002/#/home/welcome"
    SPLASH_SCREEN              = (By.TAG_NAME, "compfie-splash-screen")
    SEARCH_LEGAL_ENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGAL_ENTITY_ROW    = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGAL_ENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Sidebar navigation ────────────────────────────────────────────────────
    OPEN_PAYROLL_MASTER_MENU = (By.XPATH, "//span[contains(text(),'Payroll Master(s)')]")
    CLICK_LOAN_MASTER_MENU = (By.XPATH,"//a[contains(@href,'loan-master')]")

    #------------COMMON LOCATORS------------------
    DROPDOWN_SEARCH          = (By.XPATH, "//input[@aria-label='dropdown search']")
    SELECT_DROPDOWN_DATA     = (By.XPATH, "(//mat-option//span[contains(@class,'mat-option-text')])[2]")

    # ── LOAN MASTER page ────────────────────────────────────────────
    ADD_LOAN_MASTER_BTN  =(By.XPATH,"//button[contains(.,'Add')]")
    UNIT_DROPDOWN            = (By.XPATH, "(//mat-select[@role='combobox'])[1]")
    CONTRACTOR_DROPDOWN      = (By.XPATH,"(//mat-select[@role='combobox'])[2]")

    #--------LOAN MASTER DETAILS LOCATORS---------------------------

    LOAN_CODE =(By.XPATH,"//input[@autocomplete='off' and @maxlength='10']")
    LOAN_DESCRIPTION =(By.XPATH,"//input[@autocomplete='off' and @maxlength='50']")
    INTEREST_PERCENTAGE =(By.XPATH,"//input[contains(@class,'mat-input-element') and contains(@class,'font-medium')]")
    TYPE_OF_CREDIT_DROPDOWN =(By.XPATH,"//span[contains(text(),'Choose Type of Credit')]")
    INTEREST_APPLICABLE_CHECKBOX =(By.XPATH,"//mat-checkbox[contains(.,'Interest Applicable')]//label")
    PRINCIPAL_MATCHING_COMPONENT_DROPDOWN =(By.XPATH,"//span[contains(text(),'Principal Matching Component')]")
    INTEREST_MATCHING_COMPONENT =(By.XPATH,"//span[contains(text(),'Interest Matching Component')]")
    TYPE_OF_INTEREST =(By.XPATH,"//span[contains(text(),'Type of Interest')]")
    SELECT_INTEREST_TYPE =(By.XPATH,f"//mat-option//span[contains(@class,'mat-option-text') and normalize-space()='{INTEREST_TYPE_VALUE}']")
    SBI_INTEREST_RATE =(By.XPATH,"//input[@autocomplete='off' and @maxlength='5']")
    DEDUCT_PRINCIPAL_FROM_FIRST_MONTH_CHECKBOX =(By.XPATH,"//mat-checkbox[contains(.,'Deduct Principal From First Month')]//label")
    #----------SAVE LOAN MASTER-------------------------------------

    SAVE_LOAN_MASTER =(By.XPATH,"//button[contains(.,'Submit as save')]")


    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("WeeklyHolidayMaster page initialized.")
        self.unit_master_data  = UNIT_MASTER_DATA
        self.Unit_Details      = self.unit_master_data.get("Unit_Details", {})
        self.date_of_creation  = self.Unit_Details.get("Date_of_Creation", "")

    # ── CGM Executive: open via app-switcher ─────────────────────────────────
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

    # # ── Step 1: Expand Payroll Master menu ────────────────────────────────
    # def general_master_menu(self):
    #     self.scroll_to_element(self.OPEN_PAYROLL_MASTER_MENU)
    #     self.sleep(0.3)
    #     parent_el = self.find_element(self.OPEN_PAYROLL_MASTER_MENU)
    #     self.driver.execute_script("arguments[0].click();", parent_el)
    #     self.logger.info("Clicked General Master(s) menu.")


    # ── Step 2: Fill and save Loan Master form ───────────────────────────────
    def loan_master(self):

        self.click(self.CLICK_LOAN_MASTER_MENU)
        self.click(self.ADD_LOAN_MASTER_BTN)
        self.click(self.UNIT_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, self._get_unit_name())
        self.click(self.SELECT_DROPDOWN_DATA)
        self.click(self.CONTRACTOR_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, self._get_contractor_name())
        self.click(self.SELECT_DROPDOWN_DATA)
        self.sleep(0.5)
        self.enter_text(self.LOAN_CODE, LOAN_CODE)
        self.enter_text(self.LOAN_DESCRIPTION, LOAN_DESCRIPTION)
        # Select Type of Credit
        self.click(self.TYPE_OF_CREDIT_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, TYPE_OF_CREDIT)
        self.click(self.SELECT_DROPDOWN_DATA)
        # Select Interest Applicable
        self.click(self.INTEREST_APPLICABLE_CHECKBOX)
        # Select Principal component (always required)
        self.click(self.PRINCIPAL_MATCHING_COMPONENT_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, PRINCIPAL_LOAN)
        self.click(self.SELECT_DROPDOWN_DATA)
        self.sleep(1)
        self.click(self.INTEREST_MATCHING_COMPONENT)
        self.enter_text(self.DROPDOWN_SEARCH, INTEREST_LOAN)
        self.click(self.SELECT_DROPDOWN_DATA)
        self.click(self.TYPE_OF_INTEREST)
        self.click(self.SELECT_INTEREST_TYPE)
        self.enter_text(self.INTEREST_PERCENTAGE, LOAN_INTEREST_PERCENTAGE)
        self.click(self.DEDUCT_PRINCIPAL_FROM_FIRST_MONTH_CHECKBOX)
        self.enter_text(self.SBI_INTEREST_RATE, SBI_PERCENTAGE)
        self.sleep(0.5)
        self.click(self.SAVE_LOAN_MASTER)
        self.sleep(5)
        self.driver.refresh()
        self.sleep(1)
        self.logger.info("Loan Master form filled and submitted.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def navigate_to_weekly_holiday_master(self):
        # self.open_cgm_executive()
        # self.general_master_menu()
        self.loan_master()
        self.logger.info("✓ Weekly Holiday Master completed.")

    # ── Helper ────────────────────────────────────────────────────────────────
    def _get_unit_name(self) -> str:
        try:
            with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("Unit_Details", {}).get("unit_name", UNIT_NAME)
        except Exception:
            return UNIT_NAME

    def _get_contractor_name(self) -> str:
        try:
            with open(CONTRACTOR_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("Contractor_Information", {}).get("Contractor_Name", CONTRACTOR_NAME)
        except Exception:
            return CONTRACTOR_NAME