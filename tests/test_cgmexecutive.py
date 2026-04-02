import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.grc_login_page import GRCLoginPage
from pages.cgmexecutive import CGMExecutivePage
from config.config import Config

@pytest.mark.regression
def test_open_general_master_executive(driver):
    """Verify the General Master-Executive flow opens and performs the expected selections."""
    login_page = GRCLoginPage(driver)

    username = Config.USERNAME
    password = Config.PASSWORD
    group_name = Config.GROUP

    captcha_text = login_page.get_captcha_text()
    login_page.login(username, password, group_name, captcha_text)

    executive_page = CGMExecutivePage(driver)
    executive_page.open_general_master_executive()

    assert driver.current_url == CGMExecutivePage.EXECUTIVE_URL
    assert driver.find_element(*CGMExecutivePage.SEARCH_INPUT).get_attribute("value") == "Pure value"
