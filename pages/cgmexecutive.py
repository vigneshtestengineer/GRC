from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
from io import BytesIO
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base_page import BasePage
from config.config import Config

class CGMExecutivePage(BasePage):
    """CGM Executive page object class"""

    MENU_BUTTON = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    GENERAL_MASTER_EXECUTIVE_CARD = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    ENTITY_ROW = (By.XPATH, "//td[contains(@class, 'cdk-column-legal_entity_name') and contains(@class, 'mat-cell')]")
    ADD_BUTTON = (By.XPATH, "//button[contains(@class, 'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")
    SELECT_LEGAL_ENTITY = (By.XPATH, "//td[contains(@class,'mat-column-legal_entity_name')]")
    OPEN_GENERAL_MASTER_MENU = (By.XPATH, "//compfie-vertical-navigation-collapsable-item[.//mat-icon[@data-mat-icon-name='apps']]")
    EXECUTIVE_URL = "http://13.203.6.58:5002/#/home/welcome"

    # Unit Creation locators

    CLICK_ON_UNIT_MASTER = (By.XPATH, "//span[normalize-space()='Unit Creation']")
    CLICK_ADD_UNIT_BUTTON = (By.XPATH, "//button[.//mat-icon[text()='add'] and .//span[contains(normalize-space(),'Add')]]")
    CLICK_BUSSINESSGROUP_DROPDOWN = (By.XPATH, "//mat-select[.//span[contains(text(),'Choose Business Group')]]")
    SEARCH_BUSSINESSGROUP = (By.XPATH, "//input[@aria-label='dropdown search']")
    CLICK_COUNTRY_DROPDOWN = (By.XPATH, "//mat-select[@id='country']")


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

        self.wait_for_element(self.SEARCH_INPUT, timeout=10)
        self.enter_text(self.SEARCH_INPUT, "Pure value")
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value").strip() == "Pure value"
        )

        self.wait_for_element_to_be_clickable(self.ENTITY_ROW, timeout=10)
        self.click(self.ENTITY_ROW)

        self.wait_for_element_to_be_clickable(self.SELECT_LEGAL_ENTITY, timeout=15)
        self.scroll_to_element(self.SELECT_LEGAL_ENTITY)
        self.click(self.SELECT_LEGAL_ENTITY)
        self.sleep(0.5)

        self.wait_for_element_to_be_clickable(self.ADD_BUTTON, timeout=15)
        self.scroll_to_element(self.ADD_BUTTON)
        self.click(self.ADD_BUTTON)

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
            
# Click General master to create the unit creation

    def general_master_menu(self):
        """Open General Master menu from the left navigation for creation of Unit creation"""
        self.wait_for_element_to_be_clickable(self.OPEN_GENERAL_MASTER_MENU, timeout=10)
        self.click(self.OPEN_GENERAL_MASTER_MENU, timeout=10)

# Create Unit master

    def create_unit_master(self):

        self.wait_for_element_to_be_clickable(self.CLICK_ON_UNIT_MASTER, timeout=10)
        self.click(self.CLICK_ON_UNIT_MASTER, timeout=10)
        self.wait_for_element_to_be_clickable(self.CLICK_ADD_UNIT_BUTTON, timeout=10)
        self.click(self.CLICK_ADD_UNIT_BUTTON, timeout=10)
        element = self.wait_for_element_to_be_clickable(self.CLICK_BUSSINESSGROUP_DROPDOWN, timeout=10)
        self.enter_text(self.SEARCH_BUSSINESSGROUP, "Microsoft Bussiness Groups", timeout=10)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_BUSSINESSGROUP).get_attribute("value").strip() == "Microsoft Bussiness Groups"
        )
        element.send_keys(Keys.ENTER)
        
