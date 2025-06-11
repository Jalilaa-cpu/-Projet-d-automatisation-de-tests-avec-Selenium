"""
Cart Page Object - Shopping cart functionality
Handles cart verification, item retrieval, and checkout process
Optimized for Weather Shopper e-commerce flow automation.
"""

import logging
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    TimeoutException,
    StaleElementReferenceException
)
from pages.base_page import BasePage


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CartPage(BasePage):
    """Page object representing the shopping cart on Weather Shopper"""

    DEFAULT_TIMEOUT = 10

    # Updated locators based on actual HTML structuree
    CART_TABLE = (By.CSS_SELECTOR, "table.table-striped")
    CART_ROWS = (By.CSS_SELECTOR, "table.table-striped tbody tr")
    TOTAL_AMOUNT = (By.ID, "total")
    PAY_BUTTON = (By.CSS_SELECTOR, "button.stripe-button-el")

    def navigate_to_cart(self):
        """Navigate to cart page by clicking the cart button."""
        cart_btn = self.driver.find_element(By.ID, "cart")
        cart_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_TABLE)
        )
        time.sleep(2)

    def get_cart_items(self):
        """Get all items in cart with comprehensive debugging"""
        try:
            # Ensure we're on cart page
            if "cart" not in self.driver.current_url.lower():
                self.navigate_to_cart()
            
            # Debug: Print current URL and page source snippet
            logging.info(f"Current URL: {self.driver.current_url}")
            
            # Debug: Print page source for cart table
            try:
                page_source = self.driver.page_source
                if "table" in page_source.lower():
                    # Find table content in page source
                    start = page_source.lower().find('<table')
                    end = page_source.lower().find('</table>') + 8
                    if start != -1 and end != -1:
                        table_html = page_source[start:end]
                        logging.info(f"Cart table HTML: {table_html[:500]}...")  # First 500 chars
                else:
                    logging.warning("No table found in page source")
            except Exception as e:
                logging.warning(f"Failed to debug page source: {e}")
            
            # Wait for table to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CART_TABLE)
            )
            
            # Find all table rows (excluding header)
            cart_items = []
            
            # Try multiple selectors with more debugging
            selectors_to_try = [
                "table tbody tr",
                "table tr:not(:first-child)", 
                ".table tbody tr",
                ".table tr:not(:first-child)",
                "table tr",  # Try all rows including header
                ".table tr"  # Try all rows with class
            ]
            
            rows = []
            for selector in selectors_to_try:
                try:
                    rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    logging.info(f"Selector '{selector}' found {len(rows)} rows")
                    if rows:
                        # Debug each row
                        for i, row in enumerate(rows):
                            try:
                                row_text = row.text.strip()
                                logging.info(f"Row {i} text: '{row_text}'")
                                cells = row.find_elements(By.TAG_NAME, "td")
                                logging.info(f"Row {i} has {len(cells)} td cells")
                                if cells:
                                    for j, cell in enumerate(cells):
                                        logging.info(f"  Cell {j}: '{cell.text.strip()}'")
                            except Exception as e:
                                logging.warning(f"Failed to debug row {i}: {e}")
                        break  # Use first selector that finds rows
                except Exception as e:
                    logging.warning(f"Selector '{selector}' failed: {e}")
                    continue
            
            if not rows:
                logging.warning("No cart rows found with any selector")
                # Try to find any elements that might contain cart items
                all_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(),'$') or contains(text(),'USD') or contains(text(),'price')]")
                logging.info(f"Found {len(all_elements)} elements with price indicators")
                for elem in all_elements[:5]:  # Show first 5
                    logging.info(f"Price element: '{elem.text.strip()}'")
                return []
            
            # Parse each row
            for i, row in enumerate(rows):
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 2:
                        name = cells[0].text.strip()
                        price_text = cells[1].text.strip()
                        
                        # Skip header row if it doesn't contain price
                        if not any(char.isdigit() for char in price_text):
                            logging.info(f"Skipping header row: '{name}' - '{price_text}'")
                            continue
                        
                        # Extract price number
                        price_match = re.search(r'(\d+)', price_text.replace(',', ''))
                        if price_match:
                            price = int(price_match.group(1))
                            cart_items.append({
                                'name': name,
                                'price': price,
                                'price_text': price_text
                            })
                            logging.info(f"Found cart item: {name} - {price_text}")
                        else:
                            logging.warning(f"Could not extract price from: {price_text}")
                    else:
                        logging.warning(f"Row {i} has {len(cells)} cells, expected at least 2")
                        
                except Exception as e:
                    logging.warning(f"Failed to parse row {i}: {e}")
                    continue
            
            logging.info(f"Total cart items found: {len(cart_items)}")
            return cart_items
            
        except Exception as e:
            logging.error(f"Failed to retrieve cart items: {e}")
            # Debug: Take screenshot
            try:
                self.driver.save_screenshot("cart_debug.png")
                logging.info("Debug screenshot saved as cart_debug.png")
            except:
                pass
            return []

    def get_displayed_total(self):
        """Get the total amount displayed on cart page"""
        try:
            total_element = self.find_element(self.TOTAL_AMOUNT)
            total_text = total_element.text.strip()
            
            # Extract number from total text
            price_match = re.search(r'(\d+)', total_text.replace(',', ''))
            if price_match:
                return int(price_match.group(1))
            else:
                logging.warning(f"Could not extract total from: {total_text}")
                return 0
                
        except Exception as e:
            logging.error(f"Failed to get displayed total: {e}")
            return 0

    def calculate_expected_total(self):
        """Calculate expected total from cart items"""
        items = self.get_cart_items()
        return sum(item['price'] for item in items)

    def click_pay_with_card(self):
        """Click the pay button"""
        try:
            pay_button = self.find_element(self.PAY_BUTTON)
            pay_button.click()
            logging.info("Clicked pay button")
        except Exception as e:
            logging.error(f"Failed to click pay button: {e}")
            raise



