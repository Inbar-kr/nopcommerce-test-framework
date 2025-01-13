from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PaymentMethodSection(BasePage):
    CHECK_METHOD_RADIO_BUTTON = (By.ID, "paymentmethod_0")
    CARD_METHOD_RADIO_BUTTON = (By.ID, "paymentmethod_1")

    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.payment-method-next-step-button")

    def select_payment_method(self, method="Check / Money Order"):
        payment_methods = {
            "Check / Money Order": self.CHECK_METHOD_RADIO_BUTTON,
            "card": self.CARD_METHOD_RADIO_BUTTON
        }

        if method not in payment_methods:
            raise ValueError(f"Invalid payment method: {method}")

        self.click(payment_methods[method])
        self.click(self.CONTINUE_BUTTON)
