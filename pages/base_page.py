"""
Base page class with common methods for all page objects
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config
from utilities.logger import Logger

class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        """
        Initialize base page
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = Logger.get_logger(self.__class__.__name__)
    
    def find_element(self, locator):
        """
        Finds and returns element
        Args:
            locator (tuple): Element locator (By.ID, "element_id")
        Returns:
            WebElement: Found element
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator):
        """
        Finds and returns list of elements
        Args:
            locator (tuple): Element locator
        Returns:
            list: List of WebElements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            self.logger.info(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            return []
    
    def wait_for_element_to_be_clickable(self, locator, timeout=None):
        """
        Waits until an element is clickable
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Wait timeout
        Returns:
            WebElement: Clickable element
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        return WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))

    def click(self, locator, timeout=None):
        """
        Clicks on element
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Wait timeout in seconds
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        try:
            element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
            element.click()
        except (TimeoutException, WebDriverException):
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            try:
                ActionChains(self.driver).move_to_element(element).click().perform()
            except WebDriverException:
                self.driver.execute_script("arguments[0].click();", element)
        self.logger.info(f"Clicked on element: {locator}")
    
    def enter_text(self, locator, text):
        """
        Enters text in input field
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

        try:
            element.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", element)

        try:
            element.clear()
        except WebDriverException:
            pass

        try:
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.DELETE)
        except WebDriverException:
            pass

        try:
            element.send_keys(text)
        except WebDriverException:
            self.driver.execute_script(
                """
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                """,
                element,
                text,
            )

        entered_value = element.get_attribute("value") or ""
        if entered_value.strip() != str(text).strip():
            self.driver.execute_script(
                """
                arguments[0].focus();
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
                """,
                element,
                text,
            )
        self.logger.info(f"Entered text '{text}' in element: {locator}")
    
    def get_text(self, locator):
        """
        Gets text from element
        Args:
            locator (tuple): Element locator
        Returns:
            str: Element text
        """
        element = self.find_element(locator)
        text = element.text
        self.logger.info(f"Got text '{text}' from element: {locator}")
        return text
    
    def is_element_visible(self, locator, timeout=5):
        """
        Checks if element is visible
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """
        Checks if element is present in DOM
        Args:
            locator (tuple): Element locator
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element(self, locator, timeout=None):
        """
        Waits for element to be present
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(locator)
        )
    
    def wait_for_element_to_disappear(self, locator, timeout=10):
        """
        Waits for element to disappear
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            pass
    
    def scroll_to_element(self, locator):
        """
        Scrolls to element
        Args:
            locator (tuple): Element locator
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
    
    def get_title(self):
        """Returns page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Returns current URL"""
        return self.driver.current_url
    
    def sleep(self, seconds):
        """
        Sleep for specified seconds
        Args:
            seconds (int/float): Sleep duration
        """
        time.sleep(seconds)
