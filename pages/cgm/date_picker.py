import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base.base_page import BasePage


class Date_of_creation(BasePage):
    """Date picker helper for the creation date field."""

    def _select_date_common(self, element_id: str, date_string: str, calendar_index: int):
        # Parse the date
        month_num, day_num, year = date_string.split("/")
        month_num = int(month_num)
        day_num = str(int(day_num))

        # Month short form in CAPS
        month_names_caps = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                            "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        month_caps = month_names_caps[month_num - 1]

        # 1. Wait for any overlay/spinner to disappear before proceeding
        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-pane"))
            )
        except Exception:
            pass
        self.sleep(1)

        # 2. Locate input field — wait for visibility (not just presence)
        try:
            date_input = self.wait.until(
                EC.visibility_of_element_located((By.ID, element_id))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", date_input)
            self.sleep(0.5)
            self.logger.info(f"Found date input field: '{element_id}'")
        except Exception as e:
            self.logger.error(f"Failed to find date input with ID '{element_id}': {e}")
            try:
                self.driver.execute_script("window.scrollBy(0, 300);")
                self.sleep(1)
                date_input = self.wait.until(
                    EC.visibility_of_element_located((By.ID, element_id))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", date_input)
                self.sleep(0.5)
                self.logger.info(f"Found date input field after scroll: '{element_id}'")
            except Exception as e2:
                self.logger.error(f"Element still not found after scroll retry: {e2}")
                raise

        # 3. Wait for all calendar buttons to be present then click by index
        try:
            self.wait.until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, "//button[@aria-label='Open calendar' and @aria-haspopup='dialog']")
                )
            )
            calendar_buttons = self.driver.find_elements(
                By.XPATH, "//button[@aria-label='Open calendar' and @aria-haspopup='dialog']"
            )
            self.logger.info(f"Found {len(calendar_buttons)} calendar buttons on page")

            target_button = calendar_buttons[calendar_index - 1]
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target_button)
            self.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", target_button)
            self.logger.info(f"Clicked calendar button index {calendar_index} for '{element_id}'")
        except IndexError:
            self.logger.error(
                f"Calendar button at index {calendar_index} not found. "
                f"Only {len(calendar_buttons)} buttons available."
            )
            raise
        except Exception as e:
            self.logger.error(f"Failed to click calendar button for '{element_id}': {e}")
            raise

        self.sleep(1)
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "cdk-overlay-pane"))
        )

        self.click((By.XPATH, "//button[@aria-label='Choose month and year']"))
        self.sleep(0.5)

        year_xpath = f"//button[.//div[normalize-space(text())='{year}']]"
        self.click((By.XPATH, year_xpath))
        self.sleep(0.5)

        month_xpath = f"//button[.//div[normalize-space(text())='{month_caps}']]"
        self.click((By.XPATH, month_xpath))
        self.sleep(0.5)

        day_xpath = f"//button[.//div[normalize-space(text())='{day_num}']]"
        self.click((By.XPATH, day_xpath))
        self.sleep(0.3)

        apply_xpath = "//button[@matdatepickerapply]"
        self.click((By.XPATH, apply_xpath))

        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-pane"))
            )
        except Exception as e:
            self.logger.warning(f"Calendar overlay wait failed: {e}")

        self.sleep(1.5)
        print(f"✅ Date {date_string} selected successfully for '{element_id}'!")

    def set_date(self, date_string: str):
        self._select_date_common("date_of_creation", date_string, calendar_index=1)


class Date_of_commencement(BasePage):
    """Date picker helper for the commencement date field."""

    def _select_date_common(self, element_id: str, date_string: str, calendar_index: int):
        # Parse the date
        month_num, day_num, year = date_string.split("/")
        month_num = int(month_num)
        day_num = str(int(day_num))

        month_names_caps = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                            "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        month_caps = month_names_caps[month_num - 1]

        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-pane"))
            )
        except Exception:
            pass
        self.sleep(1)

        try:
            date_input = self.wait.until(
                EC.visibility_of_element_located((By.ID, element_id))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", date_input)
            self.sleep(0.5)
            self.logger.info(f"Found date input field: '{element_id}'")
        except Exception as e:
            self.logger.error(f"Failed to find date input with ID '{element_id}': {e}")
            try:
                self.driver.execute_script("window.scrollBy(0, 300);")
                self.sleep(1)
                date_input = self.wait.until(
                    EC.visibility_of_element_located((By.ID, element_id))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", date_input)
                self.sleep(0.5)
                self.logger.info(f"Found date input field after scroll: '{element_id}'")
            except Exception as e2:
                self.logger.error(f"Element still not found after scroll retry: {e2}")
                raise

        try:
            self.wait.until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, "//button[@aria-label='Open calendar' and @aria-haspopup='dialog']")
                )
            )
            calendar_buttons = self.driver.find_elements(
                By.XPATH, "//button[@aria-label='Open calendar' and @aria-haspopup='dialog']"
            )
            self.logger.info(f"Found {len(calendar_buttons)} calendar buttons on page")

            target_button = calendar_buttons[calendar_index - 1]
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target_button)
            self.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", target_button)
            self.logger.info(f"Clicked calendar button index {calendar_index} for '{element_id}'")
        except IndexError:
            self.logger.error(
                f"Calendar button at index {calendar_index} not found. "
                f"Only {len(calendar_buttons)} buttons available."
            )
            raise
        except Exception as e:
            self.logger.error(f"Failed to click calendar button for '{element_id}': {e}")
            raise

        self.sleep(1)
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "cdk-overlay-pane"))
        )

        self.click((By.XPATH, "//button[@aria-label='Choose month and year']"))
        self.sleep(0.5)

        year_xpath = f"//button[.//div[normalize-space(text())='{year}']]"
        self.click((By.XPATH, year_xpath))
        self.sleep(0.5)

        month_xpath = f"//button[.//div[normalize-space(text())='{month_caps}']]"
        self.click((By.XPATH, month_xpath))
        self.sleep(0.5)

        day_xpath = f"//button[.//div[normalize-space(text())='{day_num}']]"
        self.click((By.XPATH, day_xpath))
        self.sleep(0.3)

        apply_xpath = "//button[@matdatepickerapply]"
        self.click((By.XPATH, apply_xpath))

        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-pane"))
            )
        except Exception as e:
            self.logger.warning(f"Calendar overlay wait failed: {e}")

        self.sleep(1.5)
        print(f"✅ Date {date_string} selected successfully for '{element_id}'!")

    def set_date(self, date_string: str):
        self._select_date_common("date_of_commencement", date_string, calendar_index=2)
