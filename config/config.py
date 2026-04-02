import os
from pathlib import Path

class Config:
    """Configuration class for framework settings"""
    
    # Project paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, 'screenshots')
    CAPTCHA_IMAGE_DIR = os.path.join(REPORTS_DIR, 'captchas')
    LOGS_DIR = os.path.join(REPORTS_DIR, 'logs')
    TEST_DATA_DIR = os.path.join(BASE_DIR, 'test_data')
    
    # Application URLs
    BASE_URL = "http://13.203.6.58:5009/#/login"
    LOGIN_URL = BASE_URL

    # Tesseract OCR executable path
    # Example for Windows: r"E:\Tesseract-OCR\tesseract.exe"
    TESSERACT_CMD = r"E:\Tesseract-OCR\tesseract.exe"
    
    # Browser settings
    BROWSER = "chrome"  # chrome, firefox, edge
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    
    # Login credentials (Executive User)
    USERNAME = "vignesh.kv@aparajitha.com"
    PASSWORD = "Admin@123"
    GROUP ="MSO"
    # Screenshot settings
    TAKE_SCREENSHOT_ON_FAILURE = True
    
    # Logging
    LOG_LEVEL = "INFO"
    