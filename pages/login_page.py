import json
import os
import pyperclip
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.test_registration import TestUserRegistration
from utils.driver_factory import DriverFactory
import logging
from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators for elements on the Login page
    EMAIL_FIELD = (By.ID, "Email")
    EMAIL_ERROR = (By.ID, "Email-error")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.XPATH, "//a[@class='ico-login']")
    LOGOUT_BUTTON = (By.XPATH, "//a[@class='ico-logout']")
    POPUP_CLOSE_BUTTON = (By.XPATH, "//div[@id='bar-notification']//span[@title='Close']")
    POPUP_BAR_NOTIFICATION = (By.CSS_SELECTOR, "div.bar-notification.success")
    REMEMBER_ME_CHECKBOX = (By.ID, "RememberMe")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot password?")
    SUBMIT_LOGIN_BUTTON = (By.XPATH, "//button[@class='button-1 login-button']")
    ERROR_MESSAGE = (By.CLASS_NAME, "message-error.validation-summary-errors")
    REGISTER_BUTTON = (By.XPATH, "//button[@class='button-1 register-button']")

    SITEMAP_LINK = (By.LINK_TEXT, "Sitemap")
    MY_ACCOUNT_LINK = (By.CLASS_NAME, "ico-account")

    CHANGE_PASSWORD_LINK = (By.XPATH, "//a[@href='/customer/changepassword']")
    CHANGE_PASSWORD_BUTTON = (By.XPATH, "//button[@class='button-1 change-password-button']")

    OLD_PASSWORD_FIELD = (By.ID, "OldPassword")
    NEW_PASSWORD_FIELD = (By.ID, "NewPassword")
    CONFIRM_PASSWORD_FIELD = (By.ID, "ConfirmNewPassword")
    PASSWORD_CHANGE_POPUP = (By.CLASS_NAME, "close")
    LOGIN_FORM_FIELDS = (By.XPATH, "//div[@class='form-fields']")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger("LoginPage")
        logging.basicConfig(level=logging.INFO)

    def open_url(self, url="https://demo.nopcommerce.com/login?returnUrl=%2F"):
        self.driver.get(url)

    def submit_login_form(self):
        self.logger.info("Submitting the login form.")
        self.click(self.LOGIN_BUTTON)

    # Helper methods to save and load cookies
    @staticmethod
    def save_cookies(driver, filepath):
        cookies = driver.get_cookies()
        with open(filepath, 'w') as cookie_file:
            json.dump(cookies, cookie_file)

    @staticmethod
    def load_cookies(driver, filepath):
        with open(filepath, 'r') as cookie_file:
            cookies = json.load(cookie_file)
            for cookie in cookies:
                driver.add_cookie(cookie)

    def is_password_hidden(self):
        password_field = self.wait_for_element(*self.PASSWORD_FIELD)
        password_type = password_field.get_attribute("type")
        return password_type == "password"

    def is_password_visible(self):
        password_field = self.wait_for_element(*self.PASSWORD_FIELD)
        password_type = password_field.get_attribute("type")
        return password_type == "text"

    def validate_password_visibility(self, is_visible):
        if is_visible:
            assert self.is_password_visible(), "Password field should be visible."
        else:
            assert self.is_password_hidden(), "Password field should be hidden."

    def toggle_password_visibility(self):
        password_field = self.wait_for_element(*self.PASSWORD_FIELD)

        if password_field.get_attribute("type") == "password":
            self.driver.execute_script("arguments[0].setAttribute('type', 'text');", password_field)
        else:
            self.driver.execute_script("arguments[0].setAttribute('type', 'password');", password_field)

        self.logger.info("Password visibility toggled.")

    def select_password_text_and_right_click(self):
        password_field = self.get_element(self.PASSWORD_FIELD)
        action_chains = ActionChains(self.driver)
        action_chains.double_click(password_field).context_click(password_field).perform()
        self.logger.info("Selected password text and opened the context menu.")

    def copy_from_context_menu(self):
        action_chains = ActionChains(self.driver)
        action_chains.send_keys(Keys.ARROW_DOWN).send_keys(Keys.RETURN).perform()
        self.logger.info("Attempted to copy text using the context menu.")

    def select_password_text(self):
        password_field = self.get_element(self.PASSWORD_FIELD)
        action_chains = ActionChains(self.driver)
        action_chains.double_click(password_field).perform()
        self.logger.info("Selected password text.")

    def press_ctrl_c(self):
        password_field = self.get_element(self.PASSWORD_FIELD)
        password_field.send_keys(Keys.CONTROL, 'c')
        self.logger.info("Pressed Ctrl+C to attempt to copy the password text.")
        
    def navigation_from_login_page(self, driver):
        self.open_url()
        self.click(LoginPage.LOGIN_BUTTON)
        self.click(LoginPage.REGISTER_BUTTON)

        assert driver.current_url == "https://demo.nopcommerce.com/register?returnUrl=%2F", \
            "User was not navigated to the Register Account page."

        driver.back()

        self.click(LoginPage.SITEMAP_LINK)

        assert driver.current_url == "https://demo.nopcommerce.com/sitemap", \
            "User was not navigated to the Sitemap page."

    def login_user(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        if self.is_element_visible(By.XPATH, self.LOGOUT_BUTTON[1]):
            self.click(self.LOGOUT_BUTTON)

        self.click(self.LOGIN_BUTTON)
        self.enter_text(self.EMAIL_FIELD, test_data['email'])
        self.enter_text(self.PASSWORD_FIELD, test_data['password'])
        self.click(self.SUBMIT_LOGIN_BUTTON)

        self.wait_for_element_to_be_visible(self.MY_ACCOUNT_LINK)
        assert self.is_element_visible(By.CLASS_NAME,
                                       self.MY_ACCOUNT_LINK[1]), "Login failed. User account/dashboard not displayed."
        self.logger.info("Login successful.")

    def login_user_without_register(self, load_test_data):
        test_data = load_test_data['mandatory_fields']

        self.enter_text(self.EMAIL_FIELD, test_data['email'])
        self.enter_text(self.PASSWORD_FIELD, test_data['password'])
        self.click(self.SUBMIT_LOGIN_BUTTON)

        self.wait_for_element_to_be_visible(self.MY_ACCOUNT_LINK)
        assert self.is_element_visible(By.CLASS_NAME,
                                       self.MY_ACCOUNT_LINK[1]), "Login failed. User account/dashboard not displayed."
        self.logger.info("Login successful.")

    def logout_user(self):
        locator_strategy, locator_value = self.LOGOUT_BUTTON

        if self.is_element_visible(locator_strategy, locator_value):
            self.click(self.LOGOUT_BUTTON)
            self.logger.info("Logged out successfully.")
        else:
            self.logger.warning("Logout button is not visible; user might already be logged out.")

    def invalid_login_user(self, load_test_data):
        test_data = load_test_data["invalid_user"]

        self.open_url()

        self.enter_text(self.EMAIL_FIELD, test_data["username"])
        self.enter_text(self.PASSWORD_FIELD, test_data["password"])

        self.click(self.SUBMIT_LOGIN_BUTTON)

        self.wait_for_element_to_be_visible(self.ERROR_MESSAGE)

        self.logger.info("Attempted login with invalid credentials.")

    def login_with_invalid_email(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        invalid_email_data = {"username": "invalidemail@example.com"}

        if self.is_element_visible(By.XPATH, self.LOGOUT_BUTTON[1]):
            self.click(self.LOGOUT_BUTTON)

        self.click(self.LOGIN_BUTTON)
        self.enter_text(self.EMAIL_FIELD, invalid_email_data['username'])
        self.enter_text(self.PASSWORD_FIELD, test_data['password'])
        self.click(self.SUBMIT_LOGIN_BUTTON)

        self.wait_for_element_to_be_visible(self.ERROR_MESSAGE)
        assert self.is_element_visible(By.CLASS_NAME, self.ERROR_MESSAGE[1]), "Login failed with invalid email. Error message not displayed."

        self.logger.info("Attempted login with invalid email.")

    def login_with_invalid_password(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        invalid_password_data = {"password": "InvalidPassword123!"}

        if self.is_element_visible(By.XPATH, self.LOGOUT_BUTTON[1]):
            self.click(self.LOGOUT_BUTTON)

        self.click(self.LOGIN_BUTTON)
        self.enter_text(self.EMAIL_FIELD, test_data['email'])
        self.enter_text(self.PASSWORD_FIELD, invalid_password_data['password'])
        self.click(self.SUBMIT_LOGIN_BUTTON)

        self.wait_for_element_to_be_visible(self.ERROR_MESSAGE)
        assert self.is_element_visible(By.CLASS_NAME, self.ERROR_MESSAGE[1]), "Login failed with invalid password. Error message not displayed."

        self.logger.info("Attempted login with invalid password.")

    def login_without_credentials(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        if self.is_element_visible(By.XPATH, self.LOGOUT_BUTTON[1]):
            self.click(self.LOGOUT_BUTTON)

        self.click(self.LOGIN_BUTTON)
        self.enter_text(self.EMAIL_FIELD, '')
        self.enter_text(self.PASSWORD_FIELD, '')
        self.click(self.SUBMIT_LOGIN_BUTTON)

        self.wait_for_element_to_be_visible(self.MY_ACCOUNT_LINK)
        assert self.is_element_visible(By.CLASS_NAME,
                                       self.MY_ACCOUNT_LINK[1]), "Login failed. User account/dashboard not displayed."
        self.logger.info("Login successful.")

    def login_with_keyboard_keys(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        test_data = load_test_data['mandatory_fields']

        if self.is_element_visible(By.XPATH, self.LOGOUT_BUTTON[1]):
            self.click(self.LOGOUT_BUTTON)

        self.click(self.LOGIN_BUTTON)
        email_field = self.wait_for_element(*self.EMAIL_FIELD)
        email_field.send_keys(test_data['email'])
        email_field.send_keys(Keys.TAB)

        password_field = self.wait_for_element(*self.PASSWORD_FIELD)
        password_field.send_keys(test_data['password'])
        password_field.send_keys(Keys.TAB)

        submit_button = self.wait_for_element(*self.SUBMIT_LOGIN_BUTTON)
        submit_button.send_keys(Keys.ENTER)

        self.wait_for_element_to_be_visible(self.MY_ACCOUNT_LINK)
        assert self.is_element_visible(*self.MY_ACCOUNT_LINK), "Login failed. User account/dashboard not displayed."
        self.logger.info("Login successful using keyboard keys.")

    def login_and_browser_back(self, driver, load_test_data):
        self.login_user(driver, load_test_data)

        driver.back()

        content_element = self.wait_for_element_to_be_visible((By.CLASS_NAME, "content"))

        assert content_element.is_displayed(), "Content element is not displayed after using the browser's back button."

    def logout_and_browser_back(self, driver, load_test_data):
        self.login_user(driver, load_test_data)
        self.logout_user()

        driver.back()

        locator_strategy, locator_value = LoginPage.LOGIN_BUTTON

        assert self.is_element_visible(locator_strategy, locator_value), \
            "Error: User logged in again after using the browser back button."

    def validate_placeholders(self, driver):
        self.open_url()

        expected_placeholders = {
            self.EMAIL_FIELD: "Email",
            self.PASSWORD_FIELD: "Password"
        }

        for field_locator, expected_placeholder in expected_placeholders.items():
            field = self.wait_for_element(field_locator, timeout=10)
            if field:
                self.wait_for_placeholder(driver, field_locator, expected_placeholder)
            else:
                print(f"Field {field_locator} not found!")
        self.logger.info("All fields have the correct placeholders.")

    def forgotten_password_link(self, driver):
        self.open_url()

        assert self.is_element_visible(LoginPage.FORGOT_PASSWORD_LINK[0], LoginPage.FORGOT_PASSWORD_LINK[1]), \
            "'Forgotten Password' link is not visible on the Login page."

        self.click(LoginPage.FORGOT_PASSWORD_LINK)

        assert driver.current_url == "https://demo.nopcommerce.com/passwordrecovery", \
            f"Password reset page not reached. Current URL is {driver.current_url}."

    def password_copying(self, load_test_data):
        test_data = load_test_data["valid_user"]

        self.open_url()

        password_text = test_data["password"]
        self.enter_text(self.PASSWORD_FIELD, password_text)

        self.select_password_text_and_right_click()
        self.copy_from_context_menu()

        clipboard_content = pyperclip.paste()
        assert clipboard_content != password_text, "Password text was unexpectedly copied using the right-click menu."

        self.select_password_text()
        self.press_ctrl_c()

        clipboard_content = pyperclip.paste()
        assert clipboard_content != password_text, "Password text was unexpectedly copied using Ctrl+C."

        self.logger.info("Attempted to copy the password using the right-click menu or the Ctrl+C shortcut.")

    def password_page_source(self, driver, load_test_data):
        test_data = load_test_data["valid_user"]

        self.open_url()

        password_text = test_data["password"]
        self.enter_text(self.PASSWORD_FIELD, password_text)

        page_source = driver.page_source
        assert password_text not in page_source, \
            "Password text was unexpectedly visible in the page source before login."

        self.click(self.SUBMIT_LOGIN_BUTTON)

        page_source = driver.page_source
        assert password_text not in page_source, \
            "Password text was unexpectedly visible in the page source after login."

        self.logger.info("Attempted to see the password in the page source")

    def change_password_page(self, driver, load_test_data):
        self.login_user(driver, load_test_data)

        test_data = load_test_data["mandatory_fields"]
        new_password = "NewPassword123!"

        self.click(self.MY_ACCOUNT_LINK)
        self.click(self.CHANGE_PASSWORD_LINK)
        self.enter_text(self.OLD_PASSWORD_FIELD, test_data['password'])
        self.enter_text(self.NEW_PASSWORD_FIELD, new_password)
        self.enter_text(self.CONFIRM_PASSWORD_FIELD, new_password)
        self.click(self.CHANGE_PASSWORD_BUTTON)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(self.PASSWORD_CHANGE_POPUP))
        popup_element = driver.find_element(*self.PASSWORD_CHANGE_POPUP)
        popup_element.click()
        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located(self.PASSWORD_CHANGE_POPUP))

        if self.is_element_visible(self.LOGOUT_BUTTON[0], self.LOGOUT_BUTTON[1]):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((self.LOGOUT_BUTTON[0], self.LOGOUT_BUTTON[1])))
            self.click(self.LOGOUT_BUTTON)

        # Login with old password, which should fail
        self.login_with_password(test_data['email'], test_data['password'], expect_success=False)

        # Login with new password, which should pass
        self.login_with_password(test_data['email'], new_password, expect_success=True)

        self.logger.info("Attempted to change the password then Login with the new password")

    def password_visibility_toggle(self, load_test_data):
        test_data = load_test_data['mandatory_fields']

        self.open_url()
        self.enter_text(self.PASSWORD_FIELD, test_data['password'])
        self.enter_text(self.CONFIRM_PASSWORD_FIELD, test_data['confirm_password'])

        assert self.is_password_hidden(), "Password field is unexpectedly visible."

        self.toggle_password_visibility()

        assert self.is_password_visible(), "Password field is still hidden after toggle."

        self.toggle_password_visibility()

        assert self.is_password_hidden(), "Password field is unexpectedly visible after second toggle."

        self.logger.info("Password visibility toggle test passed successfully.")

    def login_with_password(self, email, password, expect_success=True):
        self.click(self.LOGIN_BUTTON)
        self.enter_text(self.EMAIL_FIELD, email)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.SUBMIT_LOGIN_BUTTON)

        if expect_success:
            assert self.wait_for_element_to_be_visible(self.MY_ACCOUNT_LINK), \
                "Login failed. User account/dashboard not displayed after password change."
            self.logger.info("Login successful with new password.")
        else:
            assert self.is_element_visible(self.ERROR_MESSAGE[0], self.ERROR_MESSAGE[1]), \
                "User was able to login with old password after password change."
            self.logger.info("Login failed with old password as expected.")

    def login_session_after_browser_restart(self, driver, load_test_data):
        self.open_url()
        self.login_user(driver, load_test_data)
        self.save_cookies(driver, 'cookies.json')

        driver.quit()

        driver = DriverFactory.get_driver()
        login_page = LoginPage(driver)
        login_page.open_url()

        self.load_cookies(driver, 'cookies.json')
        driver.refresh()

        # To fix: Wait for the popup to be visible and clickable, if it's present
        if self.wait_for_element_to_be_visible(self.POPUP_BAR_NOTIFICATION):
            self.logger.info("Popup displayed after reopening the browser.")
            close_button = driver.find_element(*self.POPUP_BAR_NOTIFICATION).find_element(By.CSS_SELECTOR, "span.close")
            close_button.click()
        else:
            self.logger.info("No popup displayed after reopening the browser.")

        # Verify session persistence
        if self.wait_for_element_to_be_visible(self.MY_ACCOUNT_LINK):
            self.logger.info("Login successful after reopening the browser.")
        else:
            assert self.is_element_visible(*self.ERROR_MESSAGE), \
                "Session was not maintained after reopening the browser."

        self.logger.info("Session persisted after reopening the browser.")

        # Clean up by removing the cookies file
        try:
            os.remove('cookies.json')
        except OSError as e:
            self.logger.error(f"Failed to delete cookies file: {e}")

    def ui_of_login_page(self):
        self.open_url()

        assert self.is_element_visible(LoginPage.LOGIN_FORM_FIELDS[0],
                                       LoginPage.LOGIN_FORM_FIELDS[1]), "Login form is not visible."
        assert self.is_element_visible(LoginPage.EMAIL_FIELD[0],
                                       LoginPage.EMAIL_FIELD[1]), "Email field is not visible."
        assert self.is_element_visible(LoginPage.PASSWORD_FIELD[0],
                                       LoginPage.PASSWORD_FIELD[1]), "Password field is not visible."
        assert self.is_element_visible(LoginPage.REMEMBER_ME_CHECKBOX[0],
                                       LoginPage.REMEMBER_ME_CHECKBOX[1]), "Remember me checkbox is not visible."
        assert self.is_element_visible(LoginPage.LOGIN_BUTTON[0],
                                       LoginPage.LOGIN_BUTTON[1]), "Login button is not visible."
        assert self.is_element_visible(LoginPage.FORGOT_PASSWORD_LINK[0],
                                       LoginPage.FORGOT_PASSWORD_LINK[1]), "Forgot password link is not visible."

        email_field = self.get_element(LoginPage.EMAIL_FIELD)
        password_field = self.get_element(LoginPage.PASSWORD_FIELD)
        assert email_field.location['x'] == password_field.location['x'], \
            "Email and Password fields are not aligned horizontally."

        login_button = self.get_element(LoginPage.LOGIN_BUTTON)
        assert login_button.text == "Log in", "Login button text is incorrect."
        forgot_password_link = self.get_element(LoginPage.FORGOT_PASSWORD_LINK)
        assert forgot_password_link.text == "Forgot password?", "Forgot password link text is incorrect."
