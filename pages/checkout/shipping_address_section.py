from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.checkout.billing_address_section import BillingAddressSection
from pages.checkout.checkout_page import CheckoutPage


class ShippingAddressSection(BasePage):
    # Same address form
    SHIPPING_ADDRESS_DROPDOWN = (By.ID, "shipping-address-select")
    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_SHIPPING_BUTTON = (By.CLASS_NAME, "button-1.new-address-next-step-button")

    # New address form
    FIRST_NAME_FIELD = (By.ID, "ShippingNewAddress_FirstName")
    LAST_NAME_FIELD = (By.ID, "ShippingNewAddress_LastName")
    EMAIL_FIELD = (By.ID, "ShippingNewAddress_Email")
    COMPANY_FIELD = (By.ID, "ShippingNewAddress_Company")
    COUNTRY_DROPDOWN = (By.ID, "ShippingNewAddress_CountryId")
    STATE_DROPDOWN = (By.ID, "ShippingNewAddress_StateProvinceId")
    CITY_FIELD = (By.ID, "ShippingNewAddress_City")
    ADDRESS1_FIELD = (By.ID, "ShippingNewAddress_Address1")
    ADDRESS2_FIELD = (By.ID, "ShippingNewAddress_Address2")
    ZIP_CODE_FIELD = (By.ID, "ShippingNewAddress_ZipPostalCode")
    PHONE_NUMBER_FIELD = (By.ID, "ShippingNewAddress_PhoneNumber")
    FAX_NUMBER_FIELD = (By.ID, "ShippingNewAddress_FaxNumber")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "div#shipping-buttons-container button.button-1.new-address-next-step-button")


    def enter_mandatory_shipping_address(self, load_test_data):
        self._select_dropdown(self.SHIPPING_ADDRESS_DROPDOWN, "New Address")

        shipping_data = load_test_data["checkout_fields"]["mandatory_shipping_address_section"]

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.COUNTRY_DROPDOWN) and
                EC.element_to_be_clickable(self.STATE_DROPDOWN)
            )

            self._select_dropdown(self.COUNTRY_DROPDOWN, shipping_data["country_dropdown"])
            self._select_dropdown(self.STATE_DROPDOWN, shipping_data["state_dropdown"])
            self._fill_shipping_field(self.CITY_FIELD, shipping_data["city"])
            self._fill_shipping_field(self.ADDRESS1_FIELD, shipping_data["address1"])
            self._fill_shipping_field(self.ZIP_CODE_FIELD, shipping_data["zip_code"])
            self._fill_shipping_field(self.PHONE_NUMBER_FIELD, shipping_data["phone_number"])

            self.scroll_to_footer()
            self.click(self.CONTINUE_BUTTON)

        except Exception as e:
            self.logger.error(f"Failed to enter mandatory shipping address: {str(e)}")
            raise

    def enter_all_shipping_address(self, load_test_data):
        self._select_dropdown(self.SHIPPING_ADDRESS_DROPDOWN, "New Address")

        shipping_data = load_test_data["checkout_fields"]["all_billing_address_section"]

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.COUNTRY_DROPDOWN) and
                EC.element_to_be_clickable(self.STATE_DROPDOWN)
            )

            self._fill_shipping_field(self.COMPANY_FIELD, shipping_data["company"])
            self._select_dropdown(self.COUNTRY_DROPDOWN, shipping_data["country_dropdown"])
            self._select_dropdown(self.STATE_DROPDOWN, shipping_data["state_dropdown"])
            self._fill_shipping_field(self.CITY_FIELD, shipping_data["city"])
            self._fill_shipping_field(self.ADDRESS1_FIELD, shipping_data["address1"])
            self._fill_shipping_field(self.ADDRESS2_FIELD, shipping_data["address2"])
            self._fill_shipping_field(self.ZIP_CODE_FIELD, shipping_data["zip_code"])
            self._fill_shipping_field(self.PHONE_NUMBER_FIELD, shipping_data["phone_number"])
            self._fill_shipping_field(self.FAX_NUMBER_FIELD, shipping_data["fax_number"])

            self.scroll_to_footer()
            self.click(self.CONTINUE_BUTTON)

        except Exception as e:
            self.logger.error(f"Failed to enter all shipping address: {str(e)}")
            raise

    def _select_dropdown(self, dropdown_locator, value):
        select = Select(self.driver.find_element(*dropdown_locator))
        select.select_by_visible_text(value)

    def _fill_shipping_field(self, field_locator, value):
        if not self.get_text_value(field_locator):
            self.enter_text(field_locator, value)

    def validate_placeholders_for_all_fields(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)
        checkout_page._login_as_user(driver, load_test_data)
        checkout_page._search_and_add_product(driver, load_test_data)

        billing_address_section = checkout_page.get_billing_address_section()
        billing_address_section.wait_for_element(BillingAddressSection.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()
        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=False)

        self._select_dropdown(self.SHIPPING_ADDRESS_DROPDOWN, "New Address")

        expected_placeholders = {
            self.COMPANY_FIELD: "ShippingNewAddress_Company",
            self.CITY_FIELD: "ShippingNewAddress_City",
            self.ADDRESS1_FIELD: "ShippingNewAddress_Address1",
            self.ADDRESS2_FIELD: "ShippingNewAddress_Address2",
            self.ZIP_CODE_FIELD: "ShippingNewAddress_ZipPostalCode",
            self.PHONE_NUMBER_FIELD: "ShippingNewAddress_PhoneNumber",
            self.FAX_NUMBER_FIELD: "ShippingNewAddress_FaxNumber"
        }

        for field_locator, expected_placeholder in expected_placeholders.items():
            self.logger.info(f"Validating placeholder for field: {field_locator}")
            checkout_page._validate_placeholder_for_field(driver, field_locator, expected_placeholder)

        self.logger.info("All Shipping address fields have the correct placeholders.")

    def submit_shipping_form_without_fields(self):
        self._select_dropdown(self.SHIPPING_ADDRESS_DROPDOWN, "New Address")
        self.driver.find_element(*self.CONTINUE_BUTTON).click()
        self.logger.info("Submitted the billing form without filling in any fields.")
        alert_text = self.extract_alert_text()
        expected_message = ("City is required, Street address is required, Country is required., Phone is required, Zip / postal code is required")

        assert alert_text == expected_message, \
            f"Unexpected alert message: '{alert_text}'. Expected: '{expected_message}'"

        self.close_popup()

    def checkout_with_shipping_address(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page._login_as_user(driver, load_test_data)
        self.logger.info("Logged in as a signed-in user.")

        checkout_page._search_and_add_product(driver, load_test_data)
        self.logger.info("Searched and added product to the cart.")

        billing_address_section = checkout_page.get_billing_address_section()
        billing_address_details = billing_address_section.get_billing_address_details()
        self.logger.info(f"Billing Address Details: {billing_address_details}")

        billing_address_section.wait_for_element(BillingAddressSection.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()
        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=False)
        self.logger.info("Billing address details verified and added.")

        self.enter_mandatory_shipping_address(load_test_data)
        self.logger.info("All shipping address details entered.")

        checkout_page._select_shipping_method("ground")
        self.logger.info("Shipping method selected.")

        checkout_page._select_payment_method("Check / Money Order")
        self.logger.info("Payment method selected.")

        checkout_page._complete_payment_and_order()
        self.logger.info("Order confirmed and completed.")

        self.logger.info("Attempt to checkout as a signed-in user with a new shipping address completed.")

    def no_fields_in_shipping_address(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page._login_as_user(driver, load_test_data)
        self.logger.info("Logged in as a signed-in user.")

        checkout_page._search_and_add_product(driver, load_test_data)
        self.logger.info("Searched and added product to the cart.")

        billing_address_section = checkout_page.get_billing_address_section()
        billing_address_details = billing_address_section.get_billing_address_details()
        self.logger.info(f"Billing Address Details: {billing_address_details}")

        billing_address_section.wait_for_element(BillingAddressSection.SAME_ADDRESS_CHECKBOX)
        billing_address_section.unselect_ship_to_same_address()
        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=False)
        self.logger.info("Billing address details verified and added.")

        self.submit_shipping_form_without_fields()
        self.logger.info("Attempted to submit shipping address form without any fields filled.")
