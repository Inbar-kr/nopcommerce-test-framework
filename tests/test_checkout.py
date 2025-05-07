import pytest
import json
import allure
from pages.checkout.billing_address_section import BillingAddressSection
from pages.checkout.payment_information_section import PaymentInformationSection
from pages.checkout.shipping_address_section import ShippingAddressSection
from tests.test_search import TestUserSearch
from tests.test_login import TestUserLogin
from pages.checkout.checkout_page import CheckoutPage
from config.config import Config
from allure_commons.types import Severity

@pytest.fixture(scope="module")
def load_test_data():
    with open(Config.TEST_DATA_PATH, 'r') as f:
        return json.load(f)

@allure.epic("Order Management")
@allure.feature("Checkout")
class TestCheckoutPage:

    @allure.story("TC_CO_001: Validate navigation to Checkout page with an empty Shopping Cart")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that clicking on 'Checkout' header option navigates the user to an empty 'Shopping Cart' page.")
    def test_checkout_navigation_empty_cart(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page.checkout_navigation_empty_cart()

        checkout_page.logger.info("Navigation successful to Checkout page with an empty Shopping Cart.")

    @allure.story("TC_CO_002: Validate navigating to Checkout page from 'Shopping Cart' page")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after adding a product to the cart and navigating to the shopping cart page, clicking the 'Checkout' button takes the user to the checkout page.")
    def test_checkout_navigation_from_cart(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page.checkout_navigation_from_cart(driver, load_test_data)

        checkout_page.logger.info("Navigation successful to Checkout page from 'Shopping Cart' page.")

    @allure.story("TC_CO_003: Validate navigating to Checkout page using 'Shopping Cart' header option")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that clicking on the 'Checkout' header option after a product is added to the shopping cart navigates the user to the checkout page.")
    def test_checkout_navigation_using_header_option(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page.checkout_navigation_using_header_option(driver, load_test_data)

        checkout_page.logger.info("Navigation successful to Checkout page from 'Shopping Cart' page.")

    @allure.story("TC_CO_004: Validate navigating to Checkout page using 'Checkout' option in the Cart block")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after adding a product to the cart, clicking on the 'Checkout' option in the Cart block navigates the user to the checkout page."
    )
    def test_checkout_navigation_from_cart_block(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page.checkout_navigation_from_cart_block(driver, load_test_data)

        checkout_page.logger.info("Navigation successful to Checkout page using 'Checkout' option in the Cart block.")

    @allure.story("TC_CO_005: Validate Checkout as Signed-In User using an existing address during checkout")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the checkout process for a signed-in user using an existing address during checkout, "
        "ensuring all sections of the checkout process are displayed correctly and the order is successfully placed.")
    def test_checkout_as_signin_user(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page.checkout_as_signin_user(driver, load_test_data)

        checkout_page.logger.info("Checkout successful as Signed-In User using an existing address during checkout.")

    @allure.story("TC_CO_006: Validate Checkout as Signed-In User by entering a new address in the Billing Details section")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the checkout process for a signed-in user by entering a new billing address during checkout, "
        "ensuring that all sections of the checkout process are displayed correctly and the order is successfully placed.")
    def test_checkout_as_signed_in_user_with_new_address(self, driver, load_test_data):
        billing_address_section = BillingAddressSection(driver)

        billing_address_section.checkout_as_signed_in_user_with_new_address(driver, load_test_data)

        billing_address_section.logger.info("Checkout successful as Signed-In User using an existing address during checkout.")

    @allure.story("TC_CO_007: Validate checkout as a signed-in user by entering a new address in all billing fields")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the checkout process for a signed-in user entering a new address in all billing fields, "
        "ensuring the user can proceed through the checkout process and complete the order."
    )
    def test_checkout_as_signed_in_user_with_new_address(self, driver, load_test_data):
        billing_address_section = BillingAddressSection(driver)

        billing_address_section.checkout_as_signin_user_with_full_billing_address(driver, load_test_data)

        billing_address_section.logger.info("Checkout successful as Signed-In User by entering a new billing address during checkout.")

    @allure.story("TC_CO_008: Validate that text fields in the Billing Details section of the checkout page have placeholders")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Smoke")
    @allure.description(
        "This test validates that the text fields in the Billing Details section of the checkout page have proper placeholder text."
    )
    def test_billing_address_placeholders(self, driver, load_test_data):
        billing_address_section = BillingAddressSection(driver)

        billing_address_section.validate_placeholders_for_all_fields(driver, load_test_data)

        billing_address_section.logger.info("All text fields in the billing address have the correct placeholder.")

    @allure.story("TC_CO_009: Validate the Billing Section of the Checkout page without entering any fields")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that appropriate field-level warning messages are displayed for all mandatory fields in the Billing address section when no fields are entered."
    )
    def test_billing_section_without_fields(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()

        billing_address_section = checkout_page.get_billing_address_section()

        billing_address_section.submit_billing_form_without_fields()

    @allure.story("TC_CO_010: Validate checkout as a signed-in user by entering all fields in the shipping address section")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the checkout process as a signed-in user when entering all fields in the shipping address section.")
    def test_checkout_with_shipping_address(self, driver, load_test_data):
        shipping_address_section = ShippingAddressSection(driver)

        shipping_address_section.checkout_with_shipping_address(driver, load_test_data)

        shipping_address_section.logger.info("Checkout successful as Signed-In User by entering all shipping address during checkout.")

    @allure.story("TC_CO_011: Validate that text fields in the Shipping address section of the checkout page have placeholders")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that all text fields in the Shipping address section of the checkout page display the correct placeholder text."
    )
    def test_shipping_address_placeholders(self, driver, load_test_data):
        shipping_address_section = ShippingAddressSection(driver)

        shipping_address_section.validate_placeholders_for_all_fields(driver, load_test_data)

        shipping_address_section.logger.info("All text fields in the Shipping address have the correct placeholder.")

    @allure.story("TC_CO_012: Validate Guest Checkout without entering any fields")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the guest checkout process, ensuring that appropriate field-level warning messages are displayed for all mandatory fields in the Billing address section when no fields are entered."
    )
    def test_guest_checkout_without_field(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()

        checkout_page.checkout_as_guest()

        billing_address_section = checkout_page.get_billing_address_section()
        billing_address_section.submit_billing_form_without_fields()

    @allure.story("TC_CO_013: Validate without entering any fields in the Shipping address Section")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test validates the behavior when no fields are entered in the Shipping address section and verifies the proper warning messages.")
    def test_no_fields_in_shipping_address(self, driver, load_test_data):
        shipping_address_section = ShippingAddressSection(driver)

        shipping_address_section.no_fields_in_shipping_address(driver, load_test_data)

        shipping_address_section.logger.info(
            "Checkout successful as Signed-In User by entering all shipping address during checkout.")

    @allure.story("TC_CO_014: Validate Guest Checkout")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the process of completing a checkout as a guest, ensuring all required sections display correctly and order is placed."
    )
    def test_guest_checkout(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page.checkout_as_guest_user(driver, load_test_data)

        checkout_page.logger.info("Checkout successful as guest User.")

    @allure.story("TC_CO_015: Validate Checkout as New User")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test validates the process of completing a checkout as a new user by registering, "
                        "ensuring all required sections display correctly and order is placed.")
    def test_checkout_as_new_user(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page.checkout_as_new_user(driver, load_test_data)

        checkout_page.logger.info("Checkout successful as new User.")

    @allure.story("TC_CO_016: Checkout by Signing in as Returning Customer")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description("This test validates the process of completing a checkout by logging in as a returning customer, "
                        "ensuring all required sections display correctly and the order is placed.")
    def test_checkout_as_returning_customer(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page.checkout_as_returning_user(driver, load_test_data)

        checkout_page.logger.info("Checkout successful as new User.")

    @allure.story("TC_CO_017: Validate Checkout using credit card as a payment.")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the user can checkout by using credit card as a payment in the payment information section.")
    def test_checkout_with_card_payment(self, driver, load_test_data):
        payment_information_section = PaymentInformationSection(driver)

        payment_information_section.checkout_with_card_payment(driver, load_test_data)

        payment_information_section.logger.info("Checkout successful as Signed-In User by using credit card as a payment.")

    @allure.story("TC_CO_018: Validate the 'Checkout' functionality in all the supported environments")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that the 'Checkout' functionality works correctly across all the supported environments, ensuring a consistent experience for users regardless of the platform."
    )
    def test_checkout_functionality_in_all_environments(self, driver, load_test_data):
        pytest.skip()
