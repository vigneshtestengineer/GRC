from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import os
import re
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.base_page import BasePage
from config.config import Config
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from pytesseract import TesseractNotFoundError

SCREENSHOT_DIR = Config.CAPTCHA_IMAGE_DIR


class GRCLoginPage(BasePage):
    """Login page object class"""
    AMBIGUOUS_ALPHA_TO_DIGIT = {
        "O": "0",
        "Q": "0",
        "D": "0",
        "I": "1",
        "L": "1",
        "T": "7",
        "Z": "2",
        "S": "5",
        "G": "6",
        "B": "8",
    }

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

    @property
    def captcha_image(self):
        return self._locate_captcha_element(timeout=4)

    @property
    def captcha_input(self):
        self.wait_for_element(self.CAPTCHA_TEXTBOX, timeout=5)
        return self.driver.find_element(*self.CAPTCHA_TEXTBOX)

    def locate_and_convert_captcha(self) -> str:
        """
        Equivalent of LocateandConvertcapctha() in Java.

        Steps:
          1. Takes a screenshot of ONLY the captcha element.
          2. Saves it to /screenshot/captcha.png
          3. Runs pytesseract OCR (equivalent of Tesseract.doOCR).
          4. Strips non-alphanumeric characters.
          5. Returns cleaned captcha text.
        """
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        dest_path = os.path.join(SCREENSHOT_DIR, "captcha.png")

        captcha_element = self.captcha_image
        captcha_element.screenshot(dest_path)
        self.logger.info(f"Captcha screenshot saved to: {dest_path}")

        tesseract_cmd = getattr(Config, "TESSERACT_CMD", r"E:\Tesseract-OCR\tesseract.exe")
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        try:
            image = Image.open(dest_path)

            candidate_images = [
                ("original", image),
                ("grayscale_autocontrast", ImageOps.autocontrast(image.convert("L"))),
                ("processed", self._prepare_captcha_image(image)),
                ("enhanced", self._prepare_captcha_image_enhanced(image)),
                ("perfect", self._prepare_captcha_image_perfect(image)),
            ]
            ocr_configs = [
                '--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                '--oem 3 --psm 13 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            ]

            best_candidate = {"text": "", "score": -1}
            fallback_candidate = {"text": "", "score": -1}

            for image_name, candidate_image in candidate_images:
                for config in ocr_configs:
                    cleaned_text, confidence = self._extract_text_with_confidence(candidate_image, config)
                    if not cleaned_text:
                        continue

                    segmented_text = self._extract_captcha_text_by_characters(candidate_image, image_name)
                    cleaned_text = self._merge_ocr_with_segmented(cleaned_text, segmented_text)
                    cleaned_text = self._resolve_numeric_ambiguities(cleaned_text)

                    score = self._score_captcha_candidate(cleaned_text, confidence)
                    self.logger.info(
                        "OCR candidate [%s | %s]: '%s' (confidence=%.2f, score=%.2f)",
                        image_name,
                        config,
                        cleaned_text,
                        confidence,
                        score,
                    )

                    if score > fallback_candidate["score"]:
                        fallback_candidate = {"text": cleaned_text, "score": score}

                    if self._is_valid_captcha_text(cleaned_text) and score > best_candidate["score"]:
                        best_candidate = {"text": cleaned_text, "score": score}

            captcha_text = best_candidate["text"] if best_candidate["text"] else fallback_candidate["text"]
        except TesseractNotFoundError as exc:
            error_message = (
                "Tesseract OCR executable not found. "
                "Install Tesseract and set pytesseract.pytesseract.tesseract_cmd correctly."
            )
            self.logger.error(error_message)
            raise RuntimeError(error_message) from exc

        captcha_text = re.sub(r"[^a-zA-Z0-9]", "", captcha_text)
        if not captcha_text:
            raise RuntimeError("Captcha OCR returned empty text.")

        self.logger.info(f"OCR captcha text: '{captcha_text}'")
        self._save_captcha_text(captcha_text)
        return captcha_text

    def _extract_text_with_confidence(self, image, config):
        cleaned = ""
        confidence = 0.0
        data = pytesseract.image_to_data(
            image,
            config=config,
            output_type=pytesseract.Output.DICT,
        )

        words = []
        conf_values = []
        for raw_word, conf_str in zip(data.get("text", []), data.get("conf", [])):
            word = re.sub(r"[^a-zA-Z0-9]", "", (raw_word or ""))
            if not word:
                continue

            words.append(word)
            try:
                conf = float(conf_str)
                if conf >= 0:
                    conf_values.append(conf)
            except (TypeError, ValueError):
                continue

        if words:
            cleaned = "".join(words)
            confidence = sum(conf_values) / len(conf_values) if conf_values else 0.0
            return cleaned, confidence

        raw_text = pytesseract.image_to_string(image, config=config)
        cleaned = re.sub(r"[^a-zA-Z0-9]", "", raw_text)
        return cleaned, confidence

    def _score_captcha_candidate(self, text, confidence):
        score = max(0.0, float(confidence))
        length = len(text)
        if 4 <= length <= 8:
            score += 20.0
        elif length > 0:
            score += 5.0

        unique_chars = len(set(text))
        score += min(unique_chars, 8)
        return score

    def _merge_ocr_with_segmented(self, ocr_text, segmented_text):
        if not ocr_text:
            return segmented_text or ""
        if not segmented_text:
            return ocr_text
        if len(ocr_text) != len(segmented_text):
            return ocr_text

        merged = []
        for base_char, seg_char in zip(ocr_text, segmented_text):
            if base_char == seg_char:
                merged.append(base_char)
                continue

            if (
                base_char.isalpha()
                and seg_char.isdigit()
                and self.AMBIGUOUS_ALPHA_TO_DIGIT.get(base_char.upper()) == seg_char
            ):
                merged.append(seg_char)
                continue

            merged.append(base_char)
        return "".join(merged)

    def _resolve_numeric_ambiguities(self, text):
        if not text:
            return text

        digits = sum(1 for ch in text if ch.isdigit())
        letters = sum(1 for ch in text if ch.isalpha())
        if digits < letters:
            return text

        resolved = []
        for ch in text:
            replacement = self.AMBIGUOUS_ALPHA_TO_DIGIT.get(ch.upper(), ch)
            resolved.append(replacement)
        return "".join(resolved)

    def enter_captcha(self, captcha_text):
        if not captcha_text or not str(captcha_text).strip():
            raise ValueError("Captcha text is empty, so it cannot be entered.")

        captcha_text = str(captcha_text).strip()
        for attempt in range(1, 4):
            field = self.captcha_input
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field)
            try:
                field.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", field)

            try:
                field.clear()
            except Exception:
                pass

            try:
                field.send_keys(Keys.CONTROL, "a")
                field.send_keys(Keys.DELETE)
                field.send_keys(captcha_text)
            except Exception:
                pass

            typed_value = (field.get_attribute("value") or "").strip()
            if typed_value != captcha_text:
                self.driver.execute_script(
                    """
                    arguments[0].focus();
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                    arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                    arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
                    """,
                    field,
                    captcha_text,
                )

            final_value = (self.driver.find_element(*self.CAPTCHA_TEXTBOX).get_attribute("value") or "").strip()
            if final_value == captcha_text:
                self.logger.info(f"Entered captcha: '{captcha_text}'")
                return

            self.logger.warning(
                "Captcha input attempt %d failed. Expected '%s', found '%s'",
                attempt,
                captcha_text,
                final_value,
            )
            self.sleep(0.2)

        raise RuntimeError(f"Captcha could not be entered. Expected '{captcha_text}'.")

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
        text = self._normalize_ocr_text(self._run_tesseract(image))
        self.logger.debug(f"OCR result for {prefix}: '{text}'")
        print(f"Captcha OCR candidate [{prefix}]: {text}")
        return text

    def _extract_captcha_text_by_characters(self, image, prefix):
        image = image.convert("L")
        image = ImageOps.autocontrast(image)
        image = image.point(lambda x: 0 if x < 170 else 255, mode='L')
        width, height = image.size
        pixels = image.load()
        segments = []
        start = None

        for x in range(width):
            dark_pixel_count = sum(1 for y in range(height) if pixels[x, y] == 0)
            has_dark_pixel = dark_pixel_count >= max(2, height // 18)
            if has_dark_pixel and start is None:
                start = x
            elif not has_dark_pixel and start is not None:
                if x - start >= 6:
                    segments.append((start, x - 1))
                start = None

        if start is not None and width - start >= 6:
            segments.append((start, width - 1))

        recognized = []
        for index, (left, right) in enumerate(segments):
            char_image = image.crop((max(0, left - 2), 0, min(width, right + 3), height))
            bbox = ImageOps.invert(char_image).getbbox()
            if bbox:
                char_image = char_image.crop(bbox)

            char_image = char_image.resize((max(24, char_image.width * 3), max(36, char_image.height * 3)), Image.LANCZOS)
            char_image = ImageOps.autocontrast(char_image)
            char_image = char_image.filter(ImageFilter.MedianFilter(size=3))
            char_image = char_image.filter(ImageFilter.UnsharpMask(radius=2, percent=180, threshold=1))
            recognized.append(self._read_single_character(char_image))

        text = "".join(recognized)
        self.logger.debug(f"Segmented OCR result for {prefix}: '{text}'")
        print(f"Captcha OCR segmented candidate [{prefix}]: {text}")
        return text

    def _prefer_digit_when_ambiguous(self, alnum_text, digit_text):
        if len(alnum_text) != 1 or len(digit_text) != 1 or not digit_text.isdigit():
            return alnum_text

        digit_confusions = {
            "0": {"O", "Q", "D"},
            "1": {"I", "L", "T"},
            "2": {"Z"},
            "5": {"S"},
            "6": {"G"},
            "8": {"B"},
        }
        if alnum_text in digit_confusions.get(digit_text, set()):
            return digit_text
        return alnum_text

    def _read_single_character(self, char_image):
        ocr_options = [
            ("alnum", '--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            ("digit", '--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789'),
            ("alpha", '--oem 3 --psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            ("alnum_fallback", '--oem 3 --psm 13 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        ]
        results = {}

        for key, config in ocr_options:
            text = self._normalize_ocr_text(pytesseract.image_to_string(char_image, config=config))
            if len(text) == 1:
                results[key] = text

        if "alnum" in results and "digit" in results:
            return self._prefer_digit_when_ambiguous(results["alnum"], results["digit"])
        if "alnum" in results:
            return results["alnum"]
        if "digit" in results:
            return results["digit"]
        if "alpha" in results:
            return results["alpha"]
        return results.get("alnum_fallback", "")

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

    def _run_tesseract(self, image):
        ocr_configs = [
            (
                '--oem 3 --psm 8 '
                '-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ '
                '-c load_system_dawg=0 -c load_freq_dawg=0 -c user_defined_dpi=300'
            ),
            (
                '--oem 3 --psm 7 '
                '-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ '
                '-c load_system_dawg=0 -c load_freq_dawg=0 -c user_defined_dpi=300'
            ),
            (
                '--oem 3 --psm 13 '
                '-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ '
                '-c load_system_dawg=0 -c load_freq_dawg=0 -c user_defined_dpi=300'
            ),
        ]
        image = image.convert("L")
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
            " ": "",
        }
        normalized = ''.join(replacements.get(ch, ch) for ch in text if ch.isalnum() or ch in replacements)
        return normalized.upper()

    def get_captcha_text(self, popup_already_closed=False):
        """
        Captures the captcha image from the page and uses OCR to read the text.
        Returns:
            str: Captcha text recognized by Tesseract
        """
        if not popup_already_closed:
            self.close_initial_popup()
        self.wait_for_element(self.CAPTCHA_TEXTBOX, timeout=3)
        return self.locate_and_convert_captcha()

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
            captcha_text = self.get_captcha_text(popup_already_closed=True)

        self.enter_captcha(captcha_text)
        self.wait.until(
            lambda d: d.find_element(*self.CAPTCHA_TEXTBOX).get_attribute("value").strip() == captcha_text
        )
        self.sleep(1)
        self.click_login_button()
        self.sleep(2)  # wait for login to process, adjust as needed
        self.logger.info("Login action performed")
