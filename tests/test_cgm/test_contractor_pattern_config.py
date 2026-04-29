import pytest
from pages.cgm.Contractor_Pattern_Config import ContractorPatternConfig


@pytest.mark.e2e
def test_contractor_pattern_config(driver):
    """Navigate to Contractor Pattern Configuration:
    Login → CGM Executive → Legal Entity → General Master → Pattern Configuration → Contractor
    """
    page = ContractorPatternConfig(driver)
    print("✓ ContractorPatternConfig page initialized")

    page.navigate_to_contractor_config()
    print("✓ Contractor Pattern Configuration page opened successfully")
