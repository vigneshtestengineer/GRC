from selenium.webdriver.common.by import By
import sys
import os
from io import BytesIO
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base_page import BasePage
from config.config import Config
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from pytesseract import TesseractNotFoundError


class GRCLoginPage(BasePage):
    """Login page object class"""

    # Locators
    USERNAME_INPUT = (By.ID, "Username")
    PASSWORD_INPUT = (By.ID, "password")
    GROUP_INPUT = (By.ID, "group_short_name")
    CAPTCHA_TEXTBOX = (By.NAME, "captcha")
    CAPTCHA_IMG = (By.ID, "captchaCanvas")
    CAPTCHA_IMAGE_LOCATORS = [
        (By.ID, "captchaCanvas"),
        (By.CSS_SELECTOR, "canvas[id*='captcha']"),
        (By.CSS_SELECTOR, "img[id*='captcha']"),
        (By.CSS_SELECTOR, "img[src*='captcha']"),
        (By.XPATH, "//input[@name='captcha']/ancestor::div[1]/following::canvas[1]"),
        (By.XPATH, "//input[@name='captcha']/ancestor::div[1]/following::img[1]"),
    ]
    CLOSE_POPUP_BUTTON = (By.XPATH, "//button[normalize-space()='✕']")
    LOGIN_BUTTON = (By.XPATH, "//button[@id='Sign In']")

    def __init__(self, driver):
        """Initialize login page"""
        super().__init__(driver)
        self.driver.get(Config.LOGIN_URL)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for login page to load"""
        self.wait_for_element(self.USERNAME_INPUT)
        self.wait_for_element(self.PASSWORD_INPUT)
        self.wait_for_element(self.GROUP_INPUT)
        self.logger.info("Login page loaded successfully")

    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)
        self.wait.until(
            lambda d: d.find_element(*self.USERNAME_INPUT).get_attribute("value").strip() == username
        )

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)
        self.wait.until(
            lambda d: d.find_element(*self.PASSWORD_INPUT).get_attribute("value").strip() == password
        )

    def enter_group_name(self, group_name):
        self.enter_text(self.GROUP_INPUT, group_name)
        self.wait.until(
            lambda d: d.find_element(*self.GROUP_INPUT).get_attribute("value").strip() == group_name
        )

    def close_initial_popup(self):
        """
        Closes any initial popup or modal before starting the login process.
        """
        if self.is_element_present(self.CLOSE_POPUP_BUTTON):
            self.click(self.CLOSE_POPUP_BUTTON)
            self.wait_for_element_to_disappear(self.CLOSE_POPUP_BUTTON, timeout=5)
            self.logger.info("Closed initial popup before login")

    def enter_captcha(self, captcha_text):
        if not captcha_text or not captcha_text.strip():
            raise ValueError("Captcha text is empty; OCR did not return a valid value.")
        self.enter_text(self.CAPTCHA_TEXTBOX, captcha_text)
        self.wait.until(
            lambda d: d.find_element(*self.CAPTCHA_TEXTBOX).get_attribute("value").strip() == captcha_text
        )

    def _is_usable_captcha_element(self, element):
        try:
            size = element.size or {}
            return (
                element.is_displayed()
                and size.get("width", 0) > 0
                and size.get("height", 0) > 0
            )
        except Exception:
            return False

    def _locate_captcha_element(self, timeout=4):
        end_time = datetime.now().timestamp() + timeout

        while datetime.now().timestamp() < end_time:
            for locator in self.CAPTCHA_IMAGE_LOCATORS:
                elements = self.driver.find_elements(*locator)
                for element in elements:
                    if self._is_usable_captcha_element(element):
                        self.logger.info(f"Using captcha element located by: {locator}")
                        return element
            self.sleep(0.2)

        raise RuntimeError(
            "Captcha image was not found on the login page. "
            f"Tried locators: {self.CAPTCHA_IMAGE_LOCATORS}"
        )

    def _prepare_captcha_image(self, image):
        image = image.convert("L")
        image = image.resize((image.width * 3, image.height * 3), Image.LANCZOS)
        image = ImageOps.autocontrast(image)
        image = image.filter(ImageFilter.MedianFilter(size=3))
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=2))
        image = image.point(lambda x: 0 if x < 170 else 255, mode='1')
        image = self._remove_noise_lines(image, line_threshold=0.62)
        image = image.filter(ImageFilter.MedianFilter(size=3))
        return image

    def _prepare_captcha_image_perfect(self, image):
        image = image.convert("L")
        image = image.resize((image.width * 4, image.height * 4), Image.LANCZOS)
        image = ImageOps.autocontrast(image, cutoff=1)
        image = ImageOps.equalize(image)
        image = image.filter(ImageFilter.MedianFilter(size=3))
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=1))
        image = image.filter(ImageFilter.MaxFilter(3))
        image = image.filter(ImageFilter.MedianFilter(size=3))
        image = self._remove_noise_lines(image, line_threshold=0.55)
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=1))
        image = image.point(lambda x: 0 if x < 170 else 255, mode='1')
        image = self._ensure_black_text_on_white_bg(image)
        return image

    def _prepare_captcha_image_enhanced(self, image):
        """Additional enhanced preprocessing for difficult captchas"""
        image = image.convert("L")
        image = image.resize((image.width * 3, image.height * 3), Image.LANCZOS)
        image = ImageOps.autocontrast(image, cutoff=2)
        image = image.filter(ImageFilter.UnsharpMask(radius=3, percent=300, threshold=1))
        image = image.filter(ImageFilter.MedianFilter(size=3))
        image = image.point(lambda x: 0 if x < 160 else 255, mode='1')
        image = self._remove_noise_lines(image, line_threshold=0.60)
        return image

    def _ensure_black_text_on_white_bg(self, image):
        if image.mode != "L":
            image = image.convert("L")
        width, height = image.size
        pixels = image.load()
        black_pixels = 0
        white_pixels = 0
        for y in range(height):
            for x in range(width):
                if pixels[x, y] == 0:
                    black_pixels += 1
                else:
                    white_pixels += 1
        if black_pixels < white_pixels:
            image = ImageOps.invert(image)
        return image

    def _remove_noise_lines(self, image, line_threshold=0.62):
        width, height = image.size
        pixels = image.load()

        for y in range(height):
            black_count = sum(1 for x in range(width) if pixels[x, y] == 0)
            if black_count / width > line_threshold:
                for x in range(width):
                    pixels[x, y] = 255

        for x in range(width):
            black_count = sum(1 for y in range(height) if pixels[x, y] == 0)
            if black_count / height > line_threshold:
                for y in range(height):
                    pixels[x, y] = 255

        return image

    def _is_valid_captcha_text(self, text):
        if not text:
            return False
        if len(text) < 4 or len(text) > 8:
            return False
        if not text.isascii():
            return False
        if not all(ch.isalpha() or ch.isdigit() for ch in text):
            return False
        return True

    def _extract_captcha_text(self, image, prefix):
        image_path = self._save_captcha_image(image, prefix)
        text = self._normalize_ocr_text(self._run_tesseract(image_path))
        self.logger.debug(f"OCR result for {prefix}: '{text}'")
        print(f"Captcha OCR candidate [{prefix}]: {text}")
        return text

    def _ensure_captcha_dir(self):
        captcha_dir = Config.CAPTCHA_IMAGE_DIR
        os.makedirs(captcha_dir, exist_ok=True)
        return captcha_dir

    def _save_captcha_image(self, image, prefix):
        captcha_dir = self._ensure_captcha_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{prefix}_{timestamp}.png"
        file_path = os.path.join(captcha_dir, filename)
        image.save(file_path)
        self.logger.info(f"Saved captcha image: {file_path}")
        return file_path

    def _save_captcha_text(self, text, prefix="captcha_text"):
        captcha_dir = self._ensure_captcha_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{prefix}_{timestamp}.txt"
        file_path = os.path.join(captcha_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        self.logger.info(f"Saved captcha text: {file_path}")
        return file_path

    def _save_captcha_debug_image(self, image, name):
        debug_dir = os.path.join(Config.REPORTS_DIR, "captcha_debug")
        os.makedirs(debug_dir, exist_ok=True)
        debug_file = os.path.join(debug_dir, f"{name}.png")
        image.save(debug_file)
        self.logger.debug(f"Saved captcha debug image: {debug_file}")
        return debug_file

    def _run_tesseract(self, image_path):
        ocr_configs = [
            (
                '--oem 3 --psm 8 '
                '-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
                '-c load_system_dawg=0 -c load_freq_dawg=0 -c user_defined_dpi=300 '
                '-c classify_bln_numeric_mode=1'
            ),
            (
                '--oem 3 --psm 7 '
                '-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
                '-c load_system_dawg=0 -c load_freq_dawg=0 -c user_defined_dpi=300'
            ),
            (
                '--oem 3 --psm 13 '
                '-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
                '-c load_system_dawg=0 -c load_freq_dawg=0 -c user_defined_dpi=300'
            ),
        ]
        image = Image.open(image_path).convert("L")
        results = []

        for config in ocr_configs:
            text = pytesseract.image_to_string(image, config=config).strip()
            normalized = self._normalize_ocr_text(text)
            if normalized:
                results.append(normalized)

        if not results:
            return ""

        return max(results, key=lambda item: (len(item), results.count(item)))

    def _normalize_ocr_text(self, text):
        replacements = {
            "|": "I",
            "!": "I",
            "$": "S",
            "O": "0",
            "Q": "0",
            "I": "1",
            "L": "1",
            "Z": "2",
            "S": "5",
            "B": "8",
        }
        normalized = ''.join(replacements.get(ch, ch) for ch in text if ch.isalnum() or ch in replacements)
        return normalized.upper()

    def get_captcha_text(self):
        """
        Captures the captcha image from the page and uses OCR to read the text.
        Returns:
            str: Captcha text recognized by Tesseract
        """
        self.close_initial_popup()
        self.wait_for_element(self.CAPTCHA_TEXTBOX, timeout=3)
        self.sleep(0.1)

        captcha_element = self._locate_captcha_element(timeout=4)
        captcha_png = captcha_element.screenshot_as_png

        original_image = Image.open(BytesIO(captcha_png))
        self._save_captcha_image(original_image, "captcha_original")

        preprocessed_image = self._prepare_captcha_image(original_image)
        self._save_captcha_image(preprocessed_image, "captcha_processed")

        if getattr(Config, "TESSERACT_CMD", None):
            tesseract_cmd = Config.TESSERACT_CMD
            if os.path.isdir(tesseract_cmd):
                tesseract_cmd = os.path.join(tesseract_cmd, "tesseract.exe")
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            if not os.path.isfile(tesseract_cmd):
                raise RuntimeError(
                    f"Tesseract executable not found at configured path: {tesseract_cmd}"
                )

        try:
            perfect_image = self._prepare_captcha_image_perfect(original_image)
            enhanced_image = self._prepare_captcha_image_enhanced(original_image)
            candidate_images = [
                ("perfect", perfect_image),
                ("enhanced", enhanced_image),
                ("perfect_inverted", ImageOps.invert(perfect_image)),
                ("processed", preprocessed_image),
                ("enhanced_inverted", ImageOps.invert(enhanced_image)),
                ("processed_inverted", ImageOps.invert(preprocessed_image.convert("L"))),
                ("grayscale", ImageOps.autocontrast(original_image.convert("L"))),
                ("equalized", ImageOps.equalize(original_image.convert("L"))),
                ("thresholded", original_image.convert("L").point(lambda x: 0 if x < 150 else 255, mode='1')),
                ("sharpened", original_image.convert("L").filter(ImageFilter.UnsharpMask(radius=2, percent=250, threshold=2))),
                ("original", original_image.convert("L"))
            ]

            captcha_text = None
            for prefix, image in candidate_images:
                candidate_text = self._extract_captcha_text(image, f"captcha_{prefix}")
                if self._is_valid_captcha_text(candidate_text):
                    captcha_text = candidate_text
                    print(f"Captcha OCR final choice [{prefix}]: {captcha_text}")
                    break
                self.logger.warning(
                    f"Captcha OCR produced invalid result from {prefix}: '{candidate_text}'"
                )

            if not captcha_text:
                fallback_candidates = []
                for prefix, image in candidate_images:
                    candidate_text = self._extract_captcha_text(image, f"captcha_fallback_{prefix}")
                    if candidate_text:
                        fallback_candidates.append(candidate_text)

                if fallback_candidates:
                    captcha_text = max(fallback_candidates, key=len)
                    self.logger.warning(
                        "Captcha OCR used best-effort fallback result: '%s'",
                        captcha_text,
                    )

            if not captcha_text:
                self._save_captcha_debug_image(original_image, "captcha_original")
                self._save_captcha_debug_image(preprocessed_image, "captcha_processed")
                self.logger.error(
                    "Captcha OCR failed to produce a valid text string. "
                    "Saved debug images to reports/captcha_debug."
                )
                raise RuntimeError(
                    "Captcha OCR returned invalid text. "
                    "Inspect debug images and adjust preprocessing."
                )
        except TesseractNotFoundError as exc:
            error_message = (
                "Tesseract OCR executable not found. "
                "Install Tesseract and add it to PATH, or set pytesseract.pytesseract.tesseract_cmd. "
                "See https://github.com/madmaze/pytesseract for installation details."
            )
            self.logger.error(error_message)
            raise RuntimeError(error_message) from exc

        self.logger.info(f"Captcha OCR result: {captcha_text}")
        print(f"Captcha OCR result: {captcha_text}")
        self._save_captcha_text(captcha_text)
        return captcha_text

    def click_login_button(self):
        self.wait_for_element(self.CAPTCHA_TEXTBOX, timeout=5)
        self.wait.until(
            lambda d: d.find_element(*self.CAPTCHA_TEXTBOX).get_attribute("value").strip()
        )
        self.wait_for_element_to_be_clickable(self.LOGIN_BUTTON, timeout=10)
        self.scroll_to_element(self.LOGIN_BUTTON)
        self.click(self.LOGIN_BUTTON, timeout=10)

    def login(self, username, password, group_name, captcha_text=None):
        """
        Complete login action
        """
        self.logger.info(f"Logging in with user: {username}")

        self.close_initial_popup()
        self.enter_username(username)
        self.enter_password(password)
        self.enter_group_name(group_name)

        if captcha_text is None or not str(captcha_text).strip():
            captcha_text = self.get_captcha_text()

        self.enter_captcha(captcha_text)
        self.wait.until(
            lambda d: d.find_element(*self.CAPTCHA_TEXTBOX).get_attribute("value").strip() == captcha_text
        )
        self.sleep(1)
        self.click_login_button()
        self.sleep(2)  # wait for login to process, adjust as needed
        self.logger.info("Login action performed")
