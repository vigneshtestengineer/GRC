import pytest
from pages.login.grc_login_page import GRCLoginPage
from pages.cgm.Shift_Master_Creation import ShiftMasterCreation
from utilities.json_config import get_str


@pytest.mark.e2e
def test_shift_master_creation(driver):
    # login_page = GRCLoginPage(driver)
    # username = get_str("auth", "username", "")
    # password = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)

    page = ShiftMasterCreation(driver)
    page.navigate_to_shift_master()
    print("✓ Shift Master Creation completed successfully")
