from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.checkout.test_data_provider import TestDataProvider
import logging
from pages.base_page import BasePage
from pages.login_page import LoginPage
from tests.test_login import TestUserLogin
from tests.test_registration import TestUserRegistration
from tests.test_search import TestUserSearch


class CheckoutPage(BasePage):
    # # Main locators for the checkout process
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "button-2.product-box-add-to-cart-button")
    SHOPPING_CART_POPUP_LINK = (By.LINK_TEXT, "shopping cart")
    SHOPPING_CART_POPUP_CLOSE = (By.CLASS_NAME, "close")
    SHOPPING_CART_BUTTON = (By.CLASS_NAME, "ico-cart")
    CART_HOVER_BUTTON = (By.CSS_SELECTOR, "a.ico-cart")
    GO_TO_CART_BUTTON = (By.CSS_SELECTOR, "#flyout-cart .button-1.cart-button")

    # Shopping cart page
    QUANTITY_PRODUCT_UP = (By.ID, "quantity-up-11228")
    QUANTITY_PRODUCT_DOWN = (By.ID, "quantity-down-11228")
    REMOVE_PRODUCT_BUTTON = (By.CLASS_NAME, "remove-btn")
    CONTINUE_SHOPPING_BUTTON = (By.CLASS_NAME, "button-2.continue-shopping-button")
    GIFT_WRAPPING_DROPDOWN = (By.ID, "checkout_attribute_1")
    AGREE_TERMS_CHECKBOX = (By.ID, "termsofservice")
    ERROR_TERMS_CLOSE_BUTTON = (By.CLASS_NAME, "ui-button ui-corner-all ui-widget ui-button-icon-only ui-dialog-titlebar-close")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    ERROR_EMPTY_CART = (By.CLASS_NAME, "no-data")

    # Guest / registration / login - page
    CHECKOUT_AS_GUEST_BUTTON = (By.CLASS_NAME, "button-1.checkout-as-guest-button")
    REGISTER_BUTTON = (By.CLASS_NAME, "button-1.register-button")
    REGISTER_CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.register-continue-button")

    EMAIL_FIELD = (By.ID, "Email")
    EMAIL_ERROR = (By.ID, "Email-error")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.CLASS_NAME, "button-1.login-button")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger("CheckoutPage")
        logging.basicConfig(level=logging.INFO)

    def open_url(self, url="https://demo.nopcommerce.com/"):
        self.driver.get(url)

    def get_billing_address_section(self):
        from pages.checkout.billing_address_section import BillingAddressSection
        return BillingAddressSection(self.driver)

    def get_shipping_address_section(self):
        from pages.checkout.shipping_address_section import ShippingAddressSection
        return ShippingAddressSection(self.driver)

    def get_shipping_method_section(self):
        from pages.checkout.shipping_method_section import ShippingMethodSection
        return ShippingMethodSection(self.driver)

    def get_payment_method_section(self):
        from pages.checkout.payment_method_section import PaymentMethodSection
        return PaymentMethodSection(self.driver)

    def get_payment_information_section(self):
        from pages.checkout.payment_information_section import PaymentInformationSection
        return PaymentInformationSection(self.driver)

    def get_confirm_order_section(self):
        from pages.checkout.confirm_order_section import ConfirmOrderSection
        return ConfirmOrderSection(self.driver)

    def _login_as_user(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

    def _logout_as_user(self, driver):
        login_page = LoginPage(driver)
        login_page.logout_user()

    def _login_as_new_user(self, driver, load_test_data):
        login_page = LoginPage(driver)
        login_page.login_user_without_register(load_test_data)

    def _register_as_user(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

    def _returning_customer(self, driver, load_test_data):
        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

    def _search_and_add_product(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)
        self.add_product_to_cart()

    def _fill_billing_and_shipping_details(self, driver, load_test_data):
        self.verify_billing_details_match(driver, load_test_data, fill_full_address=True)

    def _select_shipping_method(self, method):
        shipping_method_section = self.get_shipping_method_section()
        shipping_method_section.select_shipping_method(method)

    def _select_payment_method(self, method):
        payment_method_section = self.get_payment_method_section()
        payment_method_section.select_payment_method(method)

    def _complete_payment_and_order(self):
        payment_information_section = self.get_payment_information_section()
        payment_information_section.click(payment_information_section.CONTINUE_BUTTON)

        confirm_order = self.get_confirm_order_section()
        confirm_order.confirm_order()
        confirm_order.complete_order()

    def _complete_card_payment_and_order(self, load_test_data):
        payment_information_section = self.get_payment_information_section()
        payment_information_section.fill_payment_information(load_test_data)

        confirm_order = self.get_confirm_order_section()
        confirm_order.confirm_order()
        confirm_order.complete_order()

    def _validate_placeholder_for_field(self, driver, field_locator, expected_placeholder):
        try:
            field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(field_locator)
            )
            if field:
                actual_placeholder = field.get_attribute("placeholder")
                if not actual_placeholder:
                    self.logger.warning(f"No placeholder found for field '{field_locator}'. Skipping validation.")
                    return
                assert actual_placeholder == expected_placeholder, \
                    f"Placeholder mismatch! Expected: '{expected_placeholder}', but got: '{actual_placeholder}'"
                self.logger.info(f"Placeholder for field '{field_locator}' is correct.")
            else:
                self.logger.error(f"Element '{field_locator}' not found on the page.")
                raise ValueError(f"Element '{field_locator}' is missing.")
        except Exception as e:
            self.logger.error(f"Error during placeholder validation for '{field_locator}': {str(e)}")
            raise

    def verify_empty_cart(self):
        self.wait_for_element(*self.ERROR_EMPTY_CART)
        return self.is_element_visible(*self.ERROR_EMPTY_CART)

    def add_product_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)
        self.click(self.SHOPPING_CART_POPUP_LINK)
        self.click(self.AGREE_TERMS_CHECKBOX)
        self.click(self.CHECKOUT_BUTTON)

    def add_product_to_cart_header(self):
        self.click(self.ADD_TO_CART_BUTTON)
        self.click(self.SHOPPING_CART_BUTTON)
        self.click(self.AGREE_TERMS_CHECKBOX)
        self.click(self.CHECKOUT_BUTTON)

    def continue_to_checkout(self):
        self.click(self.REGISTER_CONTINUE_BUTTON)
        self.click(self.SHOPPING_CART_BUTTON)
        self.click(self.AGREE_TERMS_CHECKBOX)
        self.click(self.CHECKOUT_BUTTON)

    def hover_cart_button(self):
        shopping_cart_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SHOPPING_CART_BUTTON)
        )
        cart_hover_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CART_HOVER_BUTTON)
        )

        actions = ActionChains(self.driver)
        actions.move_to_element(shopping_cart_button).perform()

        self.wait_for_element(self.CART_HOVER_BUTTON)
        self.wait_for_element(self.GO_TO_CART_BUTTON)

        actions.move_to_element(cart_hover_button).click().perform()

    def proceed_as_guest(self):
        self.click(self.CHECKOUT_AS_GUEST_BUTTON)

    def proceed_to_register(self):
        self.click(self.REGISTER_BUTTON)

    def register_account(self, email, password):
        self.enter_text(self.EMAIL_FIELD, email)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.REGISTER_BUTTON)

    def login(self, email, password):
        self.enter_text(self.EMAIL_FIELD, email)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    def confirm_order(self):
        confirm_order_section = self.get_confirm_order_section()
        confirm_order_section.confirm_order()

    def checkout_as_guest(self):
        self.click(self.CHECKOUT_AS_GUEST_BUTTON)

    def checkout_navigation_empty_cart(self):
        self.open_url()

        self.wait_for_element(self.SHOPPING_CART_BUTTON)
        self.click(self.SHOPPING_CART_BUTTON)

        self.wait_for_element(self.ERROR_EMPTY_CART)
        assert self.verify_empty_cart(), "Empty cart message was not displayed"

    def checkout_navigation_from_cart(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        self.add_product_to_cart()
        assert "checkout" in driver.current_url, "User was not redirected to the checkout page"

    def checkout_navigation_using_header_option(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        self.add_product_to_cart_header()
        assert "checkout" in driver.current_url, "User was not redirected to the checkout page!"

    def verify_billing_details_match(self, driver, load_test_data, fill_full_address):
        registration_helper = TestDataProvider()
        registered_details = registration_helper.get_registered_details(load_test_data)

        billing_address_section = self.get_billing_address_section()
        billing_details = billing_address_section.get_billing_address_details()

        for field in ["first_name", "last_name", "email"]:
            assert registered_details[field] == billing_details[field], \
                f"{field.replace('_', ' ').title()} does not match. Expected: {registered_details[field]}, Found: {billing_details[field]}"

        if fill_full_address:
            billing_address_section.enter_all_billing_address(load_test_data)
        else:
            billing_address_section.enter_mandatory_billing_address(load_test_data)

    def checkout_navigation_from_cart_block(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)
        self.logger.info("Product added to the cart.")

        self.click(self.ADD_TO_CART_BUTTON)
        self.click(self.SHOPPING_CART_POPUP_CLOSE)
        self.wait_for_element(self.SHOPPING_CART_BUTTON)
        time.sleep(2)
        self.logger.info("Cart button and popup handled.")

        self.hover_cart_button()

        assert self.is_element_visible(*self.CHECKOUT_BUTTON), \
            "Checkout page failed. User was not redirected to the checkout page."
        self.logger.info("User successfully redirected to the checkout page.")

    def checkout_as_signin_user(self, driver, load_test_data):
        self._login_as_user(driver, load_test_data)
        self._search_and_add_product(driver, load_test_data)
        self._fill_billing_and_shipping_details(driver, load_test_data)
        self._select_shipping_method("ground")
        self._select_payment_method("Check / Money Order")
        self._complete_payment_and_order()

        self.logger.info("Attempt to checkout as a signin user.")

    def checkout_as_guest_user(self, driver, load_test_data):
        self._login_as_user(driver, load_test_data)
        self._search_and_add_product(driver, load_test_data)
        self.proceed_as_guest()
        self._fill_billing_and_shipping_details(driver, load_test_data)
        self._select_shipping_method("ground")
        self._select_payment_method("Check / Money Order")
        self._complete_payment_and_order()

        self.logger.info("Attempt to checkout as a guest user.")

    def checkout_as_new_user(self, driver, load_test_data):
        self._search_and_add_product(driver, load_test_data)
        self.proceed_to_register()
        self._register_as_user(driver, load_test_data)
        self.continue_to_checkout()
        self._fill_billing_and_shipping_details(driver, load_test_data)
        self._select_shipping_method("ground")
        self._select_payment_method("Check / Money Order")
        self._complete_payment_and_order()

        self.logger.info("Attempt to checkout as a new user.")

    def checkout_as_returning_user(self, driver, load_test_data):
        self._register_as_user(driver, load_test_data)
        self._logout_as_user(driver)
        self._search_and_add_product(driver, load_test_data)
        self._login_as_new_user(driver, load_test_data)
        self.click(self.AGREE_TERMS_CHECKBOX)
        self.click(self.CHECKOUT_BUTTON)
        self._fill_billing_and_shipping_details(driver, load_test_data)
        self._select_shipping_method("ground")
        self._select_payment_method("Check / Money Order")
        self._complete_payment_and_order()

        self.logger.info("Attempt to checkout as a returning user.")
