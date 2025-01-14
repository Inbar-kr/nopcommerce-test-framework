from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.checkout.shipping_address_section import ShippingAddressSection
from pages.checkout.billing_address_section import BillingAddressSection
from pages.checkout.confirm_order_section import ConfirmOrderSection
from pages.checkout.test_data_provider import TestDataProvider
import logging
from pages.base_page import BasePage
from utils.wait_util import WaitUtil

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

    def verify_empty_cart(self):
        self.wait_for_element(self.ERROR_EMPTY_CART)
        return self.is_element_visible(self.ERROR_EMPTY_CART)

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
        shopping_cart_button = self.wait_for_element(self.SHOPPING_CART_BUTTON)
        cart_hover_button = self.wait_for_element(self.CART_HOVER_BUTTON)

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

    def extract_alert_text(self):
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        print("Alert Text:", alert_text)
        return alert_text

    def close_popup(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def checkout_as_guest(self):
        self.click(self.CHECKOUT_AS_GUEST_BUTTON)

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



    def verify_billing_and_confirmation_match(self):
        try:
            billing_details = self.get_billing_address_section().get_all_billing_address_details()
            confirm_order_details = self.get_confirm_order_section().get_confirm_order_details()

            self.logger.info(f"Billing Info: {billing_details}")
            self.logger.info(f"Confirmation Info: {confirm_order_details}")

            for key in billing_details.keys():
                assert billing_details[key] == confirm_order_details[key], \
                    f"Mismatch in {key}: Billing - {billing_details[key]}, Confirmation - {confirm_order_details[key]}"

            print("All billing and confirmation order details match successfully.")
        except AssertionError as e:
            self.logger.error(f"Assertion failed: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error during verification of billing and confirmation details: {str(e)}")
            raise





