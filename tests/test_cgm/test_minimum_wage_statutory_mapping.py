import pytest
from pages.cgm.statutory_mapping.Minimum_Wage_mapping import MinimumWageStatutoryMapping
from pages.cgm.statutory_mapping.PTAX_Statutory_mapping import PTAXStatutoryMapping
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Minimum Wage Statutory Mapping"

@pytest.mark.e2e
def test_minimum_wage_statutory_mapping(driver):
    """Login → CGM Executive → Statutory Master(s) → Statutory Mapping → Minimum Wage Statutory Mapping.

    Full flow:
      1. Login via GRC login page (CAPTCHA handled automatically)
      2. Open CGM Executive via app-switcher and select legal entity
      3. Navigate: Statutory Master(s) → Statutory Mapping
      4. Click Add, select State & Unit, enable Minimum Wage Statutory Mapping, configure settings, save
    """
    login_page = GRCLoginPage(driver)
    username   = get_str("auth", "username", "")
    password   = get_str("auth", "password", "")
    group_name = get_str("auth", "group", "")
    login_page.login(username, password, group_name)
    print("✓ Logged in successfully")

    page = MinimumWageStatutoryMapping(driver)
    page.add_minimum_wage_statutory_mapping()
    print("✓ Minimum Wage Statutory Mapping completed successfully")