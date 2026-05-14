import pytest
from pages.cgm.statutory_mapping.PF_Statutory_mapping import PFStatutoryMapping
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "PF Statutory Mapping"

@pytest.mark.e2e
def test_pf_statutory_mapping(driver):

    # login_page = GRCLoginPage(driver)
    # username   = get_str("auth", "username", "")
    # password   = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)
    # print("✓ Logged in successfully")

    page = PFStatutoryMapping(driver)
    page.add_pf_statutory_mapping()
