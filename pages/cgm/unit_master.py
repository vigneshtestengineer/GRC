from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
import os
from io import BytesIO
from datetime import datetime
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base.base_page import BasePage
from pages.cgm.date_picker import Date_of_creation, Date_of_commencement
from utilities.json_config import get_str

LEGAL_ENTITY = get_str("auth", "legal_entity", "")
UNIT_MASTER_DATA_FILE = Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"

try:
    with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as file:
        UNIT_MASTER_DATA = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    UNIT_MASTER_DATA = {}

MASTER_DETAILS = UNIT_MASTER_DATA.get("Master_Details", {})
UNIT_DETAILS = UNIT_MASTER_DATA.get("Unit_Details", {})
BUSSINESS_GROUP = MASTER_DETAILS.get("Bussiness_Group", "")
COUNTRY = MASTER_DETAILS.get("Country", "")
STATE = UNIT_DETAILS.get("State", "")
PIN_CODE = UNIT_DETAILS.get("Pin_Code", "")
MOBILE_NUMBER = UNIT_DETAILS.get("Mobile_Number", "")
UNIT_EMAIL = UNIT_DETAILS.get("Unit_Email", "")
NATURE_OF_WORK = UNIT_DETAILS.get("Nature_of_Work", "")
INDUSTRY_TYPE = UNIT_DETAILS.get("Industry_Type", "")

