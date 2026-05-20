from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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

PAY_COMPONENT_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Pay_Component_Data.json"
)


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


UNIT_NAME       = _load_json(UNIT_MASTER_DATA_FILE).get("Unit_Details", {}).get("unit_name", "")
CONTRACTOR_NAME = _load_json(CONTRACTOR_DATA_FILE).get("Contractor_Information", {}).get("Contractor_Name", "")

_pay_data      = _load_json(PAY_COMPONENT_DATA_FILE)
_basic_details = _pay_data.get("Basic Details", {})
_fixed         = _pay_data.get("Fixed components", {})
_earned        = _pay_data.get("Earned components", {})
_monthly       = _pay_data.get("Monthly Components", {})
_arrear        = _pay_data.get("Arrear Components", {})
_days          = _pay_data.get("Days Matching Components", {})
_loan          = _pay_data.get("Loan Components", {})
_rounding      = _pay_data.get("Rounding Method", {})

_CTC_APPLICABILITY_TEXT      = _basic_details.get("Payroll Applicability CTC",      "Include for CTC")
_GROSS_APPLICABILITY_TEXT    = _basic_details.get("Payroll Applicability Gross",   "Include for Gross Earnings")
_TAXABLE_COMPONENT_TEXT      = _basic_details.get("Payroll Applicability Taxable", "Taxable Component")
_ARREAR_COMPONENT_TEXT       = _basic_details.get("Arrear Components", "Arrear Component (Pay Revisions)")
_FIXED_BASIC_TEXT            = _fixed.get("Basic",          "FD Basic")
_FIXED_HRA_TEXT              = _fixed.get("HRA",            "FD HRA")
_FIXED_DA_TEXT               = _fixed.get("DA",             "DA")
_FIXED_BEHAVIOUR_TYPE_TEXT   = _fixed.get("Behaviour Type", "Direct Input")
_EARNED_BASIC_TEXT           = _earned.get("Earned Basic",  "Earn Basic")
_EARNED_HRA_TEXT             = _earned.get("Earned HRA",    "Earned HRA")
_EARNED_DA_TEXT              = _earned.get("Earned DA",     "Earned DA")
_EARNED_BEHAVIOUR_TYPE_TEXT  = _earned.get("Behaviour Type","Percentage-Field")
_PAYROLL_BASED_ON            = _earned.get("Payroll_Based_On", "Work Days")
_MONTHLY_INCENTIVE_TEXT      = _monthly.get("Incentive",    "Incentive")
_MONTHLY_BEHAVIOUR_TYPE_TEXT = _monthly.get("Behaviour Type","Direct Input")
_ARREAR_BASIC_TEXT           = _arrear.get("Arrear Basic",  "Arrear Basic")
_ARREAR_HRA_TEXT             = _arrear.get("Arrear HRA",    "Arrear HRA")
_ARREAR_DA_TEXT              = _arrear.get("Arrear DA",     "Arrear DA Component")
_ARREAR_BEHAVIOUR_TYPE_TEXT  = _arrear.get("Behaviour Type","Direct Input")
_DAYS_MONTH_DAYS_TEXT        = _days.get("Month Days",      "Month Days")
_DAYS_PAID_DAYS_TEXT         = _days.get("Paid Days",       "Paid Days")
_DAYS_WORKED_DAYS_TEXT       = _days.get("Worked Days",     "Worked Days")
_DAYS_LOP_TEXT               = _days.get("LOP Days",        "LOP")
_DAYS_BEHAVIOUR_TYPE_TEXT    = _days.get("Behaviour Type",  "Days Matching-Field")
_LOAN_TEXT                   = _loan.get("Loan",            "EDU Loan")
_LOAN_INTEREST_TEXT          = _loan.get("Loan Interest",   "EDU LOANINT")
_LOAN_BEHAVIOUR_TYPE_TEXT    = _loan.get("Behaviour Type",  "Direct Input")
_ROUNDING_METHOD_TEXT        = _rounding.get("Rounding Method", "Normal")


