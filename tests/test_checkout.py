import time
import pytest
import json
import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys

from pages.checkout.confirm_order_section import ConfirmOrderSection
from tests.test_registration import TestUserRegistration
from tests.test_search import TestUserSearch
from tests.test_login import TestUserLogin
from pages.checkout.checkout_page import CheckoutPage
from pages.checkout.billing_address_section import BillingAddressSection
from pages.checkout.test_data_provider import TestDataProvider
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
        from pages.checkout.checkout_page import CheckoutPage

        checkout_page = CheckoutPage(driver)
        checkout_page.open_url()

        checkout_page.wait_for_element(checkout_page.SHOPPING_CART_BUTTON)
        checkout_page.click(checkout_page.SHOPPING_CART_BUTTON)

        checkout_page.wait_for_element(checkout_page.ERROR_EMPTY_CART)
        assert checkout_page.verify_empty_cart(), "Empty cart message was not displayed"

    @allure.story("TC_CO_002: Validate navigating to Checkout page from 'Shopping Cart' page")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after adding a product to the cart and navigating to the shopping cart page, clicking the 'Checkout' button takes the user to the checkout page.")
    def test_checkout_navigation_from_cart(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)

        checkout_page.add_product_to_cart()

        assert "checkout" in driver.current_url, "User was not redirected to the checkout page"

    @allure.story("TC_CO_003: Validate navigating to Checkout page using 'Shopping Cart' header option")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that clicking on the 'Checkout' header option after a product is added to the shopping cart navigates the user to the checkout page.")
    def test_checkout_navigation_using_header_option(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)

        checkout_page.add_product_to_cart_header()

        assert "checkout" in driver.current_url, "User was not redirected to the checkout page!"

    @allure.story("TC_CO_004: Validate navigating to Checkout page using 'Checkout' option in the Cart block")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after adding a product to the cart, clicking on the 'Checkout' option in the Cart block navigates the user to the checkout page."
    )
    def test_checkout_navigation_from_cart_block(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)

        checkout_page.click(CheckoutPage.ADD_TO_CART_BUTTON)
        checkout_page.click(CheckoutPage.SHOPPING_CART_POPUP_CLOSE)
        checkout_page.wait_for_element(CheckoutPage.SHOPPING_CART_BUTTON)

        checkout_page.hover_cart_button()

        assert checkout_page.is_element_visible(
            CheckoutPage.CHECKOUT_BUTTON), "Checkout page failed. User was not redirected to the checkout page."

    @allure.story("TC_CO_005: Validate Checkout as Signed-In User using an existing address during checkout")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the checkout process for a signed-in user using an existing address during checkout, "
        "ensuring all sections of the checkout process are displayed correctly and the order is successfully placed.")
    def test_checkout_as_signin_user(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()

        checkout_page.verify_billing_details_match(driver, load_test_data)

        shipping_method_section = checkout_page.get_shipping_method_section()
        shipping_method_section.select_shipping_method("ground")

        payment_method_section = checkout_page.get_payment_method_section()
        payment_method_section.select_payment_method("Check / Money Order")

        payment_information_section = checkout_page.get_payment_information_section()
        payment_information_section.click(payment_information_section.CONTINUE_BUTTON)

        # checkout_page.verify_billing_and_confirmation_match()

        confirm_order = ConfirmOrderSection(driver)
        confirm_order.confirm_order()

        confirm_order.complete_order()

    @allure.story("TC_CO_006: Validate Checkout as Signed-In User by entering a new address in the Billing Details section")
    @allure.severity(Severity.NORMAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the checkout process for a signed-in user by entering a new billing address during checkout, "
        "ensuring that all sections of the checkout process are displayed correctly and the order is successfully placed.")
    def test_checkout_as_signed_in_user_with_new_address(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)

        checkout_page.add_product_to_cart()
        time.sleep(2)

        billing_address_section = checkout_page.get_billing_address_section()
        time.sleep(2)

        billing_address_section.wait_for_element(billing_address_section.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()

        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=False)
        time.sleep(2)

        shipping_address_section = checkout_page.get_shipping_address_section()
        shipping_address_section.enter_mandatory_shipping_address(load_test_data)
        time.sleep(2)

        shipping_method_section = checkout_page.get_shipping_method_section()
        shipping_method_section.select_shipping_method("ground")

        payment_method_section = checkout_page.get_payment_method_section()
        payment_method_section.select_payment_method("Check / Money Order")

        payment_information_section = checkout_page.get_payment_information_section()
        payment_information_section.click(payment_information_section.CONTINUE_BUTTON)

        # checkout_page.verify_billing_and_confirmation_match()

        confirm_order = ConfirmOrderSection(driver)
        confirm_order.confirm_order()
        time.sleep(2)

        confirm_order.complete_order()

    @allure.story("TC_CO_007: Validate checkout as a signed-in user by entering a new address in all billing fields")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the checkout process for a signed-in user entering a new address in all billing fields, ensuring the user can proceed through the checkout process and complete the order."
    )
    def test_checkout_as_signin_user_with_full_billing_address(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()
        time.sleep(2)

        billing_address_section = checkout_page.get_billing_address_section()
        time.sleep(2)

        billing_address_section.wait_for_element(billing_address_section.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()

        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=True)
        time.sleep(2)

        shipping_address_section = checkout_page.get_shipping_address_section()
        shipping_address_section.enter_mandatory_shipping_address(load_test_data)
        time.sleep(2)

        shipping_method_section = checkout_page.get_shipping_method_section()
        shipping_method_section.select_shipping_method("ground")

        payment_method_section = checkout_page.get_payment_method_section()
        payment_method_section.select_payment_method("Check / Money Order")

        payment_information_section = checkout_page.get_payment_information_section()
        payment_information_section.click(payment_information_section.CONTINUE_BUTTON)

        # checkout_page.verify_billing_and_confirmation_match()

        confirm_order = ConfirmOrderSection(driver)
        confirm_order.confirm_order()
        time.sleep(2)

        confirm_order.complete_order()

    @allure.story("TC_CO_008: Validate that text fields in the Billing Details section of the checkout page have placeholders")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Smoke")
    @allure.description(
        "This test validates that the text fields in the Billing Details section of the checkout page have proper placeholder text."
    )
    def test_billing_address_placeholders(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()

        billing_address_section = checkout_page.get_billing_address_section()

        billing_address_section.validate_placeholders_for_all_fields(driver)

    @allure.story("TC_CO_008: Validate that text fields in the Billing Details section of the checkout page have placeholders")
    @allure.severity(Severity.NORMAL)
    @allure.label("Smoke")
    @allure.description(
        "This test validates that the text fields in the Billing Details section of the checkout page have proper placeholder text.")
    def test_billing_address_placeholders(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()

        billing_address_section = checkout_page.get_billing_address_section()
        billing_address_section.wait_for_element(billing_address_section.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()

        billing_address_section.validate_placeholders_for_all_fields(driver)

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
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()

        billing_address_section = checkout_page.get_billing_address_section()
        time.sleep(2)

        billing_address_section.wait_for_element(billing_address_section.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()

        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=False)
        time.sleep(2)

        shipping_address_section = checkout_page.get_shipping_address_section()
        shipping_address_section.enter_mandatory_shipping_address(load_test_data)
        time.sleep(2)

        shipping_method_section = checkout_page.get_shipping_method_section()
        shipping_method_section.select_shipping_method("ground")

        payment_method_section = checkout_page.get_payment_method_section()
        payment_method_section.select_payment_method("Check / Money Order")

        payment_information_section = checkout_page.get_payment_information_section()
        payment_information_section.click(payment_information_section.CONTINUE_BUTTON)

        # checkout_page.verify_billing_and_confirmation_match()

        confirm_order = ConfirmOrderSection(driver)
        confirm_order.confirm_order()
        time.sleep(2)

        confirm_order.complete_order()

    @allure.story("TC_CO_011: Validate that text fields in the Shipping address section of the checkout page have placeholders")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that all text fields in the Shipping address section of the checkout page display the correct placeholder text."
    )
    def test_shipping_address_placeholders(self, driver, load_test_data):
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()

        billing_address_section = checkout_page.get_billing_address_section()
        billing_address_section.wait_for_element(billing_address_section.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()

        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=False)

        shipping_address_section = checkout_page.get_shipping_address_section()
        shipping_address_section.validate_placeholders_for_all_fields(driver)

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
        login_test = TestUserLogin()
        login_test.test_valid_login(driver, load_test_data)

        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()

        billing_address_section = checkout_page.get_billing_address_section()

        billing_address_section.wait_for_element(billing_address_section.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()

        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=False)

        shipping_address_section = checkout_page.get_shipping_address_section()
        shipping_address_section.submit_shipping_form_without_fields()

    @allure.story("TC_CO_014: Validate Guest Checkout")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the process of completing a checkout as a guest, ensuring all required sections display correctly and order is placed."
    )
    def test_guest_checkout(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()
        checkout_page.proceed_as_guest()

        billing_address_section = checkout_page.get_billing_address_section()
        billing_address_section.enter_full_billing_address(load_test_data)

        shipping_method_section = checkout_page.get_shipping_method_section()
        shipping_method_section.select_shipping_method("ground")

        payment_method_section = checkout_page.get_payment_method_section()
        payment_method_section.select_payment_method("Check / Money Order")

        payment_information_section = checkout_page.get_payment_information_section()
        payment_information_section.click(payment_information_section.CONTINUE_BUTTON)

        # checkout_page.verify_billing_and_confirmation_match()

        confirm_order = ConfirmOrderSection(driver)
        confirm_order.confirm_order()

        confirm_order.complete_order()

    @allure.story("TC_CO_015: Validate Checkout as New User")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the process of completing a checkout as a new user by registering, ensuring all required sections display correctly and order is placed."
    )
    def test_checkout_as_new_user(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()
        checkout_page.proceed_to_register()

        registration_test = TestUserRegistration()
        registration_test.test_mandatory_fields_registration(driver, load_test_data)

        checkout_page.continue_to_checkout()

        billing_address_section = checkout_page.get_billing_address_section()
        billing_address_section.enter_mandatory_billing_address(load_test_data)
        time.sleep(2)

        shipping_method_section = checkout_page.get_shipping_method_section()
        shipping_method_section.select_shipping_method("ground")

        payment_method_section = checkout_page.get_payment_method_section()
        payment_method_section.select_payment_method("Check / Money Order")

        payment_information_section = checkout_page.get_payment_information_section()
        payment_information_section.click(payment_information_section.CONTINUE_BUTTON)

        # checkout_page.verify_billing_and_confirmation_match()

        confirm_order = ConfirmOrderSection(driver)
        confirm_order.confirm_order()

        confirm_order.complete_order()

    @allure.story("TC_CO_016: Checkout by Signing in as Returning Customer")
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates the process of completing a checkout by logging in as a returning customer, ensuring all required sections display correctly and the order is placed."
    )
    def test_checkout_as_returning_customer(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)


