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
        self.click(self.GENERAL_SETTINGS_MENU, timeout=6)
        self.wait_for_element(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=6)
        self.click(self.SELECT_APPROVAL_SETTINGS_MENU, timeout=6)

        self._setup_module(CGM_MODULE, has_other_settings=False)
        self._setup_module(TAMS_MODULE, has_other_settings=True)
        self._setup_module(PAYROLL_MODULE, has_other_settings=True)

        self.verify_success_notification()

    def _setup_module(self, module_name, has_other_settings=False):
        """Creates approval settings for a single module."""
        self.wait_for_element(self.ADD_APPROVAL_SETTINGS_BUTTON, timeout=6)
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
        self.enter_text(self.SEARCH, UNIT_NAME)
        self.logger.info(f"Searched for unit: {UNIT_NAME}")
        self.sleep(0.3)
        self.click(self.SELECT_DROPDOWN_VALUE, timeout=6)
        self.logger.info(f"Selected unit: {UNIT_NAME}")
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

        # Send for Approval
        self.click(self.CLICK_SEND_FOR_APPROVAL_BUTTON, timeout=6)
        self.sleep(1)
        self.click(self.CLICK_SEND_FOR_APPROVAL_BUTTON, timeout=6)
        self.sleep(1)
        self.logger.info(f"Clicked 'Send for Approval' button for {module_name} module")

    def verify_success_notification(self, timeout=6):
        """Verify success notification appears after sending for approval and wait for processing

        Args:
            timeout (int): Maximum time to wait in seconds (default: 6)
        """
        try:
            # Wait for success notification to appear
            self.wait_for_element(self.SUCCESS_NOTIFICATION_MESSAGE, timeout=10)
            self.logger.info("✓ Success notification appeared: 'Successfully Queued'")

            # Take screenshot of the success message
            self.driver.save_screenshot("success_notification.png")

            # Wait for processing to complete (2 minutes)
            self.logger.info(f"Waiting for {timeout} seconds for processing to complete...")
            self.sleep(timeout)
            self.logger.info("✓ Processing completed after 2 minutes")

        except Exception as e:
            self.logger.error(f"Failed to verify success notification: {str(e)}")
            raise RuntimeError(f"Success notification not found or timeout occurred: {str(e)}")

    def save_approval_settings(self):
        """Save the approval settings"""
        self.logger.info("Saving approval settings...")
        self.click(self.SAVE_BUTTON, timeout=6)
        self.logger.info("Approval settings saved successfully")
