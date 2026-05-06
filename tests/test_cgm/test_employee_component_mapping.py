import pytest
from pages.login.grc_login_page import GRCLoginPage
from pages.cgm.Employee_Component_Mapping import EmployeeComponentMapping
from utilities.json_config import get_str


@pytest.mark.e2e
def test_employee_component_mapping(driver):
    # """Login → CGM Executive → General Master(s) → Component Mapping → Save.

    # Full flow:
    #   1. Login via GRC login page (CAPTCHA handled automatically)
    #   2. Open CGM Executive via app-switcher and select legal entity
    #   3. Expand General Master(s) → Component Mapping
    #   4. Click Add, select Unit, select Contractor, show details, save
    # """
    # login_page = GRCLoginPage(driver)
    # username   = get_str("auth", "username", "")
    # password   = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)
    # print("✓ Logged in successfully")

    page = EmployeeComponentMapping(driver)
    page.navigate_to_component_mapping()
    print("✓ Employee Component Mapping completed successfully")
