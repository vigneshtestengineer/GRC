import pytest
from pages.login.grc_login_page import GRCLoginPage
from pages.cgm.Employee_Pattern_Config import EmployeePatternConfig
from utilities.json_config import get_str


@pytest.mark.e2e
def test_employee_pattern_config(driver):
    """Login → CGM Executive → Pattern Configuration → Contract Labour(s) → Save.

    Full flow:
      1. Login via GRC login page (CAPTCHA handled automatically)
      2. Open CGM Executive via app-switcher and select legal entity
      3. Navigate: General Master(s) → Pattern Configuration → Contract Labour(s)
      4. Click Add, select Unit & Contractor, choose pattern type, save
    """
    login_page = GRCLoginPage(driver)
    username   = get_str("auth", "username", "")
    password   = get_str("auth", "password", "")
    group_name = get_str("auth", "group", "")
    login_page.login(username, password, group_name)
    print("✓ Logged in successfully")

    page = EmployeePatternConfig(driver)
    page.navigate_to_employee_pattern_config()
    print("✓ Employee Pattern Configuration completed successfully")
