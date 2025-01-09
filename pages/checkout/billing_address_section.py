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

    def enter_all_billing_address(self, load_test_data):
        billing_data = load_test_data["all_billing_address_section"]

        # Check if the fields are empty before entering the data
        if not self.get_text_value(self.FIRST_NAME_FIELD):
            self.enter_text(self.FIRST_NAME_FIELD, billing_data["first_name"])
        if not self.get_text_value(self.LAST_NAME_FIELD):
            self.enter_text(self.LAST_NAME_FIELD, billing_data["last_name"])
        if not self.get_text_value(self.EMAIL_FIELD):
            self.enter_text(self.EMAIL_FIELD, billing_data["email"])
        if not self.get_text_value(self.COUNTRY_DROPDOWN):
            self.select_dropdown_option(self.COUNTRY_DROPDOWN, billing_data["country_dropdown"])
        if not self.get_text_value(self.STATE_DROPDOWN):
            self.select_dropdown_option(self.STATE_DROPDOWN, billing_data["state_dropdown"])
        if not self.get_text_value(self.CITY_FIELD):
            self.enter_text(self.CITY_FIELD, billing_data["city"])
        if not self.get_text_value(self.ADDRESS1_FIELD):
            self.enter_text(self.ADDRESS1_FIELD, billing_data["address1"])
        if not self.get_text_value(self.ADDRESS2_FIELD):
            self.enter_text(self.ADDRESS1_FIELD, billing_data["address2"])
        if not self.get_text_value(self.ZIP_CODE_FIELD):
            self.enter_text(self.ZIP_CODE_FIELD, billing_data["zip_code"])
        if not self.get_text_value(self.PHONE_NUMBER_FIELD):
            self.enter_text(self.PHONE_NUMBER_FIELD, billing_data["phone_number"])
        if not self.get_text_value(self.FAX_NUMBER_FIELD):
            self.enter_text(self.FAX_NUMBER_FIELD, billing_data["fax_number"])

        self.click(self.CONTINUE_BUTTON)

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
