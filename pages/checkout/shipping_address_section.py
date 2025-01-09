from selenium.webdriver.common.by import By
from pages.base_page import BasePage

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
    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.new-address-next-step-button")

    def enter_shipping_address(self, first_name, last_name, email, country, city, address, zip_code, phone_number):
        self.enter_text(self.FIRST_NAME_FIELD, first_name)
        self.enter_text(self.LAST_NAME_FIELD, last_name)
        self.enter_text(self.EMAIL_FIELD, email)
        self.select_from_dropdown(self.COUNTRY_DROPDOWN, country)
        self.enter_text(self.CITY_FIELD, city)
        self.enter_text(self.ADDRESS1_FIELD, address)
        self.enter_text(self.ZIP_CODE_FIELD, zip_code)
        self.enter_text(self.PHONE_NUMBER_FIELD, phone_number)

        self.click(self.CONTINUE_BUTTON)
