import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login.grc_login_page import GRCLoginPage
from pages.cgm.unit_master import unit_Master
from utilities.json_config import get_str

@pytest.mark.regression
def test_open_general_master_executive(driver):
    """Verify the General Master-Executive flow opens and performs the expected selections."""
    login_page = GRCLoginPage(driver)

    username = get_str("auth", "username", "")
    password = get_str("auth", "password", "")
    group_name = get_str("auth", "group", "")

    login_page.login(username, password, group_name)

    executive_page = unit_Master(driver)
    executive_page.open_general_master_executive()
    executive_page.general_master_menu()
    executive_page.create_unit_master()

    assert driver.current_url == unit_Master.EXECUTIVE_URL
    assert driver.find_element(*unit_Master.SEARCH_LEGALENTITY).get_attribute("value") == "Pure value"
