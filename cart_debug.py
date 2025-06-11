from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Go to homepage
    driver.get("https://weathershopper.pythonanywhere.com")
    logging.info("Opened homepage")
    time.sleep(2)
    
    # Click moisturizers 
    driver.find_element(By.XPATH, "//button[contains(text(), 'moisturizers')]").click()
    logging.info("Clicked on moisturizers")
    time.sleep(2)
    
    # Find the first product and its Add button
    product_elements = driver.find_elements(By.CSS_SELECTOR, ".col-4")
    if product_elements:
        product = product_elements[0]  # First product
        product_name = product.find_element(By.TAG_NAME, "p").text.strip()
        
        # Get cart text before adding
        cart_before = driver.find_element(By.XPATH, "//a[contains(@href, '/cart')]").text
        logging.info(f"Cart before adding: {cart_before}")
        
        # Find and click Add button using JavaScript
        add_button = product.find_element(By.TAG_NAME, "button")
        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(1)
        
        # THIS IS KEY: Instead of using the regular click, let's execute the JavaScript function directly
        # First, we need to extract the product name and price from the onclick attribute
        onclick_attr = add_button.get_attribute("onclick")
        logging.info(f"Button onclick attribute: {onclick_attr}")
        
        # Click using both methods to ensure it works
        logging.info(f"Adding product: {product_name}")
        driver.execute_script("arguments[0].click();", add_button)
        
        # Wait to see if cart updates
        time.sleep(3)
        
        # Get cart text after adding
        try:
            cart_after = driver.find_element(By.XPATH, "//a[contains(@href, '/cart')]").text
            logging.info(f"Cart after adding: {cart_after}")
        except:
            logging.info("Could not find cart text after adding")
        
        # Take screenshot
        driver.save_screenshot("after_add_product.png")
        
        # Navigate to cart page
        driver.get("https://weathershopper.pythonanywhere.com/cart")
        logging.info("Navigated to cart page")
        time.sleep(3)
        
        # Check if cart has items
        cart_items = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        logging.info(f"Found {len(cart_items)} items in cart")
        
        # Take screenshot of cart page
        driver.save_screenshot("cart_page.png")
        
        # Check page source
        page_source = driver.page_source
        if product_name in page_source:
            logging.info(f"Product '{product_name}' found in cart page source")
        else:
            logging.info(f"Product '{product_name}' NOT found in cart page source")
    else:
        logging.error("No products found")

finally:
    # Quit driver
    driver.quit()