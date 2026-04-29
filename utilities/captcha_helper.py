"""
utilities/captcha_helper.py
---------------------------
Canvas-interceptor CAPTCHA strategy.

Chrome  — CDP Page.addScriptToEvaluateOnNewDocument injects the hook
          BEFORE the page loads, so fillText/strokeText calls are
          captured as the CAPTCHA canvas is first drawn.

Firefox — CDP is not supported.  Instead, the hook is injected
          POST-load via execute_script, then the CAPTCHA refresh
          button is clicked to trigger a re-render that the hook
          will capture.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ── Canvas hook (shared by Chrome and Firefox) ────────────────────────────────
_INTERCEPTOR_JS = """
(function() {
    if (window.__captchaInterceptorInstalled) return;
    window.__captchaInterceptorInstalled = true;
    window._captchaText = '';

    var _origFill   = CanvasRenderingContext2D.prototype.fillText;
    var _origStroke = CanvasRenderingContext2D.prototype.strokeText;
    var _inFill   = false;
    var _inStroke = false;

    CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
        if (!_inFill) {
            _inFill = true;
            try {
                var txt = (text !== null && text !== undefined) ? String(text).trim() : '';
                if (txt) window._captchaText += txt;
            } finally { _inFill = false; }
        }
        return (maxWidth !== undefined)
            ? _origFill.call(this, text, x, y, maxWidth)
            : _origFill.call(this, text, x, y);
    };

    CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
        if (!_inStroke) {
            _inStroke = true;
            try {
                var txt = (text !== null && text !== undefined) ? String(text).trim() : '';
                if (txt) window._captchaText += txt;
            } finally { _inStroke = false; }
        }
        return (maxWidth !== undefined)
            ? _origStroke.call(this, text, x, y, maxWidth)
            : _origStroke.call(this, text, x, y);
    };
})();
"""

# Resets the guard so _INTERCEPTOR_JS can be re-injected into an existing page
_RESET_JS = "window.__captchaInterceptorInstalled = false; window._captchaText = '';"

# Selectors tried in order to find the CAPTCHA refresh/reload button
_REFRESH_SELECTORS = [
    ".captcha-buttons button",
    "button.captcha-refresh",
    "[class*='captcha'] button",
    "button[title*='refresh' i]",
    "button[aria-label*='refresh' i]",
    "button[title*='reload' i]",
    ".captcha-buttons",
]


# ── Chrome: pre-load injection via CDP ───────────────────────────────────────
def inject_captcha_interceptor(driver, logger=None) -> None:
    """
    Chrome  — injects hook via CDP before any page loads.
    Firefox — no-op here; injection happens inside read_captcha_from_canvas.
    """
    browser = (driver.capabilities or {}).get("browserName", "").lower()

    if browser == "firefox":
        if logger:
            logger.info("Firefox: pre-load captcha injection skipped; will inject post-load.")
        return

    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": _INTERCEPTOR_JS},
        )
        if logger:
            logger.info("CAPTCHA canvas interceptor injected via CDP (Chrome).")
    except Exception as exc:
        msg = f"CAPTCHA canvas interceptor could not be injected: {exc}"
        if logger:
            logger.warning(msg)
        else:
            print(f"[captcha_helper] WARNING: {msg}")


# ── Firefox: post-load injection + refresh click ──────────────────────────────
def _read_captcha_firefox(driver, locator, canvas_wait: int, logger=None) -> str:
    """
    Firefox-specific CAPTCHA reading:
      1. Wait for the canvas element.
      2. Inject the hook into the already-loaded document.
      3. Click the CAPTCHA refresh button so the canvas re-draws
         and our hook captures the new text.
      4. Return the captured text.
    """
    try:
        WebDriverWait(driver, canvas_wait).until(
            EC.presence_of_element_located(locator)
        )
    except TimeoutException:
        if logger:
            logger.warning("Firefox: CAPTCHA canvas not found within %ds.", canvas_wait)
        return ""

    # Reset guard then re-inject so the hook is live in the current document
    driver.execute_script(_RESET_JS)
    driver.execute_script(_INTERCEPTOR_JS)
    if logger:
        logger.info("Firefox: canvas hook injected into current document.")

    # Click the CAPTCHA refresh button to trigger a new render
    clicked = False
    for sel in _REFRESH_SELECTORS:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, sel)
            btn.click()
            clicked = True
            if logger:
                logger.info("Firefox: clicked CAPTCHA refresh button (%s).", sel)
            break
        except Exception:
            pass

    if not clicked:
        if logger:
            logger.warning("Firefox: no refresh button found — trying window resize to force redraw.")
        size = driver.get_window_size()
        driver.set_window_size(size["width"] - 1, size["height"])
        time.sleep(0.3)
        driver.set_window_size(size["width"], size["height"])

    # Wait for the hook to capture text from the re-rendered CAPTCHA
    def _text_ready(d):
        return d.execute_script(
            "return window._captchaText ? window._captchaText.trim() : '';"
        ) or False

    try:
        text = WebDriverWait(driver, 6.0, poll_frequency=0.1).until(_text_ready)
    except TimeoutException:
        text = ""

    if text:
        half = len(text) // 2
        if half >= 4 and text[:half] == text[half:]:
            text = text[:half]
            if logger:
                logger.info("Firefox: doubled CAPTCHA text deduplicated: '%s'", text)
        if logger:
            logger.info("Firefox: CAPTCHA captured: '%s'", text)

    return text


# ── Shared: read window._captchaText (Chrome) ─────────────────────────────────
def read_captcha_from_canvas(driver, logger=None, locator=None,
                              canvas_wait: int = 10,
                              settle_sleep: float = 0.3) -> str:
    if locator is None:
        locator = (By.ID, "captchaCanvas")

    browser = (driver.capabilities or {}).get("browserName", "").lower()

    # Firefox uses its own post-load injection path
    if browser == "firefox":
        return _read_captcha_firefox(driver, locator, canvas_wait, logger)

    # Chrome: hook was injected pre-load, just read the captured text
    try:
        WebDriverWait(driver, canvas_wait).until(
            EC.presence_of_element_located(locator)
        )

        def _captcha_text_ready(d):
            return d.execute_script(
                "return window._captchaText ? window._captchaText.trim() : '';"
            ) or False

        try:
            text = WebDriverWait(driver, settle_sleep + 3.0, poll_frequency=0.1).until(
                _captcha_text_ready
            )
        except TimeoutException:
            text = ""

        if text:
            half = len(text) // 2
            if half >= 4 and text[:half] == text[half:]:
                text = text[:half]
                if logger:
                    logger.info("Detected doubled CAPTCHA text, using first half: '%s'", text)
            if logger:
                logger.info("CAPTCHA from canvas interceptor: '%s'", text)
            return text

    except TimeoutException:
        if logger:
            logger.warning("CAPTCHA canvas element not found within %ds.", canvas_wait)
    except Exception as exc:
        if logger:
            logger.debug("Canvas CAPTCHA read failed: %s", exc)

    return ""
