import pytest
from pages.cgm.statutory_mapping.LWF_Statutory_mapping import LWFStatutoryMapping
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "LWF Statutory Mapping"

@pytest.mark.e2e
def test_esi_statutory_mapping(driver):

    # login_page = GRCLoginPage(driver)
    # username   = get_str("auth", "username", "")
    # password   = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)
    # print("✓ Logged in successfully")

    page = LWFStatutoryMapping(driver)
    page.add_LWF_statutory_mapping()
    print("✓ ESI Statutory Mapping completed successfully")
