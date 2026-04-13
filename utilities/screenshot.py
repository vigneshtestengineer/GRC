"""
Screenshot utility for capturing screenshots on failure
"""
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.json_config import get_path

SCREENSHOTS_DIR = get_path("paths", "screenshots_dir", "reports/screenshots")

class Screenshot:
    """Utility class for taking screenshots"""
    
    @staticmethod
    def take_screenshot(driver, test_name):
        """
        Captures screenshot and saves to reports folder
        Args:
            driver: WebDriver instance
            test_name (str): Name of the test
        Returns:
            str: Screenshot file path
        """
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"{test_name}_{timestamp}.png"
        screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
        
        driver.save_screenshot(screenshot_path)
        return screenshot_path
