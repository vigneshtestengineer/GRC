import pytest
from pages.cgm.Approval_settings_creation import ApprovalSettingsCreation


@pytest.mark.e2e
def test_create_approval_settings(driver):
    """Test approval settings creation (continues session from unit_master — already inside CGM app)"""

    approval_settings_page = ApprovalSettingsCreation(driver)
    print(f"✓ Approval Settings page initialized")

    approval_settings_page.create_approval_settings({})
    print(f"✓ Created approval settings")

