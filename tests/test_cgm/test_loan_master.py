import pytest
from pages.cgm.Loan_Master import LoanMaster
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Loan Master"

@pytest.mark.e2e
def test_loan_master(driver):

    # login_page = GRCLoginPage(driver)
    # username   = get_str("auth", "username", "")
    # password   = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)
    # print("✓ Logged in successfully")

    page = LoanMaster(driver)
    page.navigate_to_weekly_holiday_master()
    print("✓ Loan Master completed successfully")
