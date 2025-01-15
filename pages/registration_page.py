import uuid
from selenium.webdriver.common.by import By
import logging
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
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
    PASSWORD_ERROR = (By.XPATH, "//span[@data-valmsg-for='Password']")
    CONFIRM_PASSWORD_FIELD = (By.ID, "ConfirmPassword")
    CONFIRM_PASSWORD_ERROR = (By.ID, "ConfirmPassword-error")
    REGISTER_BUTTON = (By.XPATH, '//*[@id="register-button"]')
    SUCCESS_MESSAGE = (By.CLASS_NAME, "result")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger("RegistrationPage")
        logging.basicConfig(level=logging.INFO)

    def open_url(self, url="https://demo.nopcommerce.com/register?returnUrl=%2F"):
        self.driver.get(url)

    def generate_unique_email(self, base_email):
        email_prefix, email_domain = base_email.split("@")
        unique_email = f"{email_prefix}_{uuid.uuid4().hex[:8]}@{email_domain}"
        return unique_email

    def submit_registration_form(self):
        self.logger.info("Submitting registration form.")
        self.click(self.REGISTER_BUTTON)

    def is_registration_successful(self):
        self.logger.info("Checking if registration was successful.")
        return self.is_element_visible(*self.SUCCESS_MESSAGE)

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

    # To use
    def validate_password_visibility(self, is_visible):
        if is_visible:
            assert self.is_password_visible(), "Password field should be visible."
            assert self.is_confirm_password_visible(), "Confirm password field should be visible."
        else:
            assert self.is_password_hidden(), "Password field should be hidden."
            assert self.is_confirm_password_hidden(), "Confirm password field should be hidden."

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

    def fill_fields(self, fields):
        for field, value in fields.items():
            self.logger.info(f"Entering value '{value}' in field '{field}'")
            self.enter_text(field, value)

    def fill_mandatory_fields(self, test_data):
        self.logger.info("Filling mandatory fields in the registration form.")

        mandatory_fields = {
            self.FIRST_NAME_FIELD: test_data['first_name'],
            self.LAST_NAME_FIELD: test_data['last_name'],
            self.EMAIL_FIELD: test_data['email'],
            self.PASSWORD_FIELD: test_data['password'],
            self.CONFIRM_PASSWORD_FIELD: test_data['confirm_password']
        }

        self.fill_fields(mandatory_fields)

        self.click(self.REGISTER_BUTTON)

    def fill_all_fields(self, test_data):
        self.logger.info("Filling all fields in the registration form.")

        gender_field = self.select_gender(test_data['gender'])
        self.click(gender_field)

        all_fields = {
            self.FIRST_NAME_FIELD: test_data['first_name'],
            self.LAST_NAME_FIELD: test_data['last_name'],
            self.EMAIL_FIELD: test_data['email'],
            self.COMPANY_NAME_FIELD: test_data['company'],
            self.PASSWORD_FIELD: test_data['password'],
            self.CONFIRM_PASSWORD_FIELD: test_data['confirm_password']
        }

        self.fill_fields(all_fields)

        self.logger.info(f"Selecting birth date: {test_data['birth_day']}-{test_data['birth_month']}-{test_data['birth_year']}")
        self.select_dropdown_option(self.BIRTH_DATE_DROPDOWNS['day'], test_data['birth_day'])
        self.select_dropdown_option(self.BIRTH_DATE_DROPDOWNS['month'], test_data['birth_month'])
        self.select_dropdown_option(self.BIRTH_DATE_DROPDOWNS['year'], test_data['birth_year'])

        if test_data['newsletter'].lower() == "yes":
            self.click(self.NEWSLETTER_CHECKBOX_FIELD)
        else:
            self.click(self.NEWSLETTER_CHECKBOX_FIELD)

        self.click(self.REGISTER_BUTTON)

    def select_gender(self, gender):
        gender_value = 'male' if gender.lower() == "male" else 'female'
        self.logger.info(f"Selected gender: {gender_value}")
        return self.GENDER_MALE_RADIO_BUTTON if gender.lower() == "male" else self.GENDER_FEMALE_RADIO_BUTTON

    def get_mandatory_fields(self):
        return [
            self.FIRST_NAME_FIELD,
            self.LAST_NAME_FIELD,
            self.EMAIL_FIELD,
            self.PASSWORD_FIELD,
            self.CONFIRM_PASSWORD_FIELD
        ]

    def get_error_mandatory_fields(self):
        return [
            self.FIRST_NAME_ERROR,
            self.LAST_NAME_ERROR,
            self.EMAIL_ERROR,
            self.PASSWORD_ERROR,
            self.CONFIRM_PASSWORD_ERROR
        ]

    def fill_form_with_mismatched_passwords(self, test_data):
        fields = {
            self.FIRST_NAME_FIELD: test_data['first_name'],
            self.LAST_NAME_FIELD: test_data['last_name'],
            self.EMAIL_FIELD: test_data['email'],
            self.PASSWORD_FIELD: test_data['password'],
            self.CONFIRM_PASSWORD_FIELD: "DifferentPassword123"
        }

        self.fill_fields(fields)

        self.submit_registration_form()

    def verify_error_fields_displayed(self, error_fields):

        self.logger.info(f"Verifying visibility of error fields: {error_fields}")
        for error_field in error_fields:
            assert self.is_element_visible(*error_field), f"{error_field} mismatch error not displayed."

    def fill_form_with_invalid_email(self, test_data):
        invalid_email = "invalid-email.com"

        fields = {
            self.FIRST_NAME_FIELD: test_data['first_name'],
            self.LAST_NAME_FIELD: test_data['last_name'],
            self.EMAIL_FIELD: invalid_email,
            self.PASSWORD_FIELD: test_data['password'],
            self.CONFIRM_PASSWORD_FIELD: "DifferentPassword123"
        }

        self.fill_fields(fields)

        self.submit_registration_form()

    def fill_form_with_keyboard_keys(self, test_data):
        mandatory_fields = {
            self.FIRST_NAME_FIELD: test_data['first_name'],
            self.LAST_NAME_FIELD: test_data['last_name'],
            self.EMAIL_FIELD: test_data['email'],
            self.PASSWORD_FIELD: test_data['password'],
            self.CONFIRM_PASSWORD_FIELD: test_data['confirm_password']
        }

        for field, value in mandatory_fields.items():
            input_field = self.wait_for_element(*field)
            input_field.send_keys(value)
            input_field.send_keys(Keys.TAB)

        confirm_password_field = self.wait_for_element(*self.CONFIRM_PASSWORD_FIELD)
        confirm_password_field.send_keys(Keys.ENTER)

        self.logger.info("Mandatory fields filled and form submitted using keyboard keys.")

    def validate_placeholders(self):
        expected_placeholders = {
            self.FIRST_NAME_FIELD: "First name",
            self.LAST_NAME_FIELD: "Last name",
            self.EMAIL_FIELD: "Email",
            self.COMPANY_NAME_FIELD: "Company",
            self.PASSWORD_FIELD: "Password",
            self.CONFIRM_PASSWORD_FIELD: "Confirm password"
        }

        all_placeholders_valid = True

        for field_locator, expected_placeholder in expected_placeholders.items():
            field = self.wait_for_element(field_locator, timeout=10)

            if field:
                actual_placeholder = field.get_attribute("placeholder")
                print(
                    f"Field: {field_locator}, Expected: '{expected_placeholder}', Actual: '{actual_placeholder}'")  # Debugging line
                if actual_placeholder != expected_placeholder:
                    all_placeholders_valid = False
            else:
                all_placeholders_valid = False

        return all_placeholders_valid

    def validate_asterisk(self):
        mandatory_fields = {
            self.FIRST_NAME_FIELD: "First Name",
            self.LAST_NAME_FIELD: "Last Name",
            self.EMAIL_FIELD: "Email",
            self.PASSWORD_FIELD: "Password",
            self.CONFIRM_PASSWORD_FIELD: "Confirm Password"
        }

        all_fields_valid = True

        for field_locator, field_name in mandatory_fields.items():
            field_label = self.wait_for_element(By.XPATH, f"//label[@for='{field_locator[1]}']")
            if not field_label:
                print(f"Label for {field_name} not found!")
                all_fields_valid = False
                continue

            try:
                asterisk = field_label.find_element(By.XPATH, ".//*[contains(@class, 'required')]")
                color = asterisk.value_of_css_property("color")
                print(f"Asterisk color for {field_name}: {color}")

                if not asterisk.is_displayed() or color != "rgba(255, 0, 0, 1)":
                    print(f"Mandatory field {field_name} is not marked with a red '*' symbol.")
                    all_fields_valid = False
            except Exception as e:
                print(f"Error locating asterisk for {field_name}: {str(e)}")
                all_fields_valid = False

        # Return whether all fields were validated successfully
        return all_fields_valid
    def validate_spaces(self):
        mandatory_fields = self.get_mandatory_fields()

        for field_locator in mandatory_fields:
            self.enter_text(field_locator, "     ")

        self.submit_registration_form()

        error_fields = [
            self.FIRST_NAME_ERROR,
            self.LAST_NAME_ERROR,
            self.EMAIL_ERROR,
            self.PASSWORD_ERROR,
            self.CONFIRM_PASSWORD_ERROR
        ]

        assert self.are_field_errors_displayed(error_fields), \
            "Validation error messages are not displayed for fields with only spaces."

        print("All mandatory fields correctly reject only spaces and display error messages.")

    def validate_password_and_registration(self, password, error_locators):
        password_strength = self.check_password_strength(password)
        self.logger.info(f"Password strength: {password_strength}")

        if password_strength != "Strong":
            self.logger.error(f"Expected strong password, but got {password_strength}")
            return False

        if self.is_registration_successful():
            self.logger.info(f"Registration with strong password {password} was successful.")
            return True
        else:
            self.logger.error("Registration failed. Checking for field errors.")
            self.verify_error_fields_displayed(error_locators)
            return False

    def validate_field_and_check_error(self, field_locator, expected_error_message, first_name, last_name,
                                       email, password, confirm_password):
        self.clear_error_messages()

        self.enter_text(self.FIRST_NAME_FIELD, first_name)
        self.enter_text(self.LAST_NAME_FIELD, last_name)
        self.enter_text(self.EMAIL_FIELD, email)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.enter_text(self.CONFIRM_PASSWORD_FIELD, confirm_password)

        self.submit_registration_form()

        error_locators = [(field_locator, expected_error_message)]
        assert self.are_field_errors_displayed(error_locators), \
            f"Expected error message '{expected_error_message}' for field {field_locator} but it was not displayed."

    def blank_fields_and_validate_errors(self, test_data):
        fields_to_test = [
            (self.FIRST_NAME_FIELD, "First name is required.", "", test_data['last_name'],
             test_data['email'], test_data['password'], test_data['confirm_password']),
            (self.LAST_NAME_FIELD, "Last name is required.", test_data['first_name'], "",
             test_data['email'], test_data['password'], test_data['confirm_password']),
            (self.EMAIL_FIELD, "Email is required.", test_data['first_name'], test_data['last_name'], "",
             test_data['password'], test_data['confirm_password']),
            (self.PASSWORD_FIELD, "Password is required.", test_data['first_name'], test_data['last_name'],
             test_data['email'], "", test_data['confirm_password']),
            (self.CONFIRM_PASSWORD_FIELD, "Confirm Password is required.", test_data['first_name'],
             test_data['last_name'], test_data['email'], test_data['password'], "")
        ]

        for field_locator, expected_error_message, first_name, last_name, email, password, confirm_password in fields_to_test:
            self.validate_field_and_check_error(field_locator, expected_error_message, first_name, last_name, email,
                                                password, confirm_password)


