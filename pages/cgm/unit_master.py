from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
from io import BytesIO
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base.base_page import BasePage

class unit_Master(BasePage):
    """CGM Executive page object class"""

    MENU_BUTTON = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXECUTIVE_CARD = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    SEARCH_LEGALENTITY = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    SELECT_LEGALENTITY = (By.XPATH, "//table//tbody//tr[1]//td")
    SELECT_LEGALENTITY_BUTTON = (By.XPATH, "//button[contains(@class, 'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")
    SELECTED_LEGALENTITY_ROW = (
        By.XPATH,
        "//tr[(contains(@class,'selected') or @aria-selected='true') and .//td[contains(@class,'cdk-column-legal_entity_name')]]",
    )
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


    def __init__(self, driver):
        """Initialize CGM Executive page"""
        super().__init__(driver)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for CGM Executive page to load"""
        self.wait_for_element(self.MENU_BUTTON)
        self.logger.info("CGM Executive Dashboard loaded successfully")

    def open_general_master_executive(self):
        """Open General Master-Executive, verify URL, search and select the Pure value row."""
        self.click(self.MENU_BUTTON)
        previous_windows = self.driver.window_handles

        self.wait_for_element_to_be_clickable(self.GENERAL_MASTER_EXECUTIVE_CARD, timeout=15)
        self.click(self.GENERAL_MASTER_EXECUTIVE_CARD)
        self._switch_to_new_window_if_opened(previous_windows)

        self.wait.until(EC.url_contains(self.EXECUTIVE_URL))
        self.logger.info(f"Switched to General Master-Executive tab and verified URL {self.EXECUTIVE_URL}")

        self.wait_for_element(self.SEARCH_LEGALENTITY, timeout=10)
        self.enter_text(self.SEARCH_LEGALENTITY, "Pure value")
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_LEGALENTITY).get_attribute("value").strip() == "Pure value"
        )
        self.sleep(0.5)

        # Ensure row selection is completed before clicking action button.
        self._select_legal_entity_first()

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

    def _select_legal_entity_first(self):
        """Select legal entity row and verify a row selection state before moving on."""
        self.wait_for_element_to_be_clickable(self.SELECT_LEGALENTITY, timeout=20)
        self.scroll_to_element(self.SELECT_LEGALENTITY)
        self.click(self.SELECT_LEGALENTITY, timeout=20)

        # Many grids set either aria-selected=true or a selected class on row.
        try:
            self.wait.until(
                lambda d: len(d.find_elements(*self.SELECTED_LEGALENTITY_ROW)) > 0
            )
        except Exception:
            # Fallback: ensure at least one legal entity cell exists post-click.
            self.wait_for_element(self.SELECT_LEGALENTITY, timeout=10)
        self.sleep(0.3)
            
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
        self.enter_text(self.SEARCH_BUSSINESSGROUP, "Microsoft Bussiness Groups")
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_BUSSINESSGROUP).get_attribute("value").strip() == "Microsoft Bussiness Groups"
        )
        self.find_element(self.SEARCH_BUSSINESSGROUP).send_keys(Keys.ENTER)

        self.wait_for_element_to_be_clickable(self.CLICK_COUNTRY_DROPDOWN, timeout=20)
        self.click(self.CLICK_COUNTRY_DROPDOWN, timeout=20)
        self.wait_for_element(self.SEARCH_COUNTRY, timeout=10)
        self.enter_text(self.SEARCH_COUNTRY, "India")
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_COUNTRY).get_attribute("value").strip() == "India"
        )
        self.find_element(self.SEARCH_COUNTRY).send_keys(Keys.ENTER)

        """ Enter the Unit master details"""

        self.wait_for_element_to_be_clickable(self.CLICK_DIVISION_DROPDOWN, timeout=20)
        self.click(self.CLICK_DIVISION_DROPDOWN, timeout=20)
        self.find_element(self.SEARCH_DIVISION).send_keys(Keys.ENTER)
        self.wait_for_element(self.CLICK_CATEGORY_DROPDOWN, timeout=20)
        self.click(self.CLICK_CATEGORY_DROPDOWN, timeout=20)
        self.find_element(self.SEARCH_CATEGORY).send_keys(Keys.ENTER)
        self.wait_for_element(self.ENTER_UNIT_NAME, timeout=20)
        self.unit_name = self.generate_unit_name() 
        self.wait_for_element(self.ENTER_UNIT_NAME, timeout=20)
        self.enter_text(self.ENTER_UNIT_NAME, self.unit_name)
        self.logger.info(f"Unit name entered: {self.unit_name}")
        self.unit_code = self.generate_unit_code()
        self.enter_text(self.ENTER_UNIT_CODE, self.unit_code)
        self.logger.info(f"Unit code entered: {self.unit_code}")
        self.enter_text(self.ENTER_UNIT_ADDRESS, self.generate_address)
        self.logger.info(f"Unit address entered: {self.generate_address}")
        self.click(self.SELECT_UNIT_STATE, timeout=20)
        self.enter_text(self.SEARCH_UNIT_STATE, self.Unit_Details["State"])
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_UNIT_STATE).get_attribute("value").strip() == self.Unit_Details["State"]
        )
        self.click(self.CLICK_UNIT_STATE, timeout=20)
        self.logger.info(f"Unit state selected: {self.Unit_Details['State']}")
        self.click(self.SELECT_UNIT_CITY, timeout=20)
        self.find_element(self.SEARCH_UNIT_CITY).send_keys(Keys.ENTER)
