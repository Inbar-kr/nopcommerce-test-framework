from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
from pages.base_page import BasePage
from utils.wait_util import WaitUtil

class LoginPage(BasePage):
    # Locators for elements on the Login page
    EMAIL_FIELD = (By.ID, "Email")
    EMAIL_ERROR = (By.ID, "Email-error")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.XPATH, '//button[@type="submit" and contains(@class, "login-button") and contains(@class, "button-1")]')
    REMEMBER_ME_CHECKBOX = (By.ID, "RememberMe")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot password?")
    ERROR_MESSAGE = (By.CLASS_NAME, "message-error.validation-summary-errors")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger("LoginPage")
        logging.basicConfig(level=logging.INFO)

    def open_url(self):
        self.driver.get("https://demo.nopcommerce.com/login?returnUrl=%2F")

    def enter_text(self, field_locator, text: str):
        self.logger.info(f"Entering text '{text}' into field {field_locator}")
        field = self.wait_for_element(field_locator)
        field.clear()
        field.send_keys(text)

    def click(self, locator):
        if isinstance(locator, tuple):
            by, value = locator
            element = self.wait_for_element((by, value))
        else:
            element = self.wait_for_element(locator)

        if element:
            element.click()
            return True
        else:
            self.logger.error(f"Element not found: {locator}")
            return False

    def submit_login_form(self):
        self.logger.info("Submitting the login form.")
        self.click(self.LOGIN_BUTTON)

    def wait_for_element(self, locator, timeout=10):
        self.logger.info(f"Waiting for element: {locator}")
        return WaitUtil.wait_for_element(self.driver, locator, EC.presence_of_element_located, timeout)

    def wait_for_element_to_be_visible(self, locator, timeout=10):
        self.logger.info(f"Waiting for element to be visible: {locator}")
        return WaitUtil.wait_for_element_to_be_visible(self.driver, locator, timeout)

    def is_element_visible(self, locator):
        try:
            self.wait_for_element(locator)
            return True
        except Exception as e:
            self.logger.error(f"Error while checking visibility of element {locator}: {str(e)}")
            return False

    def get_element(self, locator):
        """Returns a WebElement after waiting for it to be visible."""
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_placeholder(self, driver, field_locator, expected_placeholder):
        """Waits for the element to be visible and validates the placeholder text."""
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(field_locator))
            field_element = driver.find_element(*field_locator)
            actual_placeholder = field_element.get_attribute("placeholder")

            assert actual_placeholder == expected_placeholder, \
                f"Expected placeholder '{expected_placeholder}', but got '{actual_placeholder}'."
            print(f"Field with locator {field_locator} has the correct placeholder: '{expected_placeholder}'")
        except Exception as e:
            print(f"Error: {e}")
