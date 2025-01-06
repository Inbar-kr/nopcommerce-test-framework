import pytest
import allure
import json
import pyperclip
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from config.config import Config
from utils.driver_factory import DriverFactory
from allure_commons.types import Severity
from selenium.webdriver.common.keys import Keys
from tests.test_registration import TestUserRegistration

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
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        login_page = LoginPage(driver)

        if login_page.is_element_visible(LoginPage.LOGOUT_BUTTON):
            login_page.click(LoginPage.LOGOUT_BUTTON)

        login_page.click(LoginPage.LOGIN_BUTTON)

        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['email'])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data['password'])
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

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

        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

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
        login_page.enter_text(LoginPage.EMAIL_FIELD, invalid_email_data["username"])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, invalid_email_data["password"])
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)
        error_locator = (By.CLASS_NAME, "message-error.validation-summary-errors")
        assert login_page.is_element_visible(error_locator), \
            "Login failed with invalid email. Error message not displayed."

        # Test 2: Valid email with invalid password
        login_page.open_url()
        login_page.enter_text(LoginPage.EMAIL_FIELD, invalid_password_data["username"])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, invalid_password_data["password"])
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)
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

        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

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
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        login_page = LoginPage(driver)

        if login_page.is_element_visible(LoginPage.LOGOUT_BUTTON):
            login_page.click(LoginPage.LOGOUT_BUTTON)

        login_page.click(LoginPage.LOGIN_BUTTON)

        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['email'])
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
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        login_page = LoginPage(driver)

        if login_page.is_element_visible(LoginPage.LOGOUT_BUTTON):
            login_page.click(LoginPage.LOGOUT_BUTTON)

        login_page.click(LoginPage.LOGIN_BUTTON)

        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['email'])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data['password'])
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

        assert login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "ico-account")), \
            "Login failed. User account/dashboard not displayed."

        driver.back()

        content_element = login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "content"))

        assert "You are already logged in as" in content_element.text, \
            "Error: User logged out after using the browser back button."
        print("User remains logged in after using the browser back button.")

    @allure.story("TC_LF_009: Validate Logging out from the Application and browsing back")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test verifies that after logging out, the user cannot log back in by using the browser's back button.")
    def test_logout_and_browser_back(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        login_page = LoginPage(driver)

        if login_page.is_element_visible(LoginPage.LOGOUT_BUTTON):
            login_page.click(LoginPage.LOGOUT_BUTTON)

        login_page.click(LoginPage.LOGIN_BUTTON)

        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['email'])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data['password'])
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

        assert login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "ico-account")), \
            "Login failed. User account/dashboard not displayed."

        if login_page.is_element_visible(LoginPage.LOGOUT_BUTTON):
            login_page.click(LoginPage.LOGOUT_BUTTON)

        driver.back()

        assert login_page.is_element_visible(LoginPage.LOGIN_BUTTON), \
            "Error: User logged in again after using the browser back button."

        print("User did not get logged in again after using the browser back button.")

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
        test_data = load_test_data["valid_user"]

        login_page = LoginPage(driver)
        login_page.open_url()

        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data["password"])

        assert login_page.is_password_hidden(), "Password field is unexpectedly visible before toggle."
        login_page.toggle_password_visibility()

        assert login_page.is_password_visible(), "Password field is unexpectedly hidden after first toggle."
        login_page.toggle_password_visibility()

        assert login_page.is_password_hidden(), "Password field is unexpectedly visible after second toggle."

        print("Password visibility toggle test passed successfully.")

    @allure.story("TC_LF_013: Validate the copying of the text entered into the Password field")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the text entered in the 'Password' field cannot be copied, either through the right-click menu or the Ctrl+C shortcut.")
    def test_password_copying(self, driver, load_test_data):
        test_data = load_test_data["valid_user"]

        login_page = LoginPage(driver)
        login_page.open_url()

        password_text = test_data["password"]
        login_page.enter_text(LoginPage.PASSWORD_FIELD, password_text)

        login_page.select_password_text_and_right_click()
        login_page.copy_from_context_menu()

        clipboard_content = pyperclip.paste()
        assert clipboard_content != password_text, "Password text was unexpectedly copied using the right-click menu."

        login_page.select_password_text()
        login_page.press_ctrl_c()

        clipboard_content = pyperclip.paste()
        assert clipboard_content != password_text, "Password text was unexpectedly copied using Ctrl+C."

        print("Password text copy test passed successfully.")

    @allure.story("TC_LF_014: Validate the Password is not visible in the Page Source")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the text entered in the 'Password' field is not visible in the page source at any point, ensuring secure handling of sensitive data.")
    def test_password_not_in_page_source(self, driver, load_test_data):
        test_data = load_test_data["valid_user"]

        login_page = LoginPage(driver)
        login_page.open_url()

        password_text = test_data["password"]
        login_page.enter_text(LoginPage.PASSWORD_FIELD, password_text)

        page_source = driver.page_source
        assert password_text not in page_source, \
            "Password text was unexpectedly visible in the page source before login."

        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

        page_source = driver.page_source
        assert password_text not in page_source, \
            "Password text was unexpectedly visible in the page source after login."

        print("Password visibility in page source test passed successfully.")

    @allure.story("TC_LF_015: Validate Logging into the Application after changing the password")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after changing the password in the 'My Account' section, the user should not be able to log in with the old credentials and should be able to log in with the new password.")
    def test_login_after_password_change(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        login_page = LoginPage(driver)

        if login_page.is_element_visible(LoginPage.LOGOUT_BUTTON):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LoginPage.LOGOUT_BUTTON))
            login_page.click(LoginPage.LOGOUT_BUTTON)

        login_page.click(LoginPage.LOGIN_BUTTON)
        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['email'])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data['password'])
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

        assert login_page.wait_for_element_to_be_visible(LoginPage.MY_ACCOUNT_LINK), \
            "Login failed. User account/dashboard not displayed."

        login_page.click(LoginPage.MY_ACCOUNT_LINK)
        login_page.click(LoginPage.CHANGE_PASSWORD_LINK)

        login_page.enter_text(LoginPage.OLD_PASSWORD_FIELD, test_data['password'])
        new_password = "NewPassword123!"
        login_page.enter_text(LoginPage.NEW_PASSWORD_FIELD, new_password)
        login_page.enter_text(LoginPage.CONFIRM_PASSWORD_FIELD, new_password)
        login_page.click(LoginPage.CHANGE_PASSWORD_BUTTON)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LoginPage.PASSWORD_CHANGE_POPUP))
        popup_element = driver.find_element(*LoginPage.PASSWORD_CHANGE_POPUP)
        popup_element.click()

        # Wait for the popup to be completely closed
        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located(LoginPage.PASSWORD_CHANGE_POPUP))

        if login_page.is_element_visible(LoginPage.LOGOUT_BUTTON):
            # Wait for the logout button to be clickable to avoid click interception
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LoginPage.LOGOUT_BUTTON))
            login_page.click(LoginPage.LOGOUT_BUTTON)

        # Login with the old password, which should fail
        login_page.click(LoginPage.LOGIN_BUTTON)
        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['email'])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data['password'])
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

        assert login_page.is_element_visible(LoginPage.ERROR_MESSAGE), \
            "User was able to login with old password after password change."

        # Login with the new password, which should pass
        login_page.click(LoginPage.LOGIN_BUTTON)
        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['email'])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, new_password)
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

        assert login_page.wait_for_element_to_be_visible(LoginPage.MY_ACCOUNT_LINK), \
            "Login failed. User account/dashboard not displayed after password change."

        print("Test passed: Login after password change validated.")

    @allure.story("TC_LF_016: Validate logging in, closing the browser without logging out, and reopening the application")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after logging into the application and closing the browser without logging out, "
        "the logged-in session should still be maintained when reopening the application.")
    def test_login_session_after_browser_restart(self, driver, load_test_data):
        # Helper methods to save and load cookies
        def save_cookies(driver, filepath):
            """Save cookies to a file."""
            cookies = driver.get_cookies()
            with open(filepath, 'w') as cookie_file:
                json.dump(cookies, cookie_file)

        def load_cookies(driver, filepath):
            """Load cookies from a file."""
            with open(filepath, 'r') as cookie_file:
                cookies = json.load(cookie_file)
                for cookie in cookies:
                    driver.add_cookie(cookie)

        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']
        login_page = LoginPage(driver)

        if login_page.is_element_visible(LoginPage.LOGOUT_BUTTON):
            login_page.click(LoginPage.LOGOUT_BUTTON)

        login_page.click(LoginPage.LOGIN_BUTTON)
        login_page.enter_text(LoginPage.EMAIL_FIELD, test_data['email'])
        login_page.enter_text(LoginPage.PASSWORD_FIELD, test_data['password'])
        login_page.click(LoginPage.SUBMIT_LOGIN_BUTTON)

        assert login_page.wait_for_element_to_be_visible((By.CLASS_NAME, "ico-account")), \
            "Login failed. User account/dashboard not displayed."

        save_cookies(driver, 'cookies.json')

        driver.quit()

        driver = DriverFactory.get_driver()
        login_page = LoginPage(driver)
        login_page.open_url()

        load_cookies(driver, 'cookies.json')

        driver.refresh()

        login_page = LoginPage(driver)
        assert login_page.is_element_visible(LoginPage.MY_ACCOUNT_LINK), \
            "Session was not maintained after reopening the browser."

        print("Test passed: Session persisted after reopening the browser.")

        os.remove('cookies.json')

    @allure.story("TC_LF_017: Validate logging in, closing the browser without logging out, and reopening the application")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after logging into the application and closing the browser without logging out, the logged-in session should still be maintained when reopening the application.")
    def test_login_session_after_browser_restart(self, driver, load_test_data):
        pytest.skip()

    @allure.story("TC_LF_018: Validate user is able to navigate to different pages from Login page")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can navigate to different pages (Register Account, Sitemap, etc.) from the Login page.")
    def test_navigation_from_login_page(self, driver, load_test_data):
        login_page = LoginPage(driver)
        login_page.open_url()

        login_page.click(LoginPage.LOGIN_BUTTON)

        login_page.click(LoginPage.REGISTER_BUTTON)

        assert driver.current_url == "https://demo.nopcommerce.com/register?returnUrl=%2F", \
            "User was not navigated to the Register Account page."

        driver.back()

        # Click on 'Sitemap' link (or any other page link from the Login page)
        login_page.click(LoginPage.SITEMAP_LINK)

        assert driver.current_url == "https://demo.nopcommerce.com/sitemap", \
            "User was not navigated to the Sitemap page."

    @allure.story("TC_LF_019: Validate the UI of the Login page")
    @allure.severity(Severity.MINOR)
    @allure.label("Regression")
    @allure.description("This test validates the UI elements on the Login page, ensuring that all elements are displayed and aligned properly.")
    def test_ui_of_login_page(self, driver):
        login_page = LoginPage(driver)
        login_page.open_url()

        # Validate that all UI elements are visible on the Login page
        assert login_page.is_element_visible(LoginPage.LOGIN_FORM_FIELDS), "Login form is not visible."
        assert login_page.is_element_visible(LoginPage.EMAIL_FIELD), "Email field is not visible."
        assert login_page.is_element_visible(LoginPage.PASSWORD_FIELD), "Password field is not visible."
        assert login_page.is_element_visible(LoginPage.REMEMBER_ME_CHECKBOX), "Remember me checkbox is not visible."
        assert login_page.is_element_visible(LoginPage.LOGIN_BUTTON), "Login button is not visible."
        assert login_page.is_element_visible(LoginPage.FORGOT_PASSWORD_LINK), "Forgot password link is not visible."

        # Check if the Email and Password fields are aligned properly
        email_field = login_page.get_element(LoginPage.EMAIL_FIELD)
        password_field = login_page.get_element(LoginPage.PASSWORD_FIELD)
        assert email_field.location['x'] == password_field.location['x'], \
            "Email and Password fields are not aligned horizontally."

        # Validate the presence of text on the page
        login_button = login_page.get_element(LoginPage.LOGIN_BUTTON)
        assert login_button.text == "Log in", "Login button text is incorrect."
        forgot_password_link = login_page.get_element(LoginPage.FORGOT_PASSWORD_LINK)
        assert forgot_password_link.text == "Forgot password?", "Forgot password link text is incorrect."

        print("UI validation for the Login page passed successfully.")

    @allure.story("TC_LF_020: Validate the login page functionality in all supported environments")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Smoke")
    @allure.description(
        "This test validates the functionality of the login page in different environments (e.g., different browsers or devices)."
    )
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_login_page_functionality_on_different_browsers(self, driver, browser, load_test_data):
        pytest.skip()
