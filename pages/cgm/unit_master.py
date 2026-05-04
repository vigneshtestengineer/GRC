from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import sys
import os
from io import BytesIO
from datetime import datetime
from pages.base.date_picker import DatePicker
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base.base_page import BasePage
from utilities.json_config import get_str

LEGAL_ENTITY = get_str("auth", "legal_entity", "")
UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)

try:
    with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as file:
        UNIT_MASTER_DATA = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    UNIT_MASTER_DATA = {}

MASTER_DETAILS = UNIT_MASTER_DATA.get("Master_Details", {})
UNIT_DETAILS = UNIT_MASTER_DATA.get("Unit_Details", {})
UNIT_RIGHTS_ALLOCATION = UNIT_MASTER_DATA.get("Unit_Rights_Allocation", {})
SCOPE_INFORMATION = UNIT_MASTER_DATA.get("Scope_Information", {})
BUSSINESS_GROUP = MASTER_DETAILS.get("Bussiness_Group", "")
COUNTRY = MASTER_DETAILS.get("Country", "")
STATE = UNIT_DETAILS.get("State", "")
PIN_CODE = UNIT_DETAILS.get("Pin_Code", "")
MOBILE_NUMBER = UNIT_DETAILS.get("Mobile_Number", "")
UNIT_EMAIL = UNIT_DETAILS.get("Unit_Email", "")
NATURE_OF_WORK = UNIT_DETAILS.get("Nature_of_Work", "")
INDUSTRY_TYPE = UNIT_DETAILS.get("Industry_Type", "")
SERVICE_AGREEMENT = UNIT_DETAILS.get("Service_Agreement", "")
EMPLOYEE_TYPE = UNIT_DETAILS.get("Employee_Type", "")
CGM_EXE = UNIT_RIGHTS_ALLOCATION.get("CGM_EXE", "")
TAMS_EXE = UNIT_RIGHTS_ALLOCATION.get("TAMS_EXE", "")
PAYROLL_EXE = UNIT_RIGHTS_ALLOCATION.get("Payroll_EXE", "")
CGM_ADMIN = UNIT_RIGHTS_ALLOCATION.get("CGM_ADMIN", "")
CGM_MODULE = UNIT_RIGHTS_ALLOCATION.get("CGM_MODULE", "")
TAMS_MODULE = UNIT_RIGHTS_ALLOCATION.get("TAMS_MODULE", "")
PAYROLL_MODULE = UNIT_RIGHTS_ALLOCATION.get("PAYROLL_MODULE", "")
EXECUTIVE_ROLE = UNIT_RIGHTS_ALLOCATION.get("EXECUTIVE_ROLE", "")
ADMIN_ROLE = UNIT_RIGHTS_ALLOCATION.get("ADMIN_ROLE", "")
DOMAIN = SCOPE_INFORMATION.get("Domain", "")
ORGANIZATION_TYPE = SCOPE_INFORMATION.get("Organization_type", "")
STATE = SCOPE_INFORMATION.get("State", "")
ACT = SCOPE_INFORMATION.get("Act", "")



