from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PaymentMethodSection(BasePage):
    CHECK_METHOD_RADIO_BUTTON = (By.ID, "paymentmethod_0")
    CARD_METHOD_RADIO_BUTTON = (By.ID, "paymentmethod_1")

    BACK_SHIPPING_LINK = (By.CLASS_NAME, "back-link")
    CONTINUE_BUTTON = (By.CLASS_NAME, "button-1.payment-method-next-step-button")

    def select_payment_method(self, method="card"):
        if method == "check":
            self.click(self.CHECK_METHOD_RADIO_BUTTON)
        elif method == "card":
            self.click(self.CARD_METHOD_RADIO_BUTTON)
        else:
            raise ValueError(f"Invalid payment method: {method}")

        self.click(self.CONTINUE_BUTTON)