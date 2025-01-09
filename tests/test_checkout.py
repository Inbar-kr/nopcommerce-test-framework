"""from pages.checkout.checkout_page import CheckoutPage
from pages.checkout.billing_address_section import BillingAddressSection
from pages.checkout.shipping_address_section import ShippingAddressSection
from pages.checkout.shipping_method_section import ShippingMethodSection
from pages.checkout.payment_method_section import PaymentMethodSection
from pages.checkout.payment_information_section import PaymentInformationSection
from pages.checkout.confirm_order_section import ConfirmOrderSection"""

import time
import pytest
import json
import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from tests.test_search import TestUserSearch
from tests.test_login import TestUserLogin
from pages.checkout.checkout_page import CheckoutPage
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
    @allure.severity(Severity.CRITICAL)
    @allure.label("Regression")
    @allure.description(
        "This test validates that after adding a product to the cart, clicking on the 'Checkout' option in the Cart block navigates the user to the checkout page.")
    def test_checkout_navigation_from_cart_block(self, driver, load_test_data):
        search_test = TestUserSearch()
        search_test.test_valid_product(driver, load_test_data)

        checkout_page = CheckoutPage(driver)

        checkout_page.click(CheckoutPage.ADD_TO_CART_BUTTON)
        checkout_page.click(CheckoutPage.SHOPPING_CART_POPUP_CLOSE)
        checkout_page.wait_for_element(CheckoutPage.SHOPPING_CART_BUTTON)

        # To fix - won't hover
        checkout_page.hover_cart_button()

        assert checkout_page.is_element_visible(CheckoutPage.CHECKOUT_BUTTON), "Checkout page failed. User was not redirected to the checkout page."

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
        time.sleep(2)