class unit_Master(BasePage):
    """CGM Executive page object class"""

    # LOCATORS

    MENU_BUTTON = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXECUTIVE_CARD = (
        By.XPATH,
        "//mat-card[span[text()='General Master-Executive']]",
    )
    SEARCH_LEGALENTITY = (
        By.XPATH,
        "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]",
    )
    SELECT_LEGALENTITY = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGALENTITY_ROW = (By.XPATH, "//table//tbody//tr[1]")
    SELECT_LEGALENTITY_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]",
    )
    OPEN_GENERAL_MASTER_MENU = (
        By.XPATH,
        "//span[normalize-space()='General Master(s)']",
    )
    OPEN_GENERAL_MASTER_MENU_WRAPPER = (
        By.XPATH,
        "//span[normalize-space()='General Master(s)']/ancestor::div[contains(@class,'compfie-vertical-navigation-item-wrapper')][1]",
    )
    CLICK_COUNTRY_DROPDOWN = (By.XPATH, "//mat-select[@id='country']")
    SEARCH_COUNTRY = (
        By.XPATH,
        "//input[@type='text' and contains(@class,'mat-select-search-input')]",
    )
    EXECUTIVE_URL = "http://13.203.6.58:5002/#/home/welcome"

    # Unit Creation locators

    CLICK_ON_UNIT_MASTER = (By.XPATH, "//span[normalize-space()='Unit Creation']")
    CLICK_ADD_UNIT_BUTTON = (
        By.XPATH,
        "//button[.//mat-icon[text()='add'] and .//span[contains(normalize-space(),'Add')]]",
    )
    CLICK_BUSSINESSGROUP_DROPDOWN = (
        By.XPATH,
        "//mat-select[.//span[contains(text(),'Choose Business Group')]]",
    )
    SEARCH_BUSSINESSGROUP = (By.XPATH, "//input[@aria-label='dropdown search']")
    CLICK_COUNTRY_DROPDOWN = (By.XPATH, "//mat-select[@id='country']")
    SPLASH_SCREEN_OVERLAY = (By.TAG_NAME, "compfie-splash-screen")

    # Unit master Details locators

    CLICK_DIVISION_DROPDOWN = (By.XPATH, "//mat-select[@id='division']")
    SEARCH_DIVISION = (By.XPATH, "//input[@placeholder='Search...']")
    CLICK_CATEGORY_DROPDOWN = (By.XPATH, "//mat-select[@id='category']")
    SEARCH_CATEGORY = (By.XPATH, "//input[@aria-label='dropdown search']")
    ENTER_UNIT_NAME = (By.XPATH, "//input[@id='unit_name']")
    ENTER_UNIT_CODE = (By.XPATH, "//input[@id='unit_code']")
    ENTER_UNIT_ADDRESS = (By.XPATH, "//textarea[@id='unit_addr1']")
    SELECT_UNIT_STATE = (By.XPATH, "//mat-select[@id='unit_state']")
    SEARCH_UNIT_STATE = (By.XPATH, "//input[@aria-label='dropdown search']")
    CLICK_UNIT_STATE = (By.XPATH, "(//mat-option[contains(@class,'mat-option')])[2]")
    SELECT_UNIT_CITY = (By.XPATH, "//mat-select[@id='unit_loc']")
    SEARCH_UNIT_CITY = (By.XPATH, "//input[@aria-label='dropdown search']")
    PIN_CODE = (By.XPATH, "//input[@id='unit_pincode']")
    MOBILE_NUMBER = (By.XPATH, "//input[@id='mat-input-22']")
    UNIT_EMAIL = (By.XPATH, "//input[@id='email_id']")
    NATURE_OF_WORK = (By.XPATH, "//input[@id='nature_of_work']")
    CLICK_INDUSTRY_DROPDOWN = (By.XPATH, "//mat-select[@id='industry_type']")
    SEARCH_INDUSTRY = (By.XPATH, "//input[@aria-label='dropdown search']")
    CLICK_DATE_OF_CREATION = (By.XPATH, "(//button[@aria-label='Open calendar'])[1]")
    DATE_OF_CREATION_INPUT = (By.ID, "date_of_creation")
    APPLY_DATE_OF_CREATION = (
        By.XPATH,
        "//button[@matdatepickerapply and .//span[normalize-space()='Apply']]",
    )
    SERVICE_AGREEMENT_DROPDOWN = (By.XPATH, "//mat-select[@id='legal_agreement_id']")
    SEARCH_AGREEMENT = (By.XPATH, "//input[@aria-label='dropdown search']")
    APPLICABLE_EMPLOYEE = (
        By.XPATH,
        "//mat-checkbox[.//span[contains(normalize-space(),'{text}')]]//label",
    )
    ECODE_BASED = (
        By.XPATH,
        "//mat-radio-button[.//span[contains(normalize-space(),'Unit')]]",
    )
    ID_CARD = (
        By.XPATH,
        "((//span[contains(@class,'mat-checkbox-inner-container')])[5])",
    )

    # Unit Rights Allocation locators

    CLICK_UNIT_RIGHTS_ALLOCATION = (
        By.XPATH,
        "//mat-expansion-panel-header[.//p[normalize-space()='Unit Rights Allocation(s)']]",
    )
    RIGHTS_ADD_BTN = (
        By.XPATH,
        "(//button[.//mat-icon[@data-mat-icon-name='plus-sm']])[6]",
    )

    # Unit Rights Allocation(s) rows

    SELECT_USER_NAME_DROPDOWN_ONE = (
        By.XPATH,
        "((//mat-select[.//span[contains(text(),'User Name')]])[1])",
    )
    SELECT_MODULE_NAME_ONE = (
        By.XPATH,
        "((//mat-select[.//span[contains(text(),'Module Name')]])[1])",
    )
    SELECT_ROLE_ONE = (
        By.XPATH,
        "((//mat-select[.//span[contains(text(),'Role Name')]])[1])",
    )

    SEARCH_UNIT_RIGHTS = (By.XPATH, "//input[@aria-label='dropdown search']")

    # SCOPE INFORMATIONS locators

    SELECT_SCOPE_INFORMATION = (By.XPATH, "//div[@role='tab'][.//span[normalize-space()='SCOPE INFORMATION']]")

    SCOPE_INFORMATION_DROPDOWN = (By.XPATH, "//p[normalize-space()='Scope Information']")

    DOMAIN_DROPDOWN = (By.XPATH, "//mat-select[@id='domain_id']")

    # Common Search locator for dropdowns
    SEARCH = (By.XPATH, "//input[@aria-label='dropdown search']")

    # Selecting the 1st element after search in dropdown
    SELECT_DATA = (By.XPATH, "//mat-option[not(@aria-disabled='true')][1]")

    ORGANIZATION_DROPDOWN = (By.XPATH, "//mat-select[@id='org_id']")

    SCOPE_STATE = (By.XPATH, "//mat-select[@id='state_id']")

    ACT_DROPDOWN = (By.XPATH, "//mat-select[@id='act_id']")

    # Save Unit master

    UNIT_MASTER_SAVE_BUTTON = (By.XPATH, "//button[.//span[normalize-space()='Submit as save']]")


    def __init__(self, driver):
        """Initialize CGM Executive page"""
        super().__init__(driver)
        self.unit_master_data = UNIT_MASTER_DATA
        self.Master_Details = self.unit_master_data.get("Master_Details", {})
        self.Unit_Details = self.unit_master_data.get("Unit_Details", {})
        self.Scope_Information = self.unit_master_data.get("Scope_Information", {})
        self.business_group = self.Master_Details.get("Bussiness_Group", "")
        self.country = self.Master_Details.get("Country", "")
        self.state = self.Unit_Details.get("State", "")
        self.pin_code = self.Unit_Details.get("Pin_Code", "")
        self.mobile_number = self.Unit_Details.get("Mobile_Number", "")
        self.unit_email = self.Unit_Details.get("Unit_Email", "")
        self.nature_of_work = self.Unit_Details.get("Nature_of_Work", "")
        self.industry_type = self.Unit_Details.get("Industry_Type", "")
        self.date_of_creation = self.Unit_Details.get("Date_of_Creation", "")
        self.date_of_commitment = self.Unit_Details.get("Date_of_Commitment", "")
        self.service_agreement = self.Unit_Details.get("Service_Agreement", "")
        self.date_of_commencement_of_operations = self.Unit_Details.get(
            "Date_of_Commencement_of_operations", ""
        )
        self.employee_type = self.Unit_Details.get("Employee_Type", "")
        self.unit_rights_allocation = self.unit_master_data.get(
            "Unit_Rights_Allocation", {}
        )
        self.cgm_exe = self.unit_rights_allocation.get("CGM_EXE", "")
        self.tams_exe = self.unit_rights_allocation.get("TAMS_EXE", "")
        self.payroll_exe = self.unit_rights_allocation.get("Payroll_EXE", "")
        self.cgm_admin = self.unit_rights_allocation.get("CGM_ADMIN", "")
        self.cgm_module = self.unit_rights_allocation.get("CGM_MODULE", "")
        self.tams_module = self.unit_rights_allocation.get("TAMS_MODULE", "")
        self.payroll_module = self.unit_rights_allocation.get("PAYROLL_MODULE", "")
        self.executive_role = self.unit_rights_allocation.get("EXECUTIVE_ROLE", "")
        self.admin_role = self.unit_rights_allocation.get("ADMIN_ROLE", "")
        self.domain = self.Scope_Information.get("Domain", "")
        self.organization_type = self.Scope_Information.get("Organization_type", "")
        self.state = self.Scope_Information.get("State", "")
        self.act = self.Scope_Information.get("Act", "")



    def open_general_master_executive(self):

        self.wait_for_element_to_be_clickable(self.MENU_BUTTON, timeout=30)
        self.click(self.MENU_BUTTON)
        self.logger.info("✓ Clicked MENU_BUTTON.")
    
        previous_windows = self.driver.window_handles

        self.logger.info("Clicked app-switcher menu.")

        self.wait_for_element_to_be_clickable(
            self.GENERAL_MASTER_EXECUTIVE_CARD, timeout=8
        )
        self.click(self.GENERAL_MASTER_EXECUTIVE_CARD)
        self._switch_to_new_window_if_opened(previous_windows)

        self.wait.until(EC.url_contains(self.EXECUTIVE_URL))
        self.logger.info(
            f"Switched to General Master-Executive tab and verified URL {self.EXECUTIVE_URL}"
        )
        self.wait_for_element(self.SEARCH_LEGALENTITY, timeout=10)
        self.enter_text(self.SEARCH_LEGALENTITY, LEGAL_ENTITY)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_LEGALENTITY)
            .get_attribute("value")
            .strip()
            == LEGAL_ENTITY
        )

        self._select_legal_entity_row()

        self.wait_for_element_to_be_clickable(
            self.SELECT_LEGALENTITY_BUTTON, timeout=8
        )
        self.scroll_to_element(self.SELECT_LEGALENTITY_BUTTON)
        self.click(self.SELECT_LEGALENTITY_BUTTON)

    def _switch_to_new_window_if_opened(self, previous_windows):
        """Switch to a newly opened browser window/tab if the click opened one."""
        current_windows = self.driver.window_handles
        if len(current_windows) > len(previous_windows):
            new_windows = [h for h in current_windows if h not in previous_windows]
            if new_windows:
                self.driver.switch_to.window(new_windows[-1])
                self.logger.info(
                    f"Switched to new browser window/tab: {new_windows[-1]}"
                )
            else:
                self.logger.debug(
                    "Detected window count change, but no new handle found."
                )
        else:
            self.logger.debug("No new browser window/tab opened after click.")

    def _select_legal_entity_row(self):
        """Click the legal entity row and wait until the action button becomes usable."""
        for attempt in range(1, 3):
            self.wait_for_element(self.SELECT_LEGALENTITY, timeout=8)
            self.scroll_to_element(self.SELECT_LEGALENTITY)
            row_cell = self.find_element(self.SELECT_LEGALENTITY)

            try:
                row_cell.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", row_cell)

            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.execute_script(
                        """
                        const button = arguments[0];
                        if (!button) {
                            return false;
                        }
                        const disabledAttr = button.getAttribute('disabled');
                        const ariaDisabled = button.getAttribute('aria-disabled');
                        const classes = (button.className || '').toLowerCase();
                        return !button.disabled &&
                            disabledAttr === null &&
                            ariaDisabled !== 'true' &&
                            !classes.includes('disabled');
                        """,
                        d.find_element(*self.SELECT_LEGALENTITY_BUTTON),
                    )
                )
                self.logger.info("Legal entity row selected successfully.")
                return
            except Exception:
                self.logger.warning(
                    "Legal entity row click did not enable the select button on attempt %d. Retrying.",
                    attempt,
                )

        raise RuntimeError(
            "Legal entity row was clicked, but the select button did not become enabled."
        )

    def _save_generated_unit_details(self, unit_name, unit_code, unit_address=""):
        """Persist generated unit values into Unit_Master_Data.json."""
        try:
            with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        unit_details = data.setdefault("Unit_Details", {})
        unit_details["unit_name"] = unit_name
        unit_details["unit_code"] = unit_code
        unit_details["unit_address"] = unit_address

        with open(UNIT_MASTER_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            file.write("\n")

        self.logger.info(
            "Saved generated unit details to %s: unit_name='%s', unit_code='%s', unit_address='%s'",
            UNIT_MASTER_DATA_FILE,
            unit_name,
            unit_code,
            unit_address,
        )

    # Click General master to create the unit creation

    def general_master_menu(self):
        # If the menu is already open, clicking again would close it (toggle).
        if self.is_element_visible(self.CLICK_ON_UNIT_MASTER, timeout=2):
            self.logger.info("General Master menu already expanded.")
            return

        for attempt in range(1, 3):
            try:
                self.click(self.OPEN_GENERAL_MASTER_MENU, timeout=5)
                self.wait_for_element_to_be_clickable(self.CLICK_ON_UNIT_MASTER, timeout=8)
                self.logger.info(
                    "General Master menu expanded successfully%s.",
                    " on retry" if attempt > 1 else "",
                )
                return
            except Exception as e:
                self.logger.debug(f"Attempt {attempt} failed: {e}")

        raise RuntimeError(
            "Could not expand 'General Master(s)' menu to access 'Unit Creation' after 2 attempts."
        )

    # Create Unit master

    def create_unit_master(self):
        # Unit Creation.
        self.general_master_menu()
        self.wait_for_element_to_be_clickable(self.CLICK_ON_UNIT_MASTER, timeout=8)
        self.click(self.CLICK_ON_UNIT_MASTER, timeout=8)
        self.wait_for_element_to_be_clickable(self.CLICK_ADD_UNIT_BUTTON, timeout=6)
        self.click(self.CLICK_ADD_UNIT_BUTTON, timeout=6)
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN_OVERLAY, timeout=10)
        self.wait_for_element_to_be_clickable(
            self.CLICK_BUSSINESSGROUP_DROPDOWN, timeout=8
        )
        self.click(self.CLICK_BUSSINESSGROUP_DROPDOWN, timeout=8)
        self.wait_for_element(self.SEARCH_BUSSINESSGROUP, timeout=8)
        self.enter_text(self.SEARCH_BUSSINESSGROUP, self.business_group)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_BUSSINESSGROUP)
            .get_attribute("value")
            .strip()
            == self.business_group
        )
        self.find_element(self.SEARCH_BUSSINESSGROUP).send_keys(Keys.ENTER)

        self.wait_for_element_to_be_clickable(self.CLICK_COUNTRY_DROPDOWN, timeout=8)
        self.click(self.CLICK_COUNTRY_DROPDOWN, timeout=8)
        self.wait_for_element(self.SEARCH_COUNTRY, timeout=6)
        self.enter_text(self.SEARCH_COUNTRY, self.country)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_COUNTRY)
            .get_attribute("value")
            .strip()
            == self.country
        )
        self.find_element(self.SEARCH_COUNTRY).send_keys(Keys.ENTER)

        """ Enter the Unit master details"""

        self.wait_for_element_to_be_clickable(self.CLICK_DIVISION_DROPDOWN, timeout=8)
        self.click(self.CLICK_DIVISION_DROPDOWN, timeout=8)
        self.find_element(self.SEARCH_DIVISION).send_keys(Keys.ENTER)
        self.wait_for_element(self.CLICK_CATEGORY_DROPDOWN, timeout=8)
        self.click(self.CLICK_CATEGORY_DROPDOWN, timeout=8)
        self.sleep(0.2)
        self.find_element(self.SEARCH_CATEGORY).send_keys(Keys.ENTER)
        self.wait_for_element(self.ENTER_UNIT_NAME, timeout=8)
        self.unit_name = self.generate_unit_name()
        self.enter_text(self.ENTER_UNIT_NAME, self.unit_name)
        self.logger.info(f"Unit name entered: {self.unit_name}")
        self.unit_code = self.generate_unit_code()
        self.enter_text(self.ENTER_UNIT_CODE, self.unit_code)
        self.logger.info(f"Unit code entered: {self.unit_code}")
        self.unit_address = self.generate_address()
        self.enter_text(self.ENTER_UNIT_ADDRESS, self.unit_address)
        self.logger.info(f"Unit address entered: {self.unit_address}")
        self._save_generated_unit_details(
            self.unit_name, self.unit_code, self.unit_address
        )
        self.click(self.SELECT_UNIT_STATE, timeout=8)
        self.enter_text(self.SEARCH_UNIT_STATE, self.state)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_UNIT_STATE)
            .get_attribute("value")
            .strip()
            == self.state
        )
        self.click(self.CLICK_UNIT_STATE, timeout=8)
        self.logger.info(f"Unit state selected: {self.state}")
        self.click(self.SELECT_UNIT_CITY, timeout=8)
        self.find_element(self.SEARCH_UNIT_CITY).send_keys(Keys.ENTER)
        self.click(self.PIN_CODE, timeout=8)
        self.enter_text(self.PIN_CODE, self.pin_code)
        self.enter_text(self.MOBILE_NUMBER, self.mobile_number)
        self.enter_text(self.UNIT_EMAIL, self.unit_email)
        self.enter_text(self.NATURE_OF_WORK, self.nature_of_work)
        self.click(self.CLICK_INDUSTRY_DROPDOWN, timeout=8)
        self.enter_text(self.SEARCH_INDUSTRY, self.industry_type)
        self.find_element(self.SEARCH_INDUSTRY).send_keys(Keys.ENTER)
        # Date of Creation  →  (//button[@aria-label='Open calendar'])[1]
        DatePicker(self.driver).set_date(
            "(//button[@aria-label='Open calendar'])[1]", self.date_of_creation
        )
        # Date of Commitment  →  (//button[@aria-label='Open calendar'])[2]
        DatePicker(self.driver).set_date(
            "(//button[@aria-label='Open calendar'])[2]", self.date_of_commitment
        )
        self.click(self.SERVICE_AGREEMENT_DROPDOWN, timeout=8)
        self.enter_text(self.SEARCH_AGREEMENT, self.service_agreement)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_AGREEMENT)
            .get_attribute("value")
            .strip()
            == self.service_agreement
        )
        self.find_element(self.SEARCH_AGREEMENT).send_keys(Keys.ENTER)
        self.logger.info(f"Service agreement selected: {self.service_agreement}")

        # Date of Commencement of Operations  →  (//button[@aria-label='Open calendar'])[5]
        DatePicker(self.driver).set_date(
            "(//button[@aria-label='Open calendar'])[5]",
            self.date_of_commencement_of_operations,
        )
        self.sleep(0.1)

        employee_type_checkbox = (
            By.XPATH,
            f"//mat-checkbox[.//span[contains(@class,'mat-checkbox-label') and contains(normalize-space(),'{self.employee_type}')]]//input[@type='checkbox']",
        )

        self.wait_for_element_to_be_clickable(employee_type_checkbox, timeout=6)
        self.driver.execute_script(
            "arguments[0].click();", self.find_element(employee_type_checkbox)
        )
        self.logger.info("Employee type checked: %s", self.employee_type)

        if self.employee_type == "Contract Labour(s)":

            self.click(self.ECODE_BASED, timeout=6)

        self.logger.info("Selected 'Unit' radio button for Contract Labour(s).")

        self.sleep(0.5)

        self.wait_for_element_to_be_clickable(self.ID_CARD, timeout=6)
        self.click(self.ID_CARD, timeout=6)
        self.logger.info("Checked 'ID Card' checkbox.")

        self.click(self.CLICK_UNIT_RIGHTS_ALLOCATION, timeout=8)
        self.wait_for_element_to_be_clickable(self.RIGHTS_ADD_BTN, timeout=8)
        self.logger.info(
            "Clicked 'Unit Rights Allocation(s)' and waiting for Add button to be clickable."
        )
        for i in range(4):
            self.wait_for_element_to_be_clickable(self.RIGHTS_ADD_BTN, timeout=6)
            self.click(self.RIGHTS_ADD_BTN, timeout=6)
            self.logger.info(
                "Clicked 'Add' button %d/4 under Unit Rights Allocation(s).", i + 1
            )
            self.sleep(0.2)

            # Unit Rights Allocation(s) (CGM,TAMS,Payroll) - Executive and Admin Role

            # FIRST ROW OF UNIT RIGHTS ALLOCATION(S)

        self.click(self.SELECT_USER_NAME_DROPDOWN_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.cgm_exe)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.click(self.SELECT_MODULE_NAME_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.cgm_module)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.click(self.SELECT_ROLE_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.executive_role)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.logger.info(
            "Assigned Unit Rights Allocation: User Name='%s', Module='%s', Role='%s'",
            self.cgm_exe,
            self.cgm_module,
            self.executive_role,
        )

            # SECOND ROW OF UNIT RIGHTS ALLOCATION(S)

        self.click(self.SELECT_USER_NAME_DROPDOWN_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.tams_exe)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.click(self.SELECT_MODULE_NAME_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.tams_module)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.click(self.SELECT_ROLE_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.executive_role)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)

            # THIRD ROW OF UNIT RIGHTS ALLOCATION(S)

        self.click(self.SELECT_USER_NAME_DROPDOWN_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.payroll_exe)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.click(self.SELECT_MODULE_NAME_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.payroll_module)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.click(self.SELECT_ROLE_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.executive_role)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)

            # FOURTH ROW OF UNIT RIGHTS ALLOCATION(S)

        self.click(self.SELECT_USER_NAME_DROPDOWN_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.cgm_admin)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.click(self.SELECT_MODULE_NAME_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.cgm_module)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.2)
        self.click(self.SELECT_ROLE_ONE, timeout=6)
        self.enter_text(self.SEARCH_UNIT_RIGHTS, self.admin_role)
        self.find_element(self.SEARCH_UNIT_RIGHTS).send_keys(Keys.ENTER)
        self.sleep(0.5)

            # Moved to SCOPE INFORMATION page

        self.click(self.SELECT_SCOPE_INFORMATION, timeout=6)
        self.sleep(0.5)
        self.click(self.SCOPE_INFORMATION_DROPDOWN, timeout=6)
        self.wait_for_element_to_be_clickable(self.DOMAIN_DROPDOWN, timeout=6)
        self.click(self.DOMAIN_DROPDOWN, timeout=6)
        self.enter_text(self.SEARCH, self.domain)
        self.click(self.SELECT_DATA, timeout=6)
        self.click(self.ORGANIZATION_DROPDOWN, timeout=6)
        self.enter_text(self.SEARCH, self.organization_type)
        self.click(self.SELECT_DATA, timeout=6)
        self.click(self.SCOPE_STATE, timeout=6)
        self.sleep(0.5)
        self.enter_text(self.SEARCH, self.state)
        self.sleep(0.5)
        self.click(self.SELECT_DATA, timeout=6)
        self.sleep(0.5)
        self.click(self.ACT_DROPDOWN, timeout=6)
        self.sleep(0.5)
        self.enter_text(self.SEARCH, self.act)
        self.sleep(0.5)
        self.click(self.SELECT_DATA, timeout=6)
        self.sleep(0.5)
        self.find_element(self.ACT_DROPDOWN).send_keys(Keys.ESCAPE)
        self.logger.info(
            "Filled Scope Information: Domain='%s', Organization Type='%s', State='%s', Act='%s'",
            self.domain,
            self.organization_type,
            self.state,
            self.act
        )
        self.sleep(0.5)
        self.scroll_to_element(self.UNIT_MASTER_SAVE_BUTTON)
        self.wait_for_element_to_be_clickable(self.UNIT_MASTER_SAVE_BUTTON, timeout=8)
        self.driver.execute_script(
            "arguments[0].click();",
            self.find_element(self.UNIT_MASTER_SAVE_BUTTON),
        )
        self.logger.info("Clicked 'Submit as save' button to save the new unit master.")

        SUCCESS_TOAST = (
            By.XPATH,
            "//div[contains(@class,'compfie-toast-notification-message') and normalize-space()='Successfully Created']",
        )
        TOAST_CLOSE_BUTTON = (
            By.XPATH,
            "//mat-icon[@data-mat-icon-name='x']",
        )
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(SUCCESS_TOAST)
            )
            self.logger.info("Unit master created successfully — toast message verified.")
        except TimeoutException:
            self.logger.error("Success toast not visible after saving unit master.")
            raise RuntimeError("Unit master save confirmation toast was not displayed.")

        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(TOAST_CLOSE_BUTTON)
            )
            self.wait_for_element_to_disappear(self.SPLASH_SCREEN_OVERLAY, timeout=15)
            self.click(TOAST_CLOSE_BUTTON, timeout=5)
            self.logger.info("Closed success toast notification.")
            self.wait_for_element_to_disappear(SUCCESS_TOAST, timeout=10)
            self.logger.info("✓ Toast fully dismissed.")
        except (TimeoutException, Exception):
            self.wait_for_element_to_disappear(SUCCESS_TOAST, timeout=10)

        self.sleep(1)

