import pytest
import json
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
        registration_page = RegistrationPage(driver)

        registration_page.mandatory_fields_registration(load_test_data)

        registration_page.logger.info("User successfully registered by filling in all the mandatory fields during registration.")

    @allure.story("TC_RF_002: Validate 'Thank you for registering' email is sent to the registered email address as a confirmation for registering the account")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates that after successful registration, an email is sent to the user confirming registration with the message 'Thank you for registering'.")
    def test_register_account_email_confirmation(self, driver, load_test_data):
        pytest.skip()

    @allure.story("TC_RF_003: Test registering with all available fields in the registration form")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that all available fields in the registration form are filled in and the form is successfully submitted.")
    def test_all_fields_registration(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)

        registration_page.all_fields_registration(load_test_data)

        registration_page.logger.info("User successfully registered by filling in all the fields during registration.")

    @allure.story("TC_RF_004: Test that proper validation messages are displayed when mandatory fields are left empty")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that proper validation messages are displayed when mandatory fields are left empty.")
    def test_mandatory_fields_validation_messages(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)

        registration_page.empty_registration()

        registration_page.logger.info("Proper validation messages appear for empty mandatory fields.")

    @allure.story("TC_RF_005: Test registration with mismatched passwords")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test verifies that an error is displayed when the password and confirm password fields do not match.")
    def test_password_mismatch_registration(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)

        registration_page.password_mismatch_registration(load_test_data)

        registration_page.logger.info("Proper validation messages appear for registration with mismatched passwords.")

    @allure.story("TC_RF_006: Test registration with an already registered email address")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that when an already registered email is used, an error message is displayed for the email field.")
    def test_existing_email_registration(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)

        registration_page.existing_email_registration(load_test_data)

        registration_page.logger.info("Proper validation messages appear for registration with an already registered email address.")

    @allure.story("TC_RF_007: Test registration with an invalid email address")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that when an invalid email is used during registration, an appropriate error message is displayed for the email field.")
    def test_invalid_email_registration(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)

        registration_page.invalid_email_registration(load_test_data)

        registration_page.logger.info("Proper validation messages appear for registration with an invalid email address.")

    @allure.story("TC_RF_008: Test registering an account using keyboard keys")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that the registration form can be successfully submitted using keyboard keys like TAB and ENTER.")
    def test_keyboard_registration(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)

        registration_page.keyboard_registration(load_test_data)

        registration_page.logger.info("User successfully registered using keyboard keys.")

    @allure.story("TC_RF_009: Test that all fields in the Register Account page have the correct placeholders")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description("This test verifies that all fields in the registration page have the correct placeholders.")
    def test_field_placeholders(self, driver):
        registration_page = RegistrationPage(driver)

        registration_page.validate_placeholders(driver)

        registration_page.logger.info("All Register fields have the correct placeholders.")

    @allure.story("TC_RF_010: Test that all mandatory fields in the Register Account page are marked with a red '*' symbol")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description("This test verifies that all mandatory fields in the registration form are marked with a red '*' symbol to indicate their importance.")
    def test_mandatory_fields_marked_with_asterisk(self, driver):
        registration_page = RegistrationPage(driver)

        registration_page.mandatory_fields_marked_with_asterisk()

        registration_page.logger.info("All mandatory fields are marked with a red '*' symbol.")

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

        registration_page.mandatory_fields_accept_only_spaces()

        registration_page.logger.info("All mandatory fields correctly reject only spaces and display error messages.")

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

        registration_page.register_account_no_newsletter(load_test_data)

        registration_page.logger.info("User successfully registered by filling in all the fields during registration but selecting 'No' for Newsletter.")

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
        registration_page = RegistrationPage(driver)

        registration_page.register_with_strong_password(load_test_data)

        registration_page.logger.info("Validate password strength while registering.")

    @allure.story("TC_RF_018: Validate Registering an Account with one blank field")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the behavior when one mandatory field is left blank during registration.")
    def test_register_account_with_blank_field(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)

        registration_page.register_with_blank_field(load_test_data)

        registration_page.logger.info("Validate Registering an Account with one blank field.")

    @allure.story("TC_RF_019: Validate the Password text entered into the 'Password' and 'Password Confirm' fields of 'Register Account' functionality is toggled to hide its visibility")
    @allure.severity(Severity.NORMAL)
    @allure.label("Functional")
    @allure.description("This test validates the toggling of the password visibility in the 'Password' and 'Confirm Password' fields during account registration.")
    def test_password_visibility_toggle(self, driver, load_test_data):
        registration_page = RegistrationPage(driver)

        registration_page.password_visibility_toggle(load_test_data)

        registration_page.logger.info("Validate the 'Password' and 'Password Confirm' text fields is toggled to hide its visibility.")
