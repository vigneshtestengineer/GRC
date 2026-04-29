import pytest
from pages.cgm.Approve_Approval_settings import Approve_Approval_Settings


@pytest.mark.e2e
def test_approve_approval_settings():
    """Approve the queued approval settings as Approver in a dedicated Firefox browser.
    PASS — 'Approved Successfully' toast appears.
    FAIL — error toast appears or any exception is raised.
    """
    approve_page = Approve_Approval_Settings()
    print("✓ Firefox browser opened for approver session")

    try:
        approve_page.approve_and_open_cgm()
        print("✓ Approval completed successfully")
        approve_page.sleep(2)
    except Exception as exc:
        pytest.fail(f"Approval failed: {exc}")
    finally:
        approve_page.quit_cgm_browser()
        print("✓ Firefox browser closed")
        approve_page.sleep(2)
