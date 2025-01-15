from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
from pages.base_page import BasePage
from utils.wait_util import WaitUtil

class LoginPage(BasePage):
    # Locators for elements on the Login page
    EMAIL_FIELD = (By.ID, "Email")
    EMAIL_ERROR = (By.ID, "Email-error")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.XPATH, "//a[@class='ico-login']")
    LOGOUT_BUTTON = (By.XPATH, "//a[@class='ico-logout']")
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

    def is_password_hidden(self):
        password_field = self.get_element(self.PASSWORD_FIELD)
        return password_field.get_attribute("type") == "password"

    def is_password_visible(self):
        password_field = self.get_element(self.PASSWORD_FIELD)
        return password_field.get_attribute("type") == "text"

    def toggle_password_visibility(self):
        password_field = self.wait_for_element(self.PASSWORD_FIELD)

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


