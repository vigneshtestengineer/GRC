import pytest
import time
from pages.grc_login_page import GRCLoginPage
from config.config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

@pytest.mark.smoke
def test_valid_login(driver):
    """Test valid login"""
    login_page = GRCLoginPage(driver)
    
    username = Config.USERNAME
    password = Config.PASSWORD
    group_name = Config.GROUP

    login_page.login(username, password, group_name)




    