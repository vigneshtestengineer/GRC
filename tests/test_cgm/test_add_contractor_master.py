import pytest
from pages.login.grc_login_page import GRCLoginPage
from pages.cgm.Add_Contractor_Master import AddContractorMaster
from utilities.json_config import get_str


@pytest.mark.e2e
def test_add_contractor_master(driver):
    # """Login then add a new Contractor Master record."""
    # login_page = GRCLoginPage(driver)
    # username = get_str("auth", "username", "")
    # password = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)

    contractor_page = AddContractorMaster(driver)
    contractor_page.add_contractor_master()
