from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import Select
from ..checkout.checkout_page import CheckoutPage

class PaymentInformationSection(BasePage):
    # Credit Card form
    CARD_TYPE_DROPDOWN = (By.ID, "CreditCardType")
    CARD_NAME_FIELD = (By.ID, "CardholderName")
    CARD_NUMBER_FIELD = (By.ID, "CardNumber")
    EXPIRY_DATE_MONTH_FIELD = (By.ID, "ExpireMonth")
    EXPIRY_DATE_YEAR_FIELD = (By.ID, "ExpireYear")
    CVV_FIELD = (By.ID, "CardCode")

    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.payment-info-next-step-button")

    def fill_payment_information(self, card_type, card_name, card_number, expiry_month, expiry_year, cvv):
        self.select_option(self.CARD_TYPE_DROPDOWN, card_type)

        self.enter_text(self.CARD_NAME_FIELD, card_name)
        self.enter_text(self.CARD_NUMBER_FIELD, card_number)
        self.enter_text(self.EXPIRY_DATE_MONTH_FIELD, expiry_month)
        self.enter_text(self.EXPIRY_DATE_YEAR_FIELD, expiry_year)
        self.enter_text(self.CVV_FIELD, cvv)

        self.click(self.CONTINUE_BUTTON)

    def select_option(self, dropdown_locator, option_value):
        dropdown = self.wait_for_element(dropdown_locator)
        select = Select(dropdown)
        select.select_by_visible_text(option_value)