"""
Products Page Object - Handles both Moisturizers and Sunscreens pages
Manages product selection, filtering, and adding to cart
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import re
import logging
from typing import List, Tuple, Optional, Dict, Union
import time


class ProductPage(BasePage):
    """Page object for products pages (moisturizers and sunscreens)"""
    
    # Locators
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".col-4")  # Product card containers
    CART_BUTTON_LOCATORS = [
        (By.XPATH, "//button[contains(text(), 'Cart')]"),
        (By.XPATH, "//a[contains(text(), 'Cart')]"),
        (By.CSS_SELECTOR, "button[onclick*='cart']")
    ]
    
    def get_all_products(self):
        """Get all products from the current page"""
        logging.info(f"Current URL: {self.driver.current_url}")
        
        # Wait for products to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".col-4"))
        )
        
        # Get all product cards
        product_elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-4")
        logging.info(f"Found {len(product_elements)} product elements")
        
        all_products = []
        
        for i, elem in enumerate(product_elements):
            try:
                # Get product name from first p tag
                paragraphs = elem.find_elements(By.TAG_NAME, "p")
                if not paragraphs:
                    continue
                    
                name = paragraphs[0].text.strip()
                
                # Get price from second p tag that contains "Price"
                price_text = None
                for p in paragraphs:
                    if "Price" in p.text:
                        price_text = p.text
                        break
                
                if not price_text:
                    logging.warning(f"No price found for product: {name}")
                    continue
                    
                # Extract price number
                price = int(''.join(filter(str.isdigit, price_text)))
                
                # Get add button
                add_button = elem.find_element(By.TAG_NAME, "button")
                
                product = {
                    "name": name,
                    "price": price,
                    "element": elem,
                    "add_to_cart_button": add_button
                }
                
                all_products.append(product)
                logging.info(f"Added product: {name} - Price: {price}")
                
            except Exception as e:
                logging.warning(f"Error parsing product {i}: {e}")
                continue
        
        logging.info(f"Successfully parsed {len(all_products)} products")
        return all_products

    
    def _extract_price_from_card(self, card) -> float:
        """
        Extract price from product card.
        
        Args:
            card: WebElement representing a product card.
            
        Returns:
            float: price value or 0.0 if not found or error.
        """
        try:
            text_elements = card.find_elements(By.TAG_NAME, "p")
            for element in text_elements:
                text = element.text
                if '$' in text:
                    price_match = re.search(r'\$(\d+(?:\.\d{2})?)', text)
                    if price_match:
                        return float(price_match.group(1))
            return 0.0
        except Exception:
            return 0.0
    
    def filter_products_by_ingredient(self, products: List[Dict], ingredient: str) -> List[Dict]:
        """
        Filter products that contain specific ingredient.
        
        Args:
            products: List of product dictionaries.
            ingredient: String to search for (e.g., 'Aloe', 'SPF-30').
            
        Returns:
            List of matching product dictionaries.
        """
        filtered = []
        
        # For sunscreens, handle SPF numbers specially
        if "SPF" in ingredient:
            spf_number = ingredient.split("-")[1]  # Get number after hyphen
            for product in products:
                if f"SPF-{spf_number}" in product["name"] or f"SPF {spf_number}" in product["name"]:
                    filtered.append(product)
                    logging.info(f"Found {ingredient} product: {product['name']}")
        else:
            # For other ingredients, do case-insensitive search
            for product in products:
                if ingredient.lower() in product["name"].lower():
                    filtered.append(product)
                    logging.info(f"Found {ingredient} product: {product['name']}")
        
        logging.info(f"Found {len(filtered)} products containing '{ingredient}'")
        return filtered

    def find_cheapest_product(self, products: List[Dict]) -> Optional[Dict]:
        """
        Find the cheapest product in the provided list.
        
        Returns None if no products available.
        """
        if not products:
            logging.warning("No products found to evaluate cheapest.")
            return None
            
        cheapest = min(products, key=lambda x: x['price'])
        logging.info(f"Found cheapest product: {cheapest['name']} at price {cheapest['price']}")
        return cheapest

    
    def select_moisturizer_products(self) -> Tuple[Optional[Dict], Optional[Dict]]:
        """
        Select required moisturizer products (cheapest Aloe + cheapest Almond).
        
        Returns:
            Tuple containing (cheapest_aloe_product, cheapest_almond_product), may contain None.
        """
        all_products = self.get_all_products()
        
        aloe_products = self.filter_products_by_ingredient(all_products, 'Aloe')
        cheapest_aloe = self.find_cheapest_product(aloe_products)
        
        almond_products = self.filter_products_by_ingredient(all_products, 'Almond')
        cheapest_almond = self.find_cheapest_product(almond_products)
        
        return cheapest_aloe, cheapest_almond
    
    def select_sunscreen_products(self) -> Tuple[Optional[Dict], Optional[Dict]]:
        """
        Select required sunscreen products (cheapest SPF-30 + cheapest SPF-50).
        
        Returns:
            Tuple containing (cheapest_spf30_product, cheapest_spf50_product), may contain None.
        """
        all_products = self.get_all_products()
        
        spf30_products = self.filter_products_by_ingredient(all_products, 'SPF-30')
        cheapest_spf30 = self.find_cheapest_product(spf30_products)
        
        spf50_products = self.filter_products_by_ingredient(all_products, 'SPF-50')
        cheapest_spf50 = self.find_cheapest_product(spf50_products)
        
        return cheapest_spf30, cheapest_spf50
    
    def add_product_to_cart(self, product: Optional[Dict]):
        """
        Add a specific product to cart by clicking the Add button.
        
        Args:
            product: Product dictionary with 'add_to_cart_button' WebElement.
        
        Raises:
            Exception: if product or button is invalid.
        """
        if product and product.get('add_to_cart_button'):
            try:
                button = product['add_to_cart_button']
                
                # Wait for button to be clickable before clicking
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(button)
                )
                
                # Scroll to button to ensure it's visible
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(0.5)
                
                # Click using JavaScript to ensure the onclick handler executes
                self.driver.execute_script("arguments[0].click();", button)
                logging.info(f"Successfully clicked add to cart for: {product.get('name', 'Unknown')}")
                
                # Wait for cart to update - check cart indicator
                try:
                    # Wait for cart to show something other than "Empty"
                    WebDriverWait(self.driver, 5).until(
                        lambda d: d.find_element(By.ID, "cart").text != "Empty"
                    )
                    cart_text = self.driver.find_element(By.ID, "cart").text
                    logging.info(f"Cart updated to: {cart_text}")
                except:
                    logging.warning("Cart indicator didn't update or couldn't be found")
                
                # Additional wait for any async operations
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"Failed to click add to cart button for {product.get('name', 'Unknown')}: {e}")
                raise
        else:
            raise Exception(f"Cannot add product to cart: {product}")
    
    def add_selected_products_to_cart(self, product_category: str) -> Tuple[Tuple[Dict, Dict], float]:
        """
        Add the appropriate products to cart based on category.
        
        Args:
            product_category: 'moisturizers' or 'sunscreens'.
        
        Returns:
            Tuple of selected products and their total price.
        
        Raises:
            ValueError: If unknown product category is provided.
            Exception: If required products cannot be found.
        """
        if product_category == 'moisturizers':
            product1, product2 = self.select_moisturizer_products()
        elif product_category == 'sunscreens':
            product1, product2 = self.select_sunscreen_products()
        else:
            raise ValueError(f"Unknown product category: {product_category}")
        
        if not product1 or not product2:
            raise Exception(f"Could not find required products for {product_category}")
        
        self.add_product_to_cart(product1)
        self.add_product_to_cart(product2)
        
        total_price = product1['price'] + product2['price']
        
        return (product1, product2), total_price
    
    def go_to_cart(self):
        """Navigate to shopping cart page by clicking the cart button/link."""
        cart_btn = self.driver.find_element(By.ID, "cart")
        cart_btn.click()
        time.sleep(2)  # Give time for navigation
    
    def get_product_count_on_page(self) -> int:
        """
        Get total number of products displayed on the page.
        
        Returns:
            int: count of product cards.
        """
        products = self.find_elements(self.PRODUCT_CARDS)
        return len(products)
    
    def get_product_count_in_cart(self) -> int:
        """
        Placeholder method: Should return number of products in cart.
        To be implemented depending on cart page structure.
        """
        # For now, raise NotImplementedError to indicate it's a stub
        raise NotImplementedError("Method get_product_count_in_cart not implemented yet.")
