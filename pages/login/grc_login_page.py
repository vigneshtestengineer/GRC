"""
GRC Login Page Object
---------------------
CAPTCHA strategy:
  1. CDP canvas interceptor — reads text from window._captchaText injected
                              before the page loads.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import os
import re
from datetime import datetime
from time import perf_counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base.base_page import BasePage
from utilities.captcha_helper import inject_captcha_interceptor, read_captcha_from_canvas
from utilities.json_config import get_path, get_str

# ── module-level constants ────────────────────────────────────────────────────
SCREENSHOT_DIR = get_path("paths", "captcha_image_dir", "reports/captchas")
LOGIN_URL      = get_str("app", "login_url", "http://13.203.6.58:5009/#/login")
REPORTS_DIR    = get_path("paths", "reports_dir", "reports")


class GRCLoginPage(BasePage):
    """Login page — handles credentials, CAPTCHA reading, and form submission."""

    # ── locators ──────────────────────────────────────────────────────────────
    USERNAME_INPUT       = (By.ID,    "Username")
    PASSWORD_INPUT       = (By.ID,    "password")
    GROUP_INPUT          = (By.ID,    "group_short_name")
    CAPTCHA_TEXTBOX      = (By.NAME,  "captcha")
    CAPTCHA_CANVAS       = (By.ID,    "captchaCanvas")
    CAPTCHA_BUTTONS      = (By.CLASS_NAME, "captcha-buttons")
    CAPTCHA_INPUT_XPATH  = (
        By.XPATH,
        "//input[@formcontrolname='captcha' or "
        "@placeholder[contains(translate(.,'CAPTCHA','captcha'),'captcha')]]",
    )
    # fallback locator list tried in order when CAPTCHA_CANVAS is not visible
    CAPTCHA_CANVAS_LOCATORS = [
        (By.ID,           "captchaCanvas"),
        (By.CSS_SELECTOR, "canvas[id*='captcha']"),
        (By.XPATH,
         "//input[@name='captcha']/ancestor::div[1]/following::canvas[1]"),
    ]
    INVALID_CAPTCHA_ERROR = (
        By.XPATH, "//mat-error[contains(text(),'Invalid Captcha')]"
    )
    CLOSE_POPUP_BUTTON   = (By.XPATH, "//button[normalize-space()='✕']")
    LOGIN_BUTTON         = (By.XPATH, "//button[@id='Sign In']")

    # ── init ──────────────────────────────────────────────────────────────────
    def __init__(self, driver):
        """
        Injects the canvas interceptor via CDP *before* the page loads,
        then navigates to the login URL so the interceptor captures every
        fillText / strokeText call made while rendering the CAPTCHA.
        """
        super().__init__(driver)
        # Inject BEFORE get() so the script runs on document creation
        inject_captcha_interceptor(driver, self.logger)
        self.driver.get(LOGIN_URL)
        # self.wait_for_page_load()

    # ── page lifecycle ────────────────────────────────────────────────────────
    def wait_for_page_load(self):
        """Wait until all three credential fields are present."""
        self.wait_for_element(self.USERNAME_INPUT)
        self.logger.info("Login page loaded successfully")

    # ── credential helpers ────────────────────────────────────────────────────
    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def enter_group_name(self, group_name):
        self.enter_text(self.GROUP_INPUT, group_name)

    def close_initial_popup(self):
        """Dismiss any modal that appears before login fields are usable."""
        if self.is_element_present(self.CLOSE_POPUP_BUTTON):
            self.click(self.CLOSE_POPUP_BUTTON)
            # self.wait_for_element_to_disappear(self.CLOSE_POPUP_BUTTON, timeout=5)
            self.logger.info("Closed initial popup before login")

    # ── CAPTCHA: primary — CDP canvas interceptor ─────────────────────────────
    def _get_captcha_from_canvas_interceptor(self, locator=None) -> str:
        """
        Read captcha text captured by the injected canvas interceptor.
        Returns empty string when nothing was captured yet.
        """
        return read_captcha_from_canvas(
            self.driver,
            self.logger,
            locator=locator or self.CAPTCHA_CANVAS,
        )

    # ── CAPTCHA: secondary — Angular native-setter injection ─────────────────
    def _write_captcha_via_angular_setter(self, field, text: str) -> bool:
        """
        Use the HTMLInputElement native setter + input event so Angular's
        reactive forms register the value correctly.
        Returns True if the field value matches after injection.
        """
        self.driver.execute_script(
            """
            var el     = arguments[0];
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input',  { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur',   { bubbles: true }));
            """,
            field,
            text,
        )
        return (field.get_attribute("value") or "").strip() == text

    def _reset_captcha_interceptor(self):
        """
        Clear the interceptor buffer so repeated CAPTCHA renders do not reuse stale text.
        """
        try:
            self.driver.execute_script("window._captchaText = '';"
            )
        except Exception:
            pass

    # ── public CAPTCHA API ────────────────────────────────────────────────────
    def get_captcha_text(self, popup_already_closed: bool = False) -> str:
        """
        Returns the CAPTCHA text using the CDP canvas interceptor only.
        Also saves the resolved text to reports/captchas/.
        """
        if not popup_already_closed:
            self.close_initial_popup()

        try:
            captcha_element, captcha_locator = self._locate_captcha_element(timeout=10)
        except RuntimeError as exc:
            self.logger.warning(
                "CAPTCHA element did not appear in time; cannot resolve CAPTCHA via canvas interceptor. %s",
                exc,
            )
            raise RuntimeError(
                "CAPTCHA element did not appear in time and canvas interceptor cannot read it."
            )

        if captcha_element.tag_name.lower() != "canvas":
            raise RuntimeError(
                "CAPTCHA is not rendered as a canvas element; canvas interceptor cannot read it."
            )

        text = self._get_captcha_from_canvas_interceptor(
            locator=captcha_locator,
        )
        if not text:
            raise RuntimeError(
                "Canvas interceptor did not capture any CAPTCHA text. "
                "Ensure the page draws the CAPTCHA using CanvasRenderingContext2D.fillText/strokeText."
            )

        self.logger.info("CAPTCHA resolved via CDP interceptor: '%s'", text)
        self._save_captcha_text(text)
        return text

    def enter_captcha(self, captcha_text: str):
        """
        Types the CAPTCHA value into the input field.
        Tries native send_keys first; falls back to the Angular native-setter
        injection when the field value does not match after send_keys.
        """
        if not captcha_text or not str(captcha_text).strip():
            raise ValueError("Captcha text is empty.")

        captcha_text = str(captcha_text).strip()
        self.wait_for_element(self.CAPTCHA_TEXTBOX, timeout=5)

        for attempt in range(1, 4):
            field = self.driver.find_element(*self.CAPTCHA_TEXTBOX)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", field
            )

            # try regular keyboard input first
            try:
                field.click()
                field.clear()
                field.send_keys(Keys.CONTROL, "a")
                field.send_keys(Keys.DELETE)
                field.send_keys(captcha_text)
            except Exception:
                pass

            if (field.get_attribute("value") or "").strip() == captcha_text:
                self.logger.info(f"Captcha entered (send_keys): '{captcha_text}'")
                return

            # Angular native-setter fallback
            if self._write_captcha_via_angular_setter(field, captcha_text):
                self.logger.info(
                    f"Captcha entered (Angular setter): '{captcha_text}'"
                )
                return

            self.logger.warning(
                "Captcha input attempt %d/3 failed (expected '%s')",
                attempt, captcha_text,
            )
            self.sleep(0.2)

        raise RuntimeError(
            f"Could not enter captcha '{captcha_text}' after 3 attempts."
        )

    # ── login orchestration ───────────────────────────────────────────────────
    def click_login_button(self):
        # self.wait_for_element(self.CAPTCHA_TEXTBOX, timeout=5)
        # self.wait.until(
        #     lambda d: d.find_element(
        #         *self.CAPTCHA_TEXTBOX
        #     ).get_attribute("value").strip()
        # )
        self.wait_for_element_to_be_clickable(self.LOGIN_BUTTON, timeout=10)
        self.scroll_to_element(self.LOGIN_BUTTON)
        self.click(self.LOGIN_BUTTON, timeout=10)

    def _is_invalid_captcha_displayed(self, timeout: int = 3) -> bool:
        end = datetime.now().timestamp() + timeout
        while datetime.now().timestamp() < end:
            for el in self.driver.find_elements(*self.INVALID_CAPTCHA_ERROR):
                try:
                    if el.is_displayed():
                        return True
                except Exception:
                    pass
            self.sleep(0.2)
        return False

    def login(self, username: str, password: str, group_name: str,
              captcha_text: str = None):
        """
        Full login sequence.  Retries up to 5 times on Invalid-Captcha errors.
        """
        self.logger.info(f"Logging in as: {username}")
        self.close_initial_popup()
        self.enter_username(username)
        self.enter_password(password)
        self.enter_group_name(group_name)

        max_attempts    = 5
        current_captcha = captcha_text

        for attempt in range(1, max_attempts + 1):
            if not current_captcha:
                current_captcha = self.get_captcha_text(popup_already_closed=True)

            self.logger.info(
                "Login attempt %d/%d — captcha: '%s'",
                attempt, max_attempts, current_captcha,
            )
            self.enter_captcha(current_captcha)
            self.wait.until(
                lambda d: d.find_element(
                    *self.CAPTCHA_TEXTBOX
                ).get_attribute("value").strip() == current_captcha
            )
            # self.sleep(1)
            self.click_login_button()
            # self.sleep(1)

            if self._is_invalid_captcha_displayed(timeout=3):
                self.logger.warning(
                    "Invalid Captcha on attempt %d/%d — retrying.",
                    attempt, max_attempts,
                )
                if attempt == max_attempts:
                    raise RuntimeError(
                        f"Login failed after {max_attempts} attempts "
                        "(repeated Invalid Captcha)."
                    )
                self._reset_captcha_interceptor()
                current_captcha = None
                continue

            self.logger.info("Login successful.")
            return

    def _is_valid_captcha(self, text: str) -> bool:
        return (bool(text)
                and 4 <= len(text) <= 8
                and text.isascii()
                and all(c.isalnum() for c in text))

    # ── captcha element locator ───────────────────────────────────────────────
    def _locate_captcha_element(self, timeout: int = 4):
        end = datetime.now().timestamp() + timeout
        while datetime.now().timestamp() < end:
            for loc in self.CAPTCHA_CANVAS_LOCATORS:
                for el in self.driver.find_elements(*loc):
                    try:
                        size = el.size or {}
                        if (el.is_displayed()
                                and size.get("width", 0) > 0
                                and size.get("height", 0) > 0):
                            self.logger.info(f"CAPTCHA element found via: {loc}")
                            return el, loc
                    except Exception:
                        pass
            self.sleep(0.2)
        raise RuntimeError(
            "CAPTCHA canvas element not found. "
            f"Tried: {self.CAPTCHA_CANVAS_LOCATORS}"
        )

    # ── file helpers ──────────────────────────────────────────────────────────
    def _ensure_captcha_dir(self) -> str:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        return SCREENSHOT_DIR

    def _save_captcha_text(self, text: str, prefix: str = "captcha_text") -> str:
        captcha_dir = self._ensure_captcha_dir()
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filepath = os.path.join(captcha_dir, f"{prefix}_{ts}.txt")
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(text)
        self.logger.info(f"Saved captcha text: {filepath}")
        return filepath
