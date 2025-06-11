"""
Base Page Object Model class with common functionality
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base page class that contains common functionality for all pages"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """Find a single element with wait"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise Exception(f"Element not found: {locator}")
    
    def find_elements(self, locator, timeout=10):
        """Find multiple elements with wait"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            raise Exception(f"Elements not found: {locator}")
    
    def click_element(self, locator):
        """Click on element with wait for clickability"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            print(f"Clicked element: {locator}")
            return element
        except TimeoutException:
            raise Exception(f"Element not clickable: {locator}")
    
    def send_keys_to_element(self, locator, text):
        """Send keys to element with wait"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            print(f"Sent keys to element: {locator}")
            return element
        except TimeoutException:
            raise Exception(f"Element not found to send keys: {locator}")
    
    def get_element_text(self, locator):
        """Get text from element"""
        element = self.find_element(locator)
        return element.text
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present on page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise Exception(f"Element not visible: {locator}")
    
    def is_element_interactable(self, locator, timeout=10):
        """Check if element is visible and enabled for clicking"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title
