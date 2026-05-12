import pytest
from pages.cgm.Contract_Labour_Master import ContractLabourMaster
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Contract Labour Master"

@pytest.mark.e2e
def test_contract_labour_master(driver):

    # """Login then add a new Contractor Master record."""
    # login_page = GRCLoginPage(driver)
    # username = get_str("auth", "username", "")
    # password = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)

    page = ContractLabourMaster(driver)
    page.add_contract_labour_master()
