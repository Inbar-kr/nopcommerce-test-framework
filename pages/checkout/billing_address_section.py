from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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

    def validate_placeholders_for_all_fields(self, driver):
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
            field = self.wait_for_element(field_locator, timeout=10)
            if field:
                self.wait_for_placeholder(driver, field_locator, expected_placeholder)
            else:
                self.logger.error(f"Field {field_locator} not found!")
                raise ValueError(f"Field {field_locator} is missing on the page.")

        self.logger.info("All billing address fields have the correct placeholders.")

    def submit_billing_form_without_fields(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()
        self.logger.info("Submitted the billing form without filling in any fields.")

        alert_text = self.extract_alert_text()

        expected_message_1 = "City is required, Street address is required, Country is required., Phone is required, Zip / postal code is required"
        expected_message_2 = "City is required, Email is required., Street address is required, Last name is required., Country is required., First name is required., Phone is required, Zip / postal code is required"

        assert alert_text == expected_message_1 or alert_text == expected_message_2, \
            f"Unexpected alert message: '{alert_text}'. Expected one of: '{expected_message_1}' or '{expected_message_2}'"

        self.close_popup()




