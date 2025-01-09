import pytest
import json
import uuid
from selenium.webdriver.common.by import By
from pages.registration_page import RegistrationPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from config.config import Config
import allure
from allure_commons.types import Severity

@pytest.fixture(scope="module")
def load_test_data():
    with open(Config.TEST_DATA_PATH, 'r') as f:
        return json.load(f)

def generate_unique_email(base_email):
    email_prefix, email_domain = base_email.split("@")
    unique_email = f"{email_prefix}_{uuid.uuid4().hex[:8]}@{email_domain}"
    return unique_email

@allure.epic("User Authentication")
@allure.feature("Registration")
class TestUserRegistration:

    @allure.story("TC_RF_001: Test mandatory fields during registration")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test verifies that all mandatory fields in the registration form are filled in and the form is successfully submitted.")
    def test_mandatory_fields_registration(self, driver, load_test_data):
        test_data = load_test_data['mandatory_fields']

        unique_email = generate_unique_email(test_data['email'])
        test_data['email'] = unique_email

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        mandatory_fields = {
            registration_page.FIRST_NAME_FIELD: test_data['first_name'],
            registration_page.LAST_NAME_FIELD: test_data['last_name'],
            registration_page.EMAIL_FIELD: unique_email,
            registration_page.PASSWORD_FIELD: test_data['password'],
            registration_page.CONFIRM_PASSWORD_FIELD: test_data['confirm_password']
        }

        for field, value in mandatory_fields.items():
            registration_page.enter_text(field, value)

        registration_page.submit_registration_form()

        assert registration_page.is_registration_successful(), "Registration failed. Success message not displayed."

    @allure.story("TC_RF_002: Validate 'Thank you for registering' email is sent to the registered email address as a confirmation for registering the account")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Functional")
    @allure.description("This test validates that after successful registration, an email is sent to the user confirming registration with the message 'Thank you for registering'.")
    def test_register_account_email_confirmation(self, driver, load_test_data):
        pytest.skip()

    @allure.story("TC_RF_003: Test registering with all available fields in the registration form")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that all available fields in the registration form are filled in and the form is successfully submitted.")
    def test_all_fields_registration(self, driver, load_test_data):
        test_data = load_test_data['all_fields']

        unique_email = generate_unique_email(test_data['email'])
        test_data['email'] = unique_email

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        gender_field = registration_page.GENDER_MALE_RADIO_BUTTON if test_data['gender'].lower() == "male" \
                       else registration_page.GENDER_FEMALE_RADIO_BUTTON
        registration_page.click(*gender_field)

        fields = {
            registration_page.FIRST_NAME_FIELD: test_data['first_name'],
            registration_page.LAST_NAME_FIELD: test_data['last_name'],
            registration_page.EMAIL_FIELD: unique_email,
            registration_page.COMPANY_NAME_FIELD: test_data['company'],
            registration_page.PASSWORD_FIELD: test_data['password'],
            registration_page.CONFIRM_PASSWORD_FIELD: test_data['confirm_password']
        }

        for field, value in fields.items():
            registration_page.enter_text(field, value)

        for dropdown, value in zip(
                [registration_page.BIRTH_DATE_DROPDOWNS['day'], registration_page.BIRTH_DATE_DROPDOWNS['month'], registration_page.BIRTH_DATE_DROPDOWNS['year']],
                [test_data['birth_day'], test_data['birth_month'], test_data['birth_year']]):
            registration_page.select_dropdown_value(dropdown, value)

        if test_data['newsletter'].lower() == "yes":
            registration_page.click(*registration_page.NEWSLETTER_CHECKBOX_FIELD)

        registration_page.submit_registration_form()

        assert registration_page.is_registration_successful(), "Registration failed. Success message not displayed."

    @allure.story("TC_RF_004: Test that proper validation messages are displayed when mandatory fields are left empty")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that proper validation messages are displayed when mandatory fields are left empty.")
    def test_mandatory_fields_validation_messages(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        registration_page.submit_registration_form()

        assert registration_page.are_field_errors_displayed([
            registration_page.FIRST_NAME_ERROR,
            registration_page.LAST_NAME_ERROR,
            registration_page.EMAIL_ERROR,
            registration_page.PASSWORD_ERROR,
            registration_page.CONFIRM_PASSWORD_ERROR
        ]), "Validation error messages are not displayed for all mandatory fields."

        print("All error messages displayed as expected.")

    @allure.story("TC_RF_005: Test registration with mismatched passwords")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that an error is displayed when the password and confirm password fields do not match.")
    def test_password_mismatch_registration(self, driver, load_test_data):
        test_data = load_test_data['user_registration']['valid_user']

        test_data['email'] = generate_unique_email(test_data['email'])

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        fields = {
            registration_page.FIRST_NAME_FIELD: test_data['first_name'],
            registration_page.LAST_NAME_FIELD: test_data['last_name'],
            registration_page.EMAIL_FIELD: test_data['email'],
            registration_page.PASSWORD_FIELD: test_data['password'],
            registration_page.CONFIRM_PASSWORD_FIELD: "DifferentPassword123"
        }

        for field, value in fields.items():
            registration_page.enter_text(field, value)

        registration_page.submit_registration_form()

        error_fields = [
            registration_page.PASSWORD_ERROR,
            registration_page.CONFIRM_PASSWORD_ERROR
        ]
        for error_field in error_fields:
            assert registration_page.is_element_visible(*error_field), f"{error_field} mismatch error not displayed."

    @allure.story("TC_RF_006: Test registration with an already registered email address")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that when an already registered email is used, an error message is displayed for the email field.")
    def test_existing_email_registration(self, driver, load_test_data):
        test_data = load_test_data['user_registration']['valid_user']

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        registration_page.enter_text(registration_page.FIRST_NAME_FIELD, test_data['first_name'])
        registration_page.enter_text(registration_page.LAST_NAME_FIELD, test_data['last_name'])
        registration_page.enter_text(registration_page.EMAIL_FIELD, test_data['email'])
        registration_page.enter_text(registration_page.PASSWORD_FIELD, test_data['password'])
        registration_page.enter_text(registration_page.CONFIRM_PASSWORD_FIELD, test_data['confirm_password'])

        registration_page.submit_registration_form()

        assert registration_page.is_element_visible(*registration_page.EMAIL_ERROR), \
            "Email already in use error not displayed."

    @allure.story("TC_RF_007: Test registration with an invalid email address")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that when an invalid email is used during registration, an appropriate error message is displayed for the email field.")
    def test_invalid_email_registration(self, driver, load_test_data):
        test_data = load_test_data['user_registration']['valid_user']

        invalid_email = "invalid-email.com"

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        fields = {
            registration_page.FIRST_NAME_FIELD: test_data['first_name'],
            registration_page.LAST_NAME_FIELD: test_data['last_name'],
            registration_page.EMAIL_FIELD: invalid_email,
            registration_page.PASSWORD_FIELD: test_data['password'],
            registration_page.CONFIRM_PASSWORD_FIELD: test_data['confirm_password']
        }

        for field, value in fields.items():
            registration_page.enter_text(field, value)

        registration_page.submit_registration_form()

        assert registration_page.is_element_visible(
            *registration_page.EMAIL_ERROR), "Invalid email error message not displayed."

    @allure.story("TC_RF_008: Test registering an account using keyboard keys")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that the registration form can be successfully submitted using keyboard keys like TAB and ENTER.")
    def test_keyboard_registration(self, driver, load_test_data):
        test_data = load_test_data['user_registration']['valid_user']

        unique_email = generate_unique_email(test_data['email'])
        test_data['email'] = unique_email

        registration_page = RegistrationPage(driver)
        registration_page.open_url()


        fields = {
            registration_page.FIRST_NAME_FIELD: test_data['first_name'],
            registration_page.LAST_NAME_FIELD: test_data['last_name'],
            registration_page.EMAIL_FIELD: unique_email,
            registration_page.PASSWORD_FIELD: test_data['password'],
            registration_page.CONFIRM_PASSWORD_FIELD: test_data['confirm_password']
        }

        for field, value in fields.items():
            registration_page.enter_text(field, value)

        confirm_password_field = registration_page.wait_for_element(*registration_page.CONFIRM_PASSWORD_FIELD)
        confirm_password_field.send_keys(Keys.TAB)
        confirm_password_field.send_keys(Keys.ENTER)

        assert registration_page.is_registration_successful(), "Registration failed. Success message not displayed."

    @allure.story("TC_RF_009: Test that all fields in the Register Account page have the correct placeholders")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description("This test verifies that all fields in the registration page have the correct placeholders.")
    def test_field_placeholders(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        expected_placeholders = {
            registration_page.FIRST_NAME_FIELD: "First name",
            registration_page.LAST_NAME_FIELD: "Last name",
            registration_page.EMAIL_FIELD: "Email",
            registration_page.COMPANY_NAME_FIELD: "Company",
            registration_page.PASSWORD_FIELD: "Password",
            registration_page.CONFIRM_PASSWORD_FIELD: "Confirm password"
        }

        for field_locator, expected_placeholder in expected_placeholders.items():
            field = registration_page.wait_for_element(*field_locator)
            if field:
                registration_page.wait_for_placeholder(driver, field_locator, expected_placeholder)
            else:
                print(f"Field {field_locator} not found!")
        print("All fields have the correct placeholders.")

    @allure.story("TC_RF_010: Test that all mandatory fields in the Register Account page are marked with a red '*' symbol")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that all mandatory fields in the registration form are marked with a red '*' symbol to indicate their importance.")
    def test_mandatory_fields_marked_with_asterisk(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        mandatory_fields = {
            registration_page.FIRST_NAME_FIELD: "First Name",
            registration_page.LAST_NAME_FIELD: "Last Name",
            registration_page.EMAIL_FIELD: "Email",
            registration_page.PASSWORD_FIELD: "Password",
            registration_page.CONFIRM_PASSWORD_FIELD: "Confirm Password"
        }

        for field_locator, field_name in mandatory_fields.items():
            field_label = registration_page.wait_for_element(By.XPATH, f"//label[@for='{field_locator[1]}']")
            if not field_label:
                print(f"Label for {field_name} not found!")
                continue
            try:
                asterisk = field_label.find_element(By.XPATH, ".//*[contains(@class, 'required')]")
                color = asterisk.value_of_css_property("color")
                print(f"Asterisk color for {field_name}: {color}")
                assert asterisk.is_displayed() and color == "rgba(255, 0, 0, 1)", \
                    f"Mandatory field {field_name} is not marked with a red '*' symbol."
            except Exception as e:
                print(f"Error locating asterisk for {field_name}: {str(e)}")
                continue
        print("All mandatory fields are correctly marked with a red '*' symbol.")

    @allure.story("TC_RF_011: Test password stored in the Database")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test verifies that the details that are provided while Registering an Account are stored in the Database.")
    def test_password_stored_in_db(self, driver, load_test_data):
        pytest.skip()

    @allure.story("TC_RF_012: Test that mandatory fields in the Register Account page do not accept only spaces")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test ensures that mandatory fields in the registration form do not accept only spaces and display appropriate validation error messages.")
    def test_mandatory_fields_accept_only_spaces(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        mandatory_fields = [
            registration_page.FIRST_NAME_FIELD,
            registration_page.LAST_NAME_FIELD,
            registration_page.EMAIL_FIELD,
            registration_page.PASSWORD_FIELD,
            registration_page.CONFIRM_PASSWORD_FIELD
        ]

        for field_locator in mandatory_fields:
            registration_page.enter_text(field_locator, "     ")

        registration_page.submit_registration_form()

        error_fields = [
            registration_page.FIRST_NAME_ERROR,
            registration_page.LAST_NAME_ERROR,
            registration_page.EMAIL_ERROR,
            registration_page.PASSWORD_ERROR,
            registration_page.CONFIRM_PASSWORD_ERROR
        ]

        assert registration_page.are_field_errors_displayed(error_fields), \
            "Validation error messages are not displayed for fields with only spaces."

        print("All mandatory fields correctly reject only spaces and display error messages.")

    @allure.story("TC_RF_013: Test Registering without providing required information")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test verifies registering an Account without providing required information.")
    def test_without_mandatory_fields_registration(self, driver, load_test_data):
        pytest.skip()

    @allure.story("TC_RF_014: Validate registering an account with valid credentials but selecting 'No' for Newsletter.")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the successful registration of an account with valid credentials and 'No' selected for the newsletter subscription.")
    def test_register_account_no_newsletter(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        test_data = load_test_data["newsletter_no_registration"]
        unique_email = generate_unique_email(test_data['email'])
        test_data['email'] = unique_email

        mandatory_fields = {
            registration_page.FIRST_NAME_FIELD: "first_name",
            registration_page.LAST_NAME_FIELD: "last_name",
            registration_page.EMAIL_FIELD: "email",
            registration_page.PASSWORD_FIELD: "password",
            registration_page.CONFIRM_PASSWORD_FIELD: "confirm_password"
        }

        for field_locator, field_key in mandatory_fields.items():
            field_value = test_data[field_key]
            registration_page.enter_text(field_locator, field_value)

        newsletter_checkbox = registration_page.wait_for_element(*RegistrationPage.NEWSLETTER_CHECKBOX_FIELD)

        if newsletter_checkbox.is_selected():
            newsletter_checkbox.click()

        registration_page.submit_registration_form()

        success_message_element = registration_page.wait_for_element(*RegistrationPage.SUCCESS_MESSAGE)

        assert success_message_element.is_displayed(), "Success message was not displayed after registration."

        success_message_text = success_message_element.text
        assert "Your registration completed" in success_message_text, f"Unexpected success message: {success_message_text}"

        print("Registration with 'No' for Newsletter was successful, and the status is correctly set.")

    @allure.story("TC_RF_015: Validate Registering an Account and checking for email confirmation.")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the successful registration of an account and checks for the email confirmation.")
    def test_register_account_email_confirmation(self, driver, load_test_data):
        pytest.skip()

    @allure.story("TC_RF_016: Validate registering an account and confirming with a new password.")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the successful registration of an account where the user confirms registration with a new password.")
    def test_register_account_with_new_password(self, driver, load_test_data):
        pytest.skip("Test is skipped.")

    @allure.story("TC_RF_017: Validate password strength while registering.")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates password strength while registering.")
    def test_register_account_with_strong_password(self, driver, load_test_data):
        test_data = load_test_data['user_registration']['valid_user']

        unique_email = generate_unique_email(test_data['email'])
        test_data['email'] = unique_email

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        mandatory_fields = [
            (registration_page.FIRST_NAME_FIELD, test_data['first_name']),
            (registration_page.LAST_NAME_FIELD, test_data['last_name']),
            (registration_page.EMAIL_FIELD, unique_email),
            (registration_page.PASSWORD_FIELD, test_data['password']),
            (registration_page.CONFIRM_PASSWORD_FIELD, test_data['confirm_password'])
        ]

        for field_locator, field_value in mandatory_fields:
            registration_page.enter_text(field_locator, field_value)

        assert registration_page.check_password_strength(test_data['password']) == "Strong", \
            f"Expected strong password, but got {registration_page.check_password_strength(test_data['password'])}"

        registration_page.submit_registration_form()

        if registration_page.is_registration_successful():
            print(f"Registration with strong password {test_data['password']} was successful.")
        else:
            error_locators = [
                registration_page.FIRST_NAME_ERROR,
                registration_page.LAST_NAME_ERROR,
                registration_page.EMAIL_ERROR,
                registration_page.PASSWORD_ERROR,
                registration_page.CONFIRM_PASSWORD_ERROR
            ]
            assert registration_page.are_field_errors_displayed(
                error_locators), "Error messages are not displayed for all fields."

    @allure.story("TC_RF_018: Validate Registering an Account with one blank field")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the behavior when one mandatory field is left blank during registration.")
    def test_register_account_with_blank_field(self, driver, load_test_data):
        test_data = load_test_data['user_registration']['valid_user']

        unique_email = generate_unique_email(test_data['email'])
        test_data['email'] = unique_email

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        fields_to_test = [
            (registration_page.FIRST_NAME_FIELD, "First name is required.", "", test_data['last_name'],
             test_data['email'], test_data['password'], test_data['confirm_password']),
            (registration_page.LAST_NAME_FIELD, "Last name is required.", test_data['first_name'], "",
             test_data['email'], test_data['password'], test_data['confirm_password']),
            (registration_page.EMAIL_FIELD, "Email is required.", test_data['first_name'], test_data['last_name'], "",
             test_data['password'], test_data['confirm_password']),
            (registration_page.PASSWORD_FIELD, "Password is required.", test_data['first_name'], test_data['last_name'],
             test_data['email'], "", test_data['confirm_password']),
            (registration_page.CONFIRM_PASSWORD_FIELD, "Confirm Password is required.", test_data['first_name'],
             test_data['last_name'], test_data['email'], test_data['password'], "")
        ]

        for field_locator, expected_error_message, first_name, last_name, email, password, confirm_password in fields_to_test:
            registration_page.clear_error_messages()

            registration_page.enter_text(registration_page.FIRST_NAME_FIELD, first_name)
            registration_page.enter_text(registration_page.LAST_NAME_FIELD, last_name)
            registration_page.enter_text(registration_page.EMAIL_FIELD, email)
            registration_page.enter_text(registration_page.PASSWORD_FIELD, password)
            registration_page.enter_text(registration_page.CONFIRM_PASSWORD_FIELD, confirm_password)

            registration_page.submit_registration_form()

            error_locators = [(field_locator, expected_error_message)]
            assert registration_page.are_field_errors_displayed(error_locators), \
                f"Expected error message '{expected_error_message}' for field {field_locator} but it was not displayed."

        print("Registration attempt with one blank field was blocked as expected.")

    @allure.story("TC_RF_019: Validate the Password text entered into the 'Password' and 'Password Confirm' fields of 'Register Account' functionality is toggled to hide its visibility")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the toggling of the password visibility in the 'Password' and 'Confirm Password' fields during account registration.")
    def test_password_visibility_toggle(self, driver, load_test_data):
        test_data = load_test_data['user_registration']['valid_user']

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        registration_page.enter_text(registration_page.PASSWORD_FIELD, test_data['password'])
        registration_page.enter_text(registration_page.CONFIRM_PASSWORD_FIELD, test_data['confirm_password'])

        assert registration_page.is_password_hidden(), "Password field is unexpectedly visible."
        assert registration_page.is_confirm_password_hidden(), "Confirm password field is unexpectedly visible."

        registration_page.toggle_password_visibility()

        assert registration_page.is_password_visible(), "Password field is still hidden after toggle."
        assert registration_page.is_confirm_password_visible(), "Confirm password field is still hidden after toggle."

        registration_page.toggle_password_visibility()

        assert registration_page.is_password_hidden(), "Password field is unexpectedly visible after second toggle."
        assert registration_page.is_confirm_password_hidden(), "Confirm password field is unexpectedly visible after second toggle."

        print("Password visibility toggle test passed successfully.")

