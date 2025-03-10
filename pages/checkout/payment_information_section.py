from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .billing_address_section import BillingAddressSection
from ..checkout.checkout_page import CheckoutPage

class PaymentInformationSection(BasePage):
    # Credit Card form
    CARD_TYPE_DROPDOWN = (By.ID, "CreditCardType")
    CARD_NAME_FIELD = (By.ID, "CardholderName")
    CARD_NUMBER_FIELD = (By.ID, "CardNumber")
    EXPIRY_DATE_MONTH_DROPDOWN = (By.ID, "ExpireMonth")
    EXPIRY_DATE_YEAR_DROPDOWN = (By.ID, "ExpireYear")
    CVV_FIELD = (By.ID, "CardCode")

    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.payment-info-next-step-button")

    def fill_payment_information(self, load_test_data):
        payment_data = load_test_data["payment_with_card"]

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CARD_TYPE_DROPDOWN) and
                EC.element_to_be_clickable(self.EXPIRY_DATE_MONTH_DROPDOWN) and
                EC.element_to_be_clickable(self.EXPIRY_DATE_YEAR_DROPDOWN)
            )

            self._select_dropdown(self.CARD_TYPE_DROPDOWN, payment_data["card_type"])
            self._fill_payment_field(self.CARD_NAME_FIELD, payment_data["cardholder_name"])
            self._fill_payment_field(self.CARD_NUMBER_FIELD, payment_data["card_number"])
            self._fill_payment_field(self.EXPIRY_DATE_MONTH_DROPDOWN, payment_data["expiry_month"])
            self._fill_payment_field(self.EXPIRY_DATE_YEAR_DROPDOWN, payment_data["expiry_year"])
            self._fill_payment_field(self.CVV_FIELD, payment_data["cvv"])

            self.click(self.CONTINUE_BUTTON)

        except Exception as e:
            self.logger.error(f"Failed to enter payment information: {str(e)}")
            raise

    def _select_dropdown(self, dropdown_locator, value):
        select = Select(self.driver.find_element(*dropdown_locator))
        select.select_by_visible_text(value)

    def _fill_payment_field(self, field_locator, value):
        if not self.get_text_value(field_locator):
            self.enter_text(field_locator, value)

    def checkout_with_card_payment(self, driver, load_test_data):
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

        shipping_address_section = checkout_page.get_shipping_address_section()
        shipping_address_section.enter_mandatory_shipping_address(load_test_data)
        self.logger.info("Mandatory shipping address details entered.")

        checkout_page._select_shipping_method("next_day")
        self.logger.info("Shipping method selected.")

        checkout_page._select_payment_method("card")
        self.logger.info("Payment method selected.")

        checkout_page._complete_card_payment_and_order(load_test_data)
        self.logger.info("Order confirmed and completed with card payment.")

        # checkout_page.verify_billing_and_confirmation_match()

        self.logger.info("Attempt to checkout as a signed-in user with a new address completed.")

