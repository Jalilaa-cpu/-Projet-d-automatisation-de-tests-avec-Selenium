from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Setup driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
service = Service(executable_path="C:\\webdrivers\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

try:
    # Go to homepage
    driver.get("https://weathershopper.pythonanywhere.com")
    time.sleep(2)
    
    # Click moisturizers (assuming temperature < 19)
    moisturizers_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'moisturizers')]")
    moisturizers_btn.click()
    time.sleep(3)
    
    # Try different selectors to find products
    selectors_to_try = [
        ".text-center.col-4",
        ".col-4",
        ".text-center",
        "[class*='col-4']",
        "[class*='text-center']",
        ".card",
        ".product",
        "div.col-4"
    ]
    
    print("=== DEBUGGING PRODUCT SELECTORS ===")
    for selector in selectors_to_try:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"Selector '{selector}': Found {len(elements)} elements")
            
            # If we found elements, show first few
            for i, elem in enumerate(elements[:3]):
                try:
                    print(f"  Element {i}: {elem.text[:100]}...")
                except:
                    print(f"  Element {i}: [Could not get text]")
        except Exception as e:
            print(f"Selector '{selector}': Error - {e}")
    
    # Also check page source for common product indicators
    page_source = driver.page_source
    print(f"\nPage contains 'Price': {'Price' in page_source}")
    print(f"Page contains 'Add': {'Add' in page_source}")
    print(f"Page contains 'Cart': {'Cart' in page_source}")
    print(f"Page contains 'col-4': {'col-4' in page_source}")
    print(f"Page contains 'text-center': {'text-center' in page_source}")
    
    # Save page source for inspection
    with open("moisturizers_page_source.html", "w", encoding="utf-8") as f:
        f.write(page_source)
    print("\nPage source saved to 'moisturizers_page_source.html'")
    
    # Take a screenshot
    driver.save_screenshot("moisturizers_page.png")
    print("Screenshot saved to 'moisturizers_page.png'")

finally:
    driver.quit()