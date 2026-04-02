from selenium.webdriver.common.by import By
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
    APPS_NAV_ITEM = (By.XPATH, "//compfie-vertical-navigation-collapsable-item[.//mat-icon[@data-mat-icon-name='apps']]")
    EXECUTIVE_URL = "http://13.203.6.58:5002/#/home/welcome"

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

        self.wait_for_element_to_be_clickable(self.APPS_NAV_ITEM, timeout=10)
        self.click(self.APPS_NAV_ITEM, timeout=10)

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

