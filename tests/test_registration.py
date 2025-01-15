import pytest
import json
import logging
from pages.registration_page import RegistrationPage
from config.config import Config
import allure
from allure_commons.types import Severity


@pytest.fixture(scope="module")
def load_test_data():
    with open(Config.TEST_DATA_PATH, 'r') as f:
        return json.load(f)


@allure.epic("User Authentication")
@allure.feature("Registration")
class TestUserRegistration:

    @allure.story("TC_RF_001: Test mandatory fields during registration")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test verifies that all mandatory fields in the registration form are filled in and the form is successfully submitted.")
    def test_mandatory_fields_registration(self, driver, load_test_data):
        test_data = load_test_data['mandatory_fields']

        registration_page = RegistrationPage(driver)

        test_data['email'] = registration_page.generate_unique_email(test_data['email'])

        registration_page.open_url()

        registration_page.fill_mandatory_fields(test_data)

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

        registration_page = RegistrationPage(driver)
        test_data['email'] = registration_page.generate_unique_email(test_data['email'])

        registration_page.open_url()

        registration_page.fill_all_fields(test_data)

        assert registration_page.is_registration_successful(), "Registration failed. Success message not displayed."

    @allure.story("TC_RF_004: Test that proper validation messages are displayed when mandatory fields are left empty")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that proper validation messages are displayed when mandatory fields are left empty.")
    def test_mandatory_fields_validation_messages(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        registration_page.submit_registration_form()

        mandatory_fields = registration_page.get_mandatory_fields()

        assert registration_page.are_field_errors_displayed(
            mandatory_fields), "Validation error messages are not displayed for all mandatory fields."

    @allure.story("TC_RF_005: Test registration with mismatched passwords")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that an error is displayed when the password and confirm password fields do not match.")
    def test_password_mismatch_registration(self, driver, load_test_data):
        test_data = load_test_data['mandatory_fields']

        registration_page = RegistrationPage(driver)

        test_data['email'] = registration_page.generate_unique_email(test_data['email'])

        registration_page.open_url()

        registration_page.fill_form_with_mismatched_passwords(test_data)

        error_fields = [
            registration_page.PASSWORD_ERROR,
            registration_page.CONFIRM_PASSWORD_ERROR
        ]
        registration_page.verify_error_fields_displayed(error_fields)

    @allure.story("TC_RF_006: Test registration with an already registered email address")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that when an already registered email is used, an error message is displayed for the email field.")
    def test_existing_email_registration(self, driver, load_test_data):
        test_data = load_test_data['mandatory_fields']

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        registration_page.fill_mandatory_fields(test_data)

        is_error_displayed = registration_page.is_element_visible(*registration_page.EMAIL_ERROR)
        assert is_error_displayed, "Expected 'Email already in use' error message is not displayed."

        if is_error_displayed:
            logging.info(
                "Registration attempt with an already registered email address correctly displays the error message.")
        else:
            logging.error("Error message for already registered email was not displayed.")

    @allure.story("TC_RF_007: Test registration with an invalid email address")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that when an invalid email is used during registration, an appropriate error message is displayed for the email field.")
    def test_invalid_email_registration(self, driver, load_test_data):
        test_data = load_test_data['mandatory_fields']

        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        registration_page.fill_form_with_invalid_email(test_data)

        is_error_displayed = registration_page.is_element_visible(*registration_page.EMAIL_ERROR)
        assert is_error_displayed, "Expected 'Invalid email address' error message not displayed."

        if is_error_displayed:
            logging.info("Invalid email registration correctly displays the error message for the email field.")
        else:
            logging.error("Error message for invalid email address was not displayed.")

    @allure.story("TC_RF_008: Test registering an account using keyboard keys")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that the registration form can be successfully submitted using keyboard keys like TAB and ENTER.")
    def test_keyboard_registration(self, driver, load_test_data):
        test_data = load_test_data['mandatory_fields']

        registration_page = RegistrationPage(driver)

        test_data['email'] = registration_page.generate_unique_email(test_data['email'])

        registration_page.open_url()

        registration_page.fill_form_with_keyboard_keys(test_data)

        is_registration_successful = registration_page.is_registration_successful()
        assert is_registration_successful, "Registration failed. Success message not displayed."

        if is_registration_successful:
            logging.info("Registration completed successfully using keyboard keys.")
        else:
            logging.error("Registration attempt failed with keyboard input.")

    @allure.story("TC_RF_009: Test that all fields in the Register Account page have the correct placeholders")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description("This test verifies that all fields in the registration page have the correct placeholders.")
    def test_field_placeholders(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        placeholders_are_correct = registration_page.validate_placeholders()

        assert placeholders_are_correct, "One or more fields have incorrect placeholders."

        if placeholders_are_correct:
            logging.info("All form fields have the correct placeholders.")
        else:
            logging.error("Some form fields have incorrect placeholders.")

    @allure.story("TC_RF_010: Test that all mandatory fields in the Register Account page are marked with a red '*' symbol")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that all mandatory fields in the registration form are marked with a red '*' symbol to indicate their importance.")
    def test_mandatory_fields_marked_with_asterisk(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.open_url()

        validation_result = registration_page.validate_asterisk()

        assert validation_result, "Not all mandatory fields are correctly marked with a red '*' symbol."

        logging.info("All mandatory fields are correctly marked with a red '*' symbol.")

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

        spaces_are_invalid = registration_page.validate_spaces()

        assert spaces_are_invalid, "Mandatory fields accepted only spaces as valid input."

        logging.info("Mandatory fields correctly reject input with only spaces.")

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
        test_data = load_test_data['all_fields']

        registration_page = RegistrationPage(driver)
        test_data['email'] = registration_page.generate_unique_email(test_data['email'])

        registration_page.open_url()

        test_data['newsletter'] = "No"

        registration_page.fill_all_fields(test_data)

        success_message_element = registration_page.wait_for_element(*RegistrationPage.SUCCESS_MESSAGE)

        assert success_message_element.is_displayed(), "Success message was not displayed after registration."

        success_message_text = success_message_element.text
        assert "Your registration completed" in success_message_text, \
            f"Unexpected success message: {success_message_text}"

        logging.info("Registration with 'No' for Newsletter was successful, and the status is correctly set.")

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
        test_data = load_test_data['mandatory_fields']

        registration_page = RegistrationPage(driver)
        test_data['email'] = registration_page.generate_unique_email(test_data['email'])

        registration_page.open_url()
        registration_page.fill_mandatory_fields(test_data)

        error_locators = [
            registration_page.PASSWORD_ERROR,
            registration_page.CONFIRM_PASSWORD_ERROR
        ]

        is_password_valid = registration_page.validate_password_and_registration(test_data['password'], error_locators)
        assert is_password_valid, "Password validation or registration failed."
        logging.info("Password strength validation and registration with a strong password were successful.")

    @allure.story("TC_RF_018: Validate Registering an Account with one blank field")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the behavior when one mandatory field is left blank during registration.")
    def test_register_account_with_blank_field(self, driver, load_test_data):
        test_data = load_test_data['mandatory_fields']

        registration_page = RegistrationPage(driver)
        test_data['email'] = registration_page.generate_unique_email(test_data['email'])

        registration_page.open_url()

        registration_page.blank_fields_and_validate_errors(test_data)

    @allure.story("TC_RF_019: Validate the Password text entered into the 'Password' and 'Password Confirm' fields of 'Register Account' functionality is toggled to hide its visibility")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the toggling of the password visibility in the 'Password' and 'Confirm Password' fields during account registration.")
    def test_password_visibility_toggle(self, driver, load_test_data):
        test_data = load_test_data['mandatory_fields']

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
