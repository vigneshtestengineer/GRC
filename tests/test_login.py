import pytest
import time
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

@pytest.mark.smoke
def test_valid_login(driver):
    """Test valid login"""
    login_page = GRCLoginPage(driver)
    
    username = get_str("auth", "username", "")
    password = get_str("auth", "password", "")
    group_name = get_str("auth", "group", "")

    login_page.login(username, password, group_name)




    
