from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import logging
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistrationPage(BasePage):
    # Locators for elements on the Registration page
    GENDER_MALE_RADIO_BUTTON = (By.ID, "gender-male")
    GENDER_FEMALE_RADIO_BUTTON = (By.ID, "gender-female")
    FIRST_NAME_FIELD = (By.ID, "FirstName")
    FIRST_NAME_ERROR = (By.ID, "FirstName-error")
    LAST_NAME_FIELD = (By.ID, "LastName")
    LAST_NAME_ERROR = (By.ID, "LastName-error")
    BIRTH_DATE_DROPDOWNS = {
        'day': (By.NAME, "DateOfBirthDay"),
        'month': (By.NAME, "DateOfBirthMonth"),
        'year': (By.NAME, "DateOfBirthYear")
    }
    EMAIL_FIELD = (By.ID, "Email")
    EMAIL_ERROR = (By.ID, "Email-error")
    COMPANY_NAME_FIELD = (By.ID, "Company")
    NEWSLETTER_CHECKBOX_FIELD = (By.ID, "Newsletter")
    PASSWORD_FIELD = (By.ID, "Password")
    PASSWORD_ERROR = (By.ID, "Password-error")
    CONFIRM_PASSWORD_FIELD = (By.ID, "ConfirmPassword")
    CONFIRM_PASSWORD_ERROR = (By.ID, "ConfirmPassword-error")
    REGISTER_BUTTON = (By.XPATH, '//*[@id="register-button"]')
    SUCCESS_MESSAGE = (By.CLASS_NAME, "result")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger("RegistrationPage")
        logging.basicConfig(level=logging.INFO)

    def open_url(self):
        self.driver.get("https://demo.nopcommerce.com/register?returnUrl=%2F")

    def select_birth_date(self, day: str, month: str, year: str):
        self.logger.info(f"Selecting birth date: Day={day}, Month={month}, Year={year}")
        self.select_dropdown_value(self.BIRTH_DATE_DROPDOWNS['day'], day)
        self.select_dropdown_value(self.BIRTH_DATE_DROPDOWNS['month'], month)
        self.select_dropdown_value(self.BIRTH_DATE_DROPDOWNS['year'], year)

    def select_dropdown_value(self, dropdown_locator, value: str):
        dropdown = self.wait_for_element(dropdown_locator[0], dropdown_locator[1])
        select = Select(dropdown)
        select.select_by_visible_text(value)
        self.logger.info(f"Selected '{value}' in dropdown {dropdown_locator}")

    def enter_text(self, field_locator, text: str):
        self.logger.info(f"Entering text '{text}' into field {field_locator}")
        field = self.wait_for_element(field_locator[0], field_locator[1])
        field.clear()
        field.send_keys(text)

    def submit_registration_form(self):
        self.logger.info("Submitting registration form.")
        self.click(*self.REGISTER_BUTTON)
        self.wait_for_element(*self.SUCCESS_MESSAGE)

    def click(self, by, value):
        element = self.wait_for_element(by, value)
        if element:
            element.click()
        else:
            self.logger.error(f"Element not found: {value}")

    def is_registration_successful(self):
        self.logger.info("Checking if registration was successful.")
        return self.is_element_present(*self.SUCCESS_MESSAGE) and \
               self.is_element_visible(*self.SUCCESS_MESSAGE)

    def is_element_present(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            return element is not None
        except Exception as e:
            self.logger.error(f"Element {value} not found: {str(e)}")
            return False

    def is_element_visible(self, by, value):
        try:
            self.wait_for_element(by, value)
            return True
        except Exception as e:
            self.logger.error(f"Error while checking visibility of element {value}: {str(e)}")
            return False

    def wait_for_element(self, by, value, timeout=10):
        self.logger.info(f"Waiting for element {value} to appear.")
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except Exception as e:
            self.logger.error(f"Error while waiting for element {value}: {str(e)}")
            return None

    def are_field_errors_displayed(self, error_locators):
        self.logger.info("Checking if error messages are displayed for each field.")
        for error_locator in error_locators:
            if not self.is_element_visible(*error_locator):
                self.logger.error(f"Error message not displayed for {error_locator}")
                return False
        return True

    def wait_for_placeholder(self, driver, field_locator, expected_placeholder, timeout=10):
        try:
            element = WebDriverWait(driver, timeout).until(
                lambda driver: driver.find_element(*field_locator)
            )
            actual_placeholder = element.get_attribute("placeholder")

            if actual_placeholder == expected_placeholder:
                self.logger.info(f"Placeholder for {field_locator} is correct: '{expected_placeholder}'")
            else:
                self.logger.error(
                    f"Expected placeholder '{expected_placeholder}', but got '{actual_placeholder}' for {field_locator}.")
                return False
        except Exception as e:
            self.logger.error(f"Error occurred while checking placeholder for {field_locator}: {e}")
            return False
        return True

    def check_password_strength(self, password: str) -> str:

        length_check = len(password) >= 8
        lowercase_check = any(c.islower() for c in password)
        uppercase_check = any(c.isupper() for c in password)
        digit_check = any(c.isdigit() for c in password)
        special_char_check = any(c in "!@#$%^&*()_+[]{}|;:,.<>?/~" for c in password)

        if length_check and lowercase_check and uppercase_check and digit_check and special_char_check:
            self.logger.info("Password is Strong")
            return "Strong"
        elif length_check and (lowercase_check or uppercase_check) and digit_check:
            self.logger.info("Password is Medium")
            return "Medium"
        else:
            self.logger.info("Password is Weak")
            return "Weak"

    def clear_error_messages(self):
        self.logger.info("Clearing error messages for all fields.")
        error_fields = [
            self.FIRST_NAME_ERROR,
            self.LAST_NAME_ERROR,
            self.EMAIL_ERROR,
            self.PASSWORD_ERROR,
            self.CONFIRM_PASSWORD_ERROR
        ]

        for error_field in error_fields:
            try:
                error_element = self.wait_for_element(*error_field)
                if error_element.is_displayed():
                    self.logger.info(f"Clearing error message: {error_field}")
                    self.driver.execute_script("arguments[0].innerHTML = '';", error_element)
            except Exception as e:
                self.logger.error(f"Error while clearing error message for {error_field}: {str(e)}")

    def is_password_hidden(self):
        password_field = self.wait_for_element(*self.PASSWORD_FIELD)
        password_type = password_field.get_attribute("type")
        return password_type == "password"

    def is_confirm_password_hidden(self):
        confirm_password_field = self.wait_for_element(*self.CONFIRM_PASSWORD_FIELD)
        confirm_password_type = confirm_password_field.get_attribute("type")
        return confirm_password_type == "password"

    def is_password_visible(self):
        password_field = self.wait_for_element(*self.PASSWORD_FIELD)
        password_type = password_field.get_attribute("type")
        return password_type == "text"

    def is_confirm_password_visible(self):
        confirm_password_field = self.wait_for_element(*self.CONFIRM_PASSWORD_FIELD)
        confirm_password_type = confirm_password_field.get_attribute("type")
        return confirm_password_type == "text"

    def toggle_password_visibility(self):
        password_field = self.wait_for_element(*self.PASSWORD_FIELD)
        confirm_password_field = self.wait_for_element(*self.CONFIRM_PASSWORD_FIELD)

        if password_field.get_attribute("type") == "password":
            self.driver.execute_script("arguments[0].setAttribute('type', 'text');", password_field)
            self.driver.execute_script("arguments[0].setAttribute('type', 'text');", confirm_password_field)
        else:
            self.driver.execute_script("arguments[0].setAttribute('type', 'password');", password_field)
            self.driver.execute_script("arguments[0].setAttribute('type', 'password');", confirm_password_field)

        self.logger.info("Password visibility toggled.")