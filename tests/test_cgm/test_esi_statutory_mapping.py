import pytest
from pages.cgm.statutory_mapping.ESI_Statutory_mapping import ESIStatutoryMapping
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "ESI Statutory Mapping"

@pytest.mark.e2e
def test_esi_statutory_mapping(driver):

    # login_page = GRCLoginPage(driver)
    # username   = get_str("auth", "username", "")
    # password   = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)
    # print("✓ Logged in successfully")

    page = ESIStatutoryMapping(driver)
    page.add_ESI_statutory_mapping()
    print("✓ ESI Statutory Mapping completed successfully")
