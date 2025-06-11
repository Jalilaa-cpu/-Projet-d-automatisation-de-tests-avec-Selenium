"""
Home Page Object - Weather Shopper Homepage
Handles temperature reading and navigation to product categories
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import re


class HomePage(BasePage):
    """Page object for Weather Shopper homepage"""
    
    # Page URL
    URL = "https://weathershopper.pythonanywhere.com"
    
    # Locators
    TEMPERATURE_DISPLAY = (By.ID, "temperature")
    MOISTURIZERS_BUTTON = (By.XPATH, "//button[contains(text(), 'moisturizers')]")
    SUNSCREENS_BUTTON = (By.XPATH, "//button[contains(text(), 'sunscreens')]")
    
    def navigate_to_homepage(self):
        """
        Navigate to the Weather Shopper homepage.
        
        Returns:
            HomePage: self instance for method chaining.
        """
        self.driver.get(self.URL)
        return self
    
    def get_current_temperature(self):
        """
        Read the temperature displayed on homepage.
        
        Returns:
            int: Temperature value (e.g., 25 for "25°C").
        
        Raises:
            Exception: If temperature text parsing fails.
        """
        temp_text = self.get_element_text(self.TEMPERATURE_DISPLAY)
        try:
            temperature = int(re.search(r'\d+', temp_text).group())
            return temperature
        except (AttributeError, ValueError) as e:
            raise Exception(f"Failed to parse temperature from text '{temp_text}': {e}")
    
    def should_buy_moisturizers(self):
        """
        Check if temperature requires moisturizers (< 19°C).
        
        Returns:
            bool
        """
        return self.get_current_temperature() < 19
    
    def should_buy_sunscreens(self):
        """
        Check if temperature requires sunscreens (> 34°C).
        
        Returns:
            bool
        """
        return self.get_current_temperature() > 34
    
    def is_moderate_temperature(self):
        """
        Check if temperature is moderate (19-34°C) - no action needed.
        
        Returns:
            bool
        """
        temp = self.get_current_temperature()
        return 19 <= temp <= 34
    
    def click_moisturizers_button(self):
        """
        Click the moisturizers button.
        
        Returns:
            HomePage: self instance for method chaining.
        """
        self.click_element(self.MOISTURIZERS_BUTTON)
        return self
    
    def click_sunscreens_button(self):
        """
        Click the sunscreens button.
        
        Returns:
            HomePage: self instance for method chaining.
        """
        self.click_element(self.SUNSCREENS_BUTTON)
        return self
    
    def navigate_to_appropriate_category(self):
        """
        Navigate to the appropriate product category based on temperature.
        
        Returns:
            str: category navigated to ('moisturizers', 'sunscreens', 'none').
        """
        if self.should_buy_moisturizers():
            self.click_moisturizers_button()
            return 'moisturizers'
        elif self.should_buy_sunscreens():
            self.click_sunscreens_button()
            return 'sunscreens'
        else:
            return 'none'  # Moderate temperature, no action needed
    
    def is_moisturizers_button_visible(self, timeout=5):
        """
        Check if moisturizers button is present on the page.
        
        Args:
            timeout (int): Seconds to wait for element presence.
        
        Returns:
            bool
        """
        return self.is_element_present(self.MOISTURIZERS_BUTTON, timeout=timeout)
    
    def is_sunscreens_button_visible(self, timeout=5):
        """
        Check if sunscreens button is present on the page.
        
        Args:
            timeout (int): Seconds to wait for element presence.
        
        Returns:
            bool
        """
        return self.is_element_present(self.SUNSCREENS_BUTTON, timeout=timeout)
