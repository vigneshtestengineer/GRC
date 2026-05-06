from pages.base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.json_config import get_str

# LEGAL_ENTITY = get_str("auth", "legal_entity", "")

CONTRACTOR_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Contractor_Master_Data.json"
)
UNIT_MASTER_DATA_FILE = (
    Path(__file__).resolve().parents[2] / "config" / "Unit_Master_Data.json"
)


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class AddContractorMaster(BasePage):

    # # ── CGM Navigation ────────────────────────────────────────────────────────
    # MENU_BUTTON                = (By.XPATH, "//button[.//mat-icon[text()='apps']]")
    # GENERAL_MASTER_EXEC_CARD   = (By.XPATH, "//mat-card[span[text()='General Master-Executive']]")
    # EXECUTIVE_URL              = "http://13.203.6.58:5002/#/home/welcome"
    # SEARCH_LEGAL_ENTITY        = (By.XPATH, "//input[@placeholder='Search here...' and contains(@class,'mat-input-element')]")
    # SELECT_LEGAL_ENTITY_ROW    = (By.XPATH, "//table//tbody//tr[1]//td")
    # SELECT_LEGAL_ENTITY_BUTTON = (By.XPATH, "//button[contains(@class,'mat-flat-button') and .//mat-icon[@data-mat-icon-name='plus']]")

    # ── Sidebar ───────────────────────────────────────────────────────────────
    OPEN_GENERAL_MASTER_MENU     = (By.XPATH, "//span[normalize-space()='General Master(s)']")
    CLICK_CONTRACTOR_MASTER_MENU = (By.XPATH, "//span[normalize-space()='Contractor Master']")

    # ── Contractor Master form ────────────────────────────────────────────────
    SPLASH_SCREEN_OVERLAY      = (By.TAG_NAME, "compfie-splash-screen")
    ADD_CONTRACTOR_BTN         = (By.XPATH, "//button[.//span[contains(@class,'mat-button-wrapper') and contains(normalize-space(),'Add')]]")
    CLICK_UNIT_DROPDOWN        = (By.XPATH, "//span[normalize-space()='Choose Unit']")
    DROPDOWN_SEARCH            = (By.XPATH, "//input[@aria-label='dropdown search']")
    CLICK_SHOW_DETAILS         = (By.XPATH, "//button[.//mat-icon[normalize-space()='sort'] and .//span[contains(.,'Show Detail')]]")

    # Contractor Information
    ENTER_CONTRACTOR_CODE      = (By.XPATH, "//input[@maxlength='50']")
    ENTER_CONTRACTOR_NAME      = (By.XPATH, "(//input[@maxlength='250'])[1]")
    ENTER_ADDRESS_1            = (By.XPATH, "(//textarea[@maxlength='450'])[1]")
    ENTER_ADDRESS_2            = (By.XPATH, "(//textarea[@maxlength='450'])[2]")
    CLICK_STATE_DROPDOWN       = (By.XPATH, "(//span[normalize-space()='Choose State'])[1]")
    CLICK_CITY_DROPDOWN        = (By.XPATH, "(//span[normalize-space()='Choose City'])[1]")
    ENTER_PINCODE              = (By.XPATH, "(//input[@maxlength='6'])[1]")
    ENTER_MOBILE_NUMBER        = (By.XPATH, "(//input[@maxlength='10'])[1]")
    ENTER_CONTRACTOR_EMAIL     = (By.XPATH, "(//input[@maxlength='75'])[1]")
    ENTER_CONTRACTOR_SHORT_NAME= (By.XPATH, "(//input[@maxlength='4'])[1]")
    ENABLE_ACCESS_FOR          = (By.XPATH, "(//div[contains(@class,'mat-select-value')])[7]")
    ENTER_ESTABLISHMENT_NAME   = (By.XPATH, "//mat-form-field[.//label[contains(.,'Establishment Name')]]//input")
    ENTER_ESTABLISHMENT_TYPE   = (By.XPATH, "//mat-form-field[.//label[contains(.,'Establishment Type')]]//input")
    ESTABLISHMENT_ADDR_SAME    = (By.XPATH, "//mat-checkbox[.//span[contains(.,'establishment address')]]")
    PERMANENT_ID_CARD_CHECKBOX = (By.XPATH, "((//span[contains(@class,'mat-checkbox-inner-container')])[5])")
    LEAVE_ACCOUNTING_DROPDOWN  = (By.XPATH, "//p[normalize-space()='Leave Accounting Period']")
    SELECT_LEAVE_ACCOUNTING    = (By.XPATH, "//label[contains(.,'Leave Acounting period based on DOJ')]")

    # Statutory Information
    STATUTORY_INFO_TAB         = (By.XPATH, "//span[normalize-space()='STATUTORY INFORMATION']")
    ENTER_NATURE_OF_WORK       = (By.XPATH, "(//input[@maxlength='150'])[1]")
    ENTER_PF_CODE              = (By.XPATH, "//mat-form-field[.//label[contains(.,'PF')]]//input")
    ENTER_ESI_CODE             = (By.XPATH, "//mat-form-field[.//label[contains(.,'ESI')]]//input")

    SAVE_BTN                   = (By.XPATH, "//button[.//span[normalize-space()='Submit as save']]")

    def __init__(self, driver):
        super().__init__(driver)
        self._contractor_data = _load_json(CONTRACTOR_DATA_FILE)
        self._unit_data       = _load_json(UNIT_MASTER_DATA_FILE)
        self._ci  = self._contractor_data.get("Contractor_Information", {})
        self._si  = self._contractor_data.get("Statutory_Information", {})
        self._unit_name = self._unit_data.get("Unit_Details", {}).get("unit_name", "")
        _ura = self._unit_data.get("Unit_Rights_Allocation", {})
        self._cgm_exe   = _ura.get("CGM_EXE", "")
        self._cgm_admin = _ura.get("CGM_ADMIN", "")

        contractor_name       = self.generate_contractor_name()
        contractor_code       = self.generate_contractor_code()
        contractor_short_name = self.generate_contractor_short_name()
        pf_code = self.generate_contractor_PF_code()
        esi_code = self.generate_contractor_ESI_code()

        self._save_generated_contractor_data(contractor_name, contractor_code, contractor_short_name, pf_code, esi_code)

        self._ci["Contractor_Name"]       = contractor_name
        self._ci["Contractor_Code"]       = contractor_code
        self._ci["Contractor_Short_Name"] = contractor_short_name
        self._si["PF_CODE"] = pf_code
        self._si["ESI_CODE"] = esi_code

        self.logger.info(
            "AddContractorMaster initialized — unit: '%s', name: '%s', code: '%s', short: '%s'",
            self._unit_name, contractor_name, contractor_code, contractor_short_name,
        )

    def _save_generated_contractor_data(self, name: str, code: str, short_name: str, pf_code: str, esi_code: str):
        try:
            with open(CONTRACTOR_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
                data = {}

        ci = data.setdefault("Contractor_Information", {})
        ci["Contractor_Name"]       = name
        ci["Contractor_Code"]       = code
        ci["Contractor_Short_Name"] = short_name

        si = data.setdefault("Statutory_Information", {})
        si["PF_CODE"]  = pf_code
        si["ESI_CODE"] = esi_code

        with open(CONTRACTOR_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            f.write("\n")

        self.logger.info(
            "Saved to %s — name: '%s', code: '%s', short: '%s', PF: '%s', ESI: '%s'",
            CONTRACTOR_DATA_FILE, os.name, code, short_name, pf_code, esi_code,
    )

    # # ── Step 1: Open CGM Executive ────────────────────────────────────────────
    # def open_cgm_executive(self):
    #     self.wait_for_element_to_be_clickable(self.MENU_BUTTON, timeout=30)
    #     self.click(self.MENU_BUTTON)
    #     self.logger.info("Clicked app-switcher menu.")

    #     previous_windows = self.driver.window_handles
    #     self.wait_for_element_to_be_clickable(self.GENERAL_MASTER_EXEC_CARD, timeout=8)
    #     self.click(self.GENERAL_MASTER_EXEC_CARD)
    #     self._switch_to_new_window(previous_windows)

    #     WebDriverWait(self.driver, 20).until(EC.url_contains(self.EXECUTIVE_URL))
    #     self.logger.info("CGM Executive tab active.")

    #     self.wait_for_element(self.SEARCH_LEGAL_ENTITY, timeout=10)
    #     self.enter_text(self.SEARCH_LEGAL_ENTITY, LEGAL_ENTITY)
    #     WebDriverWait(self.driver, 10).until(
    #         lambda d: d.find_element(*self.SEARCH_LEGAL_ENTITY)
    #                    .get_attribute("value").strip() == LEGAL_ENTITY
    #     )
    #     self._select_legal_entity()

    #     self.wait_for_element_to_be_clickable(self.SELECT_LEGAL_ENTITY_BUTTON, timeout=8)
    #     self.scroll_to_element(self.SELECT_LEGAL_ENTITY_BUTTON)
    #     self.click(self.SELECT_LEGAL_ENTITY_BUTTON)
    #     self.logger.info("Legal entity selected and confirmed.")

    # def _switch_to_new_window(self, previous_windows):
    #     try:
    #         WebDriverWait(self.driver, 10).until(
    #             lambda d: len(d.window_handles) > len(previous_windows)
    #         )
    #         new = [h for h in self.driver.window_handles if h not in previous_windows]
    #         if new:
    #             self.driver.switch_to.window(new[-1])
    #             self.logger.info("Switched to new CGM Executive window.")
    #     except Exception:
    #         self.logger.info("No new window opened — continuing in current window.")

    # def _select_legal_entity(self):
    #     for attempt in range(1, 3):
    #         self.wait_for_element(self.SELECT_LEGAL_ENTITY_ROW, timeout=8)
    #         self.scroll_to_element(self.SELECT_LEGAL_ENTITY_ROW)
    #         row = self.find_element(self.SELECT_LEGAL_ENTITY_ROW)
    #         try:
    #             row.click()
    #         except Exception:
    #             self.driver.execute_script("arguments[0].click();", row)
    #         try:
    #             WebDriverWait(self.driver, 5).until(
    #                 lambda d: not d.find_element(*self.SELECT_LEGAL_ENTITY_BUTTON).get_attribute("disabled")
    #             )
    #             self.logger.info("Legal entity row selected (attempt %d).", attempt)
    #             return
    #         except Exception:
    #             self.logger.warning("Legal entity click attempt %d did not enable button.", attempt)
    #     raise RuntimeError("Legal entity row was clicked but the select button did not become enabled.")

    # ── Step 1: Navigate to Contractor Master ─────────────────────────────────
    def navigate_to_contractor_master(self):
        if not self.is_element_visible(self.CLICK_CONTRACTOR_MASTER_MENU, timeout=2):
            self.click(self.OPEN_GENERAL_MASTER_MENU, timeout=10)
            self.wait_for_element_to_be_clickable(self.CLICK_CONTRACTOR_MASTER_MENU, timeout=8)
        self.click(self.CLICK_CONTRACTOR_MASTER_MENU, timeout=10)
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN_OVERLAY, timeout=15)
        self.logger.info("Navigated to Contractor Master.")

    # ── Step 3: Select unit ───────────────────────────────────────────────────
    def _select_unit(self):
        self.click(self.CLICK_UNIT_DROPDOWN, timeout=10)
        self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
        self.enter_text(self.DROPDOWN_SEARCH, self._unit_name)
        self.sleep(0.5)
        self.click(
            (By.XPATH, f"//mat-option//span[contains(text(),'{self._unit_name}')]"),
            timeout=8,
        )
        self.logger.info("Unit selected: '%s'", self._unit_name)

    # ── Step 4: Fill Contractor Information ───────────────────────────────────
    def fill_contractor_information(self):
        ci = self._ci
        self.enter_text(self.ENTER_CONTRACTOR_CODE, ci.get("Contractor_Code", ""))
        self.enter_text(self.ENTER_CONTRACTOR_NAME, ci.get("Contractor_Name", ""))
        self.enter_text(self.ENTER_ADDRESS_1, ci.get("Contactor_Addreess_1", ""))
        self.enter_text(self.ENTER_ADDRESS_2, ci.get("Contractor_Address_2", ""))

        state = ci.get("State", "")
        if state:
            self.click(self.CLICK_STATE_DROPDOWN, timeout=10)
            self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
            self.enter_text(self.DROPDOWN_SEARCH, state)
            self.sleep(0.4)
            self.click(
                (By.XPATH, f"//mat-option//span[normalize-space()='{state}']"), timeout=8
            )

        city = ci.get("City", "")
        if city:
            self.click(self.CLICK_CITY_DROPDOWN, timeout=10)
            self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)
            self.enter_text(self.DROPDOWN_SEARCH, city)
            self.sleep(0.4)
            self.click(
                (By.XPATH, f"//mat-option//span[normalize-space()='{city}']"), timeout=8
            )

        self.enter_text(self.ENTER_PINCODE, ci.get("Pin_Code", ""))
        self.enter_text(self.ENTER_MOBILE_NUMBER, ci.get("Mobile_Number", ""))
        self.enter_text(self.ENTER_CONTRACTOR_EMAIL, ci.get("Email", ""))
        self.enter_text(self.ENTER_CONTRACTOR_SHORT_NAME, ci.get("Contractor_Short_Name", ""))

        self.click(self.ENABLE_ACCESS_FOR, timeout=10)
        self.wait_for_element(self.DROPDOWN_SEARCH, timeout=8)

        self.enter_text(self.DROPDOWN_SEARCH, self._cgm_exe)
        self.sleep(0.4)
        self.click((By.XPATH, f"//mat-option[.//span[contains(.,'{self._cgm_exe}')]]"), timeout=8)
        self.logger.info("Access For — selected CGM_EXE: '%s'", self._cgm_exe)

        self.enter_text(self.DROPDOWN_SEARCH, self._cgm_admin)
        self.sleep(0.4)
        self.click((By.XPATH, f"//mat-option[.//span[contains(.,'{self._cgm_admin}')]]"), timeout=8)
        self.logger.info("Access For — selected CGM_ADMIN: '%s'", self._cgm_admin)
        self.sleep(0.5)
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        self.sleep(0.5)
        self.scroll_to_element(self.ENTER_ESTABLISHMENT_NAME)
        self.enter_text(self.ENTER_ESTABLISHMENT_NAME, ci.get("Establishment_Name", ""))
        self.enter_text(self.ENTER_ESTABLISHMENT_TYPE, ci.get("Establishment_Type", ""))
        self.click(self.ESTABLISHMENT_ADDR_SAME)
        self.click(self.PERMANENT_ID_CARD_CHECKBOX)

        self.click(self.LEAVE_ACCOUNTING_DROPDOWN, timeout=10)
        self.click(self.SELECT_LEAVE_ACCOUNTING, timeout=8)
        self.logger.info("Contractor Information filled.")
        self.sleep(2)
    # ── Step 5: Fill Statutory Information ───────────────────────────────────
    def fill_statutory_information(self):
        si = self._si
        self.click(self.STATUTORY_INFO_TAB, timeout=10)
        self.wait_for_element_to_be_clickable(self.ENTER_NATURE_OF_WORK, timeout=10)
        self.enter_text(self.ENTER_NATURE_OF_WORK, si.get("Nature_of_Work", ""))
        self.enter_text(self.ENTER_PF_CODE, si.get("PF_CODE", ""))
        self.enter_text(self.ENTER_ESI_CODE, si.get("ESI_CODE", ""))
        self.logger.info("Statutory Information filled.")

    # ── Public orchestration ──────────────────────────────────────────────────
    def add_contractor_master(self):
        self.logger.info("=== Add Contractor Master flow started ===")
        self.navigate_to_contractor_master()
        self.click(self.ADD_CONTRACTOR_BTN, timeout=20)
        self._select_unit()
        self.click(self.CLICK_SHOW_DETAILS, timeout=10)
        self.fill_contractor_information()
        self.fill_statutory_information()
        self.click(self.SAVE_BTN, timeout=10)
        self.sleep(0.5)
        self.click(self.SAVE_BTN, timeout=10)
        self.sleep(2)
        self.driver.refresh()
        self.sleep(2)
        self.wait_for_element_to_disappear(self.SPLASH_SCREEN_OVERLAY, timeout=15)
        self.logger.info("Page refreshed after save.")
        self.logger.info("=== Add Contractor Master flow completed ===")