class PayComponentMapping(BasePage):
    """Page object for Pay Component Mapping under Payroll Master(s)."""

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

    # ── Pay component mapping page ────────────────────────────────────────────
    CLICK_PAY_COMPONENT_MAPPING = (By.XPATH, "//a[contains(@href,'pay-component-mapping')]")
    ADD_PAY_COMPONENT_BUTTON = (By.XPATH, "//button[contains(.,'Add')]")
    UNIT_DROPDOWN            = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    DROPDOWN_SEARCH          = (By.XPATH, "//input[@aria-label='dropdown search']")
    SELECT_DROPDOWN_DATA      = (By.XPATH, "(//mat-option[contains(@class,'mat-option')])[2]")
    CONTRACTOR_DROPDOWN        = (By.XPATH, "(//mat-select[@role='combobox'])[2]")
    CLICK_EFFECTIVE_MONTH_DROPDOWN = (By.XPATH, "(//div[contains(@class,'mat-select-value')])[3]")
    ENTER_EFFECTIVE_YEAR = (By.XPATH, "//input[@id='mat-input-2']")
    CLICK_SHOW_DETAILS_BUTTON = (By.XPATH, "//button[@type='button' and .//span[contains(text(),'Show Detail')]]")

    # Mapping the Pay components Locators
    
    #---------------------------Components Loactors---------------------------
    CLICK_MORE_OPTION = (By.XPATH, "(//button[contains(@class,'mat-menu-trigger')])[2]")
    EDIT_COMPONENT = (By.XPATH, "//button[@role='menuitem' and .//span[contains(text(),'Edit')]]")

    #---------------------------Edit Component Locators---------------------------
    CLICK_BEHAVIOUR_TYPE_DROPDOWN = (By.XPATH, "//span[contains(text(),'Choose Behaviour Type')]")
    ENTER_DECIMAL_NUMBER = (By.XPATH, "(//input[@maxlength='1' and @autocomplete='off'])[1]")
    ENTER_ORDER_NUMBER = (By.XPATH, "(//input[contains(@class,'mat-input-element')])[6]")
    CLICK_ROUNDING_MODE_DROPDOWN = (By.XPATH, "//span[contains(text(),'Rounding Mode')]")
    CLICK_WAGE_DEFINITION_DROPDOWN = (By.XPATH, "//mat-select[@placeholder='Choose Wage Definition']")
    SELECT_WAGE_DEFINITION = (By.XPATH, "//mat-option//span[normalize-space()='Inclusive']")
    CLICK_COMPONENT_TYPE_DROPDOWN = (By.XPATH, "//mat-select[@placeholder='Choose Component Type']")
    SELECT_COMPONENT_TYPE = (By.XPATH, "//mat-option//span[normalize-space()='Basic Salary']")
    SELECT_FIXED_COMPONENT_CHECKBOX = (By.XPATH, "//mat-checkbox[.//span[contains(normalize-space(),'Fixed Earning Component')]]")
    SELECT_STATIC_VALUE_BTN = (By.XPATH, "//button[.//span[normalize-space()='Static Value Component']]")
    SELECT_INDIVIDUAL_WISE_BTN = (By.XPATH, "//span[normalize-space()='Individual Wise']")
    SAVE_COMPONENT_BUTTON = (By.XPATH, "//button[.//span[contains(normalize-space(),'Save & Close')]]")
    PAYROLL_APPLICABILITY_DROPDOWN = (By.XPATH, "//mat-panel-title[contains(normalize-space(),'Payroll Applicability')]")
    SELECT_CTC_APPLICABILITY   = (By.XPATH, f"//tr[.//td[contains(normalize-space(),'{_CTC_APPLICABILITY_TEXT}')]]//mat-checkbox")
    SELECT_GROSS_APPLICABILITY = (By.XPATH, f"//tr[.//td[contains(normalize-space(),'{_GROSS_APPLICABILITY_TEXT}')]]//mat-checkbox")
    SELECT_TAXABLE_COMPONENT = (By.XPATH, f"//tr[.//td[contains(normalize-space(),'{_TAXABLE_COMPONENT_TEXT}')]]//input[@type='checkbox']")
    SELECT_ARREAR_COMPONENT = (By.XPATH, "//tr[.//td[contains(text(),'Arrear Component (Pay Revisions)')]]//input[@type='checkbox']")
    OPEN_STATUTORY_APPLICABILITY =(By.XPATH,"//mat-panel-title[contains(normalize-space(),'Statutory Applicability')]")
    SELECT_PT_GROSS =(By.XPATH,"//tr[.//td[contains(normalize-space(),'Include for PT Gross')]]//label[contains(@class,'mat-checkbox-layout')]")



    #── Deduction Component Locators ────────────────────────────

    CLICK_DEDUCTION_COMPONENT_PAGE = (By.XPATH, "//span[contains(normalize-space(),'DEDUCTION COMPONENT')]")


    # ── Pay Component Mapping — Component Locators ────────────────────────────

    # ── Fixed Components ─────────────────────────────────────────────────────
    SELECT_FIXED_BASIC             = (By.XPATH, f"//tr[.//span[contains(text(),'{_FIXED_BASIC_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_FIXED_HRA               = (By.XPATH, f"//tr[.//span[contains(text(),'{_FIXED_HRA_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_FIXED_DA                = (By.XPATH, f"//tr[.//span[contains(text(),'{_FIXED_DA_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_FIXED_BEHAVIOUR_TYPE    = (By.XPATH, f"//mat-option[.//span[contains(text(),'{_FIXED_BEHAVIOUR_TYPE_TEXT}')]]")

    # ── Earned Components ────────────────────────────────────────────────────
    SELECT_EARNED_EARNED_BASIC     = (By.XPATH, f"//tr[.//span[contains(text(),'{_EARNED_BASIC_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_EARNED_EARNED_HRA       = (By.XPATH, f"//tr[.//span[contains(text(),'{_EARNED_HRA_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_EARNED_EARNED_DA        = (By.XPATH, f"//tr[.//span[contains(text(),'{_EARNED_DA_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_EARNED_BEHAVIOUR_TYPE   = (By.XPATH, f"//mat-option[.//span[contains(text(),'{_EARNED_BEHAVIOUR_TYPE_TEXT}')]]")
    CLICK_EARNED_COMPONENT_DROPDOWN = (By.XPATH, "//mat-select[@placeholder='Choose Earning Component']")
    SELECT_EARNED_COMPONENT_BASIC  = (By.XPATH, f"//span[@class='mat-option-text' and normalize-space()='{_FIXED_BASIC_TEXT}']")
    SELECT_EARNED_COMPONENT_HRA    = (By.XPATH, f"//span[@class='mat-option-text' and normalize-space()='{_FIXED_HRA_TEXT}']")
    SELECT_EARNED_COMPONENT_DA     = (By.XPATH, f"//span[@class='mat-option-text' and normalize-space()='{_FIXED_DA_TEXT}']")
    CLICK_MULTIPLIER_SYMBOL        = (By.XPATH, "//p[normalize-space()='*']")
    DAY_MATCHING_DROPDOWN          = (By.XPATH, "//span[contains(@class,'mat-select-placeholder') and normalize-space()='Choose Day(s) Matching Field']")
    SELECT_DAY_MATCHING            = (By.XPATH, f"//span[@class='mat-option-text' and normalize-space()='{_DAYS_WORKED_DAYS_TEXT}']")
    DIVIDE_SYMBOL                  = (By.XPATH, "//p[normalize-space()='/']")
    SELECT_MONTH_DAYS              = (By.XPATH, f"//span[@class='mat-option-text' and normalize-space()='{_DAYS_MONTH_DAYS_TEXT}']")
    SELECT_SUB_SYMBOL              = (By.XPATH,"//div[contains(@class,'cursor-pointer') and .//p[text()='-']]")
    SELECT_OPEN_BRACKET_SYMBOL     = (By.XPATH,"//div[contains(@class,'cursor-pointer') and .//p[text()='(']]")
    SELECT_CLOSE_BRACKET_SYMBOL    = (By.XPATH,"//div[contains(@class,'cursor-pointer') and .//p[text()=')']]")


    @property
    def SELECT_DAY_MATCHING_DYNAMIC(self):
        day_text = _days.get(_PAYROLL_BASED_ON, _PAYROLL_BASED_ON)
        return (By.XPATH, f"//span[@class='mat-option-text' and normalize-space()='{day_text}']")

    # ── Monthly Components ───────────────────────────────────────────────────
    SELECT_MONTHLY_INCENTIVE       = (By.XPATH, f"//tr[.//span[contains(text(),'{_MONTHLY_INCENTIVE_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_MONTHLY_BEHAVIOUR_TYPE  = (By.XPATH, f"//mat-option[.//span[contains(text(),'{_MONTHLY_BEHAVIOUR_TYPE_TEXT}')]]")
    SELECT_MONTHLY_INPUT_CHECKBOX  = (By.XPATH, "//span[@class='mat-button-toggle-label-content' and normalize-space()='Monthly-Input']")
    # ── Arrear Components ────────────────────────────────────────────────────
    SELECT_ARREAR_ARREAR_BASIC     = (By.XPATH, f"//tr[.//span[contains(text(),'{_ARREAR_BASIC_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_ARREAR_ARREAR_HRA       = (By.XPATH, f"//tr[.//span[contains(text(),'{_ARREAR_HRA_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_ARREAR_ARREAR_DA        = (By.XPATH, f"//tr[.//span[contains(text(),'{_ARREAR_DA_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_ARREAR_BEHAVIOUR_TYPE   = (By.XPATH, f"//mat-option[.//span[contains(text(),'{_ARREAR_BEHAVIOUR_TYPE_TEXT}')]]")

    # ── Days Matching Components ─────────────────────────────────────────────
    SELECT_DAYS_MONTH_DAYS         = (By.XPATH, f"//tr[.//span[contains(text(),'{_DAYS_MONTH_DAYS_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_DAYS_PAID_DAYS          = (By.XPATH, f"//tr[.//span[contains(text(),'{_DAYS_PAID_DAYS_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_DAYS_WORKED_DAYS        = (By.XPATH, f"//tr[.//span[contains(text(),'{_DAYS_WORKED_DAYS_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_DAYS_LOP_DAYS           = (By.XPATH, f"//tr[.//span[contains(text(),'{_DAYS_LOP_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_DAYS_BEHAVIOUR_TYPE     = (By.XPATH, f"//mat-option[.//span[contains(text(),'{_DAYS_BEHAVIOUR_TYPE_TEXT}')]]")

    # ── Loan Components ──────────────────────────────────────────────────────
    SELECT_LOAN_LOAN               = (By.XPATH, f"//tr[.//span[contains(text(),'{_LOAN_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_LOAN_LOAN_INTEREST      = (By.XPATH, f"//tr[.//span[contains(text(),'{_LOAN_INTEREST_TEXT}')]]//span[contains(@class,'mat-checkbox-inner-container')]")
    SELECT_LOAN_BEHAVIOUR_TYPE     = (By.XPATH, f"//mat-option[.//span[contains(text(),'{_LOAN_BEHAVIOUR_TYPE_TEXT}')]]")
    SELECT_INCLUDE_FOR_GROSS_DEDUCTION =(By.XPATH,"//tr[.//td[contains(normalize-space(),'Include for Gross Deduction')]]//input[@type='checkbox']")
    # ── Save Pay component mapping locator ───────────────────────────────────────────────────────
    SAVE_PAY_COMPONENT_MAPPING =(By.XPATH,"//button[contains(.,'Submit as save')]")
    SUCCESS_MESSAGE =(By.XPATH,"//div[contains(@class,'compfie-toast-notification-title') and normalize-space()='Success']")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("PayComponentMapping page initialized.")
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

    # ── Step 1: Expand General Master(s) menu ────────────────────────────────
    def general_master_menu(self):
        self.scroll_to_element(self.OPEN_PAYROLL_MASTER_MENU)
        self.sleep(0.3)
        parent_el = self.find_element(self.OPEN_PAYROLL_MASTER_MENU)
        self.driver.execute_script("arguments[0].click();", parent_el)
        self.logger.info("Clicked Payroll Master(s) menu.")
        self.click(self.CLICK_PAY_COMPONENT_MAPPING)
        self.sleep(1)


    # ── Private helpers ───────────────────────────────────────────────────────
    def _setup_mapping_form(self):
        data = self._load_pay_component_data().get("Basic Details", {})
        effective_month = data.get("Effective Month", "")
        effective_year  = data.get("Effective Year",  "")
        self.click(self.ADD_PAY_COMPONENT_BUTTON)
        self.sleep(0.5)
        self.click(self.UNIT_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, self._get_unit_name())
        self.click(self.SELECT_DROPDOWN_DATA)
        self.click(self.CONTRACTOR_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, self._get_contractor_name())
        self.click(self.SELECT_DROPDOWN_DATA)
        self.find_element(self.DROPDOWN_SEARCH).send_keys(Keys.ESCAPE)
        self.driver.execute_script("arguments[0].click();", self.find_element(self.CLICK_EFFECTIVE_MONTH_DROPDOWN))
        self.enter_text(self.DROPDOWN_SEARCH, effective_month)
        self.click(self.SELECT_DROPDOWN_DATA)
        self.enter_text(self.ENTER_EFFECTIVE_YEAR, effective_year)
        self.click(self.CLICK_SHOW_DETAILS_BUTTON)
        NO_RECORDS = (By.XPATH, "//div[contains(normalize-space(),'No records found')]")
        if self.is_element_visible(NO_RECORDS, timeout=3):
            self.logger.info("'No records found' detected — retrying Show Details.")
            self.click(self.CLICK_SHOW_DETAILS_BUTTON)
        self.wait_for_element(self.SELECT_FIXED_BASIC, timeout=15)
        self.logger.info("Mapping form ready — component table loaded.")

    def _load_pay_component_data(self) -> dict:
        try:
            with open(PAY_COMPONENT_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _open_edit_panel(self, select_locator):
        self.click(select_locator)
        self.sleep(0.5)
        try:
            label = select_locator[1].split("contains(text(),'")[1].split("')")[0]
            row_locator  = (By.XPATH, f"//tr[.//span[contains(text(),'{label}')]]")
            more_option  = (By.XPATH, f"//tr[.//span[contains(text(),'{label}')]]//button[contains(@class,'mat-menu-trigger')]")
        except (IndexError, AttributeError):
            row_locator = None
            more_option = self.CLICK_MORE_OPTION
        if row_locator:
            ActionChains(self.driver).move_to_element(self.find_element(row_locator)).perform()
            self.sleep(0.3)
        self.click(more_option)
        self.click(self.EDIT_COMPONENT)
        self.sleep(0.5)

    def _fill_direct_input_fields(self, order: int):
        self.clear_text(self.ENTER_DECIMAL_NUMBER)
        self.enter_text(self.ENTER_DECIMAL_NUMBER, "2")
        self.enter_text(self.ENTER_ORDER_NUMBER, str(order))
        self.click(self.CLICK_ROUNDING_MODE_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, _ROUNDING_METHOD_TEXT)
        self.click(self.SELECT_DROPDOWN_DATA)

    def _edit_fixed_component(self, locator, order: int):
        self._open_edit_panel(locator)
        self.click(self.CLICK_BEHAVIOUR_TYPE_DROPDOWN)
        self.click(self.SELECT_FIXED_BEHAVIOUR_TYPE)
        self._fill_direct_input_fields(order)
        self.click(self.CLICK_WAGE_DEFINITION_DROPDOWN)
        self.click(self.SELECT_WAGE_DEFINITION)
        self.click(self.CLICK_COMPONENT_TYPE_DROPDOWN)
        self.click(self.SELECT_COMPONENT_TYPE)
        self.click(self.SELECT_FIXED_COMPONENT_CHECKBOX)
        self.sleep(0.5)
        self.click(self.SELECT_STATIC_VALUE_BTN)
        self.sleep(0.5)
        self.click(self.SELECT_INDIVIDUAL_WISE_BTN)
        self.click(self.PAYROLL_APPLICABILITY_DROPDOWN)
        self.sleep(0.5)
        self.scroll_to_element(self.SELECT_CTC_APPLICABILITY)
        self.click(self.SELECT_CTC_APPLICABILITY)
        self.sleep(0.5)
        self.click(self.SELECT_GROSS_APPLICABILITY)
        self.sleep(1)
        self.click(self.SELECT_TAXABLE_COMPONENT)
        self.sleep(0.5)
        self.click(self.OPEN_STATUTORY_APPLICABILITY)
        self.sleep(0.5)
        self.click(self.SELECT_PT_GROSS)
        self.click(self.SAVE_COMPONENT_BUTTON)
        self.sleep(2)

    def _edit_monthly_component(self, locator, order: int):
        self._open_edit_panel(locator)
        self.click(self.CLICK_BEHAVIOUR_TYPE_DROPDOWN)
        self.click(self.SELECT_MONTHLY_BEHAVIOUR_TYPE)
        self._fill_direct_input_fields(order)
        self.sleep(0.5)
        self.click(self.SELECT_MONTHLY_INPUT_CHECKBOX)
        self.sleep(0.5)
        self.click(self.PAYROLL_APPLICABILITY_DROPDOWN)
        self.scroll_to_element(self.SELECT_GROSS_APPLICABILITY)
        self.click(self.SELECT_GROSS_APPLICABILITY)
        self.sleep(0.5)
        self.click(self.SAVE_COMPONENT_BUTTON)
        self.sleep(2)

    def _edit_arrear_component(self, locator, order: int):
        self._open_edit_panel(locator)
        self.click(self.CLICK_BEHAVIOUR_TYPE_DROPDOWN)
        self.click(self.SELECT_ARREAR_BEHAVIOUR_TYPE)
        self._fill_direct_input_fields(order)
        self.sleep(0.5)
        self.click(self.CLICK_WAGE_DEFINITION_DROPDOWN)
        self.click(self.SELECT_WAGE_DEFINITION)
        self.click(self.CLICK_COMPONENT_TYPE_DROPDOWN)
        self.click(self.SELECT_COMPONENT_TYPE)
        self.sleep(0.5)
        self.click(self.PAYROLL_APPLICABILITY_DROPDOWN)
        self.scroll_to_element(self.SELECT_ARREAR_COMPONENT)
        self.sleep(0.5)
        self.click(self.SELECT_ARREAR_COMPONENT)
        self.click(self.SELECT_GROSS_APPLICABILITY)
        self.click(self.SELECT_TAXABLE_COMPONENT)
        self.sleep(1)
        self.click(self.OPEN_STATUTORY_APPLICABILITY)
        self.sleep(0.5)
        self.click(self.SELECT_PT_GROSS)
        self.sleep(0.5)
        self.click(self.SAVE_COMPONENT_BUTTON)
        self.sleep(2)

    def _edit_days_component(self, locator, order: int):
        self._open_edit_panel(locator)
        self.click(self.CLICK_BEHAVIOUR_TYPE_DROPDOWN)
        self.click(self.SELECT_DAYS_BEHAVIOUR_TYPE)
        self._fill_direct_input_fields(order)
        self.click(self.SAVE_COMPONENT_BUTTON)
        self.sleep(2)

    def _edit_earned_component(self, locator, order: int, component_select_locator=None):
        self._open_edit_panel(locator)
        self.click(self.CLICK_BEHAVIOUR_TYPE_DROPDOWN)
        self.click(self.SELECT_EARNED_BEHAVIOUR_TYPE)
        self._fill_direct_input_fields(order)
        self.click(self.CLICK_WAGE_DEFINITION_DROPDOWN)
        self.click(self.SELECT_WAGE_DEFINITION)
        self.click(self.CLICK_COMPONENT_TYPE_DROPDOWN)
        self.click(self.SELECT_COMPONENT_TYPE)
        self.sleep(0.5)
        self.click(self.PAYROLL_APPLICABILITY_DROPDOWN)
        self.sleep(0.5)
        self.scroll_to_element(self.SELECT_CTC_APPLICABILITY)
        self.click(self.SELECT_CTC_APPLICABILITY)
        self.click(self.SELECT_GROSS_APPLICABILITY)
        self.click(self.SELECT_TAXABLE_COMPONENT)
        self.sleep(1)

        payroll_based_on = _PAYROLL_BASED_ON.strip().lower()
        if payroll_based_on == "work days":
            self.logger.info("Earning formula: Payroll based on Work Days")
            self.click(self.CLICK_EARNED_COMPONENT_DROPDOWN)
            self.click(component_select_locator or self.SELECT_EARNED_COMPONENT_BASIC)
            self.sleep(0.5)
            self.click(self.CLICK_MULTIPLIER_SYMBOL)
            self.click(self.DAY_MATCHING_DROPDOWN)
            self.click(self.SELECT_DAY_MATCHING_DYNAMIC)
            self.click(self.DIVIDE_SYMBOL)
            self.click(self.DAY_MATCHING_DROPDOWN)
            self.click(self.SELECT_MONTH_DAYS)
            self.sleep(1)
        elif payroll_based_on == "lop":
            self.logger.info("Earning formula: Payroll based on LOP")
            self.click(self.CLICK_EARNED_COMPONENT_DROPDOWN)
            self.click(component_select_locator or self.SELECT_EARNED_COMPONENT_BASIC)
            self.sleep(0.5)
            self.click(self.SELECT_SUB_SYMBOL)
            self.click(self.SELECT_OPEN_BRACKET_SYMBOL)
            self.sleep(0.5)
            self.click(self.CLICK_EARNED_COMPONENT_DROPDOWN)
            self.click(component_select_locator or self.SELECT_EARNED_COMPONENT_BASIC)
            self.sleep(0.5)
            self.click(self.CLICK_MULTIPLIER_SYMBOL)
            self.click(self.DAY_MATCHING_DROPDOWN)
            self.click(self.SELECT_DAY_MATCHING_DYNAMIC)
            self.click(self.SELECT_CLOSE_BRACKET_SYMBOL)
            self.click(self.DIVIDE_SYMBOL)
            self.click(self.DAY_MATCHING_DROPDOWN)
            self.click(self.SELECT_MONTH_DAYS)
            self.sleep(1)
        else:
            self.logger.warning(f"Unknown Payroll_Based_On value: '{_PAYROLL_BASED_ON}'. No formula executed.")

        self.click(self.OPEN_STATUTORY_APPLICABILITY)
        self.sleep(0.5)
        self.click(self.SELECT_PT_GROSS)
        self.sleep(0.5)
        self.click(self.SAVE_COMPONENT_BUTTON)
        self.sleep(2)

    #--------DEDUCTIONS COMPONENTS EDITING FUNCTION-----------------

    def _edit_loan_component(self, locator, order: int):
        self.click(self.CLICK_DEDUCTION_COMPONENT_PAGE)
        self.sleep(1)
        self._open_edit_panel(locator)
        self.click(self.CLICK_BEHAVIOUR_TYPE_DROPDOWN)
        self.click(self.SELECT_LOAN_BEHAVIOUR_TYPE)
        self._fill_direct_input_fields(order)
        self.sleep(0.5)
        self.click(self.SELECT_STATIC_VALUE_BTN)
        self.sleep(0.5)
        self.click(self.SELECT_INDIVIDUAL_WISE_BTN)
        self.click(self.PAYROLL_APPLICABILITY_DROPDOWN)
        self.sleep(0.5)
        self.click(self.SELECT_INCLUDE_FOR_GROSS_DEDUCTION)
        self.sleep(1)
        self.click(self.SAVE_COMPONENT_BUTTON)
        self.sleep(2)

    # ── Per-type component functions ──────────────────────────────────────────
    def add_fixed_components(self, start_order=1):
        components = [self.SELECT_FIXED_BASIC, self.SELECT_FIXED_HRA, self.SELECT_FIXED_DA]
        for order, component in enumerate(components, start=start_order):
            self._edit_fixed_component(component, order)
        self.logger.info("Fixed components configured.")
        return start_order + len(components)

    def add_earned_components(self, start_order=1):
        components = [
            (self.SELECT_EARNED_EARNED_BASIC, self.SELECT_EARNED_COMPONENT_BASIC),
            (self.SELECT_EARNED_EARNED_HRA,   self.SELECT_EARNED_COMPONENT_HRA),
            (self.SELECT_EARNED_EARNED_DA,    self.SELECT_EARNED_COMPONENT_DA),
        ]
        for order, (component, comp_select) in enumerate(components, start=start_order):
            self._edit_earned_component(component, order, comp_select)
        self.logger.info("Earned components configured.")
        return start_order + len(components)

    def add_monthly_components(self, start_order=1):
        components = [self.SELECT_MONTHLY_INCENTIVE]
        for order, component in enumerate(components, start=start_order):
            self._edit_monthly_component(component, order)
        self.logger.info("Monthly components configured.")
        return start_order + len(components)

    def add_arrear_components(self, start_order=1):
        components = [self.SELECT_ARREAR_ARREAR_BASIC, self.SELECT_ARREAR_ARREAR_HRA, self.SELECT_ARREAR_ARREAR_DA]
        for order, component in enumerate(components, start=start_order):
            self._edit_arrear_component(component, order)
        self.logger.info("Arrear components configured.")
        return start_order + len(components)

    def add_days_matching_components(self, start_order=1):
        components = [
            self.SELECT_DAYS_MONTH_DAYS,
            self.SELECT_DAYS_PAID_DAYS,
            self.SELECT_DAYS_WORKED_DAYS,
            self.SELECT_DAYS_LOP_DAYS,
        ]
        for order, component in enumerate(components, start=start_order):
            self._edit_days_component(component, order)
        self.logger.info("Days Matching components configured.")
        return start_order + len(components)

    def add_loan_components(self, start_order=1):
        components = [self.SELECT_LOAN_LOAN, self.SELECT_LOAN_LOAN_INTEREST]
        for order, component in enumerate(components, start=start_order):
            self._edit_loan_component(component, order)
        self.logger.info("Loan components configured.")
        return start_order + len(components)

    # ── All-components orchestrator ───────────────────────────────────────────
    def map_all_components(self):
        self._setup_mapping_form()
        order = self.add_fixed_components(start_order=1)
        order = self.add_monthly_components(start_order=order)
        order = self.add_arrear_components(start_order=order)
        order = self.add_days_matching_components(start_order=order)
        order = self.add_earned_components(start_order=order)
        self.add_loan_components(start_order=order)
        self.logger.info("✓ All pay components mapped.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def pay_component_mapping(self):
        # self.open_cgm_executive()
        self.general_master_menu()
        self.map_all_components()
        self.click(self.SAVE_PAY_COMPONENT_MAPPING)
        self.wait_for_element(self.SUCCESS_MESSAGE, timeout=30)
        self.logger.info("Pay Component mapping created")
        self.driver.refresh()
        self.sleep(5)
        self.logger.info("✓ Pay Component Mapping completed.")

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