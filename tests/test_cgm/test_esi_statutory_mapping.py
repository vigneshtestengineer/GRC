import pytest
from pages.cgm.statutory_mapping.ESI_Statutory_mapping import ESIStatutoryMapping
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "ESI Statutory Mapping"

@pytest.mark.e2e
def test_esi_statutory_mapping(driver):
    """Login → CGM Executive → Statutory Master(s) → Statutory Mapping → ESI Statutory Mapping.

    Full flow:
      1. Login via GRC login page (CAPTCHA handled automatically)
      2. Open CGM Executive via app-switcher and select legal entity
      3. Navigate: Statutory Master(s) → Statutory Mapping
      4. Click Add, select State & Unit, enable ESI Statutory Mapping, configure settings, save
    """
    login_page = GRCLoginPage(driver)
    username   = get_str("auth", "username", "")
    password   = get_str("auth", "password", "")
    group_name = get_str("auth", "group", "")
    login_page.login(username, password, group_name)
    print("✓ Logged in successfully")

    page = ESIStatutoryMapping(driver)
    page.add_ESI_statutory_mapping()
    print("✓ ESI Statutory Mapping completed successfully")
