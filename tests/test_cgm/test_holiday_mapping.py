import pytest
from pages.cgm.statutory_mapping.Holiday_Mapping import HolidayMapping
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Holiday Mapping"

@pytest.mark.e2e
def test_holiday_mapping(driver):
    """Login → CGM Executive → Statutory Master(s) → Statutory Mapping → Holiday Mapping.

    Full flow:
      1. Login via GRC login page (CAPTCHA handled automatically)
      2. Open CGM Executive via app-switcher and select legal entity
      3. Navigate: Statutory Master(s) → Statutory Mapping
      4. Click Add, select State & Unit, enable Holiday Rules Statutory Mapping, configure settings, save
    """
    login_page = GRCLoginPage(driver)
    username   = get_str("auth", "username", "")
    password   = get_str("auth", "password", "")
    group_name = get_str("auth", "group", "")
    login_page.login(username, password, group_name)
    print("✓ Logged in successfully")

    page = HolidayMapping(driver)
    page.add_holiday_mapping()
    print("✓ Holiday Mapping completed successfully")