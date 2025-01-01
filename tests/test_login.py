import pytest
import allure
import json
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from config.config import Config
from allure_commons.types import Severity
from selenium.webdriver.common.keys import Keys

@pytest.fixture(scope="module")
def load_test_data():
    with open(Config.TEST_DATA_PATH, 'r') as f:
        return json.load(f)


@allure.epic("User Authentication")
@allure.feature("Login")
class TestUserLogin:

    @allure.story("TC_RF_001: Validate logging into the Application using valid credentials")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test verifies that a user can log in successfully with valid credentials.")
    def test_valid_login(self, driver, load_test_data):
        test_data = load_test_data["valid_user"]

        login_page = LoginPage(driver)

        login_page.open_url()

        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data["username"])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data["password"])

        login_page.submit_login_form()

        assert login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "ico-account")), \
            "Login failed. User account/dashboard not displayed."

    @allure.story("TC_LF_002: Validate logging into the Application using invalid credentials")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user cannot log in with invalid credentials and an appropriate error message is displayed.")
    def test_invalid_login(self, driver, load_test_data):
        test_data = load_test_data["invalid_user"]

        login_page = LoginPage(driver)

        login_page.open_url()

        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data["username"])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data["password"])

        login_page.submit_login_form()

        error_locator = (By.CLASS_NAME, "message-error.validation-summary-errors")

        assert login_page.is_element_visible(error_locator), \
            "Login failed. Error message for invalid credentials not displayed."

    @allure.story("TC_LF_003: Validate login with invalid email and valid password, or valid email and invalid password")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user cannot log in with an invalid email and valid password, or valid email and invalid password.")
    def test_invalid_email_or_password(self, driver, load_test_data):
        invalid_email_data = {
            "username": "invalidemail@example.com",
            "password": load_test_data["valid_user"]["password"]
        }

        invalid_password_data = {
            "username": load_test_data["valid_user"]["username"],
            "password": "InvalidPassword123!"
        }

        login_page = LoginPage(driver)

        # Test 1: Invalid email with valid password
        login_page.open_url()
        # Pass the locators directly without unpacking them
        login_page.enter_text(LoginPage.EMAIL_FIELD, invalid_email_data["username"])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, invalid_email_data["password"])
        login_page.submit_login_form()
        error_locator = (By.CLASS_NAME, "message-error.validation-summary-errors")
        assert login_page.is_element_visible(error_locator), \
            "Login failed with invalid email. Error message not displayed."

        # Test 2: Valid email with invalid password
        login_page.open_url()
        login_page.enter_text(LoginPage.EMAIL_FIELD, invalid_password_data["username"])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, invalid_password_data["password"])
        login_page.submit_login_form()
        assert login_page.is_element_visible(error_locator), \
            "Login failed with invalid password. Error message not displayed."

    @allure.story("TC_LF_004: Validate logging into the Application without providing any credentials")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user cannot log in without providing any credentials and an appropriate error message is displayed.")
    def test_login_without_credentials(self, driver):
        login_page = LoginPage(driver)

        login_page.open_url()

        login_page.enter_text(*LoginPage.EMAIL_FIELD, "")
        login_page.enter_text(*LoginPage.PASSWORD_FIELD, "")

        login_page.submit_login_form()

        assert login_page.is_element_visible(LoginPage.EMAIL_ERROR), \
            "Email error message is not displayed when email is empty."
        assert login_page.is_element_visible(LoginPage.PASSWORD_ERROR), \
            "Password error message is not displayed when password is empty."\

    @allure.story("TC_LF_005: Validate 'Forgotten Password' link is available in the Login page and is working")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that the 'Forgotten Password' link is visible on the Login page and works correctly, redirecting to the password reset page.")
    def test_forgotten_password_link(self, driver):
        login_page = LoginPage(driver)

        login_page.open_url()

        assert login_page.is_element_visible(LoginPage.FORGOT_PASSWORD_LINK), \
            "'Forgotten Password' link is not visible on the Login page."

        login_page.click(LoginPage.FORGOT_PASSWORD_LINK)

        assert driver.current_url == "https://demo.nopcommerce.com/passwordrecovery", \
            f"Password reset page not reached. Current URL is {driver.current_url}."

    @allure.story("TC_LF_006: Validate logging into the Application using Keyboard keys (Tab and Enter)")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user can log in using the keyboard keys (Tab and Enter.")
    def test_login_using_keyboard(self, driver, load_test_data):
        test_data = load_test_data['valid_user']

        login_page = LoginPage(driver)
        login_page.open_url()

        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['username'])

        login_page.get_element(LoginPage.EMAIL_FIELD).send_keys(Keys.TAB)

        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data['password'])

        login_page.get_element(LoginPage.PASSWORD_FIELD).send_keys(Keys.ENTER)

        assert login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "ico-account")), \
            "Login failed. User account/dashboard not displayed."

    @allure.story("TC_LF_007: Validate that all fields in the Login page have the placeholder text")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that the E-Mail Address and Password text fields on the Login page have the correct placeholder text.")
    def test_field_placeholders(self, driver):
        login_page = LoginPage(driver)
        login_page.open_url()

        expected_placeholders = {
            login_page.EMAIL_FIELD: "Email",
            login_page.PASSWORD_FIELD: "Password"
        }

        for field_locator, expected_placeholder in expected_placeholders.items():
            field = login_page.wait_for_element(field_locator, timeout=10)
            if field:
                login_page.wait_for_placeholder(driver, field_locator, expected_placeholder)
            else:
                print(f"Field {field_locator} not found!")
        print("All fields have the correct placeholders.")

    @allure.story("TC_LF_008: Validate Logging into the Application and browsing back using Browser back button")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user can log in and then use the browser's back button to navigate away and return to the login page.")
    def test_login_and_browser_back(self, driver, load_test_data):
        test_data = load_test_data["valid_user"]

        login_page = LoginPage(driver)
        login_page.open_url()

        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data["username"])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data["password"])
        login_page.submit_login_form()

        assert login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "ico-account")), \
            "Login failed. User account/dashboard not displayed."

        driver.back()

        content_element = login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "content"))

        assert "You are already logged in as" in content_element.text, \
            "Error: User logged out after using the browser back button."
        print("User remains logged in after using the browser back button.")