class unit_Master(BasePage):
    """CGM Executive page object class"""

    MENU_BUTTON = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXECUTIVE_CARD = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    SEARCH_LEGALENTITY = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGALENTITY = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGALENTITY_ROW = (By.XPATH, "//table//tbody//tr[1]")
    SELECT_LEGALENTITY_BUTTON = (By.XPATH, "//button[contains(@class, 'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")
    OPEN_GENERAL_MASTER_MENU = (By.XPATH, "//span[normalize-space()='General Master(s)']")
    OPEN_GENERAL_MASTER_MENU_WRAPPER = (
        By.XPATH,
        "//span[normalize-space()='General Master(s)']/ancestor::div[contains(@class,'compfie-vertical-navigation-item-wrapper')][1]",
    )
    CLICK_COUNTRY_DROPDOWN = (By.XPATH, "//mat-select[@id='country']")
    SEARCH_COUNTRY = (By.XPATH, "//input[@type='text' and contains(@class,'mat-select-search-input')]")
    EXECUTIVE_URL = "http://13.203.6.58:5002/#/home/welcome"

    # Unit Creation locators

    CLICK_ON_UNIT_MASTER = (By.XPATH, "//span[normalize-space()='Unit Creation']")
    CLICK_ADD_UNIT_BUTTON = (By.XPATH, "//button[.//mat-icon[text()='add'] and .//span[contains(normalize-space(),'Add')]]")
    CLICK_BUSSINESSGROUP_DROPDOWN = (By.XPATH, "//mat-select[.//span[contains(text(),'Choose Business Group')]]")
    SEARCH_BUSSINESSGROUP = (By.XPATH, "//input[@aria-label='dropdown search']")
    CLICK_COUNTRY_DROPDOWN = (By.XPATH, "//mat-select[@id='country']")
    SPLASH_SCREEN_OVERLAY = (By.TAG_NAME, "compfie-splash-screen")

    # Unit master Details locators

    CLICK_DIVISION_DROPDOWN = (By.XPATH, "//mat-select[@id='division']")
    SEARCH_DIVISION= (By.XPATH, "//input[@placeholder='Search...']")
    CLICK_CATEGORY_DROPDOWN = (By.XPATH, "//mat-select[@id='category']")
    SEARCH_CATEGORY=(By.XPATH, "//input[@aria-label='dropdown search']")
    ENTER_UNIT_NAME = (By.XPATH, "//input[@id='unit_name']")
    ENTER_UNIT_CODE = (By.XPATH, "//input[@id='unit_code']")
    ENTER_UNIT_ADDRESS = (By.XPATH, "//textarea[@id='unit_addr1']")
    SELECT_UNIT_STATE= (By.XPATH, "//mat-select[@id='unit_state']")
    SEARCH_UNIT_STATE=  (By.XPATH, "//input[@aria-label='dropdown search']")
    CLICK_UNIT_STATE=  (By.XPATH, "(//mat-option[contains(@class,'mat-option')])[2]")
    SELECT_UNIT_CITY= (By.XPATH, "//mat-select[@id='unit_loc']")
    SEARCH_UNIT_CITY= (By.XPATH, "//input[@aria-label='dropdown search']")
    PIN_CODE = (By.XPATH, "//input[@id='unit_pincode']")
    MOBILE_NUMBER = (By.XPATH, "//input[@id='mat-input-22']")
    UNIT_EMAIL = (By.XPATH, "//input[@id='email_id']")
    NATURE_OF_WORK = (By.XPATH, "//input[@id='nature_of_work']")
    CLICK_INDUSTRY_DROPDOWN = (By.XPATH, "//mat-select[@id='industry_type']")
    SEARCH_INDUSTRY = (By.XPATH, "//input[@aria-label='dropdown search']")
    CLICK_DATE_OF_CREATION = (By.XPATH, "(//button[@aria-label='Open calendar'])[1]")
    DATE_OF_CREATION_INPUT = (By.ID, "date_of_creation")
    APPLY_DATE_OF_CREATION = (By.XPATH, "//button[@matdatepickerapply and .//span[normalize-space()='Apply']]")

    def __init__(self, driver):
        """Initialize CGM Executive page"""
        super().__init__(driver)
        self.unit_master_data = UNIT_MASTER_DATA
        self.Master_Details = self.unit_master_data.get("Master_Details", {})
        self.Unit_Details = self.unit_master_data.get("Unit_Details", {})
        self.business_group = self.Master_Details.get("Bussiness_Group", "")
        self.country = self.Master_Details.get("Country", "")
        self.state = self.Unit_Details.get("State", "")
        self.pin_code = self.Unit_Details.get("Pin_Code", "")
        self.mobile_number = self.Unit_Details.get("Mobile_Number", "")
        self.unit_email = self.Unit_Details.get("Unit_Email", "")
        self.nature_of_work = self.Unit_Details.get("Nature_of_Work", "")
        self.industry_type = self.Unit_Details.get("Industry_Type", "")
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for CGM Executive page to load"""
        self.wait_for_element(self.MENU_BUTTON)
        self.logger.info("CGM Executive Dashboard loaded successfully")

    def open_general_master_executive(self):
 
        self.click(self.MENU_BUTTON)
        previous_windows = self.driver.window_handles

        self.wait_for_element_to_be_clickable(self.GENERAL_MASTER_EXECUTIVE_CARD, timeout=15)
        self.click(self.GENERAL_MASTER_EXECUTIVE_CARD)
        self._switch_to_new_window_if_opened(previous_windows)

        self.wait.until(EC.url_contains(self.EXECUTIVE_URL))
        self.logger.info(f"Switched to General Master-Executive tab and verified URL {self.EXECUTIVE_URL}")
        self.sleep(0.5)
        self.wait_for_element(self.SEARCH_LEGALENTITY, timeout=20)
        self.enter_text(self.SEARCH_LEGALENTITY, LEGAL_ENTITY)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_LEGALENTITY).get_attribute("value").strip() == LEGAL_ENTITY
        )
        self.sleep(0.5)

        self._select_legal_entity_row()

        self.wait_for_element_to_be_clickable(self.SELECT_LEGALENTITY_BUTTON, timeout=15)
        self.scroll_to_element(self.SELECT_LEGALENTITY_BUTTON)
        self.click(self.SELECT_LEGALENTITY_BUTTON)

    def _switch_to_new_window_if_opened(self, previous_windows):
        """Switch to a newly opened browser window/tab if the click opened one."""
        current_windows = self.driver.window_handles
        if len(current_windows) > len(previous_windows):
            new_windows = [h for h in current_windows if h not in previous_windows]
            if new_windows:
                self.driver.switch_to.window(new_windows[-1])
                self.logger.info(f"Switched to new browser window/tab: {new_windows[-1]}")
            else:
                self.logger.debug("Detected window count change, but no new handle found.")
        else:
            self.logger.debug("No new browser window/tab opened after click.")

    def _select_legal_entity_row(self):
        """Click the legal entity row and wait until the action button becomes usable."""
        for attempt in range(1, 4):
            self.wait_for_element(self.SELECT_LEGALENTITY, timeout=20)
            self.scroll_to_element(self.SELECT_LEGALENTITY)
            row_cell = self.find_element(self.SELECT_LEGALENTITY)

            try:
                row_cell.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", row_cell)

            try:
                self.wait.until(
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
                self.sleep(0.5)
                return
            except Exception:
                self.logger.warning(
                    "Legal entity row click did not enable the select button on attempt %d. Retrying.",
                    attempt,
                )
                self.sleep(0.5)

        raise RuntimeError("Legal entity row was clicked, but the select button did not become enabled.")

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
        # """ Open General Master menu from the left navigation for creation of Unit creation """"
        for attempt in range(1, 3):
            self.wait_for_element_to_be_clickable(self.OPEN_GENERAL_MASTER_MENU, timeout=20)
            self.scroll_to_element(self.OPEN_GENERAL_MASTER_MENU)
            self.click(self.OPEN_GENERAL_MASTER_MENU, timeout=20)
            self.sleep(0.5)

            if self.is_element_visible(self.CLICK_ON_UNIT_MASTER, timeout=6):
                self.logger.info("General Master menu expanded successfully.")
                return

            # Retry by clicking the parent wrapper in case only label click was captured.
            self.logger.warning(
                "General Master menu did not expand on attempt %d. Retrying with wrapper click.",
                attempt,
            )
            self.click(self.OPEN_GENERAL_MASTER_MENU_WRAPPER, timeout=20)
            self.sleep(0.5)
            if self.is_element_visible(self.CLICK_ON_UNIT_MASTER, timeout=6):
                self.logger.info("General Master menu expanded successfully using wrapper click.")
                return

        raise RuntimeError("Could not expand 'General Master(s)' menu to access 'Unit Creation'.")

# Create Unit master

    def create_unit_master(self):
        # Unit Creation.
        self.general_master_menu()
        self.wait_for_element_to_be_clickable(self.CLICK_ON_UNIT_MASTER, timeout=20)
        self.scroll_to_element(self.CLICK_ON_UNIT_MASTER)
        self.click(self.CLICK_ON_UNIT_MASTER, timeout=20)
        self.wait_for_element_to_be_clickable(self.CLICK_ADD_UNIT_BUTTON, timeout=10)
        self.click(self.CLICK_ADD_UNIT_BUTTON, timeout=10)
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN_OVERLAY, timeout=20)
        self.wait_for_element_to_be_clickable(self.CLICK_BUSSINESSGROUP_DROPDOWN, timeout=20)
        self.click(self.CLICK_BUSSINESSGROUP_DROPDOWN, timeout=20)
        self.wait_for_element(self.SEARCH_BUSSINESSGROUP, timeout=20)
        self.enter_text(self.SEARCH_BUSSINESSGROUP, self.business_group)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_BUSSINESSGROUP).get_attribute("value").strip() == self.business_group
        )
        self.find_element(self.SEARCH_BUSSINESSGROUP).send_keys(Keys.ENTER)

        self.wait_for_element_to_be_clickable(self.CLICK_COUNTRY_DROPDOWN, timeout=20)
        self.click(self.CLICK_COUNTRY_DROPDOWN, timeout=20)
        self.wait_for_element(self.SEARCH_COUNTRY, timeout=10)
        self.enter_text(self.SEARCH_COUNTRY, self.country)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_COUNTRY).get_attribute("value").strip() == self.country
        )
        self.find_element(self.SEARCH_COUNTRY).send_keys(Keys.ENTER)

        """ Enter the Unit master details"""

        self.wait_for_element_to_be_clickable(self.CLICK_DIVISION_DROPDOWN, timeout=20)
        self.click(self.CLICK_DIVISION_DROPDOWN, timeout=20)
        self.find_element(self.SEARCH_DIVISION).send_keys(Keys.ENTER)
        self.wait_for_element(self.CLICK_CATEGORY_DROPDOWN, timeout=20)
        self.click(self.CLICK_CATEGORY_DROPDOWN, timeout=20)
        self.sleep(0.7)
        self.find_element(self.SEARCH_CATEGORY).send_keys(Keys.ENTER)
        self.wait_for_element(self.ENTER_UNIT_NAME, timeout=20)
        self.unit_name = self.generate_unit_name()
        self.wait_for_element(self.ENTER_UNIT_NAME, timeout=20)
        self.enter_text(self.ENTER_UNIT_NAME, self.unit_name)
        self.logger.info(f"Unit name entered: {self.unit_name}")
        self.unit_code = self.generate_unit_code()
        self.enter_text(self.ENTER_UNIT_CODE, self.unit_code)
        self.logger.info(f"Unit code entered: {self.unit_code}")
        self.unit_address = self.generate_address()
        self.enter_text(self.ENTER_UNIT_ADDRESS, self.unit_address)
        self.logger.info(f"Unit address entered: {self.unit_address}")
        self._save_generated_unit_details(self.unit_name, self.unit_code, self.unit_address)
        self.click(self.SELECT_UNIT_STATE, timeout=20)
        self.enter_text(self.SEARCH_UNIT_STATE, self.state)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_UNIT_STATE).get_attribute("value").strip() == self.state
        )
        self.click(self.CLICK_UNIT_STATE, timeout=20)
        self.logger.info(f"Unit state selected: {self.state}")
        self.click(self.SELECT_UNIT_CITY, timeout=20)
        self.find_element(self.SEARCH_UNIT_CITY).send_keys(Keys.ENTER)
        self.click(self.PIN_CODE, timeout=20)
        self.enter_text(self.PIN_CODE, self.pin_code)
        self.enter_text(self.MOBILE_NUMBER, self.mobile_number)
        self.enter_text(self.UNIT_EMAIL, self.unit_email)
        self.enter_text(self.NATURE_OF_WORK, self.nature_of_work)
        self.click(self.CLICK_INDUSTRY_DROPDOWN, timeout=20)
        self.enter_text(self.SEARCH_INDUSTRY, self.industry_type)
        self.find_element(self.SEARCH_INDUSTRY).send_keys(Keys.ENTER)
        self.sleep(0.5)
        Date_of_creation(self.driver).set_date("01/01/2020")
        self.sleep(0.5)
        Date_of_commencement(self.driver).set_date("01/02/2020")
        self.sleep(0.5)