import pytest
from pages.cgm.Approval_settings_creation import ApprovalSettingsCreation
from pages.login.grc_login_page import GRCLoginPage
from utilities.json_config import get_str

MODULE_NAME = "Approval Settings"

@pytest.mark.e2e
def test_create_approval_settings(driver):

    approval_settings_page = ApprovalSettingsCreation(driver)
    print(f"✓ Approval Settings page initialized")

    approval_settings_page.create_approval_settings({})
    print(f"✓ Created approval settings")

