import uuid
from selenium.webdriver.common.by import By
import logging
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys


class RegistrationPage(BasePage):
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

    def _validate_placeholder_for_field(self, driver, field_locator, expected_placeholder):
        field = self.wait_for_element(field_locator, timeout=10)
        if field:
            actual_placeholder = field.get_attribute("placeholder")
            assert actual_placeholder == expected_placeholder, \
                f"Placeholder mismatch! Expected: '{expected_placeholder}', but got: '{actual_placeholder}'"
            self.logger.info(f"Placeholder for field '{field_locator}' is correct.")
        else:
            self.logger.error(f"Field '{field_locator}' not found.")

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

        self.logger.info("Attempted to fill in all the mandatory fields.")

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

    def validate_placeholders(self, driver):
        self.open_url()

        expected_placeholders = {
            self.FIRST_NAME_FIELD: "First name",
            self.LAST_NAME_FIELD: "Last name",
            self.EMAIL_FIELD: "Email",
            self.COMPANY_NAME_FIELD: "Company",
            self.PASSWORD_FIELD: "Password",
            self.CONFIRM_PASSWORD_FIELD: "Confirm password"
        }

        for field_locator, expected_placeholder in expected_placeholders.items():
            self._validate_placeholder_for_field(driver, field_locator, expected_placeholder)

    def validate_asterisk(self, field_locator, field_name):
        field_label = self.wait_for_element(By.XPATH, f"//label[@for='{field_locator[1]}']")
        if not field_label:
            self.logger.info(f"Label for {field_name} not found!")
            return False
        try:
            asterisk = field_label.find_element(By.XPATH, ".//*[contains(@class, 'required')]")
            color = asterisk.value_of_css_property("color")
            self.logger.info(f"Asterisk color for {field_name}: {color}")
            return asterisk.is_displayed() and color == "rgba(255, 0, 0, 1)"
        except Exception as e:
            self.logger.error(f"Error locating asterisk for {field_name}: {str(e)}")
            return False

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

        self.logger.info("Attempt to fill the registration form with only spaces.")

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

    def mandatory_fields_registration(self, load_test_data):
        test_data = load_test_data['mandatory_fields']
        self.open_url()

        test_data['email'] = self.generate_unique_email(test_data['email'])
        self.fill_mandatory_fields(test_data)

        if self.is_registration_successful():
            self.logger.info("Registration successful. Success message displayed.")
        else:
            self.logger.error("Registration failed. Success message not displayed.")

        assert self.is_registration_successful(), "Registration failed. Success message not displayed."

    def all_fields_registration(self, load_test_data):
        test_data = load_test_data['all_fields']
        self.open_url()

        test_data['email'] = self.generate_unique_email(test_data['email'])

        self.open_url()

        self.fill_all_fields(test_data)

        if self.is_registration_successful():
            self.logger.info("Registration successful. Success message displayed.")
        else:
            self.logger.error("Registration failed. Success message not displayed.")

        assert self.is_registration_successful(), "Registration failed. Success message not displayed."

    def empty_registration(self):
        self.open_url()
        self.submit_registration_form()

        mandatory_fields = self.get_mandatory_fields()

        assert self.are_field_errors_displayed(
            mandatory_fields), "Validation error messages are not displayed for all mandatory fields."

    def password_mismatch_registration(self, load_test_data):
        test_data = load_test_data['mandatory_fields']
        self.open_url()

        test_data['email'] = self.generate_unique_email(test_data['email'])
        self.fill_form_with_mismatched_passwords(test_data)

        error_fields = [
            self.PASSWORD_ERROR,
            self.CONFIRM_PASSWORD_ERROR
        ]
        self.verify_error_fields_displayed(error_fields)
        self.logger.info(f"Verified error fields displayed: {error_fields}")

        assert self.are_field_errors_displayed(error_fields), "Error fields not displayed as expected."

    def existing_email_registration(self, load_test_data):
        test_data = load_test_data['mandatory_fields']
        self.open_url()

        self.fill_mandatory_fields(test_data)

        is_error_displayed = self.is_element_visible(*self.EMAIL_ERROR)
        assert is_error_displayed, "Expected 'Email already in use' error message is not displayed."

        if is_error_displayed:
            self.logger.info("Registration attempt with an already registered email address correctly displays the error message.")
        else:
            self.logger.error("Error message for already registered email was not displayed.")

    def invalid_email_registration(self, load_test_data):
        test_data = load_test_data['mandatory_fields']
        self.open_url()

        self.fill_form_with_invalid_email(test_data)

        is_error_displayed = self.is_element_visible(*self.EMAIL_ERROR)
        assert is_error_displayed, "Expected 'Invalid email address' error message not displayed."

        if is_error_displayed:
            self.logger.info("Invalid email registration correctly displays the error message for the email field.")
        else:
            self.logger.error("Error message for invalid email address was not displayed.")

    def keyboard_registration(self, load_test_data):
        test_data = load_test_data['mandatory_fields']
        test_data['email'] = self.generate_unique_email(test_data['email'])

        self.open_url()
        self.fill_form_with_keyboard_keys(test_data)

        is_registration_successful = self.is_registration_successful()
        assert is_registration_successful, "Registration failed. Success message not displayed."

        if is_registration_successful:
            self.logger.info("Registration completed successfully using keyboard keys.")
        else:
            self.logger.error("Registration attempt failed with keyboard input.")

    def mandatory_fields_accept_only_spaces(self):
        self.open_url()
        spaces_are_invalid = self.validate_spaces()

        assert spaces_are_invalid, "Mandatory fields accepted only spaces as valid input."

        self.logger.info("Mandatory fields correctly reject input with only spaces.")

    def register_account_no_newsletter(self, load_test_data):
        test_data = load_test_data['all_fields']
        test_data['newsletter'] = "No"

        self.all_fields_registration(load_test_data)

        success_message_element = self.wait_for_element(*RegistrationPage.SUCCESS_MESSAGE)

        assert success_message_element.is_displayed(), "Success message was not displayed after registration."

        success_message_text = success_message_element.text
        assert "Your registration completed" in success_message_text, \
            f"Unexpected success message: {success_message_text}"

        self.logger.info("Registration with 'No' for Newsletter was successful, and the status is correctly set.")

    def register_with_strong_password(self, load_test_data):
        test_data = load_test_data['mandatory_fields']
        test_data['email'] = self.generate_unique_email(test_data['email'])

        self.open_url()
        self.fill_mandatory_fields(test_data)

        error_locators = [
            self.PASSWORD_ERROR,
            self.CONFIRM_PASSWORD_ERROR
        ]

        is_password_valid = self.validate_password_and_registration(test_data['password'], error_locators)
        assert is_password_valid, "Password validation or registration failed."
        self.logger.info("Password strength validation and registration with a strong password were successful.")

    def mandatory_fields_marked_with_asterisk(self):
        mandatory_fields = {
            self.FIRST_NAME_FIELD: "First Name",
            self.LAST_NAME_FIELD: "Last Name",
            self.EMAIL_FIELD: "Email",
            self.PASSWORD_FIELD: "Password",
            self.CONFIRM_PASSWORD_FIELD: "Confirm Password"
        }

        self.open_url()
        all_fields_valid = True
        for field_locator, field_name in mandatory_fields.items():
            is_valid = self.validate_asterisk(field_locator, field_name)
            if not is_valid:
                self.logger.info(f"Mandatory field {field_name} is not correctly marked with a red '*' symbol.")
                all_fields_valid = False

        if all_fields_valid:
            self.logger.info("All mandatory fields are correctly marked with a red '*' symbol.")
        else:
            self.logger.error("Some mandatory fields are not correctly marked with a red '*' symbol.")

    def register_with_blank_field(self, load_test_data):
        test_data = load_test_data['mandatory_fields']
        test_data['email'] = self.generate_unique_email(test_data['email'])

        self.open_url()
        self.blank_fields_and_validate_errors(test_data)

        self.logger.info("Attempting to register with one blank field.")

    def password_visibility_toggle(self, load_test_data):
        test_data = load_test_data['mandatory_fields']

        self.open_url()
        self.enter_text(self.PASSWORD_FIELD, test_data['password'])
        self.enter_text(self.CONFIRM_PASSWORD_FIELD, test_data['confirm_password'])

        assert self.is_password_hidden(), "Password field is unexpectedly visible."
        assert self.is_confirm_password_hidden(), "Confirm password field is unexpectedly visible."

        self.toggle_password_visibility()

        assert self.is_password_visible(), "Password field is still hidden after toggle."
        assert self.is_confirm_password_visible(), "Confirm password field is still hidden after toggle."

        self.toggle_password_visibility()

        assert self.is_password_hidden(), "Password field is unexpectedly visible after second toggle."
        assert self.is_confirm_password_hidden(), "Confirm password field is unexpectedly visible after second toggle."

        self.logger.info("Password visibility toggle test passed successfully.")
