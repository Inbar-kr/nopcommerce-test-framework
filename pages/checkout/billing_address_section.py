from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.checkout.checkout_page import CheckoutPage


class BillingAddressSection(BasePage):
    # Locators for billing address fields
    SAME_ADDRESS_CHECKBOX = (By.ID, "ShipToSameAddress")
    FIRST_NAME_FIELD = (By.ID, "BillingNewAddress_FirstName")
    LAST_NAME_FIELD = (By.ID, "BillingNewAddress_LastName")
    EMAIL_FIELD = (By.ID, "BillingNewAddress_Email")
    EMAIL_ERROR = (By.ID, "BillingNewAddress_Email-error")
    COMPANY_FIELD = (By.ID, "BillingNewAddress_Company")
    COUNTRY_DROPDOWN = (By.ID, "BillingNewAddress_CountryId")
    STATE_DROPDOWN = (By.ID, "BillingNewAddress_StateProvinceId")
    CITY_FIELD = (By.ID, "BillingNewAddress_City")
    ADDRESS1_FIELD = (By.ID, "BillingNewAddress_Address1")
    ADDRESS2_FIELD = (By.ID, "BillingNewAddress_Address2")
    ZIP_CODE_FIELD = (By.ID, "BillingNewAddress_ZipPostalCode")
    PHONE_NUMBER_FIELD = (By.ID, "BillingNewAddress_PhoneNumber")
    FAX_NUMBER_FIELD = (By.ID, "BillingNewAddress_FaxNumber")

    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.new-address-next-step-button")


    def enter_mandatory_billing_address(self, load_test_data):
        billing_data = load_test_data["checkout_fields"]["mandatory_billing_address_section"]

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.COUNTRY_DROPDOWN) and
                EC.element_to_be_clickable(self.STATE_DROPDOWN)
            )

            self._select_dropdown(self.COUNTRY_DROPDOWN, billing_data["country_dropdown"])
            self._select_dropdown(self.STATE_DROPDOWN, billing_data["state_dropdown"])
            self._fill_billing_field(self.CITY_FIELD, billing_data["city"])
            self._fill_billing_field(self.ADDRESS1_FIELD, billing_data["address1"])
            self._fill_billing_field(self.ZIP_CODE_FIELD, billing_data["zip_code"])
            self._fill_billing_field(self.PHONE_NUMBER_FIELD, billing_data["phone_number"])

            self.click(self.CONTINUE_BUTTON)

        except Exception as e:
            self.logger.error(f"Failed to enter mandatory billing address: {str(e)}")
            raise

    def enter_all_billing_address(self, load_test_data):
        all_billing_data = load_test_data["checkout_fields"]["all_billing_address_section"]

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.COUNTRY_DROPDOWN) and
                EC.element_to_be_clickable(self.STATE_DROPDOWN)
            )

            self._fill_billing_field(self.COMPANY_FIELD, all_billing_data["company"])
            self._select_dropdown(self.COUNTRY_DROPDOWN, all_billing_data["country_dropdown"])
            self._select_dropdown(self.STATE_DROPDOWN, all_billing_data["state_dropdown"])
            self._fill_billing_field(self.CITY_FIELD, all_billing_data["city"])
            self._fill_billing_field(self.ADDRESS1_FIELD, all_billing_data["address1"])
            self._fill_billing_field(self.ADDRESS2_FIELD, all_billing_data["address2"])
            self._fill_billing_field(self.ZIP_CODE_FIELD, all_billing_data["zip_code"])
            self._fill_billing_field(self.PHONE_NUMBER_FIELD, all_billing_data["phone_number"])
            self._fill_billing_field(self.FAX_NUMBER_FIELD, all_billing_data["fax_number"])

            self.click(self.CONTINUE_BUTTON)

        except Exception as e:
            self.logger.error(f"Failed to enter mandatory billing address: {str(e)}")
            raise

    def enter_full_billing_address(self, load_test_data):
        full_billing_data = load_test_data["checkout_fields"]["full_billing_address_section"]

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.COUNTRY_DROPDOWN) and
                EC.element_to_be_clickable(self.STATE_DROPDOWN)
            )

            self._fill_billing_field(self.FIRST_NAME_FIELD, full_billing_data["first_name"])
            self._fill_billing_field(self.LAST_NAME_FIELD, full_billing_data["last_name"])
            self._fill_billing_field(self.EMAIL_FIELD, full_billing_data["email"])
            self._fill_billing_field(self.COMPANY_FIELD, full_billing_data["company"])
            self._select_dropdown(self.COUNTRY_DROPDOWN, full_billing_data["country_dropdown"])
            self._select_dropdown(self.STATE_DROPDOWN, full_billing_data["state_dropdown"])
            self._fill_billing_field(self.CITY_FIELD, full_billing_data["city"])
            self._fill_billing_field(self.ADDRESS1_FIELD, full_billing_data["address1"])
            self._fill_billing_field(self.ADDRESS2_FIELD, full_billing_data["address2"])
            self._fill_billing_field(self.ZIP_CODE_FIELD, full_billing_data["zip_code"])
            self._fill_billing_field(self.PHONE_NUMBER_FIELD, full_billing_data["phone_number"])
            self._fill_billing_field(self.FAX_NUMBER_FIELD, full_billing_data["fax_number"])

            self.click(self.CONTINUE_BUTTON)

        except Exception as e:
            self.logger.error(f"Failed to enter mandatory billing address: {str(e)}")
            raise

    def unselect_ship_to_same_address(self):
        checkbox = self.driver.find_element(*self.SAME_ADDRESS_CHECKBOX)
        if checkbox.is_selected():
            checkbox.click()

    def _select_dropdown(self, dropdown_locator, value):
        select = Select(self.driver.find_element(*dropdown_locator))
        select.select_by_visible_text(value)

    def _fill_billing_field(self, field_locator, value):
        if not self.get_text_value(field_locator):
            self.enter_text(field_locator, value)

    def get_billing_address_details(self):
        return {
            "first_name": self.get_text_value(self.FIRST_NAME_FIELD),
            "last_name": self.get_text_value(self.LAST_NAME_FIELD),
            "email": self.get_text_value(self.EMAIL_FIELD),
        }

    def get_all_billing_address_details(self):
        return {
            "first_name": self.get_text_value(self.FIRST_NAME_FIELD),
            "last_name": self.get_text_value(self.LAST_NAME_FIELD),
            "email": self.get_text_value(self.EMAIL_FIELD),
            "country": self.get_text_value(self.COUNTRY_DROPDOWN),
            "state": self.get_text_value(self.STATE_DROPDOWN),
            "city": self.get_text_value(self.CITY_FIELD),
            "address1": self.get_text_value(self.ADDRESS1_FIELD),
            "zip_code": self.get_text_value(self.ZIP_CODE_FIELD),
            "phone_number": self.get_text_value(self.PHONE_NUMBER_FIELD),
        }

    def validate_placeholders_for_all_fields(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)
        checkout_page._login_as_user(driver, load_test_data)
        checkout_page._search_and_add_product(driver, load_test_data)
        self.get_billing_address_details()

        expected_placeholders = {
            self.COMPANY_FIELD: "BillingNewAddress_Company",
            self.CITY_FIELD: "BillingNewAddress_City",
            self.ADDRESS1_FIELD: "BillingNewAddress_Address1",
            self.ADDRESS2_FIELD: "BillingNewAddress_Address2",
            self.ZIP_CODE_FIELD: "BillingNewAddress_ZipPostalCode",
            self.PHONE_NUMBER_FIELD: "BillingNewAddress_PhoneNumber",
            self.FAX_NUMBER_FIELD: "BillingNewAddress_FaxNumber"
        }

        for field_locator, expected_placeholder in expected_placeholders.items():
            checkout_page._validate_placeholder_for_field(driver, field_locator, expected_placeholder)

        self.logger.info("All billing address fields have the correct placeholders.")

    def submit_billing_form_without_fields(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()
        self.logger.info("Submitted the billing form without filling in any fields.")

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text.strip()
            self.logger.info(f"Alert text: {alert_text}")

            expected_message_1 = "City is required, Street address is required, Phone is required, Zip / postal code is required, State / province is required."
            expected_message_2 = "City is required, Email is required., Street address is required, Last name is required., First name is required., Phone is required, Zip / postal code is required, State / province is required."

            assert alert_text == expected_message_1 or alert_text == expected_message_2, \
                f"Unexpected alert message: '{alert_text}'"

            alert.accept()
            self.logger.info("Alert accepted.")

        except Exception as e:
            self.logger.error(f"Failed to handle alert: {e}")
            raise

    def checkout_as_signed_in_user_with_new_address(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page._login_as_user(driver, load_test_data)
        self.logger.info("Logged in as a signed-in user.")

        checkout_page._search_and_add_product(driver, load_test_data)
        self.logger.info("Searched and added product to the cart.")

        self.get_billing_address_details()
        self.wait_for_element(BillingAddressSection.SAME_ADDRESS_CHECKBOX)
        self.unselect_ship_to_same_address()
        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=False)
        self.logger.info("Billing address details verified and updated.")

        shipping_address_section = checkout_page.get_shipping_address_section()
        shipping_address_section.enter_mandatory_shipping_address(load_test_data)
        self.logger.info("Mandatory shipping address details entered.")

        checkout_page._select_shipping_method("ground")
        self.logger.info("Shipping method selected.")

        checkout_page._select_payment_method("Check / Money Order")
        self.logger.info("Payment method selected.")

        checkout_page._complete_payment_and_order()
        self.logger.info("Order confirmed and completed.")

        self.logger.info("Attempt to checkout as a signed-in user with a new address completed.")

    def checkout_as_signin_user_with_full_billing_address(self, driver, load_test_data):
        checkout_page = CheckoutPage(driver)

        checkout_page._login_as_user(driver, load_test_data)
        self.logger.info("Logged in as a signed-in user.")

        checkout_page._search_and_add_product(driver, load_test_data)
        self.logger.info("Searched and added product to the cart.")

        self.get_billing_address_details()
        self.wait_for_element(BillingAddressSection.SAME_ADDRESS_CHECKBOX)
        self.unselect_ship_to_same_address()
        checkout_page.verify_billing_details_match(driver, load_test_data, fill_full_address=True)
        self.logger.info("Billing address details verified and added.")

        shipping_address_section = checkout_page.get_shipping_address_section()
        shipping_address_section.enter_mandatory_shipping_address(load_test_data)
        self.logger.info("Mandatory shipping address details entered.")

        checkout_page._select_shipping_method("ground")
        self.logger.info("Shipping method selected.")

        checkout_page._select_payment_method("Check / Money Order")
        self.logger.info("Payment method selected.")

        checkout_page._complete_payment_and_order()
        self.logger.info("Order confirmed and completed.")

        self.logger.info("Attempt to checkout as a signed-in user with a new address completed.")
