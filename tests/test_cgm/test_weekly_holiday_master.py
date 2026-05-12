import pytest
from pages.cgm.Weekly_Holiday_Master import WeeklyHolidayMaster
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Weekly Holiday Master"

@pytest.mark.e2e
def test_weekly_holiday_master(driver):

    page = WeeklyHolidayMaster(driver)
    page.navigate_to_weekly_holiday_master()
    print("✓ Weekly Holiday Master completed successfully")
