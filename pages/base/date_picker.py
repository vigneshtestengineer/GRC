import sys
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base.base_page import BasePage


class DatePicker(BasePage):

    CALENDAR_OVERLAY = (By.CLASS_NAME, "cdk-overlay-pane")
    YEAR_DROPDOWN = (By.XPATH, "//button[@aria-label='Choose month and year']")
    APPLY_BUTTON = (By.XPATH, "//button[.//span[normalize-space()='Apply']]")

    def _wait_overlay_gone(self):
        try:
            WebDriverWait(self.driver, 5).until(  # ✅ Reduced to 5s
                EC.invisibility_of_element_located(self.CALENDAR_OVERLAY)
            )
        except TimeoutException:
            self.logger.warning("Calendar did not close in time.")
            pass  # ✅ Don't block, continue anyway

    def _wait_overlay_open(self):
        try:
            WebDriverWait(self.driver, 5).until(  # ✅ Reduced to 5s
                EC.presence_of_element_located(self.CALENDAR_OVERLAY)
            )
            self.logger.info("Calendar opened.")
        except TimeoutException:
            self.logger.warning("Calendar did not open in time.")

    def set_date(self, calendar_xpath: str, date_string: str):
        """
        Args:
            calendar_xpath : XPath of the calendar icon button.
                             e.g. "(//button[@aria-label='Open calendar'])[1]"
            date_string    : Date in MM/DD/YYYY format.
                             e.g. "01/01/2021"
        """
        # Parse the date string
        month_num, day, year = date_string.split("/")
        date_obj = datetime(int(year), int(month_num), int(day))
        month_name = date_obj.strftime("%B")  # e.g. "January"
        day_clean = str(int(day))  # strip leading zero e.g. "1"

        # Step 1 - make sure no calendar is already open
        # self._wait_overlay_gone()

        # Step 2 - click the calendar icon
        calendar_btn = (By.XPATH, calendar_xpath)
        self.wait_for_element_to_be_clickable(calendar_btn, timeout=10)  # ✅ 15 → 10
        element = self.find_element(calendar_btn)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.sleep(0.3)  # ✅ Let scroll settle
        try:
            element.click()  # ✅ Normal click first (faster)
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)  # fallback
        self.logger.info("Clicked calendar icon.")

        # Step 3 - wait for calendar to open
        self._wait_overlay_open()

        # Step 4 - click "Choose month and year" to open year/month view
        # xpath : //button[@aria-label='Choose month and year']
        self.wait_for_element_to_be_clickable(self.YEAR_DROPDOWN, timeout=10)
        self.click(self.YEAR_DROPDOWN)

        # Step 5 - select the year
        # xpath : //button[@aria-label='2021']
        year_btn = (By.XPATH, f"//button[@aria-label='{year}']")
        self.wait_for_element_to_be_clickable(year_btn, timeout=10)
        self.click(year_btn)
        self.logger.info("Selected year: %s", year)

        # Step 6 - select the month
        # xpath : //button[@aria-label='January 2021']
        month_btn = (By.XPATH, f"//button[@aria-label='{month_name} {year}']")
        self.wait_for_element_to_be_clickable(month_btn, timeout=10)
        self.click(month_btn)
        self.logger.info("Selected month: %s", month_name)

        # Step 7 - select the day
        # xpath : //button[@aria-label='January 1, 2021']
        day_btn = (
            By.XPATH,
            f"//button[@aria-label='{month_name} {day_clean}, {year}']",
        )
        self.wait_for_element_to_be_clickable(day_btn, timeout=10)
        self.click(day_btn)
        self.logger.info("Selected day: %s", day_clean)

        # Step 8 - click Apply
        # xpath : //button[.//span[normalize-space()='Apply']]
        self.wait_for_element_to_be_clickable(self.APPLY_BUTTON, timeout=10)
        self.click(self.APPLY_BUTTON)
        self.logger.info("Clicked Apply button.")

        # Step 9 - wait for calendar to close
        self._wait_overlay_gone()

        self.logger.info("Date '%s' set successfully.", date_string)
