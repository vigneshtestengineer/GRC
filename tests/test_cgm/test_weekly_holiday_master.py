import pytest
from pages.cgm.Weekly_Holiday_Master import WeeklyHolidayMaster
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str


@pytest.mark.e2e
def test_weekly_holiday_master(driver):
    login_page = GRCLoginPage(driver)
    username = get_str("auth", "username", "")
    password = get_str("auth", "password", "")
    group_name = get_str("auth", "group", "")
    login_page.login(username, password, group_name)
    page = WeeklyHolidayMaster(driver)
    page.navigate_to_weekly_holiday_master()
    print("✓ Weekly Holiday Master completed successfully")
