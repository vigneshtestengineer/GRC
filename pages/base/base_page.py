"""
Base page class with common methods for all page objects
"""
import string

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import os
import time
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.json_config import get_int
from utilities.logger import Logger

EXPLICIT_WAIT = get_int("browser", "explicit_wait", 20)

FACTORY_NAMES = [
    "Alpha", "Beta", "Gamma", "Delta", "Sigma",
    "Apex", "Nova", "Titan", "Orion", "Nexus",
    "Vega", "Zeta", "Lynx", "Atlas", "Cobalt"
]
FACTORY_SUFFIXES = ["Industries", "Works", "Manufacturing", "Fabricators", "Systems"]

CONTRACTOR_PREFIXES = [
    "Apex", "Nova", "Titan", "Orion", "Nexus", "Vega", "Atlas",
    "Delta", "Sigma", "Prime", "Global", "Sterling", "Summit", "Crest",
]
CONTRACTOR_SUFFIXES = [
    "Construction", "Builders", "Contractors", "Infrastructure",
    "Projects", "Services", "Works", "Associates", "Enterprises",
]

STREET_NAMES = [
    "MG Road", "Brigade Road", "Anna Salai", "Park Street", "Ring Road",
    "Nehru Street", "Gandhi Nagar", "Lake View Road", "Temple Road"
]

CITIES = [
    "Chennai", "Bangalore", "Mumbai", "Hyderabad", "Pune",
    "Delhi", "Kolkata", "Ahmedabad", "Jaipur"
]

STATES = [
    "Tamil Nadu", "Karnataka", "Maharashtra", "Telangana", "Delhi",
    "West Bengal", "Gujarat", "Rajasthan", "Kerala"
]

class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        """
        Initialize base page
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.generated_codes = set()
    
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
        wait_time = timeout or EXPLICIT_WAIT
        return WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))

    def click(self, locator, timeout=None):
        """
        Clicks on element
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Wait timeout in seconds
        """
        wait_time = timeout or EXPLICIT_WAIT

        def try_click(driver):
            try:
                el = driver.find_element(*locator)
                if el.is_displayed() and el.is_enabled():
                    el.click()
                    return True
            except ElementClickInterceptedException:
                # Overlay is covering the element — JS click bypasses hit-testing
                try:
                    driver.execute_script("arguments[0].click();", el)
                    return True
                except Exception:
                    pass
            except (StaleElementReferenceException, NoSuchElementException):
                pass
            return False

        try:
            WebDriverWait(self.driver, wait_time).until(try_click)
        except TimeoutException:
            element = self.driver.find_element(*locator)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
                element,
            )
        self.logger.info(f"Clicked on element: {locator}")
    
    def enter_text(self, locator, text):
        """
        Enters text in input field
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
        """
        for attempt in range(3):
            try:
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
                return

            except StaleElementReferenceException:
                if attempt == 2:
                    raise
                self.logger.warning(
                    f"Stale element on enter_text attempt {attempt + 1}/3 for {locator}, retrying..."
                )
                time.sleep(0.4)
    
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
        wait_time = timeout or EXPLICIT_WAIT
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

    def generate_unit_name(self):
        """
        Generates a random factory-based unit name
        Returns:
            str: Random unit name e.g. 'Nova Manufacturing 472'
        """
        unit_name = f"{random.choice(FACTORY_NAMES)} {random.choice(FACTORY_SUFFIXES)} {random.randint(100, 999)}"
        self.logger.info(f"Generated unit name: {unit_name}")
        return unit_name
    
    def generate_unit_code(self):
        while True:
            code = (
                ''.join(random.choices(string.ascii_uppercase, k=3)) +
                ''.join(random.choices(string.digits, k=2))
            )

            if code not in self.generated_codes:
                self.generated_codes.add(code)
                self.logger.info(f"Generated unit code: {code}")
                return code
         

    def generate_address(self):

     house_no = random.randint(1, 999)
     street = random.choice(STREET_NAMES)
     city = random.choice(CITIES)
     state = random.choice(STATES)
     pincode = random.randint(100000, 999999)

     address = f"No. {house_no}, {street}, {city}, {state} - {pincode}"

     self.logger.info(f"Generated address: {address}")
     return address

    def generate_contractor_name(self) -> str:
        name = (
            f"{random.choice(CONTRACTOR_PREFIXES)} {random.choice(CONTRACTOR_PREFIXES)} "
            f"{random.choice(CONTRACTOR_SUFFIXES)} {random.randint(100, 999)}"
        )
        self.logger.info(f"Generated contractor name: {name}")
        return name

    def generate_contractor_code(self) -> str:
        """
        Generates a unique contractor code: 3 uppercase letters + 3 digits.
        Returns:
            str: e.g. 'ABC123'
        """
        while True:
            code = (
                ''.join(random.choices(string.ascii_uppercase, k=3)) +
                ''.join(random.choices(string.digits, k=3))
            )
            if code not in self.generated_codes:
                self.generated_codes.add(code)
                self.logger.info(f"Generated contractor code: {code}")
                return code

    def generate_contractor_short_name(self) -> str:
        """
        Generates a unique 4-character uppercase short name.
        Returns:
            str: e.g. 'APEX'
        """
        while True:
            short_name = ''.join(random.choices(string.ascii_uppercase, k=4))
            if short_name not in self.generated_codes:
                self.generated_codes.add(short_name)
                self.logger.info(f"Generated contractor short name: {short_name}")
                return short_name
            
    def generate_contractor_PF_code(self) -> str:
    # """
    # Generates a unique PF code in the format: ABCDE1234F
    # (5 uppercase letters + 4 digits + 1 uppercase letter)
    # Returns:
    #     str: e.g. 'KARBN0012A'
    # """
        while True:
            pf_code = (
            ''.join(random.choices(string.ascii_uppercase, k=5)) +
            ''.join(random.choices(string.digits, k=4)) +
            random.choice(string.ascii_uppercase)
            )
            if pf_code not in self.generated_codes:
                self.generated_codes.add(pf_code)
                self.logger.info(f"Generated contractor PF code: {pf_code}")
                return pf_code
            
    def generate_contractor_ESI_code(self) -> str:
    # """
    # Generates a unique ESI code in the format: 12345678901000001
    # (17 digits: 11-digit employer code + 6-digit serial number)
    # Returns:
    #     str: e.g. '12345678901000001'
    # """
        while True:
            esi_code = (
            ''.join(random.choices(string.digits, k=11)) +
            ''.join(random.choices(string.digits, k=6))
            )
            if esi_code not in self.generated_codes:
                self.generated_codes.add(esi_code)
                self.logger.info(f"Generated contractor ESI code: {esi_code}")
                return esi_code