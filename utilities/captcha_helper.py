"""
utilities/captcha_helper.py
---------------------------
Centralised helpers for the CDP canvas-interceptor CAPTCHA strategy.

How it works
~~~~~~~~~~~~
1.  inject_captcha_interceptor(driver)
        Called once before driver.get(url).
        Uses Page.addScriptToEvaluateOnNewDocument so the injected script
        runs on every new document — including the login page — before any
        of the page's own scripts execute.

        The script monkey-patches CanvasRenderingContext2D.prototype.fillText
        and .strokeText so every character drawn on a canvas is appended to
        window._captchaText.

2.  read_captcha_from_canvas(driver)
        Waits for the canvas element to exist, sleeps briefly for rendering,
        then returns window._captchaText.trim().
        Returns '' when nothing was captured (caller falls back to OCR).

Both helpers are pure functions — they take the driver (and an optional
logger) as arguments so they can be imported and called from anywhere.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# JavaScript injected before page load
_INTERCEPTOR_JS = """
(function() {
    // Guard: only patch once, even if this script runs multiple times
    if (window.__captchaInterceptorInstalled) return;
    window.__captchaInterceptorInstalled = true;
    window._captchaText = '';

    var _origFill   = CanvasRenderingContext2D.prototype.fillText;
    var _origStroke = CanvasRenderingContext2D.prototype.strokeText;

    // Re-entrancy flag — prevents the patched method from calling itself
    var _inFill   = false;
    var _inStroke = false;

    CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
        if (!_inFill) {
            _inFill = true;
            try {
                var txt = (text !== null && text !== undefined) ? String(text).trim() : '';
                if (txt) {
                    window._captchaText += txt;
                }
            } finally {
                _inFill = false;
            }
        }
        // Call the REAL original — use explicit argument count to avoid
        // spreading `arguments` which could re-trigger a patched version
        return (maxWidth !== undefined)
            ? _origFill.call(this, text, x, y, maxWidth)
            : _origFill.call(this, text, x, y);
    };

    CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
        if (!_inStroke) {
            _inStroke = true;
            try {
                var txt = (text !== null && text !== undefined) ? String(text).trim() : '';
                if (txt) {
                    window._captchaText += txt;
                }
            } finally {
                _inStroke = false;
            }
        }
        return (maxWidth !== undefined)
            ? _origStroke.call(this, text, x, y, maxWidth)
            : _origStroke.call(this, text, x, y);
    };
})();
"""


def inject_captcha_interceptor(driver, logger=None) -> None:
    """
    Inject the canvas text interceptor via Chrome DevTools Protocol.

    Must be called BEFORE driver.get(url) so the script is evaluated on
    document creation.  Safe to call multiple times (subsequent calls
    overwrite the previous injection).

    Args:
        driver:  Selenium WebDriver instance (Chrome).
        logger:  Optional Python logger; falls back to print on failure.
    """
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": _INTERCEPTOR_JS},
        )
        if logger:
            logger.info("CAPTCHA canvas interceptor injected via CDP.")
    except Exception as exc:
        msg = f"CAPTCHA canvas interceptor could not be injected: {exc}"
        if logger:
            logger.warning(msg)
        else:
            print(f"[captcha_helper] WARNING: {msg}")


def read_captcha_from_canvas(driver, logger=None, locator=None,
                              canvas_wait: int = 10,
                              settle_sleep: float = 0.3) -> str:
    from selenium.webdriver.common.by import By
    if locator is None:
        locator = (By.ID, "captchaCanvas")

    try:
        WebDriverWait(driver, canvas_wait).until(
            EC.presence_of_element_located(locator)
        )
        # time.sleep(settle_sleep)
        # text = driver.execute_script(
        #     "return window._captchaText ? window._captchaText.trim() : '';"
        # )

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
            # De-duplicate: if the same string appears twice (shadow rendering),
            # take just the first half.  e.g. "AB12AB12" → "AB12"
            half = len(text) // 2
            if half >= 4 and text[:half] == text[half:]:
                text = text[:half]
                if logger:
                    logger.info(f"Detected doubled CAPTCHA text, using first half: '{text}'")

            if logger:
                logger.info(f"CAPTCHA from canvas interceptor: '{text}'")
            return text
    except TimeoutException:
        if logger:
            logger.warning("CAPTCHA canvas element not found within %ds.", canvas_wait)
    except Exception as exc:
        if logger:
            logger.debug(f"Canvas CAPTCHA read failed: {exc}")

    return ""
