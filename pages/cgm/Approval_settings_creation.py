from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load Unit Master Data
UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)

try:
    with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as file:
        UNIT_MASTER_DATA = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    UNIT_MASTER_DATA = {}

UNIT_DETAILS = UNIT_MASTER_DATA.get("Unit_Details", {})
APPROVAL_MODULE = UNIT_MASTER_DATA.get("Approval_Module", {})

UNIT_NAME = UNIT_DETAILS.get("unit_name", "")
CGM_MODULE = APPROVAL_MODULE.get("CGM_MODULE", "")
TAMS_MODULE = APPROVAL_MODULE.get("TAMS_MODULE", "")
PAYROLL_MODULE = APPROVAL_MODULE.get("PAYROLL_MODULE", "")


class ApprovalSettingsCreation(BasePage):
    """Approval Settings Creation page object"""

    # LOCATORS

    GENERAL_SETTINGS_MENU = (By.XPATH, "//span[normalize-space()='General Setting(s)']")
    SELECT_APPROVAL_SETTINGS_MENU = (By.XPATH,"//span[normalize-space()='Approval Setting(s)']",)
    ADD_APPROVAL_SETTINGS_BUTTON = (By.XPATH, "//button[contains(., 'Add')]")
    SELECT_BASED_ON = (By.XPATH,"//label[contains(@class, 'mat-radio-label') and contains(., 'Unit')]",)
    SELECT_UNIT_DROPDOWN = (By.XPATH, "//div[contains(@class, 'mat-select-value') and .//span[contains(text(), 'Choose Unit')]]")
    SEARCH = (By.XPATH, "//input[@placeholder='Search...']")
    SELECT_DROPDOWN_VALUE = (By.XPATH, "(//span[contains(@class,'mat-option-text')])[2]")
    SELECT_MODULE = (By.XPATH, "//div[contains(@class, 'mat-select-value') and .//span[contains(text(), 'Choose Module')]]")
    TYPE_OF_APPROVAL_DROPDOWN = (By.XPATH, "//div[contains(@class, 'mat-select-value') and .//span[contains(text(), 'Choose Type of Approval(s)')]]")
    SELECT_ALL_CHECKBOX = (By.XPATH, "//label[contains(@class,'mat-checkbox-layout') and .//span[text()='Select All']]")
    CLICK_SEND_FOR_APPROVAL_BUTTON = (By.XPATH, "//span[contains(normalize-space(),'Send for Approval')]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(., 'Save') or contains(., 'Submit')]")

    # Other Settings locators

    CLICK_OTHER_SETTINGS = (By.XPATH, "//div[@role='tab']//span[normalize-space()='Other Setting(s)']")
    CRITERIA_MISMATCH = (By.XPATH, "//mat-select[@placeholder='For Criteria Mismatch']")
    NO_APPROVER = (By.XPATH, "//mat-select[@placeholder='In case of no Approver']")
    SELECT_AUTOAPPROVE = (By.XPATH, "//mat-option//span[normalize-space()='Auto Approve']")

    # Success notification locators
    SUCCESS_NOTIFICATION_CONTENT = (By.XPATH, "//div[contains(@class, 'compfie-toast-notification-content')]")
    SUCCESS_NOTIFICATION_TITLE = (By.XPATH, "//div[contains(@class, 'compfie-toast-notification-title') and contains(text(), 'Success')]")
    SUCCESS_NOTIFICATION_MESSAGE = (By.XPATH, "//div[contains(@class, 'compfie-toast-notification-message') and contains(text(), 'Successfully Queued')]")
    TOAST_CLOSE_BUTTON = (By.XPATH, "//mat-icon[@data-mat-icon-name='x']")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("ApprovalSettingsCreation page initialized.")
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for the approval settings page to load"""

        self.wait_for_element(self.GENERAL_SETTINGS_MENU, timeout=10)
        self.logger.info("Approval Settings page loaded successfully")

    def create_approval_settings(self, _data=None):
        """Navigate to Approval Settings and create entries for CGM, TAMS, and Payroll."""
        self.logger.info("Starting approval settings creation process.")
        self.scroll_to_element(self.GENERAL_SETTINGS_MENU)
        self.click(self.GENERAL_SETTINGS_MENU, timeout=6)
        self.wait_for_element(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=6)
        self.click(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=6)

        self._setup_module(CGM_MODULE, has_other_settings=False, refresh_before=False)
        self._setup_module(TAMS_MODULE, has_other_settings=True, refresh_before=True)
        self._setup_module(PAYROLL_MODULE, has_other_settings=True, refresh_before=True)

    def _get_unit_name(self):
        """Read unit name from JSON at runtime to pick up the value saved by unit_master."""
        try:
            with open(UNIT_MASTER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("Unit_Details", {}).get("unit_name", UNIT_NAME)
        except Exception:
            return UNIT_NAME

    def _setup_module(self, module_name, has_other_settings=False, refresh_before=False):
        """Creates approval settings for a single module."""
        if refresh_before:
            self.logger.info(f"Refreshing page before starting {module_name} module...")
            self.driver.refresh()
            self.wait_for_element(self.ADD_APPROVAL_SETTINGS_BUTTON, timeout=15)
            self.logger.info(f"✓ Page refreshed — ready for {module_name}.")

        unit_name = self._get_unit_name()

        self.click(self.ADD_APPROVAL_SETTINGS_BUTTON, timeout=6)
        self.logger.info("Clicked Add Approval Settings button")

        self.wait_for_element(self.SELECT_BASED_ON, timeout=6)
        self.click(self.SELECT_BASED_ON, timeout=6)
        self.logger.info("Selected 'Based On' as 'Unit'")
        self.sleep(0.5)

        # Select Unit
        self.click(self.SELECT_UNIT_DROPDOWN, timeout=6)
        self.wait_for_element(self.SEARCH, timeout=6)
        search_element = self.find_element(self.SEARCH)
        search_element.clear()
        self.enter_text(self.SEARCH, unit_name)
        self.logger.info(f"Searched for unit: {unit_name}")
        self.sleep(0.3)
        self.click(self.SELECT_DROPDOWN_VALUE, timeout=6)
        self.logger.info(f"Selected unit: {unit_name}")
        self.sleep(2)

        # Select Module
        self.click(self.SELECT_MODULE, timeout=6)
        self.sleep(2)
        search_element = self.find_element(self.SEARCH)
        search_element.clear()
        self.enter_text(self.SEARCH, module_name)
        self.logger.info(f"Searched for module: {module_name}")
        self.sleep(0.3)
        self.click(self.SELECT_DROPDOWN_VALUE, timeout=6)

        # Type of Approval
        self.click(self.TYPE_OF_APPROVAL_DROPDOWN, timeout=6)
        self.click(self.SELECT_ALL_CHECKBOX, timeout=6)
        self.sleep(0.5)
        search_element = self.find_element(self.SEARCH)
        search_element.send_keys(Keys.ESCAPE)
        self.sleep(0.5)

        # Other Settings (only for TAMS and Payroll)
        if has_other_settings:
            self.click(self.CLICK_OTHER_SETTINGS, timeout=6)
            self.sleep(0.5)
            self.click(self.CRITERIA_MISMATCH, timeout=6)
            self.sleep(1)
            self.click(self.SELECT_AUTOAPPROVE, timeout=6)
            self.sleep(1)
            self.scroll_to_element(self.NO_APPROVER)
            self.click(self.NO_APPROVER, timeout=6)
            self.sleep(1)
            self.click(self.SELECT_AUTOAPPROVE, timeout=6)
            self.sleep(1)

        # First click submits the form / opens confirmation dialog
        self.click(self.CLICK_SEND_FOR_APPROVAL_BUTTON, timeout=6)
        self.sleep(3)

        # Second click confirms the dialog if it is still present
        try:
            self.click(self.CLICK_SEND_FOR_APPROVAL_BUTTON, timeout=4)
            self.logger.info(f"Confirmed Send for Approval dialog for {module_name}.")
        except Exception:
            self.logger.info(f"No confirmation dialog found for {module_name} — continuing.")

        self.sleep(2)
        self.logger.info(f"✓ Sent for Approval — {module_name} module done.")

    def verify_success_notification(self, timeout=6):
        """Verify success notification appears after sending for approval and wait for processing"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SUCCESS_NOTIFICATION_CONTENT)
            )
            self.logger.info("✓ Success notification appeared: 'Successfully Queued'")
            self.driver.save_screenshot("success_notification.png")

            self.logger.info("Refreshing page to dismiss toast and reset state...")
            self.driver.refresh()
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located(self.SUCCESS_NOTIFICATION_CONTENT)
            )
            self.wait_for_element(self.GENERAL_SETTINGS_MENU, timeout=15)
            self.click(self.GENERAL_SETTINGS_MENU, timeout=10)
            self.wait_for_element(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=10)
            self.click(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=10)
            self.logger.info("✓ Page refreshed and re-navigated to Approval Settings.")

            self.logger.info(f"Waiting {timeout} seconds for processing to complete...")
            self.sleep(timeout)
            self.logger.info("✓ Processing completed")

        except TimeoutException:
            self.logger.error("Success notification did not appear within 30 seconds")
            self.driver.save_screenshot("missing_notification.png")
            raise RuntimeError("Success notification not found after Send for Approval")

    def save_approval_settings(self):
        """Save the approval settings"""
        self.logger.info("Saving approval settings...")
        self.click(self.SAVE_BUTTON, timeout=6)
        self.logger.info("Approval settings saved successfully")
