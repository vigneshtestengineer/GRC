import pytest
from pages.login.grc_login_page import GRCLoginPage
from pages.cgm.Work_Order_Master import WorkOrderMaster
from utilities.json_config import get_str

MODULE_NAME = "Work Order Master"

@pytest.mark.e2e
def test_work_order_master(driver):
    # login_page = GRCLoginPage(driver)
    # username = get_str("auth", "username", "")
    # password = get_str("auth", "password", "")
    # group_name = get_str("auth", "group", "")
    # login_page.login(username, password, group_name)

    page = WorkOrderMaster(driver)
    page.add_workorder_master()
    print("✓ Work Order Master creation completed successfully")
