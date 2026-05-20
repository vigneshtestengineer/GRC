import pytest
from pages.cgm.statutory_mapping.Holiday_Rules_Statutory_mapping import HolidayRulesStatutoryMapping
from pages.cgm.statutory_mapping.PTAX_Statutory_mapping import PTAXStatutoryMapping
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Holiday Rules Statutory Mapping"

@pytest.mark.e2e
def test_holiday_rules_statutory_mapping(driver):

    # login_page = GRCLoginPage(driver)
    # username   = get_str("auth", "username", "")
    # password   = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)
    # print("✓ Logged in successfully")

    page = HolidayRulesStatutoryMapping(driver)
    page.add_holiday_rules_statutory_mapping()
    print("✓ Holiday Rules Statutory Mapping completed successfully")