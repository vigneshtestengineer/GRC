import pytest
from pages.login.grc_login_page import GRCLoginPage
from pages.cgm.unit_master import unit_Master
from pages.cgm.Approval_settings_creation import ApprovalSettingsCreation, UNIT_NAME
from utilities.json_config import get_str


@pytest.mark.e2e
def test_create_approval_settings(driver):
    """Test approval settings creation flow: Login -> CGM -> Approval Settings"""

    # Step 1: Login to the application
    login_page = GRCLoginPage(driver)
    username = get_str("auth", "username", "")
    password = get_str("auth", "password", "")
    group_name = get_str("auth", "group", "")

    login_page.login(username, password, group_name)
    print(f"✓ Successfully logged in")

    # Step 2: Open CGM (General Master-Executive)
    cgm_page = unit_Master(driver)
    cgm_page.open_general_master_executive()
    print(f"✓ Opened General Master-Executive")

    # Step 3: Navigate to Approval Settings Creation
    approval_settings_page = ApprovalSettingsCreation(driver)
    print(f"✓ Approval Settings page initialized")

    # Step 4: Create approval settings
    # Unit name is automatically loaded from Unit_Master_Data.json
    approval_settings_page.create_approval_settings({})
    print(f"✓ Created approval settings for unit: {UNIT_NAME}")

    # Step 5: Save the approval settings
    approval_settings_page.save_approval_settings()
    print(f"✓ Approval settings saved successfully")

