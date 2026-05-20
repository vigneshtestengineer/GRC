import pytest
from pages.cgm.Pay_Component_Mapping import PayComponentMapping
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Pay Component Mapping"

@pytest.mark.e2e
def test_pay_component_mapping(driver):

    # login_page = GRCLoginPage(driver)
    # username   = get_str("auth", "username", "")
    # password   = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)
    # print("✓ Logged in successfully")

    page = PayComponentMapping(driver)
    page.pay_component_mapping()
    print("✓ Pay Component Mapping completed successfully")
