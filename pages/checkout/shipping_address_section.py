from selenium.webdriver.common.by import By
import time
from pages.base_page import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class ShippingAddressSection(BasePage):
    # Same address form
    SHIPPING_ADDRESS_DROPDOWN = (By.ID, "shipping-address-select")
    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_SHIPPING_BUTTON = (By.CLASS_NAME, "button-1.new-address-next-step-button")

    # New address form
    FIRST_NAME_FIELD = (By.ID, "ShippingNewAddress_FirstName")
    LAST_NAME_FIELD = (By.ID, "ShippingNewAddress_LastName")
    EMAIL_FIELD = (By.ID, "ShippingNewAddress_Email")
    COMPANY_FIELD = (By.ID, "BShippingNewAddress_Company")
    COUNTRY_DROPDOWN = (By.ID, "ShippingNewAddress_CountryId")
    STATE_DROPDOWN = (By.ID, "ShippingNewAddress_StateProvinceId")
    CITY_FIELD = (By.ID, "ShippingNewAddress_City")
    ADDRESS1_FIELD = (By.ID, "ShippingNewAddress_Address1")
    ADDRESS2_FIELD = (By.ID, "ShippingNewAddress_Address2")
    ZIP_CODE_FIELD = (By.ID, "ShippingNewAddress_ZipPostalCode")
    PHONE_NUMBER_FIELD = (By.ID, "ShippingNewAddress_PhoneNumber")
    FAX_NUMBER_FIELD = (By.ID, "ShippingNewAddress.FaxNumber")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "div#shipping-buttons-container button.button-1.new-address-next-step-button")

    """def enter_shipping_address(self, first_name, last_name, email, country, city, address, zip_code, phone_number):
        self.enter_text(self.FIRST_NAME_FIELD, first_name)
        self.enter_text(self.LAST_NAME_FIELD, last_name)
        self.enter_text(self.EMAIL_FIELD, email)
        self.select_dropdown_option(self.COUNTRY_DROPDOWN, country)
        self.enter_text(self.CITY_FIELD, city)
        self.enter_text(self.ADDRESS1_FIELD, address)
        self.enter_text(self.ZIP_CODE_FIELD, zip_code)
        self.enter_text(self.PHONE_NUMBER_FIELD, phone_number)

        self.scroll_into_view(self.CONTINUE_BUTTON)
        self.click(self.CONTINUE_BUTTON)"""

    def enter_mandatory_shipping_address(self, load_test_data):
        # Select a shipping address from your address book or enter a new address
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
        # Select a shipping address from your address book or enter a new address
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

    def validate_placeholders_for_all_fields(self, driver):
        self._select_dropdown(self.SHIPPING_ADDRESS_DROPDOWN, "New Address")

        expected_placeholders = {
            self.COMPANY_FIELD: "",
            self.CITY_FIELD: "",
            self.ADDRESS1_FIELD: "",
            self.ADDRESS2_FIELD: "",
            self.ZIP_CODE_FIELD: "",
            self.PHONE_NUMBER_FIELD: "",
            self.FAX_NUMBER_FIELD: ""
        }

        for field_locator, expected_placeholder in expected_placeholders.items():
            field = self.wait_for_element(field_locator, timeout=20)
            if field:
                self.wait_for_placeholder(driver, field_locator, expected_placeholder)
            else:
                self.logger.error(f"Field {field_locator} not found!")
                raise ValueError(f"Field {field_locator} is missing on the page.")

        self.logger.info("All shipping address fields have the correct placeholders.")

    def submit_shipping_form_without_fields(self):
        self._select_dropdown(self.SHIPPING_ADDRESS_DROPDOWN, "New Address")
        self.driver.find_element(*self.CONTINUE_BUTTON).click()
        self.logger.info("Submitted the billing form without filling in any fields.")
        alert_text = self.extract_alert_text()
        expected_message = ("City is required, Street address is required, Country is required., Phone is required, Zip / postal code is required")

        assert alert_text == expected_message, \
            f"Unexpected alert message: '{alert_text}'. Expected: '{expected_message}'"

        self.close_popup()




