"""
Payment Page Object - Stripe payment form handling
Manages payment form filling and success verification
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
import time


class PaymentPage(BasePage):
    """Page object for Stripe payment page"""

    # Test data for Stripe payment form (can be overridden)
    TEST_EMAIL = "test@example.com"
    TEST_CARD_NUMBER = "4242424242424242"
    TEST_EXPIRY = "1225"  # MMYY format
    TEST_CVC = "123"
    TEST_ZIP = "12345"

    # Locators (Stripe form fields are often in iframe)
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[name='email']")
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, "input[name='cardnumber']")
    EXPIRY_FIELD = (By.CSS_SELECTOR, "input[name='exp-date']")
    CVC_FIELD = (By.CSS_SELECTOR, "input[name='cvc']")
    ZIP_FIELD = (By.CSS_SELECTOR, "input[name='postal']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # Alternative locators (fallbacks)
    ALT_EMAIL_FIELD = (By.ID, "email")
    ALT_CARD_FIELD = (By.ID, "card-number")
    ALT_EXPIRY_FIELD = (By.ID, "card-expiry")
    ALT_CVC_FIELD = (By.ID, "card-cvc")
    ALT_ZIP_FIELD = (By.ID, "billing-zip")

    # Success message locators
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'Payment successful')]")
    ALT_SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'Success')]")

    def wait_for_payment_form(self, timeout=15):
        """
        Wait for Stripe Checkout popup iframe and its fields to load.
        Returns True if form appears within timeout, else False.
        """
        try:
            print(f"Waiting for Stripe iframe and payment form to load (timeout={timeout}s)...")
            # Wait for the Stripe iframe to appear
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='stripe_checkout_app'], iframe[title*='Stripe']"))
            )
            # Now inside the iframe, wait for the email field
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            print("Stripe payment form loaded successfully.")
            # Switch back to default content for safety
            self.driver.switch_to.default_content()
            return True
        except Exception as e:
            print(f"[ERROR] Stripe payment form did not load within {timeout}s: {e}")
            self.driver.switch_to.default_content()
            return False

    def switch_to_stripe_iframe_if_needed(self):
        """
        Detect and switch to Stripe iframe if payment fields reside inside.
        Returns True if switched successfully, False otherwise.
        """
        try:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            print(f"Found {len(iframes)} iframe(s), scanning for Stripe payment form...")

            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    if self.is_element_present(self.EMAIL_FIELD, 2) or self.is_element_present(self.CARD_NUMBER_FIELD, 2):
                        print("Switched to Stripe iframe containing payment form.")
                        return True
                    self.driver.switch_to.default_content()
                except Exception as inner_e:
                    print(f"[WARN] Error checking iframe for payment fields: {inner_e}")
                    self.driver.switch_to.default_content()
                    continue

            print("No Stripe iframe detected or payment fields not found in any iframe.")
            return False
        except Exception as e:
            print(f"[ERROR] Exception during iframe switching: {e}")
            self.driver.switch_to.default_content()
            return False

    def fill_email_field(self, email=None):
        """
        Fill the email input field in payment form.
        Attempts multiple locator strategies before raising.
        """
        email = email or self.TEST_EMAIL
        print(f"Filling email field with '{email}'...")

        try:
            if self.is_element_present(self.EMAIL_FIELD):
                self.send_keys_to_element(self.EMAIL_FIELD, email)
            elif self.is_element_present(self.ALT_EMAIL_FIELD):
                self.send_keys_to_element(self.ALT_EMAIL_FIELD, email)
            else:
                # Attempt by common email input attributes
                email_field = self.driver.find_element(
                    By.XPATH, "//input[@type='email' or contains(@placeholder, 'email') or contains(@placeholder, 'Email')]"
                )
                email_field.clear()
                email_field.send_keys(email)
            print("Email field filled successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to fill email field: {e}")
            raise

    def fill_card_number_field(self, card_number=None):
        """
        Fill card number field with provided or test card number.
        """
        card_number = card_number or self.TEST_CARD_NUMBER
        print(f"Filling card number field with '{card_number}'...")

        try:
            if self.is_element_present(self.CARD_NUMBER_FIELD):
                self.send_keys_to_element(self.CARD_NUMBER_FIELD, card_number)
            elif self.is_element_present(self.ALT_CARD_FIELD):
                self.send_keys_to_element(self.ALT_CARD_FIELD, card_number)
            else:
                card_field = self.driver.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'card') or contains(@placeholder, 'Card') or contains(@name, 'card')]"
                )
                card_field.clear()
                card_field.send_keys(card_number)
            print("Card number field filled successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to fill card number field: {e}")
            raise

    def fill_expiry_field(self, expiry=None):
        """
        Fill expiry date field.
        """
        expiry = expiry or self.TEST_EXPIRY
        print(f"Filling expiry date field with '{expiry}'...")

        try:
            if self.is_element_present(self.EXPIRY_FIELD):
                self.send_keys_to_element(self.EXPIRY_FIELD, expiry)
            elif self.is_element_present(self.ALT_EXPIRY_FIELD):
                self.send_keys_to_element(self.ALT_EXPIRY_FIELD, expiry)
            else:
                expiry_field = self.driver.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'expir') or contains(@placeholder, 'MM') or contains(@name, 'exp')]"
                )
                expiry_field.clear()
                # Format expiry as "MM / YY" with spaces
                exp_formatted = expiry.replace("/", " / ")
                expiry_field.send_keys(exp_formatted)
            print("Expiry date field filled successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to fill expiry date field: {e}")
            raise

    def fill_cvc_field(self, cvc=None):
        """
        Fill CVC field.
        """
        cvc = cvc or self.TEST_CVC
        print(f"Filling CVC field with '{cvc}'...")

        try:
            if self.is_element_present(self.CVC_FIELD):
                self.send_keys_to_element(self.CVC_FIELD, cvc)
            elif self.is_element_present(self.ALT_CVC_FIELD):
                self.send_keys_to_element(self.ALT_CVC_FIELD, cvc)
            else:
                cvc_field = self.driver.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'CVC') or contains(@placeholder, 'cvc') or contains(@name, 'cvc')]"
                )
                cvc_field.clear()
                cvc_field.send_keys(cvc)
            print("CVC field filled successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to fill CVC field: {e}")
            raise

    def fill_zip_field(self, zip_code=None):
        """
        Fill ZIP/postal code field if present.
        This field might be optional, so failure here doesn't block the flow.
        """
        zip_code = zip_code or self.TEST_ZIP
        print(f"Attempting to fill ZIP/postal code field with '{zip_code}' (optional)...")

        try:
            if self.is_element_present(self.ZIP_FIELD):
                self.send_keys_to_element(self.ZIP_FIELD, zip_code)
                print("ZIP/postal code field filled successfully.")
            elif self.is_element_present(self.ALT_ZIP_FIELD):
                self.send_keys_to_element(self.ALT_ZIP_FIELD, zip_code)
                print("ZIP/postal code field filled successfully (alternative locator).")
            else:
                zip_field = self.driver.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'zip') or contains(@placeholder, 'postal') or contains(@name, 'postal')]"
                )
                zip_field.clear()
                zip_field.send_keys(zip_code)
                print("ZIP/postal code field filled successfully (by XPath).")
        except Exception as e:
            print(f"[WARN] Could not fill ZIP/postal code field: {e}")
            print("ZIP/postal code field might be optional, continuing without error.")

    def submit_payment_form(self):
        """
        Click the submit/pay button to submit the payment.
        Throws exception if no submit button found or click fails.
        """
        print("Submitting payment form...")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='stripe_checkout_app'], iframe[title*='Stripe']"))
            )
            try:
                payer_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Payer')]")
                self.driver.execute_script("arguments[0].click();", payer_button)
                print("Clicked 'Payer' button (JS).")
            except Exception:
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                self.driver.execute_script("arguments[0].click();", submit_button)
                print("Clicked submit button (fallback, JS).")
            self.driver.switch_to.default_content()
        except Exception as e:
            print(f"[ERROR] Failed to submit payment form: {e}")
            self.driver.switch_to.default_content()
            raise

    def fill_payment_form(self, email="test@example.com", card="4242424242424242", exp="1234", cvc="123", zip_code="12345"):
        """
        Orchestrates filling the entire payment form.
        Waits for form, switches iframe if needed, fills all fields.
        Raises Exception on failure.
        """
        print("Starting payment form fill procedure...")

        if not self.wait_for_payment_form():
            raise Exception("Payment form did not load properly within expected time.")

        # Switch to the Stripe Checkout popup iframe
        WebDriverWait(self.driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='stripe_checkout_app'], iframe[title*='Stripe']"))
        )

        # Fill email
        email_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        email_field.clear()
        email_field.send_keys(email)
        print("Email field filled.")

        # Fill card number (send in 4-digit chunks)
        card_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='carte'], input[placeholder*='card']")
        card_field.clear()
        card_number = card.replace(" ", "")
        for i in range(0, len(card_number), 4):
            chunk = card_number[i:i+4]
            card_field.send_keys(chunk)
            time.sleep(0.2)  # Small delay to mimic human typing and allow Stripe's JS to process
        print("Card number filled.")

        # Fill expiry (send as MMYY, e.g., "0124")
        exp_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='MM'], input[aria-label*='Expiration'], input[name*='exp']")
        exp_field.clear()
        exp_digits = exp.replace("/", "").replace(" ", "")[:4]
        # Type month, wait, then type year
        exp_field.send_keys(exp_digits[:2])
        time.sleep(0.2)
        exp_field.send_keys(exp_digits[2:])
        time.sleep(0.2)
        exp_field.send_keys(Keys.TAB)
        print("Expiry filled.")

        # Fill CVC
        cvc_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='CVV'], input[placeholder*='CVC']")
        cvc_field.clear()
        cvc_field.send_keys(cvc)
        cvc_field.send_keys(Keys.TAB)
        print("CVC filled.")

        # Fill ZIP/postal code if present
        try:
            zip_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='ZIP'], input[placeholder*='zip'], input[placeholder*='Code postal']")
            zip_field.clear()
            zip_field.send_keys(zip_code)
            print("ZIP/postal code filled.")
        except Exception:
            print("ZIP/postal code field not present or not required.")

        self.driver.switch_to.default_content()
        print("Payment form filled successfully.")

    def submit_payment(self):
        """
        Submits the payment form and waits for confirmation message.
        Returns True if payment success detected, else False.
        """
        try:
            self.submit_payment_form()
            print("Payment form submitted, awaiting success confirmation...")

            WebDriverWait(self.driver, 10).until(
                lambda d: (
                    self.is_element_present(self.SUCCESS_MESSAGE, 2) or
                    self.is_element_present(self.ALT_SUCCESS_MESSAGE, 2)
                )
            )

            print("Payment successful!")
            return True

        except Exception as e:
            print(f"[ERROR] Payment submission failed or success message not found: {e}")
            return False
    def is_payment_successful(self):
        """
        Check if payment was successful by looking for success message.
        Returns True if success message found, else False.
        """
        try:
            print("Checking for payment success message...")
            return self.is_element_present(self.SUCCESS_MESSAGE) or self.is_element_present(self.ALT_SUCCESS_MESSAGE)
        except Exception as e:
            print(f"[ERROR] Error checking payment success: {e}")
            return False