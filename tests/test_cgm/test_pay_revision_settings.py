import pytest
from pages.cgm.Pay_Revision_Settings import PayRevisionSettings
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Pay Revision Settings"

@pytest.mark.e2e
def test_pay_revision_settings(driver):

    # login_page = GRCLoginPage(driver)
    # username   = get_str("auth", "username", "")
    # password   = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)
    # print("✓ Logged in successfully")

    page = PayRevisionSettings(driver)
    page.create_pay_revision_settings()
    print("✓ Pay Revision Settings completed successfully")
