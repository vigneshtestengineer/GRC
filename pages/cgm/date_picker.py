from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def select_date_in_datepicker(self, element_id: str, date_string: str):
    # Parse the date
    month_num, day_num, year = date_string.split("/")
    month_num = int(month_num)
    day_num = str(int(day_num))

    # Month short form in CAPS
    month_names_caps = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                        "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    month_caps = month_names_caps[month_num - 1]

    # 1. Locate and clear input field
    date_input = self.wait.until(
    EC.visibility_of_element_located((By.ID, element_id))
    )

    parent_div = date_input.find_element(By.XPATH, "./ancestor::div[2]")

    # 2. Click calendar button
    calendar_button = parent_div.find_element(
        By.XPATH, ".//button[@aria-label='Open calendar']"
    )
    calendar_button.click()
    self.sleep(0.5)

    # 3. Open month/year picker
    self.click((By.XPATH, "//button[@aria-label='Choose month and year']"))
    self.sleep(0.5)

    # 4. Select year
    year_xpath = f"//button[.//div[normalize-space(text())='{year}']]"
    self.click((By.XPATH, year_xpath))
    self.sleep(0.5)

    # 5. Select month (FIXED → button + div content)
    month_xpath = f"//button[.//div[normalize-space(text())='{month_caps}']]"
    self.click((By.XPATH, month_xpath))
    self.sleep(0.5)

    # 6. Select day (FIXED → same structure)
    day_xpath = f"//button[.//div[normalize-space(text())='{day_num}']]"
    self.click((By.XPATH, day_xpath))
    self.sleep(0.5)

    # 7. Click Apply (FIXED → button, not span)
    apply_xpath = "//button[@matdatepickerapply]"
    self.click((By.XPATH, apply_xpath))
    self.sleep(0.5)

    print(f"✅ Date {date_string} selected successfully!")


# Wrapper (UNCHANGED usage)
def set_date_of_creation(self, date_string: str):
    select_date_in_datepicker(self, "date_of_creation", date_string)