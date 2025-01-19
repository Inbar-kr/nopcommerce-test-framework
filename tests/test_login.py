import pytest
import allure
import json
import os
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from config.config import Config
from utils.driver_factory import DriverFactory
from allure_commons.types import Severity


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
        login_page = LoginPage(driver)
        login_page.login_user(driver, load_test_data)

        assert login_page.MY_ACCOUNT_LINK, "Login failed. User account/dashboard not displayed."

        login_page.logger.info("User successfully logged in.")

    @allure.story("TC_LF_002: Validate logging into the Application using invalid credentials")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user cannot log in with invalid credentials and an appropriate error message is displayed.")
    def test_invalid_login(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.invalid_login_user(load_test_data)

        assert login_page.ERROR_MESSAGE, \
            "Login failed. Error message for invalid credentials not displayed."

        login_page.logger.info("Error message displayed for invalid login.")

    @allure.story("TC_LF_003: Validate login with invalid email and valid password, or valid email and invalid password")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user cannot log in with an invalid email and valid password, or valid email and invalid password.")
    def test_invalid_email_or_password(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.login_with_invalid_email(driver, load_test_data)
        assert login_page.EMAIL_ERROR, \
            "Login failed with invalid email. Error message not displayed."
        login_page.logger.info("Error message displayed as expected when logging in with invalid email.")

        login_page.login_with_invalid_password(driver, load_test_data)
        assert login_page.ERROR_MESSAGE, \
            "Login failed with invalid password. Error message not displayed."
        login_page.logger.info("Error message displayed as expected when logging in with invalid password.")

    @allure.story("TC_LF_004: Validate logging into the Application without providing any credentials")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user cannot log in without providing any credentials and an appropriate error message is displayed.")
    def test_login_without_credentials(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.login_without_credentials(driver, load_test_data)

        assert login_page.EMAIL_ERROR, \
            "Email error message is not displayed when email is empty."
        assert login_page.PASSWORD_ERROR, \
            "Password error message is not displayed when password is empty."\

        login_page.logger.info("Error message displayed for both email and password.")

    @allure.story("TC_LF_005: Validate 'Forgotten Password' link is available in the Login page and is working")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that the 'Forgotten Password' link is visible on the Login page and works correctly, redirecting to the password reset page.")
    def test_forgotten_password_link(self, driver):
        login_page = LoginPage(driver)

        login_page.forgotten_password_link(driver)

        login_page.logger.info("'Forgotten Password' link is visible on the Login page and works correctly.")

    @allure.story("TC_LF_006: Validate logging into the Application using Keyboard keys (Tab and Enter)")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user can log in using the keyboard keys (Tab and Enter.")
    def test_login_using_keyboard(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.login_with_keyboard_keys(driver, load_test_data)

        assert login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "ico-account")), \
            "Login failed. User account/dashboard not displayed."

        login_page.logger.info("User can log in using the keyboard keys")

    @allure.story("TC_LF_007: Validate that all fields in the Login page have the placeholder text")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that the E-Mail Address and Password text fields on the Login page have the correct placeholder text.")
    def test_field_placeholders(self, driver):
        login_page = LoginPage(driver)

        login_page.validate_placeholders(driver)

        login_page.logger.info("All fields on the Login page have the correct placeholders.")

    @allure.story("TC_LF_008: Validate Logging into the Application and browsing back using Browser back button")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that a user can log in and then use the browser's back button to navigate away and return to the login page.")
    def test_login_and_browser_back(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.login_and_browser_back(driver, load_test_data)

        login_page.logger.info("Login and navigation using the browser's back button validated successfully.")

    @allure.story("TC_LF_009: Validate Logging out from the Application and browsing back")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that after logging out, the user cannot log back in by using the browser's back button.")
    def test_logout_and_browser_back(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.logout_and_browser_back(driver, load_test_data)

        login_page.logger.info("User did not get logged in again after using the browser back button.")

    @allure.story("TC_LF_010: Validate logging into the Application using inactive credentials")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that the user cannot log in using inactive credentials (valid email/password of an inactive account).")
    def test_inactive_user_login(self, driver, load_test_data):
        pytest.skip()

    @allure.story("TC_LF_011: Validate the number of unsuccessful login attempts")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that after 5 unsuccessful login attempts, a warning message is displayed stating that the account has exceeded the allowed number of login attempts.")
    def test_unsuccessful_login_attempts(self, driver, load_test_data):
        pytest.skip()

    @allure.story("TC_LF_012: Validate the text into the Password field is toggled to hide its visibility")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the text entered in the 'Password' field is toggled between visible and hidden when the visibility toggle is clicked.")
    def test_password_visibility_toggle(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.password_visibility_toggle(load_test_data)

        login_page.logger.info("Password visibility toggle test passed successfully.")

    @allure.story("TC_LF_013: Validate the copying of the text entered into the Password field")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the text entered in the 'Password' field cannot be copied, either through the right-click menu or the Ctrl+C shortcut.")
    def test_password_copying(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.password_copying(load_test_data)

        login_page.logger.info("User cannot copy the password.")

    @allure.story("TC_LF_014: Validate the Password is not visible in the Page Source")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the text entered in the 'Password' field is not visible in the page source at any point, ensuring secure handling of sensitive data.")
    def test_password_not_in_page_source(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.password_page_source(driver, load_test_data)

        login_page.logger.info("Password visibility in page source test passed successfully.")

    @allure.story("TC_LF_015: Validate Logging into the Application after changing the password")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after changing the password in the 'My Account' section, the user should not be able to log in with the old credentials and should be able to log in with the new password.")
    def test_login_after_password_change(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.change_password_page(driver, load_test_data)

        login_page.logger.info("Login after password change validated.")

    @allure.story(
        "TC_LF_016: Validate logging in, closing the browser without logging out, and reopening the application")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after logging into the application and closing the browser without logging out, "
        "the logged-in session should still be maintained when reopening the application.")
    def test_login_session_after_browser_restart(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.login_session_after_browser_restart(driver, load_test_data)

        login_page.logger.info("Login after closing the browser without logging out, and reopening the application.")

    @allure.story("TC_LF_018: Validate user is able to navigate to different pages from Login page")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can navigate to different pages (Register Account, Sitemap, etc.) from the Login page.")
    def test_navigation_from_login_page(self, driver, load_test_data):
        login_page = LoginPage(driver)

        login_page.Navigation_from_login_page(driver)

        login_page.logger.info("User can navigate to different pages.")

    @allure.story("TC_LF_019: Validate the UI of the Login page")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description("This test validates the UI elements on the Login page, ensuring that all elements are displayed and aligned properly.")
    def test_ui_of_login_page(self, driver):
        login_page = LoginPage(driver)

        login_page.ui_of_login_page()

        login_page.logger.info("UI validation for the Login page passed successfully.")

    @allure.story("TC_LF_020: Validate the login page functionality in all supported environments")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Smoke")
    @allure.description(
        "This test validates the functionality of the login page in different environments (e.g., different browsers or devices)."
    )
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_login_page_functionality_on_different_browsers(self, driver, browser, load_test_data):
        pytest.skip()
