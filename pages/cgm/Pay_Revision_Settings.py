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
from utilities.json_config import get_str

LEGAL_ENTITY = get_str("auth", "legal_entity", "")

UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)

CONTRACTOR_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Contractor_Master_Data.json"
)

LOAN_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Loan_Master_Data.json"
)

PAY_COMPONENT_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Pay_Component_Data.json"
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
    with open(PAY_COMPONENT_DATA_FILE, "r", encoding="utf-8") as _f:
        _pay_data = json.load(_f)
        _fixed  = _pay_data.get("Fixed components", {})
        BASIC_COMPONENT = _fixed.get("Basic", "")
        HRA_COMPONENT   = _fixed.get("HRA", "")
        DA_COMPONENT    = _fixed.get("DA", "")
        _arrear = _pay_data.get("Arrear Components", {})
        ARREAR_BASIC_COMPONENT = _arrear.get("Arrear Basic", "")
        ARREAR_HRA_COMPONENT   = _arrear.get("Arrear HRA", "")
        ARREAR_DA_COMPONENT    = _arrear.get("Arrear DA", "")
except (FileNotFoundError, json.JSONDecodeError):
    BASIC_COMPONENT = HRA_COMPONENT = DA_COMPONENT = ""
    ARREAR_BASIC_COMPONENT = ARREAR_HRA_COMPONENT = ARREAR_DA_COMPONENT = ""



class PayRevisionSettings(BasePage):
    """Page object for Pay Revision Settings."""

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

    #-------------Pay Revision settings-----------------------
    CLICK_PAY_REVISION_SETTINGS_MENU =(By.XPATH,"//span[normalize-space()='Pay Revision Setting(s)']")
    ADD_PAY_REVISION_SETTING_BUTTON =(By.XPATH,"//button[contains(.,'Add')]")
    UNIT_MASTER_DROPDOWN =(By.XPATH,"(//mat-select[@role='combobox'])[1]")
    CONTRACTOR_MASTER_DROPDOWN =(By.XPATH,"(//mat-select[@role='combobox'])[2]")
    CLICK_SHOW_DETAILS_BUTTON =(By.XPATH,"//span[contains(normalize-space(),'Show Detail(s)')]")
    CLICK_ADD_PAY_REVISION_BUTTON =(By.XPATH,"//mat-icon[@data-mat-icon-name='plus-sm']")

    #---------Revision Component selection locators----------------------
    CLICK_REVISION_COMPONENT_DROPDOWN =(By.XPATH,"(//span[normalize-space()='Select component'])[1]")
    CLICK_ARREARS_COMPONENT_DROPDOWN =(By.XPATH,"(//span[normalize-space()='Select Component'])[1]")

    #---------Select All Checkboxs----------------------
    CLICK_CHECK_BOX_CONSIDER_LOP =(By.XPATH,"//span[contains(@class,'mat-checkbox-inner-container')]")

    #----------SAVE PAY REVISION SETTINGS-------------------------------------

    SAVE_PAY_REVISION_SETTINGS =(By.XPATH,"//button[contains(.,'Submit as save')]")
    SUCCESS_TOAST              =(By.XPATH,"//div[contains(@class,'compfie-toast-notification-title') and normalize-space()='Success']")
    CLOSE_TOAST                =(By.XPATH,"//compfie-toast-notification//mat-icon[@data-mat-icon-name='x']")


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
    def pay_revision_settings(self):

        self.click(self.CLICK_PAY_REVISION_SETTINGS_MENU)
        self.wait_for_element_to_be_clickable( self.ADD_PAY_REVISION_SETTING_BUTTON, timeout=15)
        self.click(self.ADD_PAY_REVISION_SETTING_BUTTON)
        # Select Unit from dropdown
        self.wait_for_element_to_be_clickable(self.UNIT_MASTER_DROPDOWN, timeout=10)
        self.click(self.UNIT_MASTER_DROPDOWN)
        self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
        self.enter_text(self.DROPDOWN_SEARCH, self._get_unit_name())
        self.click(self.SELECT_DROPDOWN_DATA)
        # Select Contractor from dropdown
        self.click(self.CONTRACTOR_MASTER_DROPDOWN)
        self.enter_text(self.DROPDOWN_SEARCH, self._get_contractor_name())
        self.click(self.SELECT_DROPDOWN_DATA)
        self.enter_text(self.DROPDOWN_SEARCH, Keys.ESCAPE)  # Close dropdown
        # Click Show Details button
        self.click(self.CLICK_SHOW_DETAILS_BUTTON)
        # Click Add Pay Revision button 3 times
        for _ in range(3):
            self.click(self.CLICK_ADD_PAY_REVISION_BUTTON)
        #-------------------Select Revision Component-------------
        for component in (BASIC_COMPONENT, HRA_COMPONENT, DA_COMPONENT):
            self.click(self.CLICK_REVISION_COMPONENT_DROPDOWN)
            self.click((By.XPATH, f"//mat-option//span[normalize-space()='{component}']"))
        #-------------------Select Arrears Component-------------
        for arrear in (ARREAR_BASIC_COMPONENT, ARREAR_HRA_COMPONENT, ARREAR_DA_COMPONENT):
            self.click(self.CLICK_ARREARS_COMPONENT_DROPDOWN)
            self.click((By.XPATH, f"//mat-option//span[normalize-space()='{arrear}']"))
        self.sleep(1)
        #--------------------Consider LOP Checkbox----------------
        checkboxes = self.find_elements(self.CLICK_CHECK_BOX_CONSIDER_LOP)
        for checkbox in checkboxes:
            try:
                checkbox.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", checkbox)
        self.click(self.SAVE_PAY_REVISION_SETTINGS)
        self.wait_for_element(self.SUCCESS_TOAST, timeout=15)
        self.logger.info("Success toast appeared.")
        self.click(self.CLOSE_TOAST)
        self.sleep(2)
        self.logger.info("Pay revision settings created.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def create_pay_revision_settings(self):
        # self.open_cgm_executive()
        # self.general_master_menu()
        self.pay_revision_settings()
        self.logger.info("✓ Pay revision settings completed.")

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