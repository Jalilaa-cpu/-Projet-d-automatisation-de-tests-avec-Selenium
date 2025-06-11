import pytest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.payment_page import PaymentPage

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weather_shopper_automation.log"),
        logging.StreamHandler()
    ]
)

# --- Utility Functions ---
def scroll_to_bottom(driver):
    logging.info("Scrolling to bottom of the page.")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

def scroll_into_view(driver, element):
    if element:
        logging.info("Scrolling element into view.")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
    else:
        logging.warning("Attempted to scroll None element into view.")

def highlight_element(driver, element, color="red"):
    if element:
        driver.execute_script(f"arguments[0].style.border='3px solid {color}'", element)

# --- Pytest Driver Fixture ---
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(executable_path="C:\\webdrivers\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

# --- Main Test ---
def test_weather_shopper_flow(driver):
    logging.info("=== Weather Shopper Automation Test Started ===")

    # Step 1: Visit Homepage
    try:
        driver.get("https://weathershopper.pythonanywhere.com")
        logging.info("Opened Weather Shopper homepage.")
    except Exception as e:
        pytest.fail(f"Failed to load homepage: {e}")

    # Step 2: Read Temperature
    try:
        home = HomePage(driver)
        temperature = home.get_current_temperature()
        logging.info(f"Current temperature: {temperature}°C")
    except Exception as e:
        pytest.fail(f"Could not read temperature: {e}")

    # Step 3: Select Products
    try:
        product_page = ProductPage(driver)

        if temperature < 19:
            logging.info("Temperature < 19°C: Selecting moisturizers.")
            home.click_moisturizers_button()
            time.sleep(2)
            scroll_to_bottom(driver)

            all_products = product_page.get_all_products()
            logging.info(f"Found {len(all_products)} total products")

            aloe_products = product_page.filter_products_by_ingredient(all_products, "Aloe")
            logging.info(f"Found {len(aloe_products)} Aloe moisturizer products.")
            aloe = product_page.find_cheapest_product(aloe_products)

            if aloe is None or aloe.get('element') is None:
                pytest.fail("No Aloe moisturizer product found to add to cart.")
            else:
                scroll_into_view(driver, aloe['element'])
                highlight_element(driver, aloe['element'], "green")
                logging.info(f"Adding Aloe product: {aloe.get('name', 'Unknown')} - ${aloe.get('price', 0)}")
                product_page.add_product_to_cart(aloe)
                time.sleep(3)  # Wait for cart update
                
                # Debug: Check if cart icon shows items
                try:
                    cart_icon = driver.find_element(By.XPATH, "//span[contains(@class, 'cart') or contains(text(), 'cart')]")
                    logging.info(f"Cart icon text after adding Aloe: {cart_icon.text}")
                except:
                    logging.info("No cart icon found")
                
                # Debug: Try to navigate to cart and check immediately
                driver.get("https://weathershopper.pythonanywhere.com/cart")
                time.sleep(2)
                page_source = driver.page_source
                if "Jose Intensive Care Aloe" in page_source or "Aloe" in page_source:
                    logging.info("Aloe product found in cart page source")
                else:
                    logging.warning("Aloe product NOT found in cart page source")
                
                # Go back to product page
                driver.back()
                time.sleep(2)

            almond_products = product_page.filter_products_by_ingredient(all_products, "Almond")
            logging.info(f"Found {len(almond_products)} Almond moisturizer products.")
            almond = product_page.find_cheapest_product(almond_products)

            if almond is None or almond.get('element') is None:
                pytest.fail("No Almond moisturizer product found to add to cart.")
            else:
                scroll_into_view(driver, almond['element'])
                highlight_element(driver, almond['element'], "blue")
                logging.info(f"Adding Almond product: {almond.get('name', 'Unknown')} - ${almond.get('price', 0)}")
                product_page.add_product_to_cart(almond)
                time.sleep(3)  # Longer wait for cart update

        elif temperature > 34:
            logging.info("Temperature > 34°C: Selecting sunscreens.")
            home.click_sunscreens_button()
            time.sleep(2)
            scroll_to_bottom(driver)

            all_products = product_page.get_all_products()
            logging.info(f"Found {len(all_products)} total products")

            filtered_spf30 = product_page.filter_products_by_ingredient(all_products, "SPF-30")
            logging.info(f"Found {len(filtered_spf30)} SPF-30 sunscreen products.")
            spf30 = product_page.find_cheapest_product(filtered_spf30)

            if spf30 is None or spf30.get('element') is None:
                pytest.fail("No SPF-30 sunscreen product found to add to cart.")
            else:
                scroll_into_view(driver, spf30['element'])
                highlight_element(driver, spf30['element'], "orange")
                logging.info(f"Adding SPF-30 product: {spf30.get('name', 'Unknown')} - ${spf30.get('price', 0)}")
                product_page.add_product_to_cart(spf30)
                time.sleep(3)  # Longer wait for cart update

            filtered_spf50 = product_page.filter_products_by_ingredient(all_products, "SPF-50")
            logging.info(f"Found {len(filtered_spf50)} SPF-50 sunscreen products.")
            spf50 = product_page.find_cheapest_product(filtered_spf50)

            if spf50 is None or spf50.get('element') is None:
                pytest.fail("No SPF-50 sunscreen product found to add to cart.")
            else:
                scroll_into_view(driver, spf50['element'])
                highlight_element(driver, spf50['element'], "red")
                logging.info(f"Adding SPF-50 product: {spf50.get('name', 'Unknown')} - ${spf50.get('price', 0)}")
                product_page.add_product_to_cart(spf50)
                time.sleep(3)  # Longer wait for cart update

        else:
            logging.info("Moderate temperature. No product to select.")
            pytest.skip("Temperature not extreme enough to select products.")

    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail(f"Error while selecting products: {e}")

    # Step 4: Validate Cart
    try:
        cart = CartPage(driver)
        cart.navigate_to_cart()  # Make sure this uses a click, not driver.get!
        
        # Check cart immediately after navigation
        initial_items = cart.get_cart_items()
        logging.info(f"Initial cart check: found {len(initial_items)} items")
        
        if len(initial_items) < 2:
            # Wait up to 15 seconds for items to appear
            for attempt in range(15):
                time.sleep(1)
                current_items = cart.get_cart_items()
                logging.info(f"Attempt {attempt + 1}: found {len(current_items)} items")
                if len(current_items) >= 2:
                    break
            else:
                # Final check - take screenshot for debugging
                driver.save_screenshot("cart_final_check.png")
                pytest.fail(f"Expected 2 items in cart, but found {len(current_items)} after waiting")
        
        cart_items = cart.get_cart_items()
        assert len(cart_items) == 2, f"Expected 2 items in cart, got {len(cart_items)}"

        expected_total = cart.calculate_expected_total()
        displayed_total = cart.get_displayed_total()
        logging.info(f"Expected total: {expected_total}, Displayed total: {displayed_total}")
        
        assert expected_total == displayed_total, f"Cart total mismatch: expected {expected_total}, got {displayed_total}"

        cart.click_pay_with_card()
        logging.info("Proceeded to payment.")

        # Wait for the payment form to appear (optional, but helps with timing)
        time.sleep(2) 

        payment = PaymentPage(driver)
        payment.fill_payment_form(
            email="test@example.com",
            card="4242424242424242",
            exp="1234",
            cvc="123",
            zip_code="12345"
        )
        payment.submit_payment()
        assert payment.is_payment_successful(), "Payment was not successful!"
        logging.info("Payment completed and verified successfully.")

    except Exception as e:
        pytest.fail(f"Cart validation or navigation to payment failed: {e}")

    logging.info("=== Test Passed Successfully ===")
    logging.info("Weather Shopper Automation Test Completed.")
    assert True, "Test completed successfully without errors."


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
    # To run the test, execute this script directly or use pytest command in terminal.
